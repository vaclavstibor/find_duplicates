import hashlib
import math


class BloomFilter:
    def __init__(self, capacity, num_hashes):
        self.capacity = capacity
        self.num_hashes = num_hashes
        self.bitfield = bytearray((capacity + 7) // 8)

    def _hashes(self, item):
        hash1 = int(hashlib.md5(item.encode()).hexdigest(), 16)
        hash2 = int(hashlib.sha1(item.encode()).hexdigest(), 16)
        for i in range(self.num_hashes):
            yield (hash1 + i * hash2) % self.capacity

    def add(self, item):
        for pos in self._hashes(item):
            self.bitfield[pos // 8] |= 1 << (pos % 8)

    def __contains__(self, item):
        return all(
            self.bitfield[pos // 8] & (1 << (pos % 8)) for pos in self._hashes(item)
        )


def find_duplicates(data_generator) -> list:
    """Find duplicates using Bloom filters."""

    epsilon = 0.0000000001  # Desired false positive rate
    num_bloom_filters = 7  # Number of Bloom filters

    # Calculate the number of hash functions
    num_hashes = math.ceil(math.log(1 / epsilon))

    # Calculate the total number of bits needed for the Bloom filter
    n = data_generator.length  # Number of items
    m = math.ceil((num_hashes * n) / math.log(2))

    # Calculate the capacity of each Bloom filter
    bloom_capacity = m // num_bloom_filters

    print(
        f"- num_bloom_filters: {num_bloom_filters} \n- bloom_capacity: {bloom_capacity} \n- num_hashes: {num_hashes}"
    )

    # Create Bloom filters
    bloom_filters = [
        BloomFilter(capacity=bloom_capacity, num_hashes=num_hashes)
        for _ in range(num_bloom_filters)
    ]

    duplicates = set()

    def select_filter(line):
        """
        Selects a bloom filter based on the hash of the line.
        """
        return int(hashlib.md5(line.encode()).hexdigest(), 16) % num_bloom_filters

    for line in data_generator:
        filter_index = select_filter(line)
        bloom_filter = bloom_filters[filter_index]

        if line in bloom_filter:
            duplicates.add(line)
        else:
            bloom_filter.add(line)

    return list(duplicates)
