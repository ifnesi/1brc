python calculateAverage.py > python.txt
python calculateAveragePypy.py > pypy.txt
python calculateAveragePolars.py > polars.txt
python calculateAverageDuckDB.py > duckdb.txt
git diff --no-index --word-diff=porcelain python.txt pypy.txt
git diff --no-index --word-diff=porcelain python.txt polars.txt
git diff --no-index --word-diff=porcelain python.txt duckdb.txt
