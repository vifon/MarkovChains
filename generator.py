#!/usr/bin/env python3

import argparse
import sys

from markov_chain import *


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=argparse.FileType('r'),
                        default=sys.stdin, dest='infile')
    parser.add_argument('--count', '-c', type=int,
                        default=1)
    return parser.parse_args()


def main(argv=None):
    args = parse_args()
    markov = MarkovChain([line.strip() for line in args.infile])
    for i in range(args.count):
        print(markov.generate_name())


if __name__ == '__main__':
    from sys import argv
    main(argv)
