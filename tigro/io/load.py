import numpy as np
from prysm.interferogram import Interferogram
import os, glob, h5py
from tigro.logging import logger


def load_phmap(dir_path, sequence_ids, down_sampling=None):
    allowed_extensions = ".h5", ".dat", ".4D"
    namelist = []

    for fextension in allowed_extensions:
        namelist = namelist + glob.glob(
            os.path.expanduser(os.path.join(dir_path, "*" + fextension))
        )

    namelist = sorted(namelist)
    list_of_sequences = []
    for fname in namelist:
        basename, fextension = os.path.splitext(os.path.basename(fname))

        sequence, number, *_ = basename.split("_")
        sequence = int(sequence)
        try:
            number = int(number)
        except ValueError:
            number = ""

        list_of_sequences.append([sequence, number, basename, fextension, fname])

    retval = {}
    metadata = {}
    for seq in sequence_ids:
        sequence_files = [x for x in list_of_sequences if x[0] == seq]

        for seq in sequence_files:
            sequence, number, name, fextension, full_path_name = seq
            logger.info("Reading {:s}".format(name))

            if not sequence in retval:
                retval[sequence] = {}
                metadata[sequence] = {}

            if fextension == ".dat":
                number = int(number)
                ima = Interferogram.from_zygo_dat(full_path_name)
                data = np.array(ima.data)
                data = np.ma.masked_array(
                    data=data, mask=np.isnan(data), fill_value=0.0
                )
                if down_sampling:
                    data = data[::down_sampling, ::down_sampling]
                retval[sequence][number] = data
                metadata[sequence][number] = {"name": name}
            elif fextension == ".4D":
                with h5py.File(full_path_name, "r") as fs:
                    if "NumOfMeasurements" in fs["Measurement"].attrs.keys():
                        Nmeas = fs["Measurement"].attrs["NumOfMeasurements"]
                        for key, item in fs["Measurement"].items():
                            if "Measurement" not in key:
                                continue
                            _, number = key.split("_")
                            wav = fs["Measurement"][key].attrs["WavelengthInNanometers"]
                            data = (
                                np.array(
                                    fs["Measurement"][key]["SurfaceInWaves"]["Data"],
                                    # fs['Measurement'][key]['UnprocessedUnwrappedPhase']['Data'],
                                    dtype=np.float64,
                                )
                                * wav
                            )
                            if down_sampling:
                                data = data[::down_sampling, ::down_sampling]
                            retval[sequence][number] = np.ma.masked_array(
                                data=data, mask=np.isnan(data), fill_value=0.0
                            )
                            metadata[sequence][number] = {"name": name}
                    else:
                        number = int(number)
                        wav = fs["Measurement"].attrs["WavelengthInNanometers"]
                        data = (
                            np.array(
                                fs["Measurement"]["SurfaceInWaves"]["Data"],
                                # fs['Measurement'][key]['UnprocessedUnwrappedPhase']['Data'],
                                dtype=np.float64,
                            )
                            * wav
                        )
                        if down_sampling:
                            data = data[::down_sampling, ::down_sampling]
                        retval[sequence][number] = np.ma.masked_array(
                            data=data, mask=np.isnan(data), fill_value=0.0
                        )
                        metadata[sequence][number] = {"name": name}

    return retval, metadata


def sort_phmap(data, meta):
    retval = {}
    metadata = {}

    for sequence in data.keys():
        _data = data[sequence]
        _meta = meta[sequence]

        numbers = sorted([num for num in _data.keys()])

        rawmap = np.ma.stack([_data[num] for num in numbers])
        names = [_meta[num]["name"] for num in numbers]
        retval[sequence] = rawmap

        if "-g" in names[0] or "-1g" in names[0] or "ng" in names[0]:
            phi_offs = np.pi
        elif (
            "+g" in names[0]
            or "1g" in names[0]
            or "+1g" in names[0]
            or "pg" in names[0]
        ):
            phi_offs = 0.0
        else:
            phi_offs = 0.0

        metadata[sequence] = {"numbers": numbers, "names": names, "phi_offs": phi_offs}

    return retval, metadata
