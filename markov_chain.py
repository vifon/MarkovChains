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
    def __init__(self, samples, chain_order=1):
        self.samples = samples
        self.chain_order = chain_order
        self._process_samples()


    def _process_samples(self):
        sample_lengths = [len(sample) for sample in self.samples]
        self.mean_length = statistics.mean(sample_lengths)
        self.length_deviation = statistics.stdev(sample_lengths)

        self.chains = Tree()
        for sample in self.samples:
            sample = SaneList_NoExcept(sample)
            self._create_chain(sample, self.chain_order)


    def _create_chain(self, sample, chain_order):
        for i in range(len(sample)):
            chain = self.chains
            for j in range(i, i-chain_order+1, -1):
                # Walk back through all the elements to memorize
                # except the last one. Create the chain in the tree
                # while doing so.
                last = sample[j-1]
                chain = chain[last]

            last = sample[i-chain_order]
            if not chain.get(last):
                # Create a tree leaf if not present already.
                chain[last] = []
            chain[last].append(sample[i])


    def _get_random_character(self, chain, result, chain_order):
        for i in range(0, chain_order):
            try:
                last = result[-i-1]
            except IndexError:
                last = None
            chain = chain.get(last)
            if not chain:
                # Empty or not existing chain: there is not such
                # sequence in the sample.
                raise KeyError
        return random.choice(chain)


    def generate(self):
        length = random.gauss(self.mean_length, self.length_deviation)
        result = []
        while len(result) < length:
            try:
                result.append(
                    self._get_random_character(
                        self.chains, result, self.chain_order))
            except KeyError:
                # Try again.
                result = []
        return result


    def generate_name(self):
        return "".join(self.generate())
