import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
PAYLOAD_PREFIX = "PAYLOAD::"

HOT_PATH_FILES = [
    "server.py",
    "agent.py",
    "config.py",
    "data_loader.py",
    "hybrid_retriever.py",
    "quiz_generator.py",
    "app.py",
    "rag_pipeline.py",
    "scripts/download_data.py",
    "tests/__init__.py",
    "tests/test_smoke.py",
]

DOCKER_COMPILE_TARGETS = [
    "server.py",
    "agent.py",
    "config.py",
    "data_loader.py",
    "hybrid_retriever.py",
    "quiz_generator.py",
    "app.py",
    "rag_pipeline.py",
    "scripts",
    "tests",
]


def _smoke_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("GOOGLE_API_KEY", "test-key")
    env["AMICUS_SMOKE_TEST"] = "1"
    return env


def _run_python(
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    cwd: Path | str | None = None,
    timeout: int = 60,
) -> subprocess.CompletedProcess[str]:
    child_env = (env or os.environ.copy()).copy()
    existing_pythonpath = child_env.get("PYTHONPATH")
    child_env["PYTHONPATH"] = (
        str(REPO_ROOT)
        if not existing_pythonpath
        else f"{REPO_ROOT}{os.pathsep}{existing_pythonpath}"
    )
    return subprocess.run(
        [PYTHON, *args],
        cwd=cwd or REPO_ROOT,
        env=child_env,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )


def _run_inline(
    code: str,
    *,
    env: dict[str, str] | None = None,
    cwd: Path | str | None = None,
    timeout: int = 60,
) -> subprocess.CompletedProcess[str]:
    return _run_python(
        ["-c", textwrap.dedent(code)],
        env=env,
        cwd=cwd,
        timeout=timeout,
    )


def _extract_payload(stdout: str):
    for line in stdout.splitlines():
        if line.startswith(PAYLOAD_PREFIX):
            return json.loads(line[len(PAYLOAD_PREFIX):])
    raise AssertionError(f"Missing {PAYLOAD_PREFIX} line in output:\n{stdout}")


def _pick_free_port() -> int:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]
    except PermissionError as exc:
        raise unittest.SkipTest(
            "Loopback socket binding is not permitted in the current sandbox."
        ) from exc


