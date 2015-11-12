from collections import defaultdict
import random
import statistics


class SaneList(list):
    """Like the standard list but raises IndexError on negative subscripts."""
    def __getitem__(self, index):
        if index < 0:
            raise IndexError
        else:
            return super(__class__, self).__getitem__(index)


class SaneList_NoExcept(SaneList):
    """Like SaneList but __getitem__ returns None instead of raising IndexError."""
    def __getitem__(self, index):
        try:
            return super(__class__, self).__getitem__(index)
        except IndexError:
            return None


def Tree():
    """Tree based on autovivificated dict."""
    return defaultdict(Tree)


class MarkovChain:
    """Word generator based on Markov chains.

    Members:
    - samples: Samples passed to the constructor.
    - chain_order: The order of the used Markov chain.
    - mean_length: Mean length of the samples.
    - length_deviation: Standard deviation of the length of the samples.
    - chains: The Markov chain tree.

    """
    def __init__(self, samples, chain_order=1):
        """Create a Markov chain of a given order with the given samples."""
        self.samples = samples
        self.chain_order = chain_order
        if self.samples:
            self._process_samples(self.samples)

    def add_samples(self, new_samples):
        self._build_tree(new_samples);
        self.samples.extend(new_samples)
        self._calculate_length_stats(self.samples)

    def _process_samples(self, samples):
        self._calculate_length_stats(samples)
        self._build_tree(samples)

    def _calculate_length_stats(self, samples):
        sample_lengths = [len(sample) for sample in samples]
        self.mean_length = statistics.mean(sample_lengths)
        self.length_deviation = statistics.stdev(sample_lengths)

    def _build_tree(self, samples):
        self.chains = Tree()
        for sample in samples:
            sample = SaneList_NoExcept(sample)
            self._build_subtree(sample)

    def _build_subtree(self, sample):
        for i in range(len(sample)):
            chain = self.chains
            for j in range(i, i-self.chain_order+1, -1):
                # Walk back through all the elements to memorize
                # except the last one. Create a path in the tree while
                # doing so.
                last = sample[j-1]
                chain = chain[last]

            last = sample[i-self.chain_order]
            if not chain.get(last):
                # Create a tree leaf if not present already.
                chain[last] = []
            chain[last].append(sample[i])

    def _get_random_character(self, result):
        chain = self.chains
        for i in range(0, self.chain_order):
            try:
                last = result[-i-1]
            except IndexError:
                last = None
            chain = chain.get(last)
            if not chain:
                # No known next element.
                raise KeyError
        return random.choice(chain)

    def generate(self, length=0):
        while not length > 0:
            length = random.gauss(self.mean_length, self.length_deviation)

        result = []
        while len(result) < length:
            try:
                result.append(self._get_random_character(result))
            except KeyError:
                # Try again.
                result = []
        return result

    def generate_name(self):
        return "".join(self.generate())
