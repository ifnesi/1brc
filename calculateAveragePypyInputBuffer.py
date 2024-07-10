from multiprocessing import Pool
import os
import math


FILE_PATH = "measurements.txt"
PROCESS_COUNT = os.cpu_count()
BUFFER_SIZE = 1024 * 128

NEW_LINE_ORD = ord(b"\n")
SEMICOLON_ORD = ord(b";")


def create_chunks():
    s = os.stat(FILE_PATH)
    FILE_SIZE = s.st_size

    CHUNK_SIZE = math.ceil(FILE_SIZE / PROCESS_COUNT)

    chunks = [[i * CHUNK_SIZE, min((i+1) * CHUNK_SIZE, FILE_SIZE - 1)] for i in range(PROCESS_COUNT)]

    # align chunks to \n
    ALIGN_RANGE = 40

    with open(FILE_PATH, "rb") as f:
        for chunk_num, chunk in enumerate(chunks):
            start, end = chunk
            if start == 0:
                continue

            f.seek(start - ALIGN_RANGE)
            haystack = f.read(ALIGN_RANGE)

            # find next \n in haystack
            for pos, c in enumerate(reversed(haystack)):
                if c == ord('\n'):
                    break
            else:
                raise Exception("ALIGN_RANGE too small, no \\n found")

            chunks[chunk_num][0] -= pos
            chunks[chunk_num - 1][1] -= pos

    return chunks


def parse_partial(chunk):
    result = dict()

    start, end = chunk

    with open(FILE_PATH, "rb") as f:
        f.seek(start)

        buffer = memoryview(bytearray(BUFFER_SIZE))
        buffer_view = buffer
        tail_size = 0

        bytes_left = end - start + 1  # end is 0 indexed, so we add 1

        while bytes_left > 0:
            if tail_size > 0:
                # write tail to the front of the buffer
                buffer[:tail_size] = buffer_view[-tail_size:]

            # fill buffer from file
            bytes_read = f.readinto1(buffer[tail_size:])

            if bytes_read > bytes_left:
                # if we have read too much we shrink our buffer view
                buffer_view = buffer[:tail_size + bytes_left]  # bytes_left is negative, so we create a smaller view on our buffer
            else:
                buffer_view = buffer[:tail_size + bytes_read]

            bytes_left -= bytes_read

            buffer_cursor = 0
            while True:
                cursor_view = buffer_view[buffer_cursor:]

                # find semicolon and new line characters
                for index, c in enumerate(cursor_view):
                    if c == NEW_LINE_ORD:
                        newline_index = index
                        break
                    elif c == SEMICOLON_ORD:
                        semicolon_index = index
                else:
                    # no complete line was found, break and read next part of data
                    tail_size = len(buffer_view) - buffer_cursor
                    break

                line = bytes(cursor_view[:newline_index])
                city = line[:semicolon_index]
                temp = int(line[semicolon_index+1:-2] + line[-1:])

                try:
                    result_values = result[city]
                    if temp < result_values[0]:
                        result_values[0] = temp
                    if temp > result_values[1]:
                        result_values[1] = temp
                    result_values[2] += temp
                    result_values[3] += 1
                except KeyError:
                    result[city] = [temp, temp, temp, 1]

                buffer_cursor += newline_index + 1

        return result


if __name__ == "__main__":
    chunks = create_chunks()

    with Pool(processes=PROCESS_COUNT) as p:
        results = p.map(parse_partial, chunks)

    overall_result = dict()

    # add all results
    for result in results:
        for city, values in result.items():
            try:
                overall_result_values = overall_result[city]
                if values[0] < overall_result_values[0]:
                    overall_result_values[0] = values[0]
                if values[1] > overall_result_values[1]:
                    overall_result_values[1] = values[1]
                overall_result_values[2] += values[2]
                overall_result_values[3] += values[3]
            except KeyError:
                overall_result[city] = [values[0], values[1], values[2], values[3]]

    # Print final results
    print("{", end="")
    for city, measurements in sorted(overall_result.items()):
        print(
            f"{city.decode('utf-8')}={measurements[0] / 10:.1f}/{(measurements[2] / 10 / measurements[3]) if measurements[3] !=0 else 0:.1f}/{measurements[1] / 10:.1f}",
            end=", ",
        )
    print("\b\b} ")
