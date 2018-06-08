import logging
import numpy as np
from sequence_utils import mutate as MUTATE
from timeit import default_timer as timer
import json
import pymongo

# Define our logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":

    # Estabilish a conneciton to our local (docker) MongoDB instance
    client = pymongo.MongoClient('localhost', 27017)
    db = client['benchmark']
    collection = db['mutants']

    # Initialize a dummy protein sequence
    sequence = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    # The number of mutations
    N = 10

    # String to sequence
    S = list(sequence)

    # Start measuring the calculation time
    start = timer()

    for i in range(N):
        S = MUTATE(S)
        # logger.info("Mutant: {}".format(S))
        mutant = {"sequence": S, "E1": np.random.rand(), "E2": np.random.rand(
        ), "E3": np.random.rand(), "E4": np.random.rand(), "E5": np.random.rand()}
        collection.insert_one(mutant)

    # End measuring the time
    end = timer()

    # Prepare the output
    print('-----------------------------------------------------------------------')
    logger.info('Protein length: {} amino acids'.format(len(S)))
    logger.info('Number of mutants: {}'.format(N))
    logger.info('Calculation time: {} s'.format(end - start))
    logger.info('{} mutants/s'.format(N / (end - start)))
    print('-----------------------------------------------------------------------')

    # Generate the index
    print('-----------------------------------------------------------------------')
    logger.info('Indexing {} mutants...'.format(N))
    start = timer()
    collection.create_index([('E1', pymongo.ASCENDING)], unique=True)
    end = timer()
    logger.info('Indexing time: {} s'.format(end - start))
    print('-----------------------------------------------------------------------')

    # Do some basic counting and aggregation
    start = timer()
    CP = collection.find({"E1": {"$lt": 0.5}}).sort("E1")
    NP = CP.count()
    M = 0.0
    for C in CP:
        M += C["E1"]
    # End measuring the time
    end = timer()

    print('-----------------------------------------------------------------------')
    logger.info('Number of samples: {}'.format(NP))
    logger.info('Average E1: {}'.format(M / NP))
    logger.info('Calculation time: {} s'.format(end - start))
    print('-----------------------------------------------------------------------')
