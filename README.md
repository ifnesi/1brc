# 1BRC: One Billion Row Challenge in Python

Python implementation of Gunnar's 1 billion row challenge:
- https://www.morling.dev/blog/one-billion-row-challenge
- https://github.com/gunnarmorling/1brc

## Performance (on a MacBook Pro M1 32GB)
| Interperter | Script | user | system | cpu | total |
| ----------- | ------ | ---- | ------ | --- | ----- |
| pypy3 | calculateAveragePypy.py | 139.15s | 3.02s | 699% | 20.323 |
| python3 | calculateAverageDuckDB.py | 186.78s | 4.21s | 806% | 23.673 |
| pypy3 | calculateAverage.py | 284.90s | 9.12s | 749% | 39.236 |
| pypy3 | calculateAverage.py | 286.33s | 9.57s | 746% | 39.665 |
| python3 | calculateAverage.py | 378.54s | 6.94s | 747% | 51.544 |

The file `calculateAveragePypy.py` was created by [donalm](https://github.com/donalm), a +2x improved version of the initial script (`calculateAverage.py`) when running in pypy3, even capable of beating the implementation using (DuckDB)[https://duckdb.org/] `calculateAverageDuckDB.py`.