import os
import configparser
import numpy as np

from tigro import logger

from tigro.utils.util import get_idx
from tigro.utils.util import get_colors


class Parser:
    def __init__(self, config, outpath=None):
        logger.info("Initializing parser")

        self.config = config

        # Read config file
        self.cparser = configparser.ConfigParser()
        self.cparser.read(self.config)
        logger.debug("Config file read")

        # System
        system = self.cparser["system"]
        self.project = system.get("project")
        self.comment = system.get("comment")
        self.version = system.get("version")
        self.datapath = system.get("datapath")

        if outpath is None:
            outpath = system.get("outpath")
        self.outpath = outpath

        self._sequence_ids = system.get("sequence_ids")
        self.sequence_ids = np.concatenate(get_idx(self._sequence_ids))
        self.store_phmap = system.getboolean("store_phmap", fallback=False)
        self.fname_phmap = system.get("fname_phmap")
        self.fname_phmap = os.path.join(self.outpath, self.fname_phmap)
        self.loglevel = system.get("loglevel")
        logger.setLevel(self.loglevel)
        logger.debug("System parameters read")

        # CGVT
        cgvt = self.cparser["cgvt"]
        self.run_cgvt = cgvt.getboolean("run_cgvt")
        self.phmap_threshold = cgvt.getfloat("phmap_threshold", fallback=0.1)
        self._phmap_filter_type = cgvt.get("phmap_filter_type", fallback="mean")
        self.phmap_filter_type = getattr(np.ma, self._phmap_filter_type)
        self.phmap_semi_major = cgvt.getfloat("phmap_semi_major", fallback=451)
        self.phmap_semi_minor = cgvt.getfloat("phmap_semi_minor", fallback=310)
        self.phmap_seq_ref = cgvt.getint("phmap_seq_ref")
        if self.phmap_seq_ref not in self.sequence_ids:
            self.phmap_seq_ref = self.sequence_ids[0]
        self.n_zernike = cgvt.getint("n_zernike", fallback=15)
        logger.debug("CGVT parameters read")

        # CGVT plots
        cgvt_plots = self.cparser["cgvt_plots"]
        self.plot_regmap = cgvt_plots.getboolean("plot_regmap")
        self.plot_regmap_imkey = cgvt_plots.getint("plot_regmap_imkey")
        self.plot_regmap_no_pttf = cgvt_plots.getboolean("plot_regmap_no_pttf")
        self.plot_regmap_no_pttf_imkey = cgvt_plots.getint("plot_regmap_no_pttf_imkey")
        self.plot_allpolys = cgvt_plots.getboolean("plot_allpolys")
        self.plot_allpolys_seq_ref = cgvt_plots.getint("plot_allpolys_seq_ref")
        if self.plot_allpolys_seq_ref not in self.sequence_ids:
            self.plot_allpolys_seq_ref = self.sequence_ids[0]
        self._plot_allpolys_colors = cgvt_plots.get("plot_allpolys_colors")
        self.plot_allpolys_colors = get_colors(self._plot_allpolys_colors)
        self.plot_polys = cgvt_plots.getboolean("plot_polys")
        self.plot_polys_seq_ref = cgvt_plots.getint("plot_polys_seq_ref")
        if self.plot_polys_seq_ref not in self.sequence_ids:
            self.plot_polys_seq_ref = self.sequence_ids[0]
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
        self._idx_gplus = zerog.get("idx_gplus")
        self._idx_gminus = zerog.get("idx_gminus")
        self.idx_gplus = get_idx(self._idx_gplus)
        self.idx_gminus = get_idx(self._idx_gminus)
        self._zerog_colors = zerog.get("zerog_colors")
        self.zerog_colors = get_colors(self._zerog_colors)
        self._dphmap_filter_type = zerog.get("dphmap_filter_type", fallback="mean")
        self.dphmap_filter_type = getattr(np.ma, self._dphmap_filter_type)
        self._dphmap0_idx = zerog.get("dphmap0_idx")
        self._dphmap1_idx = zerog.get("dphmap1_idx")
        self.dphmap0_idx = np.concatenate(get_idx(self._dphmap0_idx))
        self.dphmap1_idx = np.concatenate(get_idx(self._dphmap1_idx))
        self.dphmap_gain = zerog.get("dphmap_gain", fallback="")
        self.dphmap_gain = float(self.dphmap_gain) if self.dphmap_gain else None

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
