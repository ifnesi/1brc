# time pypy3 calculateAveragePypy.py
import argparse
import os
import multiprocessing as mp
from gc import disable as gc_disable, enable as gc_enable


def get_file_chunks(
    file_name: str,
    max_cpu: int = 8,
) -> list:
    """Split flie into chunks"""
    cpu_count = min(max_cpu, mp.cpu_count())

    file_size = os.path.getsize(file_name)
    chunk_size = file_size // cpu_count

    start_end = list()
    with open(file_name, "r+b") as f:

        def is_new_line(position):
            if position == 0:
                return True
            else:
                f.seek(position - 1)
                return f.read(1) == b"\n"

        def next_line(position):
            f.seek(position)
            f.readline()
            return f.tell()

        chunk_start = 0
        while chunk_start < file_size:
            chunk_end = min(file_size, chunk_start + chunk_size)

            while not is_new_line(chunk_end):
                chunk_end -= 1

            if chunk_start == chunk_end:
                chunk_end = next_line(chunk_end)

            start_end.append(
                (
                    file_name,
                    chunk_start,
                    chunk_end,
                )
            )

            chunk_start = chunk_end

    return (
        cpu_count,
        start_end,
    )


def _process_file_chunk(
    file_name: str,
    chunk_start: int,
    chunk_end: int,
    blocksize: int = 1024 * 1024,
) -> dict:
    """Process each file chunk in a different process"""
    result = dict()

    with open(file_name, "r+b") as fh:
        fh.seek(chunk_start)
        gc_disable()

        tail = b""
        location = None
        byte_count = chunk_end - chunk_start

        while byte_count > 0:
            if blocksize > byte_count:
                blocksize = byte_count
            byte_count -= blocksize

            index = 0
            data = tail + fh.read(blocksize)
            while data:
                if location is None:
                    try:
                        semicolon = data.index(b";", index)
                    except ValueError:
                        tail = data[index:]
                        break

                    location = data[index:semicolon]
                    index = semicolon + 1

                try:
                    newline = data.index(b"\n", index)
                except ValueError:
                    tail = data[index:]
                    break

                value = float(data[index:newline])
                index = newline + 1
                try:
                    _result = result[location]
                    if value < _result[0]:
                        _result[0] = value
                    if value > _result[1]:
                        _result[1] = value
                    _result[2] += value
                    _result[3] += 1
                except KeyError:
                    result[location] = [
                        value,
                        value,
                        value,
                        1,
                    ]  # min, max, sum, count

                location = None
        
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
            if location not in result:
                result[location] = measurements
            else:
                _result = result[location]
                if measurements[0] < _result[0]:
                    _result[0] = measurements[0]
                if measurements[1] > _result[1]:
                    _result[1] = measurements[1]
                _result[2] += measurements[2]
                _result[3] += measurements[3]

    # Print final results
    print("{", end="")
    for location, measurements in sorted(result.items()):
        print(
            f"{location.decode('utf-8')}={measurements[0]:.1f}/{(measurements[2] / measurements[3]) if measurements[3] !=0 else 0:.1f}/{measurements[1]:.1f}",
            end=", ",
        )
    print("\b\b} ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate average of measurements.")
    parser.add_argument(
        "-i",
        "--input",
        dest="input",
        type=str,
        help='Measurement file name (default is "measurements.txt")',
        default="measurements.txt",
    )
    
    args = parser.parse_args()
    cpu_count, *start_end = get_file_chunks(args.input)
    process_file(cpu_count, start_end[0])
