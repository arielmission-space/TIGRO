import numpy as np
from pyNastran.bdf.bdf import BDF

def read_dat(fname, RCF):
    model = BDF()
    model.read_bdf(fname, punch=True)

    optsurf = {}
    for pid in model.property_ids:
        optsurf[pid] = {}
        elements = model.get_element_ids_dict_with_pids(pid)[pid]
        nodes = model.get_node_ids_with_elements(elements)
        coordinates = {nid: model.nodes[nid].get_position_wrt(model,RCF) for nid in nodes}
        xyz =  np.array([xyz for _, xyz in coordinates.items()])
        node_id = np.array([key for key, _ in coordinates.items()])

        optsurf[pid] = {
            'nodes': node_id,
            'xyz': xyz
        }
    return optsurf

def read_pch(fname):
    with open(fname, "r") as file:
        lines = file.readlines()
    
    inside_disp_block = False
    displacements = {}
    for line in lines:
        if "$DISPLACEMENTS" in line: 
            inside_disp_block = True
            continue
        if "$REAL OUTPUT" in line: continue
        if "$SUBCASE ID" in line: continue
        if line[0] in "\r\n$": 
                    inside_disp_block = False
                    continue
        
        if not inside_disp_block: continue   
        if "-CONT-" in line: continue
        col = line.split()
        if len(col) < 6 or col[1] != "G": continue
        node_id = int(col[0])

        displacements[node_id] = np.array(col[2:5], dtype=float)
    return displacements