import numpy as np

one_digit = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6, 'I': 7, 'K': 8, 'L': 9,
             'M': 10, 'N': 11, 'P': 12, 'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19}


def letter2onehot(sequence):
    """
        Return a binary one-hot vector
    """

    assert(len(sequence) >= 1)
    encoded = []
    for letter in sequence:
        tmp = np.zeros(20)
        tmp[one_digit[letter]] = 1
        encoded.append(tmp)
    assert(len(encoded) == len(sequence))
    encoded = np.asarray(encoded)
    return encoded.flatten()


def onehot2letter(array):
    """
    Return a letter representation
    """

    # Do the inverse mapping
    one_letter = dict((v, k) for k, v in one_digit.iteritems())

    # Slice the input vector into the sub - vectors of the size=20
    chunks = np.split(array, array.size / 20)

    # Loop over the chunks and return the amino acid identities
    sequence = [one_letter[np.argmax(chunk)] for chunk in chunks]

    return ''.join(sequence)


def mutate(sequence, alphabet='complete', N=1):
    """
    Mutate protein sequence randomly at N-positions.
    Use different alphabets:
    - complete - all residues
    - polar
    - apolar
    - charged
    """

    def complete():
        return ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V"]

    def charged():
        return ["R", "D", "E", "H", "K", "Y"]

    def polar():
        return ["N", "C", "Q", "H", "S", "T", "W", "Y"]

    def apolar():
        return ["A", "G", "I", "L", "M", "F", "P", "V"]

    options = {'complete': complete, 'charged': charged,
               'polar': polar, 'apolar': apolar}

    # Select our alphabet, make sure we have a gracefull fallback to the
    # default one if wrong option is specified
    try:
        alphabet = options[alphabet]()
    except:
        alphabet = options['complete']()

    # Just in case we got carried away and supplied number of mutations
    # that exceeds the length of our protein
    if N > len(sequence):
        N = len(sequence)

    # Split our string
    sequence = list(sequence)

    # Select the indexes at which the mutation will occur
    rndx = np.arange(len(sequence))
    np.random.shuffle(rndx)
    rndx = rndx[:N]

    # Do the mutations in the squence vector
    for ndx in rndx:
        randx = np.random.randint(0, high=len(alphabet), size=1)
        sequence[ndx] = alphabet[randx[0]]

    return ''.join(sequence)
