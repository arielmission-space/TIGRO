import pickle


def to_pickle(phmap, path):
    with open(path, 'wb') as f:
        pickle.dump(phmap, f) 