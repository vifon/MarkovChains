#!/usr/bin/env python3

import argparse
import sys

from markov_chain import *


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=argparse.FileType('r'),
                        default=sys.stdin, dest='infile',
                        help="File with the samples. Default: stdin")
    parser.add_argument('--count', '-c', type=int,
                        default=1, help="Number of entries to generate. Default: 1")
    parser.add_argument('--order', '-o', type=int,
                        default=1, help="Order of the Markov chain used. Default: 1")
    return parser.parse_args()


def main(argv=None):
    args = parse_args()
    markov = MarkovChain([line.strip() for line in args.infile],
                         args.order)

    for i in range(args.count):
        print("".join(markov.generate()))


if __name__ == '__main__':
    from sys import argv
    main(argv)
