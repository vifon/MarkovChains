from collections import defaultdict
import random
import statistics


class MarkovChain:
    def __init__(self, samples):
        self.samples = samples
        self._process_samples()

    def _process_samples(self):
        sample_lengths = [len(sample) for sample in self.samples]
        self.mean_length = statistics.mean(sample_lengths)
        self.length_deviation = statistics.stdev(sample_lengths)

        self.distribution = defaultdict(list)
        for line in self.samples:
            line = [None] + list(line)
            for last, current in zip(line, line[1:]):
                self.distribution[last].append(current)

    def generate(self):
        length = random.gauss(self.mean_length, self.length_deviation)
        result = []
        result.append(random.choice(self.distribution[None]))
        while len(result) < length:
            result.append(random.choice(self.distribution[result[-1]]))
        return result

    def generate_name(self):
        return "".join(self.generate())
