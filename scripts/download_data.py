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
            "url": "https://www.openintro.org/go?id=os4_for_screen_readers&referrer=/book/os/index.php",
            "filename": "openintro_statistics.pdf",
            "format": "binary",
            "fallback_url": "https://github.com/OpenIntroStat/openintro-statistics/raw/master/OS4_for_screen_readers.pdf",
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


def download_binary(url: str, save_path: Path, fallback_url: str = None) -> bool:
    """Download a binary file (PDF, etc.)."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=120, stream=True)
        resp.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  [WARN] Primary URL failed ({e})")
        if fallback_url:
            print(f"  Trying fallback URL: {fallback_url}")
            try:
                resp = requests.get(fallback_url, headers=HEADERS, timeout=120, stream=True)
                resp.raise_for_status()
                with open(save_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            except Exception as e2:
                print(f"  [ERROR] Fallback also failed: {e2}")
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

            if res["format"] == "html":
                ok = download_html_as_md(res["url"], save_path)
            else:
                ok = download_binary(res["url"], save_path, res.get("fallback_url"))

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


if __name__ == "__main__":
    sys.exit(main())
