from mola.layouts import DefaultStructureImage


def baseline(file_parent_path, save_parent_path):
    # Initial visualization of the structures in case.
    for structure_name in ["7QQA", "Predict"]:
        origin_structure = DefaultStructureImage(structure_path=[file_parent_path + structure_name + ".pdb"])
        origin_structure.save(save_path=save_parent_path + "3." + structure_name + ".png", width=1280)


def designed(file_parent_path, save_parent_path):
    # Visualization and alignment of the structure 7QQA and Predict.
    structure = DefaultStructureImage(structure_path=[file_parent_path + "7QQA.pdb", file_parent_path + "Predict.pdb"])
    structure.align_structures(structure1="7QQA", structure2="Predict")
    structure.set_state(representation_plan=[("all", "cartoon")], rotate_x=30, rotate_y=0, rotate_z=180)
    structure.set_cache(cache_contents=["residue:HOH", "residue:ADP", "residue:MG", "residue:SF4",
                                          "chain:7QQA+B", "chain:7QQA+C", "chain:7QQA+D"])
    structure.set_color(coloring_plan=[("model:7QQA", "0xAAAAAA")])
    structure.set_spectrum_color(palette_plan=[("model:Predict", "rmbc")], expression="RMSD",
                                 template_structure="7QQA+A", color_structure="Predict+2-274")
    structure.save(save_path=save_parent_path + "3.png", width=1800, ratio=0.5)

    # Alignment of the structure 7QQA and Predict, the visualization the Predict clearer.
    structure = DefaultStructureImage(structure_path=[file_parent_path + "7QQA.pdb", file_parent_path + "Predict.pdb"])
    structure.align_structures(structure1="7QQA", structure2="Predict")
    structure.set_state(representation_plan=[("all", "cartoon")], rotate_x=30, rotate_y=180, rotate_z=180)
    structure.set_cache(cache_contents=["model:7QQA"])
    structure.set_spectrum_color(palette_plan=[("model:Predict", "rainbow")], expression="RMSD",
                                 template_structure="7QQA+A", color_structure="Predict+2-274")
    structure.set_advance(settings={"cartoon_putty_transform": 7}, cartoon_putty="on")
    structure.save(save_path=save_parent_path + "3(clearer).png", width=1800, ratio=0.5)


if __name__ == "__main__":
    baseline(file_parent_path="./molecule/3/", save_parent_path="./baseline/")
    designed(file_parent_path="./molecule/3/", save_parent_path="./designed/")
