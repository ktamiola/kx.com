import logging
import numpy as np
from sequence_utils import mutate as MUTATE
from timeit import default_timer as timer
import json
import pymongo
from bson.code import Code

# Define our logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

###
# FUNCTION DEFINITIONS
###


def insertDummies(sequence="", N=1000, I=20, collection=None):

    # stats
    stats = np.zeros(I)

    # String to sequence
    S = list(sequence)

    for ii in range(I):
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

        stats[ii] = end - start

    # Prepare the output
    print('-----------------------------------------------------------------------')
    logger.info('Protein length: {} amino acids'.format(len(S)))
    logger.info('Number of mutants: {}'.format(N))
    logger.info('Number of loops: {}'.format(I))
    logger.info(
        'Read/Write time: {} +/- {} s'.format(np.mean(stats), np.std(stats)))
    print('-----------------------------------------------------------------------')

    return np.mean(stats), np.std(stats)


def indexDummies(N=1000):

    # Generate the index
    print('-----------------------------------------------------------------------')
    logger.info('Indexing mutants...')
    logger.info('Sorting E1 energies in ascending order...')
    start = timer()
    collection.create_index([('E1', pymongo.ASCENDING)], unique=True)
    end = timer()
    logger.info('Indexing time: {} s'.format(end - start))
    print('-----------------------------------------------------------------------')

    return True


def basicMeanDummies(I=20, collection=None):

    # stats
    stats = np.zeros(I)

    # Do some basic counting and aggregation
    for ii in range(I):
        start = timer()
        # Find and sort the most suitable records
        CP = collection.find().sort("E1")
        NP = CP.count()
        M = 0.0
        for C in CP:
            M += C["E1"]
        # End measuring the time
        end = timer()
        stats[ii] = end - start

    print('-----------------------------------------------------------------------')
    logger.info('Basic aggregation demo...')
    logger.info('Number of loops: {}'.format(I))
    logger.info(
        'Calculation time: {} +/- {} s'.format(np.mean(stats), np.std(stats)))
    print('-----------------------------------------------------------------------')

    return np.mean(stats), np.std(stats)


def advancedMeanDummies(I=20, collection=None):

    # stats
    stats = np.zeros(I)

    # Do advanced counting and aggregation
    for ii in range(I):
        start = timer()
        # Find and sort the most suitable records
        pipeline = [{'$group': {'_id': 'null', 'mean': {'$avg': '$E1'}}}]
        CP = list(collection.aggregate(pipeline))
        # End measuring the time
        end = timer()

        # Collect our stats
        stats[ii] = end - start

    print('-----------------------------------------------------------------------')
    logger.info('Advanced aggregation demo...')
    logger.info('Number of loops: {}'.format(I))
    logger.info(
        'Calculation time: {} +/- {} s'.format(np.mean(stats), np.std(stats)))
    print('-----------------------------------------------------------------------')

    return np.mean(stats), np.std(stats)

#
# END OF THE FUNCTION DEFINITION BLOCK
#


if __name__ == "__main__":

    # Estabilish a conneciton to our local (docker) MongoDB instance
    try:
        client = pymongo.MongoClient('localhost', 27017)
        db = client['benchmark']
        collection = db['mutants']
    except:
        logger.error('I could not connect to a running MongoDB instance!')
        logger.error('Is your database up and running?')


    # Initialize a dummy protein sequence
    sequence = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    # The number of mutations
    N = 10000

    # The number of repetitions
    I = 20

    # Generate dummy protein sequences
    A1, A2 = insertDummies(sequence, N, I, collection)

    # Index our dummy sequences
    B1 = indexDummies(N)

    # A primitive aggregator that uses intrinsic search and sort functionalities
    C1, C2 = basicMeanDummies(I, collection)

    # An advanced aggregator that uses intrinsic mean functionality in the aggregator classes
    D1, D2 = advancedMeanDummies(I, collection)

    # Summarize our findings
    print('-----------------------------------------------------------------------')
    logger.info(
        'Basic vs Built-in aggregation gain: {} x'.format(C1/D1))
    print('-----------------------------------------------------------------------')
