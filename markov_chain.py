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
    def __init__(self, samples, memory=1):
        self.samples = samples
        self.memory = memory
        self._process_samples()


    def _process_samples(self):
        sample_lengths = [len(sample) for sample in self.samples]
        self.mean_length = statistics.mean(sample_lengths)
        self.length_deviation = statistics.stdev(sample_lengths)

        self.chains = Tree()
        for line in self.samples:
            line = SaneList_NoExcept(line)
            self._create_chain(line, self.memory)


    def _create_chain(self, line, memory):
        for i in range(len(line)):
            chain = self.chains
            for j in range(i, i-memory+1, -1):
                # Walk back through all the elements to memorize
                # except the last one. Create the chain in the tree
                # while doing so.
                last = line[j-1]
                chain = chain[last]

            last = line[i-memory]
            if not chain.get(last):
                # Create a tree leaf if not present already.
                chain[last] = list()
            chain[last].append(line[i])


    def _get_random_character(self, chain, line, memory):
        try:
            last = line.pop(-1)
        except IndexError:
            last = None

        if memory > 1:
            return self._get_random_character(chain[last], line, memory-1)
        else:
            return random.choice(chain[last])


    def generate(self):
        length = random.gauss(self.mean_length, self.length_deviation)
        result = []
        while len(result) < length:
            result.append(
                self._get_random_character(
                    self.chains, result[:], self.memory))
        return result


    def generate_name(self):
        return "".join(self.generate())
