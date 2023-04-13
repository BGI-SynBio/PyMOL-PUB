from mola.layouts import DefaultStructureImage, Figure


def baseline(file_parent_path, save_parent_path):
    # Initial visualization of the structures in case.
    for structure_name in ["T0950", "Predict"]:
        origin_structure = DefaultStructureImage(structure_path=[file_parent_path + structure_name + ".pdb"])
        origin_structure.save(save_path=save_parent_path + "2." + structure_name + ".png", width=1280)


def designed(file_parent_path, temp_parent_path, save_parent_path):
    # Alignment of the structure T0950 and Predict, then visualization T0950.
    t0950 = DefaultStructureImage(structure_path=[file_parent_path + "T0950.pdb", file_parent_path + "Predict.pdb"])
    t0950.align_structures(structure1="T0950", structure2="Predict")
    t0950.set_state(representation_plan=[("model:T0950", "cartoon")], rotate_x=60, rotate_y=345, rotate_z=0)
    t0950.set_cache(cache_contents=["model:Predict"])
    t0950.set_color(coloring_plan=[("model:T0950", "0xAAAAAA")])
    t0950.save(save_path=temp_parent_path + "T0950.png", width=1800, ratio=0.5)

    # Alignment of the structure T0950 and Predict, then visualization Predict.
    predict = DefaultStructureImage(structure_path=[file_parent_path + "T0950.pdb", file_parent_path + "Predict.pdb"])
    predict.align_structures(structure1="T0950", structure2="Predict")
    predict.set_state(representation_plan=[("model:Predict", "cartoon")], rotate_x=60, rotate_y=345, rotate_z=0)
    predict.set_cache(cache_contents=["model:T0950"])
    predict.set_spectrum_color(palette_plan=[("model:Predict", "rainbow")])
    predict.set_advance(settings={"ray_trace_color": "0x000000", "ray_trace_mode": 1})
    predict.save(save_path=temp_parent_path + "Predict.png", width=1800, ratio=0.5)

    # Construct the case figure.
    case = Figure(figsize=(18, 9))
    case.set_image(image_path=temp_parent_path + "T0950.png", layout=(1, 1, 1))
    case.set_image(image_path=temp_parent_path + "Predict.png", layout=(1, 1, 1))
    case.save_figure(save_parent_path + "2.png")

    # Visualization and alignment of the structure T0950 and Predict(no outline).
    structure = DefaultStructureImage(structure_path=[file_parent_path + "T0950.pdb", file_parent_path + "Predict.pdb"])
    structure.align_structures(structure1="T0950", structure2="Predict")
    structure.set_state(representation_plan=[("all", "cartoon")], rotate_x=60, rotate_y=345, rotate_z=0)
    structure.set_color(coloring_plan=[("model:T0950", "0xAAAAAA")])
    structure.set_spectrum_color(palette_plan=[("model:Predict", "rainbow")])
    structure.save(save_path=save_parent_path + "2(no outline).png", width=1800, ratio=0.5)


if __name__ == "__main__":
    baseline(file_parent_path="./molecule/2/", save_parent_path="./baseline/")
    designed(file_parent_path="./molecule/2/", temp_parent_path="./temp/", save_parent_path="./designed/")
