import os
import configparser
import numpy as np

from tigro import logger


class Parser:
    def __init__(self, file_name, outpath):
        logger.info("Initializing parser")

        self.file_name = file_name
        self.outpath = outpath

        # Read config file
        self.config = configparser.ConfigParser()
        self.config.read(self.file_name)
        logger.debug("Config file read")

        # General
        general = self.config["general"]
        self.datapath = general.get("datapath")
        self.sequence_ids = []
        for seq_id in general.get("sequence_ids").split(","):
            if "-" in seq_id:
                start, end = map(int, seq_id.split("-"))
                self.sequence_ids.extend(range(start, end + 1))
            else:
                self.sequence_ids.append(int(seq_id))
        self.n_zernike = general.getint("n_zernike", fallback=15)
        self.store_phmap = general.getboolean("store_phmap")
        self.fname_phmap = general.get("fname_phmap")
        self.fname_phmap = os.path.join(self.outpath, self.fname_phmap)
        self.loglevel = general.get("loglevel")
        logger.debug("General parameters read")

        # CGVT
        cgvt = self.config["cgvt"]
        self.run_cgvt = cgvt.getboolean("run_cgvt")
        self.phmap_filter_type = getattr(np.ma, cgvt.get("phmap_filter_type", fallback="mean"))
        self.phmap_semi_major = cgvt.getfloat("phmap_semi_major", fallback=451)
        self.phmap_semi_minor = cgvt.getfloat("phmap_semi_minor", fallback=310)
        self.phmap_seq_ref = cgvt.getint("phmap_seq_ref")
        logger.debug("CGVT parameters read")

        # CGVT plots
        cgvt_plots = self.config["cgvt_plots"]
        self.plot_regmap = cgvt_plots.getboolean("plot_regmap")
        self.plot_regmap_imkey = cgvt_plots.getint("plot_regmap_imkey")
        self.plot_regmap_no_pttf = cgvt_plots.getboolean("plot_regmap_no_pttf")
        self.plot_regmap_no_pttf_imkey = cgvt_plots.getint("plot_regmap_no_pttf_imkey")
        self.plot_allpolys = cgvt_plots.getboolean("plot_allpolys")
        self.plot_allpolys_seq_ref = cgvt_plots.getint("plot_allpolys_seq_ref")

        def get_colors(dd, key):
            return "".join(
                color[-1] * int(color[:-1]) for color in dd.get(key).split(",")
            )

        self.plot_allpolys_colors = get_colors(cgvt_plots, "plot_allpolys_colors")
        self.plot_polys = cgvt_plots.getboolean("plot_polys")
        self.plot_polys_seq_ref = cgvt_plots.getint("plot_polys_seq_ref")
        self.plot_polys_order = [
            int(order) for order in cgvt_plots.get("plot_polys_order").split(",")
        ]
        self.plot_polys_colors = get_colors(cgvt_plots, "plot_polys_colors")
        logger.debug("CGVT plots options read")

        # ZeroG options
        zerog = self.config["zerog"]
        self.run_zerog = zerog.getboolean("run_zerog")
        self.zerog_start_indices_pairs = [
            tuple(map(int, x.split(", ")))
            for x in zerog.get("zerog_start_indices_pairs")[1:-1].split("), (")
        ]
        self.zerog_num_pairs = [
            int(num) for num in zerog.get("zerog_num_pairs").split(",")
        ]
        self.zerog_colors = get_colors(zerog, "zerog_colors")
        self.dphmap_filter_type = getattr(np.ma, zerog.get("dphmap_filter_type", fallback="mean"))
        self.dphmap_idx = [
            tuple(map(int, x.split("-"))) for x in zerog.get("dphmap_idx").split(",")
        ]
        self.dphmap_gain = zerog.getfloat("dphmap_gain", fallback=None)

        # Zerog plots
        zerog_plots = self.config["zerog_plots"]
        self.plot_zerog = zerog_plots.getboolean("plot_zerog")
        self.plot_zerog_ylim = tuple(
            map(float, zerog_plots.get("plot_zerog_ylim", fallback="-40, 40").split(","))
        )
        self.plot_dphmap = zerog_plots.getboolean("plot_dphmap")
        self.plot_dphmap_hlines = tuple(
            map(int, zerog_plots.get("plot_dphmap_hlines", fallback="240, 512").split(","))
        )
        self.plot_dphmap_vlines = tuple(
            map(int, zerog_plots.get("plot_dphmap_vlines", fallback="512").split(","))
        )
        self.plot_dphmap_hist_xlim = tuple(
            map(float, zerog_plots.get("plot_dphmap_hist_xlim", fallback="-200, 200").split(","))
        )
        self.plot_dphmap_hist_ylim = tuple(
            map(float, zerog_plots.get("plot_dphmap_hist_ylim", fallback="-200, 200").split(","))
        )
        logger.debug("Zerog plots options read")

    @classmethod
    def input_keywords(cls):
        return ["parser", "configparser"]
