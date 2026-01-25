import numpy as np
import pickle, glob, os

def get_processed_sequence(sequence, path, SN=None, ):
    if SN:
        full_path = os.path.expanduser(os.path.join(path, "*{:s}*.pkl".format(SN)))
    else: 
        full_path =  os.path.expanduser(os.path.join(path, "*.pkl"))
   
    all_files = glob.glob(full_path)
    
    for fname in all_files:
        basename, fext = os.path.splitext( os.path.basename(fname) )
        seq = basename.split('_')[0]
        seq = int(seq)
        if seq != sequence: continue
        with open(fname, 'rb') as fs:
            _map, _map_ptt, _map_pttf, _map_residual, _metadata = pickle.load(fs)
            return _map, _map_ptt, _map_pttf, _map_residual, _metadata
    raise FileNotFoundError("Sequence not found.")  