class SmokeTests(unittest.TestCase):
    def test_requirements_are_pinned(self):
        requirements = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        loose = [line for line in requirements if line.strip() and not line.startswith("#") and "==" not in line]
        self.assertFalse(loose, f"Found unpinned requirements: {loose}")

    def test_hot_path_files_compile(self):
        for path in HOT_PATH_FILES:
            source = (REPO_ROOT / path).read_text(encoding="utf-8")
            try:
                compile(source, str(REPO_ROOT / path), "exec")
            except SyntaxError as exc:
                self.fail(f"{path} failed to compile in memory:\n{exc}")

    def test_dockerfile_compileall_covers_backend_hot_path(self):
        dockerfile = (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8")
        for target in DOCKER_COMPILE_TARGETS:
            self.assertIn(target, dockerfile, f"Dockerfile compile coverage is missing {target}")

    def test_dockerignore_blocks_local_secrets_and_work_files(self):
        dockerignore = (REPO_ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
        required_entries = {".env", ".venv", ".git", "server.log", "HANDOFF.md", "CURSOR_*.md"}
        self.assertTrue(required_entries.issubset(set(dockerignore)))

    def test_default_cost_guardrails_are_conservative(self):
        result = _run_inline(
            """
            import json
            import config

            payload = {
                "chat_min": config.RATE_LIMIT_CHAT_PER_MIN,
                "quiz_min": config.RATE_LIMIT_QUIZ_PER_MIN,
                "chat_hour": config.GLOBAL_RATE_LIMIT_CHAT_PER_HOUR,
                "quiz_hour": config.GLOBAL_RATE_LIMIT_QUIZ_PER_HOUR,
                "chat_day": config.GLOBAL_RATE_LIMIT_CHAT_PER_DAY,
                "quiz_day": config.GLOBAL_RATE_LIMIT_QUIZ_PER_DAY,
                "ip_chat_day": config.IP_RATE_LIMIT_CHAT_PER_DAY,
                "ip_quiz_day": config.IP_RATE_LIMIT_QUIZ_PER_DAY,
                "agent_iterations": config.MAX_AGENT_ITERATIONS,
                "llm_tokens": config.LLM_MAX_OUTPUT_TOKENS,
                "quiz_tokens": config.QUIZ_MAX_OUTPUT_TOKENS,
            }
            print("PAYLOAD::" + json.dumps(payload))
            """,
            env=_smoke_env(),
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(
            _extract_payload(result.stdout),
            {
                "chat_min": 3,
                "quiz_min": 1,
                "chat_hour": 20,
                "quiz_hour": 6,
                "chat_day": 25,
                "quiz_day": 8,
                "ip_chat_day": 20,
                "ip_quiz_day": 6,
                "agent_iterations": 4,
                "llm_tokens": 900,
                "quiz_tokens": 1200,
            },
        )

    def test_download_data_dry_run(self):
        result = _run_python(["scripts/download_data.py", "--dry-run"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dry run only", result.stdout)
        self.assertIn("python_tutorial_intro.md", result.stdout)

    def test_rag_pipeline_uses_canonical_smoke_persist_dir(self):
        result = _run_python(
            [
                "-c",
                (
                    "from rag_pipeline import get_persist_path, resolve_persist_dir; "
                    "print(resolve_persist_dir('A')); "
                    "print(get_persist_path('A'))"
                ),
            ],
            env=_smoke_env(),
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(output_lines[0], "./.smoke_chroma_db_strategy_A")
        self.assertTrue(output_lines[1].endswith(".smoke_chroma_db_strategy_A"))

    def test_imports_work_in_smoke_mode(self):
        for module_name in ("rag_pipeline", "server"):
            result = _run_python(["-c", f"import {module_name}; print('ok')"], env=_smoke_env())
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            self.assertIn("ok", result.stdout)

    def test_health_endpoint_starts_in_smoke_mode(self):
        port = _pick_free_port()
        process = subprocess.Popen(
            [
                PYTHON,
                "-m",
                "uvicorn",
                "server:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
            ],
            cwd=REPO_ROOT,
            env=_smoke_env(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        try:
            deadline = time.time() + 45
            last_error = ""
            while time.time() < deadline:
                if process.poll() is not None:
                    output = process.communicate(timeout=5)[0]
                    self.fail(f"Uvicorn exited before health check passed:\n{output}")

                try:
                    with urllib.request.urlopen(
                        f"http://127.0.0.1:{port}/api/health",
                        timeout=1,
                    ) as response:
                        payload = json.loads(response.read().decode("utf-8"))
                    self.assertEqual(payload["status"], "ok")
                    self.assertTrue(payload["backend_loaded"])
                    return
                except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                    last_error = str(exc)
                    time.sleep(1)

            self.fail(f"/api/health did not become ready in time: {last_error}")
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)


class StartupAlignmentTests(unittest.TestCase):
    def test_server_canonical_persist_dir_matches_rag_pipeline_without_smoke(self):
        result = _run_python(
            [
                "-c",
                (
                    "from server import _canonical_persist_dir; "
                    "from rag_pipeline import resolve_persist_dir; "
                    "print(_canonical_persist_dir('A')); "
                    "print(resolve_persist_dir('A'))"
                ),
            ],
            env={**os.environ, "GOOGLE_API_KEY": "test-key"},
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(output_lines, ["./chroma_db_strategy_A", "./chroma_db_strategy_A"])

    def test_server_canonical_persist_dir_matches_rag_pipeline_in_smoke_mode(self):
        result = _run_python(
            [
                "-c",
                (
                    "from server import _canonical_persist_dir; "
                    "from rag_pipeline import resolve_persist_dir; "
                    "print(_canonical_persist_dir('A')); "
                    "print(resolve_persist_dir('A'))"
                ),
            ],
            env=_smoke_env(),
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(output_lines, ["./.smoke_chroma_db_strategy_A", "./.smoke_chroma_db_strategy_A"])

    def test_server_persisted_store_exists_requires_chroma_sqlite3(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store_dir = Path(temp_dir) / "store"
            store_dir.mkdir()
            result = _run_python(
                [
                    "-c",
                    (
                        "from pathlib import Path; "
                        "from server import _canonical_persist_dir, _persisted_store_exists; "
                        f"store_dir = Path({str(store_dir)!r}); "
                        "print(_canonical_persist_dir('A', store_dir)); "
                        "print(_persisted_store_exists('A', store_dir)); "
                        "(store_dir / 'chroma.sqlite3').write_text('ok', encoding='utf-8'); "
                        "print(_persisted_store_exists('A', store_dir))"
                    ),
                ],
                env=_smoke_env(),
            )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(output_lines[0], str(store_dir))
        self.assertEqual(output_lines[1:], ["False", "True"])

    def test_server_persisted_store_rejects_lfs_pointer(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store_dir = Path(temp_dir) / "store"
            store_dir.mkdir()
            (store_dir / "chroma.sqlite3").write_text(
                "version https://git-lfs.github.com/spec/v1\n"
                "oid sha256:abc123\n"
                "size 123456\n",
                encoding="utf-8",
            )
            result = _run_python(
                [
                    "-c",
                    (
                        "from pathlib import Path; "
                        "from server import _persisted_store_exists; "
                        f"print(_persisted_store_exists('A', Path({str(store_dir)!r})))"
                    ),
                ],
                env=_smoke_env(),
            )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(result.stdout.strip(), "False")

    def test_server_default_persisted_store_exists_uses_smoke_canonical_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            live_dir = temp_root / "chroma_db_strategy_A"
            smoke_dir = temp_root / ".smoke_chroma_db_strategy_A"
            (temp_root / "static").mkdir()
            live_dir.mkdir()
            smoke_dir.mkdir()
            (smoke_dir / "chroma.sqlite3").write_text("ok", encoding="utf-8")

            smoke_result = _run_python(
                [
                    "-c",
                    "from server import _persisted_store_exists; print(_persisted_store_exists('A'))",
                ],
                env=_smoke_env(),
                cwd=temp_root,
            )
            self.assertEqual(smoke_result.returncode, 0, smoke_result.stderr or smoke_result.stdout)
            self.assertEqual(smoke_result.stdout.strip(), "True")

            live_result = _run_python(
                [
                    "-c",
                    "from server import _persisted_store_exists; print(_persisted_store_exists('A'))",
                ],
                env={**os.environ, "GOOGLE_API_KEY": "test-key"},
                cwd=temp_root,
            )
            self.assertEqual(live_result.returncode, 0, live_result.stderr or live_result.stdout)
            self.assertEqual(live_result.stdout.strip(), "False")

            (live_dir / "chroma.sqlite3").write_text("ok", encoding="utf-8")
            live_result_with_sqlite = _run_python(
                [
                    "-c",
                    "from server import _persisted_store_exists; print(_persisted_store_exists('A'))",
                ],
                env={**os.environ, "GOOGLE_API_KEY": "test-key"},
                cwd=temp_root,
            )
            self.assertEqual(
                live_result_with_sqlite.returncode,
                0,
                live_result_with_sqlite.stderr or live_result_with_sqlite.stdout,
            )
            self.assertEqual(live_result_with_sqlite.stdout.strip(), "True")


class RoutingTests(unittest.TestCase):
    def test_chat_history_schema_rejects_malformed_items(self):
        result = _run_inline(
            """
            from pydantic import ValidationError
            from server import ChatRequest

            try:
                ChatRequest(message="hello", history=["bad-history-item"])
            except ValidationError:
                print("rejected")
            else:
                print("accepted")
            """,
            env=_smoke_env(),
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(result.stdout.strip(), "rejected")

    def test_client_ip_ignores_spoofable_headers_by_default(self):
        result = _run_inline(
            """
            import os
            from types import SimpleNamespace
            from server import _get_client_ip

            os.environ.pop("AMICUS_TRUST_PROXY_HEADERS", None)
            request = SimpleNamespace(
                headers={"x-real-ip": "203.0.113.99", "x-forwarded-for": "198.51.100.10"},
                client=SimpleNamespace(host="127.0.0.1"),
            )
            print(_get_client_ip(request))

            os.environ["AMICUS_TRUST_PROXY_HEADERS"] = "1"
            print(_get_client_ip(request))
            """,
            env=_smoke_env(),
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(result.stdout.splitlines(), ["127.0.0.1", "198.51.100.10"])

    def test_chat_daily_limit_blocks_after_configured_limit(self):
        result = _run_inline(
            """
            from fastapi.testclient import TestClient
            import server

            original = {
                "RATE_LIMIT_CHAT_PER_MIN": server.RATE_LIMIT_CHAT_PER_MIN,
                "IP_RATE_LIMIT_CHAT_PER_DAY": server.IP_RATE_LIMIT_CHAT_PER_DAY,
                "GLOBAL_RATE_LIMIT_CHAT_PER_HOUR": server.GLOBAL_RATE_LIMIT_CHAT_PER_HOUR,
                "GLOBAL_RATE_LIMIT_CHAT_PER_DAY": server.GLOBAL_RATE_LIMIT_CHAT_PER_DAY,
            }
            try:
                server._rate_buckets.clear()
                server.RATE_LIMIT_CHAT_PER_MIN = 10
                server.IP_RATE_LIMIT_CHAT_PER_DAY = 2
                server.GLOBAL_RATE_LIMIT_CHAT_PER_HOUR = 10
                server.GLOBAL_RATE_LIMIT_CHAT_PER_DAY = 10
                client = TestClient(server.app)
                statuses = [
                    client.post("/api/chat", json={"message": "who are you?", "history": []}).status_code
                    for _ in range(3)
                ]
                print("PAYLOAD::" + __import__("json").dumps(statuses))
            finally:
                server._rate_buckets.clear()
                for name, value in original.items():
                    setattr(server, name, value)
            """,
            env=_smoke_env(),
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(_extract_payload(result.stdout), [200, 200, 429])

    def test_follow_up_context_restores_topic_and_current_request(self):
        result = _run_python(
            [
                "-c",
                (
                    "from server import _build_query_context; "
                    "history = ["
                    "{'role': 'user', 'content': 'Should I use a loop or a list comprehension?'},"
                    "{'role': 'assistant', 'content': '1. Use a loop when you want clarity\\n2. Use a list comprehension when you want a compact transformation'}"
                    "]; "
                    "context = _build_query_context('the second one', history); "
                    "print(context['is_follow_up']); "
                    "print(context['lookup_query'])"
                ),
            ],
            env=_smoke_env(),
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(output_lines[0], "True")
        self.assertIn("Earlier topic: Should I use a loop or a list comprehension?", output_lines[1])
        self.assertIn("Current follow-up request: the second one", output_lines[1])

    def test_simple_course_question_uses_direct_path_before_agent(self):
        result = _run_inline(
            """
            from server import _build_query_context, _should_use_direct_course_path

            first_turn = _build_query_context("Explain a Python variable", [])
            follow_up = _build_query_context(
                "explain that again",
                [{"role": "user", "content": "What is a Python variable?"}],
            )
            unsupported = _build_query_context("What is the capital of France?", [])

            print("PAYLOAD::" + __import__("json").dumps({
                "first_turn": _should_use_direct_course_path(first_turn),
                "follow_up": _should_use_direct_course_path(follow_up),
                "unsupported": _should_use_direct_course_path(unsupported),
            }))
            """,
            env=_smoke_env(),
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(
            _extract_payload(result.stdout),
            {"first_turn": True, "follow_up": False, "unsupported": False},
        )


class SafetyTests(unittest.TestCase):
    def test_download_validator_rejects_lfs_pointer(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pointer_path = Path(temp_dir) / "bad.pdf"
            pointer_path.write_text(
                "version https://git-lfs.github.com/spec/v1\n"
                "oid sha256:abc123\n"
                "size 123456\n",
                encoding="utf-8",
            )
            result = _run_inline(
                """
                from pathlib import Path
                from scripts.download_data import is_valid_download

                path = Path(__import__("os").environ["POINTER_PATH"])
                resource = {"format": "binary", "min_size_bytes": 1}
                print(is_valid_download(path, resource))
                """,
                env={**_smoke_env(), "POINTER_PATH": str(pointer_path)},
            )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(result.stdout.strip(), "False")

    def test_quiz_generation_does_not_return_backend_errors(self):
        result = _run_inline(
            """
            from langchain_core.documents import Document
            from quiz_generator import QuizGenerationError, generate_quiz

            class FakeVectorStore:
                def similarity_search_with_relevance_scores(self, query, **kwargs):
                    doc = Document(
                        page_content="A Python loop repeats a block of code.",
                        metadata={"source": "python_tutorial_intro.md", "topic": "python"},
                    )
                    return [(doc, 1.0)]

            class FailingLLM:
                def invoke(self, prompt):
                    raise RuntimeError("SECRET_BACKEND_DETAIL quota exhausted")

            try:
                generate_quiz("python loops", FakeVectorStore(), llm=FailingLLM())
            except QuizGenerationError as exc:
                print(str(exc))
                print("SECRET_BACKEND_DETAIL" in str(exc))
            else:
                print("no-error")
            """,
            env=_smoke_env(),
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(result.stdout.splitlines(), ["Quiz generation failed.", "False"])


class PromptTruthfulnessTests(unittest.TestCase):
    def test_system_prompt_no_longer_defaults_to_micro_challenge_closing(self):
        result = _run_inline(
            """
            import json
            from config import SYSTEM_PROMPT

            payload = {
                "clean_ending_default": "Default to a clean ending or ONE short invitation, not a numbered menu." in SYSTEM_PROMPT,
                "no_default_micro_challenge": "Do NOT default to a Socratic micro-challenge." in SYSTEM_PROMPT,
                "practice_only_micro_challenge": "Only use one very sparingly when the student explicitly asks to practice" in SYSTEM_PROMPT,
            }
            print("PAYLOAD::" + json.dumps(payload))
            """,
            env=_smoke_env(),
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = _extract_payload(result.stdout)
        self.assertEqual(
            payload,
            {
                "clean_ending_default": True,
                "no_default_micro_challenge": True,
                "practice_only_micro_challenge": True,
            },
        )
