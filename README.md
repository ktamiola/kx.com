## Description

This is a synthetic benchmark to asses the relative benefit of `kdb+` over the latest `mongodb` given a real-life, combinatorial protein mutagenesis scenario.

The `benchmark.py` contains two adjustable parameters:

1. `sequence` - the starting amino acid sequence
2. `N` - the number of mutants to be generated

## Dependencies

Python:`pymongo`, `numpy`

Docker: `mongo:latest`

## Execution

1. Pull the latest MongoDB from `docker`; `docker pull mongo`.
2. Run a single-instance container `docker run -p 27017:27017 mongo`.
3. Run `python benchmark.py`.
