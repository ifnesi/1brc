# time python3 calculateAverage.py
import os
from gc import disable as gc_disable, enable as gc_enable
import multiprocessing as mp


def get_file_chunks(
    file_name: str,
    max_cpu: int = 8,
) -> tuple[int, list]:
    """Split file into chunks"""
    cpu_count = min(max_cpu, mp.cpu_count())
    file_size = os.path.getsize(file_name)
    chunk_size = file_size // cpu_count
    chunks = [
        (file_name, offset, offset + chunk_size)
        for offset in range(0, file_size, chunk_size)
    ]
    # ensure last chunk covers any remaining bits
    chunks[-1] = (file_name, chunks[-1][1], file_size)
    return cpu_count, chunks


def _process_file_chunk(
    file_name: str,
    chunk_start: int,
    chunk_end: int,
) -> dict:
    """Process each file chunk in a different process"""
    result = dict()
    with open(file_name, encoding="utf-8", mode="rb") as f:
        f.seek(chunk_start)
        gc_disable()
        if chunk_start != 0 and f.peek(1) != b"\n":
            _ = next(f)  # skip incomplete line

        for line in f:
            location, measurement = line.split(b";")
            measurement = float(measurement)
            _result = result.get(location)
            if _result:
                if measurement < _result[0]:
                    _result[0] = measurement
                if measurement > _result[1]:
                    _result[1] = measurement
                _result[2] += measurement
                _result[3] += 1
            else:
                result[location] = [
                    measurement,
                    measurement,
                    measurement,
                    1,
                ]  # min, max, sum, count

            if (chunk_start := chunk_start + len(line)) > chunk_end:
                break

        gc_enable()
    return result


def process_file(
    cpu_count: int,
    start_end: list,
) -> dict:
    """Process data file"""
    with mp.Pool(cpu_count) as p:
        # Run chunks in parallel
        chunk_results = p.starmap(
            _process_file_chunk,
            start_end,
        )

    # Combine all results from all chunks
    result = dict()
    for chunk_result in chunk_results:
        for location, measurements in chunk_result.items():
            _result = result.get(location)
            if _result:
                if measurements[0] < _result[0]:
                    _result[0] = measurements[0]
                if measurements[1] > _result[1]:
                    _result[1] = measurements[1]
                _result[2] += measurements[2]
                _result[3] += measurements[3]
            else:
                result[location] = measurements
    # Print final results
    print("{", end="")
    for location, measurements in sorted(result.items()):
        print(
            f"{location.decode('utf8')}={measurements[0]:.1f}/{(measurements[2] / measurements[3]) if measurements[3] != 0 else 0:.1f}/{measurements[1]:.1f}",
            end=", ",
        )
    print("\b\b} ")


if __name__ == "__main__":
    cpu_count, start_end = get_file_chunks("measurements.txt")
    process_file(cpu_count, start_end)
