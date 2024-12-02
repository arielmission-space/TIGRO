from tigro.ui.shared import to_configparser


def to_ini(input, tmp):
    dictionary = {}

    # system
    system = {}
    system["project"] = input.project()
    system["comment"] = input.comment()
    system["version"] = input.version()
    system["datapath"] = input.datapath()
    system["sequence_ids"] = input.sequence_ids()
    system["outpath"] = input.outpath()
    system["store_phmap"] = False
    try:
        system["fname_phmap"] = input.save_phmap_pkl()
    except:
        system["fname_phmap"] = "tigro.pkl"
    system["loglevel"] = input.loglevel()

    dictionary.update({"system": system})

    # cgvt
    cgvt = {}
    cgvt["run_cgvt"] = True
    cgvt["phmap_threshold"] = input.phmap_threshold()
    cgvt["phmap_filter_type"] = input.phmap_filter_type()
    cgvt["phmap_semi_major"] = input.phmap_semi_major()
    cgvt["phmap_semi_minor"] = input.phmap_semi_minor()
    cgvt["phmap_seq_ref"] = input.phmap_seq_ref()
    cgvt["n_zernike"] = input.n_zernike()

    dictionary.update({"cgvt": cgvt})

    # cgvt_plots
    cgvt_plots = {}
    cgvt_plots["plot_regmap"] = True
    cgvt_plots["plot_regmap_imkey"] = input.plot_regmap_imkey()
    cgvt_plots["plot_regmap_no_pttf"] = True
    cgvt_plots["plot_regmap_no_pttf_imkey"] = input.plot_regmap_no_pttf_imkey()
    cgvt_plots["plot_allpolys"] = True
    cgvt_plots["plot_allpolys_seq_ref"] = input.plot_allpolys_seq_ref()
    cgvt_plots["plot_allpolys_colors"] = input.plot_allpolys_colors()
    cgvt_plots["plot_allpolys_separator"] = input.plot_allpolys_separator()
    cgvt_plots["plot_polys"] = True
    cgvt_plots["plot_polys_seq_ref"] = input.plot_polys_seq_ref()
    cgvt_plots["plot_polys_order"] = input.plot_polys_order()
    cgvt_plots["plot_polys_colors"] = input.plot_polys_colors()

    dictionary.update({"cgvt_plots": cgvt_plots})

    # zerog
    zerog = {}
    zerog["run_zerog"] = True
    zerog["idx_gplus"] = input.idx_gplus()
    zerog["idx_gminus"] = input.idx_gminus()
    zerog["zerog_colors"] = input.zerog_colors()
    zerog["dphmap_filter_type"] = input.dphmap_filter_type()
    zerog["dphmap_gain"] = input.dphmap_gain()
    zerog["dphmap0_idx"] = input.dphmap0_idx()
    zerog["dphmap1_idx"] = input.dphmap1_idx()

    dictionary.update({"zerog": zerog})

    # zerog_plots
    zerog_plots = {}
    zerog_plots["plot_zerog"] = True
    zerog_plots["plot_zerog_ylim"] = input.plot_zerog_ylim()
    zerog_plots["plot_dphmap"] = True
    zerog_plots["plot_dphmap_vmin_vmax"] = input.plot_dphmap_vmin_vmax()
    zerog_plots["plot_dphmap_hlines"] = input.plot_dphmap_hlines()
    zerog_plots["plot_dphmap_vlines"] = input.plot_dphmap_vlines()
    zerog_plots["plot_dphmap_hist_xlim"] = input.plot_dphmap_hist_xlim()
    zerog_plots["plot_dphmap_hist_ylim"] = input.plot_dphmap_hist_ylim()

    dictionary.update({"zerog_plots": zerog_plots})

    # save to file
    config = to_configparser(dictionary)
    with open(tmp, "w") as cf:
        config.write(cf)
