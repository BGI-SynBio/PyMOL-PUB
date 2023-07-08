from molpub import DefaultStructureImage, HighlightStructureImage, Figure


def baseline(file_parent_path, save_parent_path):
    # Initial visualization of the structures in case.
    for structure_name in ["5U1R"]:
        origin_structure = DefaultStructureImage(structure_paths=[file_parent_path + structure_name + ".pdb"])
        origin_structure.save(save_path=save_parent_path + "5." + structure_name + ".png", width=1280)


def designed(file_parent_path, temp_parent_path, save_parent_path):
    # Visualization structure 5U1R.
    s6mss = HighlightStructureImage(structure_paths=[file_parent_path + "5U1R.pdb"])
    s6mss.set_cache(cache_contents=["residue:HOH"])
    s6mss.set_state(rotate=[105, 180, 90])
    s6mss.set_color(coloring_plan=[("residue:DIF", "0xEE0000")])
    s6mss.save(save_path=save_parent_path + "5(no zoom).png", width=1280)

    # Visualization docking area.
    dock_area = HighlightStructureImage(structure_paths=[file_parent_path + "5U1R.pdb"])
    dock_area.set_shape(representation_plan=[("residue:A+DIF", "lines")])
    dock_area.set_cache(cache_contents=["residue:HOH", "chain:B"])
    dock_area.set_state(rotate=[105, 180, 90])
    dock_area.set_zoom(zoom_contents=["residue:A+DIF"], buffer=5.0)
    dock_area.save(save_path=save_parent_path + "5.png", width=1280, ratio=1.0)


if __name__ == "__main__":
    baseline(file_parent_path="./molecule/5/", save_parent_path="./baseline/")
    designed(file_parent_path="./molecule/5/", temp_parent_path="./temp/", save_parent_path="./designed/")
