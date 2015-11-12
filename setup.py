#!/usr/bin/env python3

from distutils.core import setup

import markov_chain

if __name__ == '__main__':
    setup(
        name='markov_chain',
        description="Sequence generator based on Markov chains",
        long_description=markov_chain.__doc__,
        version=markov_chain.__version__,
        author=markov_chain.__author__,
        author_email=markov_chain.__email__,
        license=markov_chain.__license__,
        url="https://github.com/Vifon/MarkovChains",
        py_modules=['markov_chain'],
        scripts=['scripts/markov-generate'],
    )
