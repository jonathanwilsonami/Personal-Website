# Utilities Guide

## Book Card Generator

`tools/book_cards.py` downloads book cover images from Open Library and generates Quarto-formatted book cards.

### Usage

Generate one or more books:

```bash
uv run tools/book_cards.py \
  "Thinking, Fast and Slow" \
  "The Pragmatic Programmer" \
  "Designing Data-Intensive Applications"
```

Write the generated Quarto markup to a file:

```bash
uv run tools/book_cards.py \
  "Thinking, Fast and Slow" \
  "The Pragmatic Programmer" \
  -o generated-books.qmd
```

Book covers are saved to:

```text
images/books/
```

### Options

```text
--image-dir PATH      Set the book cover directory.
-o, --output FILE     Write generated markup to a file.
--no-heading TITLE    Omit the ### heading for a specific book.
--force               Redownload an existing cover.
```

View all options:

```bash
uv run tools/book_cards.py --help
```

### Output

Generated Quarto markup:

```markdown
::: {.book}
::: {.book-cover}
[![Thinking, Fast and Slow](/images/books/thinking-fast-and-slow.jpg)](https://www.amazon.com/dp/0374533555){target="_blank" rel="noopener"}
:::
::: {.book-body}
### Thinking, Fast and Slow
*Daniel Kahneman*

:::
:::
```

The area beneath the author is intentionally left blank for personal commentary.
