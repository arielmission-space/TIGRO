import os
import glob
import pickle
import numpy as np
from prysm.interferogram import Interferogram


def load_phmap(dir_path, sequence_ids, verbose=False):
    # Read and organise data

    namelist = sorted(glob.glob(os.path.join(dir_path, "*.dat")))

    phmap = {}
    print('Loading files ...')
    for k, fname in enumerate(namelist):
        #print(' {:d}/{:d}'.format(k+1, len(namelist)), end="\r" )
        name = os.path.splitext(os.path.basename(fname))[0]
        sequence, number, date, *_ = name.split("_")
        sequence, number = int(sequence), int(number)
        
        if sequence not in sequence_ids: continue
        
        if not sequence in phmap:
            phmap[sequence] = {}

        ima = Interferogram.from_zygo_dat(fname)
        
        phmap[sequence][number] = {'ima': ima.copy()}


        phmap[sequence][number]['name'] = name 
        phmap[sequence][number]['rawmap'] = np.ma.masked_array(
                                    data = ima.data,
                                    mask = np.isnan(ima.data),
                                    fill_value = 0.0)
        
        if verbose:
            print(sequence, number, date, name, *_)
    
    
    for sequence in phmap.keys():
        _phmap = phmap[sequence]
        numbers = sorted([num for num in _phmap.keys()])

        rawmap = np.ma.stack([_phmap[num]['rawmap'] for num in numbers])
        names = [_phmap[num]['name'] for num in numbers]
        
        for num in numbers: del _phmap[num]
        _phmap['rawmap'] = rawmap
        _phmap['number'] = numbers
        _phmap['name'] = names
        
        if "-g" in names[0] or "-1g" in names[0]:
            _phmap["phi_offs"] = 0.0
        elif "+g" in names[0] or "1g" in names[0] or "+1g" in names[0]:
            _phmap["phi_offs"] = np.pi
        else: 
            _phmap["phi_offs"] = 0.0

    return phmap


def from_pickle(path):
    with open(path, "rb") as fs:
        phmap=pickle.load(fs)
    return phmap