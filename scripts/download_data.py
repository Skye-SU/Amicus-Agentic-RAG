"""
Data collection script for Amicus.
Downloads free educational resources and copies local files.
"""

import argparse
import sys
from pathlib import Path

import requests

try:
    from markdownify import markdownify as md
except ImportError:
    print("markdownify not installed. Run: pip install markdownify")
    md = None

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
GIT_LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1"

WEB_RESOURCES = {
    "python": [
        {
            "url": "https://docs.python.org/3/tutorial/introduction.html",
            "filename": "python_tutorial_intro.md",
            "format": "html",
        },
        {
            "url": "https://docs.python.org/3/tutorial/controlflow.html",
            "filename": "python_tutorial_controlflow.md",
            "format": "html",
        },
        {
            "url": "https://docs.python.org/3/tutorial/datastructures.html",
            "filename": "python_tutorial_datastructures.md",
            "format": "html",
        },
        {
            "url": "https://do1.dr-chuck.com/pythonlearn/EN_us/pythonlearn.pdf",
            "filename": "py4e_textbook.pdf",
            "format": "binary",
        },
    ],
    "statistics": [
        {
            "url": "https://docs.scipy.org/doc/scipy/tutorial/stats.html",
            "filename": "scipy_stats_tutorial.md",
            "format": "html",
        },
        {
            "url": "https://greenteapress.com/thinkstats2/thinkstats2.pdf",
            "filename": "thinkstats2.pdf",
            "format": "binary",
            "min_size_bytes": 100_000,
        },
        {
            "url": "https://www.statsmodels.org/stable/regression.html",
            "filename": "statsmodels_regression.md",
            "format": "html",
        },
    ],
    "nlp": [
        {
            "url": "https://spacy.io/usage/linguistic-features",
            "filename": "spacy_linguistic_features.md",
            "format": "html",
        },
        {
            "url": "https://www.nltk.org/book/ch01.html",
            "filename": "nltk_book_ch01.md",
            "format": "html",
        },
    ],
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def is_git_lfs_pointer(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            return f.read(len(GIT_LFS_POINTER_PREFIX)).startswith(GIT_LFS_POINTER_PREFIX)
    except OSError:
        return False


def is_valid_download(path: Path, resource: dict) -> bool:
    if not path.exists() or path.stat().st_size == 0:
        return False
    if is_git_lfs_pointer(path):
        return False

    if resource["format"] == "binary":
        min_size = resource.get("min_size_bytes", 1024)
        if path.stat().st_size < min_size:
            return False
        if path.suffix.lower() == ".pdf":
            with path.open("rb") as f:
                return f.read(4) == b"%PDF"

    return True


def download_html_as_md(url: str, save_path: Path) -> bool:
    """Download an HTML page and convert to Markdown."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        if md is None:
            save_path.write_text(resp.text, encoding="utf-8")
            print(f"  [WARN] markdownify unavailable, saved raw HTML: {save_path.name}")
        else:
            markdown_text = md(resp.text, heading_style="ATX", strip=["script", "style"])
            save_path.write_text(markdown_text, encoding="utf-8")
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to download {url}: {e}")
        return False


def _stream_binary(url: str, save_path: Path) -> None:
    resp = requests.get(url, headers=HEADERS, timeout=120, stream=True)
    resp.raise_for_status()
    with open(save_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)


def download_binary(
    url: str,
    save_path: Path,
    fallback_url: str = None,
    resource: dict | None = None,
) -> bool:
    """Download a binary file (PDF, etc.)."""
    temp_path = save_path.with_name(f".{save_path.name}.download")
    try:
        _stream_binary(url, temp_path)
        if resource and not is_valid_download(temp_path, resource):
            raise ValueError("downloaded file failed validation")
        temp_path.replace(save_path)
        return True
    except Exception as e:
        print(f"  [WARN] Primary URL failed ({e})")
        if fallback_url:
            print(f"  Trying fallback URL: {fallback_url}")
            try:
                _stream_binary(fallback_url, temp_path)
                if resource and not is_valid_download(temp_path, resource):
                    raise ValueError("fallback file failed validation")
                temp_path.replace(save_path)
                return True
            except Exception as e2:
                print(f"  [ERROR] Fallback also failed: {e2}")
        temp_path.unlink(missing_ok=True)
        return False


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable form."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Amicus public reference materials."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the collection plan without downloading anything.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download files even when existing local files look valid.",
    )
    return parser.parse_args(argv)


def ensure_data_dirs():
    for subdir in ["python", "statistics", "nlp", "legal"]:
        (DATA_DIR / subdir).mkdir(parents=True, exist_ok=True)


def print_collection_plan():
    print("\n--- Public web resources ---")
    for topic, resources in WEB_RESOURCES.items():
        print(f"  {topic}: {len(resources)} files")
        for res in resources:
            print(f"    - {res['filename']} <- {res['url']}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    print("=" * 60)
    print("Amicus — Data Collection")
    print("=" * 60)

    print_collection_plan()
    if args.dry_run:
        print("\nDry run only. No files were downloaded.")
        return 0

    ensure_data_dirs()
    success = []
    failed = []

    for topic, resources in WEB_RESOURCES.items():
        print(f"\n--- Downloading {topic.upper()} resources ---")
        for res in resources:
            save_path = DATA_DIR / topic / res["filename"]
            print(f"  Downloading: {res['filename']}...")

            if not args.force and is_valid_download(save_path, res):
                ok = True
                print(f"  ✓ Already valid: {save_path.relative_to(BASE_DIR)}")
            elif res["format"] == "html":
                ok = download_html_as_md(res["url"], save_path)
            else:
                ok = download_binary(res["url"], save_path, res.get("fallback_url"), res)

            if ok:
                success.append(save_path)
                print(f"  ✓ Saved: {save_path.relative_to(BASE_DIR)}")
            else:
                failed.append(res["filename"])

    print("\n" + "=" * 60)
    print("COLLECTION SUMMARY")
    print("=" * 60)
    print(f"\nSuccessfully collected: {len(success)} files")
    print(f"Failed: {len(failed)} files")

    if success:
        print("\n{:<50} {:>10}".format("File", "Size"))
        print("-" * 62)
        for path in success:
            size = path.stat().st_size if path.exists() else 0
            print(f"{str(path.relative_to(BASE_DIR)):<50} {format_size(size):>10}")

    if failed:
        print("\nFailed downloads:")
        for f in failed:
            print(f"  ✗ {f}")

    print("\nDone!")
    return 1 if failed else 0


def ensure_reference_data(force: bool = False) -> bool:
    """Ensure public reference materials are present and not LFS pointers."""
    args = ["--force"] if force else []
    return main(args) == 0


if __name__ == "__main__":
    sys.exit(main())
