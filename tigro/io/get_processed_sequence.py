import numpy as np
import pickle, glob, os
import h5py


def load_recursively_from_h5(group, metadata):
    for key, item in group.items():
        if isinstance(item, h5py.Dataset):
            metadata[key] = item[()]
        elif isinstance(item, h5py.Group):
            metadata[key] = {}
            load_recursively_from_h5(item, metadata[key])


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
                load_recursively_from_h5(fs["data"], _data)
                _map, _map_ptt, _map_pttf, _map_residual = (
                    np.ma.masked_invalid(_data["regmap"]),
                    np.ma.masked_invalid(_data["regmap_ptt"]),
                    np.ma.masked_invalid(_data["regmap_pttf"]),
                    np.ma.masked_invalid(_data["regmap_residual"]),
                )
                _metadata = {}
                load_recursively_from_h5(fs["metadata"], _metadata)

        else:
            raise ValueError("Unsupported file extension: {:s}".format(ext))

        return _map, _map_ptt, _map_pttf, _map_residual, _metadata
    raise FileNotFoundError("Sequence not found.")
