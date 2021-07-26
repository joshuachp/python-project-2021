# Sentimental analysis

Sentimental analysis of text from stdin, json or csv file.

The project has a `main.py` in the `src/` directory. The requirements are
listed in `requirements.txt`. The rest of the code is implemented in the
`sentiment_analysis` module.

## Input

The input file can be:

1. STDIN
2. JSON file with a single Array of Objects with a `text` field.
3. CSV file with at least 4 columns, it will use the first as id (`int`) and
   the fourth as text.

## Test

The project has some basic unit test throw `pytest` in the `tests/` directory.
