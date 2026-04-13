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
    return subprocess.run(
        [PYTHON, *args],
        cwd=cwd or REPO_ROOT,
        env=env,
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
