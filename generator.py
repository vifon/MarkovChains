#!/usr/bin/env python3

import argparse
import sys

from markov_chain import MarkovChain


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=argparse.FileType('r'),
                        default=sys.stdin, dest='infile',
                        help="File with the samples. Default: stdin")
    parser.add_argument('--count', '-c', type=int,
                        default=1, help="Number of entries to generate. Default: 1")
    parser.add_argument('--length', '-l', type=int,
                        default=0, help="Generate sequences of fixed length.")
    parser.add_argument('--order', '-o', type=int,
                        default=1, help="Order of the Markov chain used. Default: 1")
    parser.add_argument('--multi-word', action='store_true',
                        help="Treat the samples as list of words, not characters. Default: false")
    parser.add_argument('--data', action='store_true',
                        help="Treat the samples as the Python data structures. Default: false")
    return parser.parse_args()


def prepare_samples_and_postprocessor(args):
    samples = [sample.strip() for sample in args.infile]

    if args.data:
        from ast import literal_eval
        samples = [literal_eval(sample) for sample in samples]
        postprocessor = lambda sequence: sequence
    elif args.multi_word:
        samples = [sample.split() for sample in samples]
        postprocessor = lambda sequence: " ".join(sequence)
    else:
        postprocessor = lambda sequence: "".join(sequence)

    return samples, postprocessor


def main(argv=None):
    args = parse_args()

    markov = MarkovChain([], args.order)

    samples, postprocessor = prepare_samples_and_postprocessor(args)
    markov.add_samples(samples)

    for i in range(args.count):
        sequence = markov.generate(args.length)
        print(postprocessor(sequence))


if __name__ == '__main__':
    from sys import argv
    main(argv)
