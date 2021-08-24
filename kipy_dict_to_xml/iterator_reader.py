import io

_empty_bytearray = bytearray(0)

class IteratorReader(io.RawIOBase):
    def __init__(self, iterator):
        self.iterator = iterator
        self.buffer = bytearray()
        self.index = 0

    def readinto(self, buffer: bytearray) -> int:
        buffer_size = len(buffer)

        p = 0
        l = len(self.buffer)
        index = self.index

        # Fill buffer from previous buffered data
        while True:
            block_size = min(buffer_size - p, l - index)

            if block_size <= 0:
                break

            buffer[p:p+block_size] = self.buffer[index:index + block_size]

            index += block_size
            p += block_size

            if p >= buffer_size:  # buffer full
                self.index = index
                return p

        self.buffer = _empty_bytearray
        self.index = 0

        try:
            while True:
                data_block = next(self.iterator)
                data_size = len(data_block)

                if data_size == 0:
                    continue

                block_size = min(buffer_size - p, data_size)

                if block_size == 0:
                    break

                buffer[p:p+block_size] = data_block if block_size == data_size else data_block[0:block_size]

                p = p + block_size

                if p < buffer_size:
                    continue

                self.buffer = data_block
                self.index = block_size

                return p

        except StopIteration:
            return p

    def readable(self) -> bool:
        return True

