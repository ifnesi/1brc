# 1BRC: One Billion Row Challenge in Python

Python implementation of Gunnar's 1 billion row challenge:
- https://www.morling.dev/blog/one-billion-row-challenge
- https://github.com/gunnarmorling/1brc

## Creating the measurements file with 1B rows

First install the Python requirements:
```shell
python3 -m pip install -r requirements.txt
```

The script `createMeasurements.py` will create the measurement file:
```
usage: createMeasurements.py [-h] [-o OUTPUT] [-r RECORDS]

Create measurement file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Measurement file name (default is "measurements.txt")
  -r RECORDS, --records RECORDS
                        Number of records to create (default is 1_000_000_000)
```

Example:
```
% python3 createMeasurements.py
Creating measurement file 'measurements.txt' with 1,000,000,000 measurements...
100%|█████████████████████████████████████████| 100/100 [01:15<00:00,  1.32it/s]
Created file 'measurements.txt' with 1,000,000,000 measurements in 75.86 seconds
```

Be patient as it can take more than a minute to have the file generated.

Maybe as another challenge is to speed up the generation of the measurements file :slightly_smiling_face:

## Performance (on a MacBook Pro M1 32GB)
| Interpreter | Script | user | system | cpu | total |
| ----------- | ------ | ---- | ------ | --- | ----- |
| python3 | calculateAveragePolars.py | 77.84 | 3.64 | 703% | 11.585 |
| pypy3 | calculateAveragePypy.py | ~~139.15~~<br>135.25 | ~~3.02s~~<br>2.92 | ~~699%~~<br>735% | ~~20.323~~<br>18.782 |
| python3 | calculateAverageDuckDB.py | 186.78 | 4.21 | 806% | 23.673 |
| pypy3 | calculateAverage.py | ~~284.90~~<br>242.89 | ~~9.12~~<br>6.28 | ~~749%~~<br>780% | ~~39.236~~<br>31.926 |
| python3 | calculateAverage.py | ~~378.54~~<br>329.20 | ~~6.94~~<br>3.77 | ~~747%~~<br>793% | ~~51.544~~<br>41.941 |
| python3 | calculateAveragePypy.py | ~~573.77~~<br>510.93 | ~~2.70~~<br>1.88 | ~~787%~~<br>793% | ~~73.170~~<br>64.660 |

The script `calculateAveragePolars.py` was suggested by [Taufan](https://github.com/mtaufanr) on this [post](https://github.com/gunnarmorling/1brc/discussions/62#discussioncomment-8026402).

The script `calculateAveragePypy.py` was created by [donalm](https://github.com/donalm), a +2x improved version of the initial script (`calculateAverage.py`) when running in pypy3, even capable of beating the implementation using [DuckDB](https://duckdb.org/) `calculateAverageDuckDB.py`.

[Olivier Scalbert](https://github.com/oscalbert) has made a simple but incredible suggestion where performance increased by an average of 15% (table above has been updated), thank you :slightly_smiling_face:

His suggestions were to change from:
```python
if measurement < result[location][0]:
    result[location][0] = measurement
if measurement > result[location][1]:
    result[location][1] = measurement
result[location][2] += measurement
result[location][3] += 1
```

to:
```python
_result = result[location]
if measurement < _result[0]:
    _result[0] = measurement
if measurement > _result[1]:
    _result[1] = measurement
_result[2] += measurement
_result[3] += 1
```

Python can be surprising sometimes.

## Compare results

Run `compare.sh` if you want to check that all the scripts produce the same output.
