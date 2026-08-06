import numpy as np
import pickle, glob, os
import h5py
import pandas as pd


def load_recursively_from_h5(group, metadata):
    for key, item in group.items():
        if isinstance(item, h5py.Dataset):
            metadata[key] = item[()]

        elif isinstance(item, h5py.Group):
            metadata[key] = {}
            load_recursively_from_h5(item, metadata[key])

        for k, element in item.attrs.items():
            if 'timestamp' in k: 
                metadata[key][k] = pd.Timestamp(element)
            else:
                metadata[key][k] = element
              

def get_processed_sequence(
    sequence,
    path,
    SN=None,
    ext=".pkl",
):
    if SN:
        full_path = os.path.expanduser(os.path.join(path, "*{:s}*{}".format(SN, ext)))
    else:
        full_path = os.path.expanduser(os.path.join(path, "*{}".format(ext)))

    all_files = glob.glob(full_path)

    for fname in all_files:
        basename, fext = os.path.splitext(os.path.basename(fname))
        seq = basename.split("_")[0]
        seq = int(seq)
        if seq != sequence:
            continue

        if ext == ".pkl":
            with open(fname, "rb") as fs:
                _map, _map_ptt, _map_pttf, _map_residual, _metadata = pickle.load(fs)

        elif ext == ".h5":
            with h5py.File(fname, "r") as fs:
                _data = {}
                load_recursively_from_h5(fs[str(seq)], _data)
                                    
                if 'timestamp' in _data['metadata'].keys():
                    _data['metadata']["timestamp"] = pd.Timestamp(_data['metadata']["timestamp"])

                if 'uref' in _data.keys(): _data['metadata']['uref'] = _data['uref']
                _map, _map_ptt, _map_pttf, _map_residual, _metadata = (
                    np.ma.masked_invalid(_data["regmap"]),
                    np.ma.masked_invalid(_data["regmap_ptt"]),
                    np.ma.masked_invalid(_data["regmap_pttf"]),
                    np.ma.masked_invalid(_data["regmap_residual"]),
                    _data["metadata"]
                )
                #_metadata = {}
                #load_recursively_from_h5(fs[f"{seq}/metadata"], _metadata)

        else:
            raise ValueError("Unsupported file extension: {:s}".format(ext))

        return _map, _map_ptt, _map_pttf, _map_residual, _metadata
    raise FileNotFoundError("Sequence not found.")
