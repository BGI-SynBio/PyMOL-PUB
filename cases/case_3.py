from molpub import DefaultStructureImage, PropertyStructureImage, set_properties


def baseline(file_parent_path, save_parent_path):
    # Initial visualization of the structures in case.
    for structure_name in ["7QQA", "Predict"]:
        origin_structure = DefaultStructureImage(structure_paths=[file_parent_path + structure_name + ".pdb"])
        origin_structure.save(save_path=save_parent_path + "3." + structure_name + ".png", width=1280)


def designed(file_parent_path, save_parent_path):
    # Visualization and alignment of the structure 7QQA and Predict.
    properties = set_properties(structure_paths=[file_parent_path + "7QQA.pdb", file_parent_path + "Predict.pdb"],
                                molecule_type="AA", property_type="PyMOL-align",
                                targets=["chain:7QQA+A", "range:Predict+2-274"])
    structure = PropertyStructureImage(structure_paths=[file_parent_path + "7QQA.pdb",
                                                        file_parent_path + "Predict.pdb"])
    structure.set_cache(cache_contents=["residue:HOH", "residue:ADP", "residue:MG", "residue:SF4",
                                        "chain:7QQA+B", "chain:7QQA+C", "chain:7QQA+D"])
    structure.set_state(rotate=[330, 0, 0], inner_align=True, target="7QQA")
    structure.set_zoom(zoom_contents=["model:Predict"])
    structure.set_color(target="range:Predict+2-274", properties=properties, color_map="rmbc")
    structure.save(save_path=save_parent_path + "3.png", width=1800, ratio=1.2)
    structure.close()

    # Alignment of the structure 7QQA and Predict, the visualization the Predict clearer.
    properties = set_properties(structure_paths=[file_parent_path + "7QQA.pdb", file_parent_path + "Predict.pdb"],
                                molecule_type="AA", property_type="PyMOL-align",
                                targets=["chain:7QQA+A", "range:Predict+2-274"])
    structure = PropertyStructureImage(structure_paths=[file_parent_path + "7QQA.pdb",
                                                        file_parent_path + "Predict.pdb"])
    structure.set_cache(cache_contents=["model:7QQA"])
    structure.set_state(rotate=[330, 0, 0], inner_align=True, target="7QQA")
    structure.set_zoom(zoom_contents=["model:Predict"])
    structure.set_color(target="range:Predict+2-274", properties=properties, color_map="rainbow", gauge_strengthen=True)
    structure.save(save_path=save_parent_path + "3(clearer).png", width=1800, ratio=1.2)
    structure.close()


if __name__ == "__main__":
    baseline(file_parent_path="./molecule/3/", save_parent_path="./baseline/")
    designed(file_parent_path="./molecule/3/", save_parent_path="./designed/")
