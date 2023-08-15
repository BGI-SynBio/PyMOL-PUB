from molpub import DefaultStructureImage, HighlightStructureImage, PropertyStructureImage, Figure


def baseline(file_parent_path, save_parent_path):
    # Initial visualization of the structures in case.
    for structure_name in ["T0950", "Predict"]:
        origin_structure = DefaultStructureImage(structure_paths=[file_parent_path + structure_name + ".pdb"])
        origin_structure.save(save_path=save_parent_path + "2." + structure_name + ".png", width=1280)


def designed(file_parent_path, temp_parent_path, save_parent_path):
    # Alignment of the structure T0950 and Predict, then visualization T0950.
    t0950 = HighlightStructureImage(structure_paths=[file_parent_path + "T0950.pdb", file_parent_path + "Predict.pdb"])
    t0950.set_cache(cache_contents=["model:Predict"])
    t0950.set_state(rotate=[120, 180, 0], inner_align=True, target="T0950")
    t0950.set_color(coloring_plan=[("model:T0950", "0xAAAAAA")])
    t0950.save(save_path=temp_parent_path + "T0950.png", width=1800, ratio=0.7)
    t0950.close()

    # Alignment of the structure T0950 and Predict, then visualization Predict.
    predict = PropertyStructureImage(structure_paths=[file_parent_path + "T0950.pdb",
                                                      file_parent_path + "Predict.pdb"])
    predict.set_cache(cache_contents=["model:T0950"])
    predict.set_state(rotate=[120, 180, 0], inner_align=True, target="T0950")
    predict.set_color(target="model:Predict", color_map="rainbow", edge_color="0x000000")
    predict.save(save_path=temp_parent_path + "Predict.png", width=1800, ratio=0.7)
    predict.close()

    # Construct the case figure.
    case = Figure(manuscript_format="Science", occupied_columns=2, aspect_ratio=(7, 10))
    case.set_image(image_path=temp_parent_path + "T0950.png", layout=(1, 1, 1))
    case.set_image(image_path=temp_parent_path + "Predict.png", layout=(1, 1, 1))
    case.save_figure(save_parent_path + "2.png")

    # Visualization and alignment of the structure T0950 and Predict(no outline).
    structure = PropertyStructureImage(structure_paths=[file_parent_path + "T0950.pdb",
                                                        file_parent_path + "Predict.pdb"])
    structure.set_state(rotate=[120, 180, 0], inner_align=True, target="T0950")
    structure.set_color(target="model:Predict", color_map="rainbow")
    structure.save(save_path=save_parent_path + "2(no outline).png", width=1800, ratio=0.7)
    structure.close()


if __name__ == "__main__":
    baseline(file_parent_path="./molecule/2/", save_parent_path="./baseline/")
    designed(file_parent_path="./molecule/2/", temp_parent_path="./temp/", save_parent_path="./designed/")
