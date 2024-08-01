from tigro.ui.shared import to_configparser


def update_ini(input, tmp):

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
    print("save_phmap_pkl" in input.__dict__["_map"])
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
    cgvt_plots["plot_polys"] = True
    cgvt_plots["plot_polys_seq_ref"] = input.plot_polys_seq_ref()
    cgvt_plots["plot_polys_order"] = input.plot_polys_order()
    cgvt_plots["plot_polys_colors"] = input.plot_polys_colors()

    dictionary.update({"cgvt_plots": cgvt_plots})

    # zerog
    zerog = {}
    zerog["run_zerog"] = True
    zerog["zerog_idx0"] = input.zerog_idx0()
    zerog["zerog_idx1"] = input.zerog_idx1()
    zerog["zerog_colors"] = input.zerog_colors()
    zerog["dphmap_filter_type"] = input.dphmap_filter_type()
    zerog["dphmap_gain"] = input.dphmap_gain()
    zerog["dphmap_idx0"] = input.dphmap_idx0()
    zerog["dphmap_idx1"] = input.dphmap_idx1()

    dictionary.update({"zerog": zerog})

    # zerog_plots
    zerog_plots = {}
    zerog_plots["plot_zerog"] = True
    zerog_plots["plot_zerog_ylim"] = input.plot_zerog_ylim()
    zerog_plots["plot_dphmap"] = True
    zerog_plots["plot_dphmap_hlines"] = input.plot_dphmap_hlines()
    zerog_plots["plot_dphmap_vlines"] = input.plot_dphmap_vlines()
    zerog_plots["plot_dphmap_hist_xlim"] = input.plot_dphmap_hist_xlim()
    zerog_plots["plot_dphmap_hist_ylim"] = input.plot_dphmap_hist_ylim()

    dictionary.update({"zerog_plots": zerog_plots})

    print(dictionary)

    # save to file
    config = to_configparser(dictionary)
    with open(tmp, "w") as cf:
        config.write(cf)
