#!/usr/bin/env python3

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote_plus
from urllib.request import Request, urlopen


OPEN_LIBRARY_SEARCH = "https://openlibrary.org/search.json"
COVER_BASE = "https://covers.openlibrary.org/b"

# Replace this with your own contact information.
# Open Library recommends identifying applications making API requests.
USER_AGENT = "book-card-generator/1.0 (your-email@example.com)"


def slugify(text: str) -> str:
    """Convert a book title into a filename-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def normalize_title(text: str) -> str:
    """Normalize titles for comparison."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def request_json(url: str) -> dict:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )

    with urlopen(request, timeout=20) as response:
        return json.load(response)


def title_match_score(query: str, candidate: dict) -> float:
    """Score Open Library results against the requested title."""
    query_norm = normalize_title(query)
    candidate_norm = normalize_title(candidate.get("title", ""))

    score = SequenceMatcher(
        None,
        query_norm,
        candidate_norm,
    ).ratio()

    # Strongly prefer exact normalized title matches.
    if query_norm == candidate_norm:
        score += 0.25

    # Slightly prefer entries that already have a known cover.
    if candidate.get("cover_i"):
        score += 0.05

    return score


def search_book(title: str) -> dict:
    """Find the best matching Open Library record for a title."""
    params = urlencode(
        {
            "title": title,
            "fields": "key,title,author_name,isbn,cover_i,first_publish_year",
            "limit": 10,
        }
    )

    url = f"{OPEN_LIBRARY_SEARCH}?{params}"
    data = request_json(url)

    results = data.get("docs", [])

    if not results:
        raise RuntimeError(f"No Open Library results found for: {title}")

    best_match = max(
        results,
        key=lambda book: title_match_score(title, book),
    )

    return best_match


def clean_isbn(isbn: str) -> str:
    return re.sub(r"[^0-9Xx]", "", isbn).upper()


def isbn13_to_isbn10(isbn13: str) -> str | None:
    """
    Convert a 978-prefixed ISBN-13 to ISBN-10.

    979 ISBNs do not have an ISBN-10 equivalent.
    """
    isbn13 = clean_isbn(isbn13)

    if len(isbn13) != 13 or not isbn13.startswith("978"):
        return None

    first_nine = isbn13[3:12]

    total = sum(
        (10 - i) * int(digit)
        for i, digit in enumerate(first_nine)
    )

    check_value = (-total) % 11
    check_digit = "X" if check_value == 10 else str(check_value)

    return first_nine + check_digit


def choose_isbn10(isbns: list[str]) -> str | None:
    """Find or derive an ISBN-10 suitable for an Amazon /dp/ URL."""
    cleaned = [clean_isbn(isbn) for isbn in isbns]

    # Prefer an ISBN-10 Open Library already provides.
    for isbn in cleaned:
        if len(isbn) == 10:
            return isbn

    # Otherwise convert a 978 ISBN-13.
    for isbn in cleaned:
        converted = isbn13_to_isbn10(isbn)
        if converted:
            return converted

    return None


def make_amazon_url(title: str, isbns: list[str]) -> str:
    """
    Generate an Amazon URL.

    Physical books generally use ISBN-10 as their Amazon ASIN,
    allowing the compact /dp/<ISBN10> URL.
    """
    isbn10 = choose_isbn10(isbns)

    if isbn10:
        return f"https://www.amazon.com/dp/{isbn10}"

    # Fall back to an Amazon title search if we cannot derive an ISBN-10.
    return f"https://www.amazon.com/s?k={quote_plus(title)}"


def download_file(url: str, destination: Path) -> None:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "image/*",
        },
    )

    with urlopen(request, timeout=30) as response:
        destination.write_bytes(response.read())


def download_cover(
    book: dict,
    destination: Path,
) -> str:
    """
    Download a large Open Library cover.

    Prefer cover ID because it identifies the cover directly.
    Fall back to ISBN when necessary.
    """
    urls = []

    cover_id = book.get("cover_i")

    if cover_id:
        urls.append(
            f"{COVER_BASE}/id/{cover_id}-L.jpg?default=false"
        )

    for isbn in book.get("isbn", []):
        isbn = clean_isbn(isbn)

        urls.append(
            f"{COVER_BASE}/isbn/{isbn}-L.jpg?default=false"
        )

    if not urls:
        raise RuntimeError("Book has no cover ID or ISBN.")

    for url in urls:
        try:
            download_file(url, destination)
            return url

        except (HTTPError, URLError):
            continue

    raise RuntimeError("No usable cover image was found.")


def make_quarto_block(
    title: str,
    author: str,
    image_filename: str,
    amazon_url: str,
    include_heading: bool = True,
) -> str:

    image_url = f"/images/books/{image_filename}"

    heading = f"### {title}\n" if include_heading else ""
    author_line = f"*{author}*" if author else ""

    return f"""::: {{.book}}
::: {{.book-cover}}
[![{title}]({image_url})]({amazon_url}){{target="_blank" rel="noopener"}}
:::
::: {{.book-body}}
{heading}{author_line}

:::
:::"""


def process_book(
    title: str,
    image_dir: Path,
    include_heading: bool = True,
    force: bool = False,
) -> str:

    print(
        f"Looking up: {title}",
        file=sys.stderr,
    )

    book = search_book(title)

    authors = book.get("author_name", [])
    author = ", ".join(authors)

    isbns = book.get("isbn", [])

    filename = f"{slugify(title)}.jpg"
    destination = image_dir / filename

    if not destination.exists() or force:
        download_cover(book, destination)

        print(
            f"Downloaded: {destination}",
            file=sys.stderr,
        )
    else:
        print(
            f"Exists: {destination}",
            file=sys.stderr,
        )

    amazon_url = make_amazon_url(
        title,
        isbns,
    )

    return make_quarto_block(
        title=title,
        author=author,
        image_filename=filename,
        amazon_url=amazon_url,
        include_heading=include_heading,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Download book covers from Open Library "
            "and generate Quarto book cards."
        )
    )

    parser.add_argument(
        "titles",
        nargs="+",
        help="One or more book titles.",
    )

    parser.add_argument(
        "--image-dir",
        default="images/books",
        help="Local directory for downloaded covers.",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Write generated Quarto markup to a file.",
    )

    parser.add_argument(
        "--no-heading",
        action="append",
        default=[],
        metavar="TITLE",
        help=(
            "Do not generate the ### heading for this title. "
            "May be used multiple times."
        ),
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Redownload covers that already exist.",
    )

    args = parser.parse_args()

    image_dir = Path(args.image_dir)
    image_dir.mkdir(parents=True, exist_ok=True)

    no_heading = {
        title.casefold()
        for title in args.no_heading
    }

    blocks = []

    for title in args.titles:
        try:
            block = process_book(
                title=title,
                image_dir=image_dir,
                include_heading=(
                    title.casefold() not in no_heading
                ),
                force=args.force,
            )

            blocks.append(block)

        except Exception as exc:
            print(
                f"ERROR: {title}: {exc}",
                file=sys.stderr,
            )

    result = "\n\n".join(blocks)

    if args.output:
        Path(args.output).write_text(
            result + "\n",
            encoding="utf-8",
        )

        print(
            f"Generated: {args.output}",
            file=sys.stderr,
        )
    else:
        print(result)


if __name__ == "__main__":
    main()