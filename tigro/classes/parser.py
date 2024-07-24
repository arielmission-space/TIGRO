import os
import configparser
import numpy as np

from tigro import logger


class Parser:
    def __init__(self, config, outpath=None):
        logger.info("Initializing parser")

        self.config = config

        # Read config file
        self.cparser = configparser.ConfigParser()
        self.cparser.read(self.config)
        logger.debug("Config file read")

        # General
        general = self.cparser["general"]
        self.project = general.get("project")
        self.comment = general.get("comment")
        self.version = general.get("version")
        self.datapath = general.get("datapath")

        if outpath is None:
            outpath = general.get("outpath")
        self.outpath = outpath

        self._sequence_ids = general.get("sequence_ids")
        self.sequence_ids = np.concatenate(get_idx(self._sequence_ids))
        self.n_zernike = general.getint("n_zernike", fallback=15)
        self.store_phmap = general.getboolean("store_phmap", fallback=False)
        self.fname_phmap = general.get("fname_phmap")
        self.fname_phmap = os.path.join(self.outpath, self.fname_phmap)
        self.loglevel = general.get("loglevel")
        logger.debug("General parameters read")

        # CGVT
        cgvt = self.cparser["cgvt"]
        self.run_cgvt = cgvt.getboolean("run_cgvt")
        self._phmap_filter_type = cgvt.get("phmap_filter_type", fallback="mean")
        self.phmap_filter_type = getattr(np.ma, self._phmap_filter_type)
        self.phmap_semi_major = cgvt.getfloat("phmap_semi_major", fallback=451)
        self.phmap_semi_minor = cgvt.getfloat("phmap_semi_minor", fallback=310)
        self.phmap_seq_ref = cgvt.getint("phmap_seq_ref")
        logger.debug("CGVT parameters read")

        # CGVT plots
        cgvt_plots = self.cparser["cgvt_plots"]
        self.plot_regmap = cgvt_plots.getboolean("plot_regmap")
        self.plot_regmap_imkey = cgvt_plots.getint("plot_regmap_imkey")
        self.plot_regmap_no_pttf = cgvt_plots.getboolean("plot_regmap_no_pttf")
        self.plot_regmap_no_pttf_imkey = cgvt_plots.getint("plot_regmap_no_pttf_imkey")
        self.plot_allpolys = cgvt_plots.getboolean("plot_allpolys")
        self.plot_allpolys_seq_ref = cgvt_plots.getint("plot_allpolys_seq_ref")
        self._plot_allpolys_colors = cgvt_plots.get("plot_allpolys_colors")
        self.plot_allpolys_colors = get_colors(self._plot_allpolys_colors)
        self.plot_polys = cgvt_plots.getboolean("plot_polys")
        self.plot_polys_seq_ref = cgvt_plots.getint("plot_polys_seq_ref")
        self._plot_polys_order = cgvt_plots.get("plot_polys_order")
        self.plot_polys_order = [
            int(order) for order in self._plot_polys_order.split(",")
        ]
        self._plot_polys_colors = cgvt_plots.get("plot_polys_colors")
        self.plot_polys_colors = get_colors(self._plot_polys_colors)
        logger.debug("CGVT plots options read")

        # ZeroG options
        zerog = self.cparser["zerog"]
        self.run_zerog = zerog.getboolean("run_zerog")
        self._zerog_idx0 = zerog.get("zerog_idx0")
        self._zerog_idx1 = zerog.get("zerog_idx1")
        self.zerog_idx0 = get_idx(self._zerog_idx0)
        self.zerog_idx1 = get_idx(self._zerog_idx1)
        self._zerog_colors = zerog.get("zerog_colors")
        self.zerog_colors = get_colors(self._zerog_colors)
        self._dphmap_filter_type = zerog.get("dphmap_filter_type", fallback="mean")
        self.dphmap_filter_type = getattr(np.ma, self._dphmap_filter_type)
        self._dphmap_idx0 = zerog.get("dphmap_idx0")
        self._dphmap_idx1 = zerog.get("dphmap_idx1")
        self.dphmap_idx0 = np.concatenate(get_idx(self._dphmap_idx0))
        self.dphmap_idx1 = np.concatenate(get_idx(self._dphmap_idx1))
        self.dphmap_gain = zerog.getfloat("dphmap_gain", fallback=None)

        # Zerog plots
        zerog_plots = self.cparser["zerog_plots"]
        self.plot_zerog = zerog_plots.getboolean("plot_zerog")
        self._plot_zerog_ylim = zerog_plots.get("plot_zerog_ylim", fallback="-40, 40")
        self.plot_zerog_ylim = tuple(map(float, self._plot_zerog_ylim.split(",")))
        self.plot_dphmap = zerog_plots.getboolean("plot_dphmap")
        self._plot_dphmap_hlines = zerog_plots.get(
            "plot_dphmap_hlines", fallback="240, 512"
        )
        self.plot_dphmap_hlines = tuple(
            map(
                int,
                self._plot_dphmap_hlines.split(","),
            )
        )
        self._plot_dphmap_vlines = zerog_plots.get("plot_dphmap_vlines", fallback="512")
        self.plot_dphmap_vlines = tuple(map(int, self._plot_dphmap_vlines.split(",")))
        self._plot_dphmap_hist_xlim = zerog_plots.get(
            "plot_dphmap_hist_xlim", fallback="-200, 200"
        )
        self.plot_dphmap_hist_xlim = tuple(
            map(
                float,
                self._plot_dphmap_hist_xlim.split(","),
            )
        )
        self._plot_dphmap_hist_ylim = zerog_plots.get(
            "plot_dphmap_hist_ylim", fallback="-200, 200"
        )
        self.plot_dphmap_hist_ylim = tuple(
            map(
                float,
                self._plot_dphmap_hist_ylim.split(","),
            )
        )
        logger.debug("Zerog plots options read")

    @classmethod
    def input_keywords(cls):
        return ["parser", "configparser"]


def get_idx(item):
    ll = []
    for idx in item.split(","):
        if "-" in idx:
            start, end = map(int, idx.split("-"))
            ll.extend([range(start, end + 1)])
        else:
            ll.append([int(idx)])
    return ll


def get_colors(item):
    return "".join(color[-1] * int(color[:-1]) for color in item.split(","))
