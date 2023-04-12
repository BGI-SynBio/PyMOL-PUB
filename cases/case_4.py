from mola.layouts import StructureImage, Figure


def baseline(file_parent_path, save_parent_path):
    # Initial visualization of the structures in case.
    for structure_name in ["GPR110Gq", "GPR110Gs", "GPR110G12", "GPR110G13", "GPR110Gi"]:
        origin_structure = StructureImage(structure_path=[file_parent_path + structure_name + ".pdb"])
        origin_structure.save(save_path=save_parent_path + "4." + structure_name + ".png", width=1280)


def designed(file_parent_path, temp_parent_path, save_parent_path):
    # Visualization of the structure GPR110Gq.
    gpr110gq = StructureImage(structure_path=[file_parent_path + "GPR110Gq.pdb"])
    gpr110gq.set_state(representation_plan=[("all", "cartoon")], rotate_x=180, rotate_y=15, rotate_z=90)
    gpr110gq.set_color(coloring_plan=[("chain:A", "0x00BFFF"), ("chain:B", "0x8A2BE2"), ("chain:G", "0xFFA54F"),
                                      ("chain:N", "0x00CD00"), ("chain:R", "0x0000EE")])
    gpr110gq.save(save_path=temp_parent_path + "GPR110Gq-cartoon.png", width=1280, ratio=1.0)
    gpr110gq.set_state(representation_plan=[("all", "surface")], rotate_x=5, rotate_y=15, rotate_z=90)
    gpr110gq.save(save_path=temp_parent_path + "GPR110Gq-surface.png", width=1280, ratio=1.0)

    # Visualization of the structure GPR110Gs.
    gpr110gs = StructureImage(structure_path=[file_parent_path + "GPR110Gs.pdb"])
    gpr110gs.set_state(representation_plan=[("all", "cartoon")], rotate_x=0, rotate_y=15, rotate_z=90)
    gpr110gs.set_color(coloring_plan=[("chain:A", "0xCD3700"), ("chain:B", "0x8A2BE2"), ("chain:C", "0xFFA54F"),
                                      ("chain:D", "0x00CD00"), ("chain:R", "0x0000EE")])
    gpr110gs.save(save_path=temp_parent_path + "GPR110Gs-cartoon.png", width=1280, ratio=1.0)
    gpr110gs.set_state(representation_plan=[("all", "surface")], rotate_x=180, rotate_y=345, rotate_z=270)
    gpr110gs.save(save_path=temp_parent_path + "GPR110Gs-surface.png", width=1280, ratio=1.0)

    # Visualization of the structure GPR110G12.
    gpr110g12 = StructureImage(structure_path=[file_parent_path + "GPR110G12.pdb"])
    gpr110g12.set_state(representation_plan=[("all", "cartoon")], rotate_x=30, rotate_y=345, rotate_z=135)
    gpr110g12.set_color(coloring_plan=[("chain:A", "0xFFB5C5"), ("chain:B", "0x8A2BE2"), ("chain:C", "0x00EE00"),
                                       ("chain:E", "0xFFA54F"), ("chain:R", "0x0000EE")])
    gpr110g12.save(save_path=temp_parent_path + "GPR110G12-cartoon.png", width=1280, ratio=1.0)
    gpr110g12.set_state(representation_plan=[("all", "surface")], rotate_x=330, rotate_y=0, rotate_z=315)
    gpr110g12.save(save_path=temp_parent_path + "GPR110G12-surface.png", width=1280, ratio=1.0)

    # Visualization of the structure GPR110G13.
    gpr110g13 = StructureImage(structure_path=[file_parent_path + "GPR110G13.pdb"])
    gpr110g13.set_state(representation_plan=[("all", "cartoon")], rotate_x=330, rotate_y=0, rotate_z=315)
    gpr110g13.set_color(coloring_plan=[("chain:A", "0xEE30A7"), ("chain:B", "0x8A2BE2"), ("chain:C", "0x00EE00"),
                                       ("chain:D", "0xFFA54F"), ("chain:R", "0x0000EE")])
    gpr110g13.save(save_path=temp_parent_path + "GPR110G13-cartoon.png", width=1280, ratio=1.0)
    gpr110g13.set_state(representation_plan=[("all", "surface")], rotate_x=315, rotate_y=0, rotate_z=315)
    gpr110g13.save(save_path=temp_parent_path + "GPR110G13-surface.png", width=1280, ratio=1.0)

    # Visualization of the structure GPR110Gi.
    gpr110gi = StructureImage(structure_path=[file_parent_path + "GPR110Gi.pdb"])
    gpr110gi.set_state(representation_plan=[("all", "cartoon")], rotate_x=165, rotate_y=0, rotate_z=315)
    gpr110gi.set_color(coloring_plan=[("chain:B", "0xB0E2FF"), ("chain:C", "0x8A2BE2"), ("chain:E", "0x00EE00"),
                                      ("chain:D", "0xFFA54F"), ("chain:R", "0x0000EE")])
    gpr110gi.save(save_path=temp_parent_path + "GPR110Gi-cartoon.png", width=1280, ratio=1.0)
    gpr110gi.set_state(representation_plan=[("all", "surface")], rotate_x=345, rotate_y=0, rotate_z=315)
    gpr110gi.save(save_path=temp_parent_path + "GPR110Gi-surface.png", width=1280, ratio=1.0)

    # # Construct the case figure.
    case = Figure(figsize=(5, 1.54))
    for order, structure_name in enumerate(["GPR110Gq", "GPR110Gs", "GPR110G12", "GPR110G13", "GPR110Gi"]):
        case.set_image(image_path=temp_parent_path + structure_name + "-surface.png", layout=(5, 1, order + 1))
        case.set_image(image_path=temp_parent_path + structure_name + "-cartoon.png",
                       locations=[(0.11 + order * 0.2), 0.45, 0.11, 0.5])
        case.set_text(annotation="G$_{" + structure_name[7::] + "}$", locations=[(0.1 + order * 0.2), 0.1, 0.2, 0.2],
                      font_size=8, weight="bold")

    case.set_text(annotation="GPR110", locations=[0.1, 0.85, 0.2, 0.2], font_size=7, weight="bold", color="#0000EE")
    case.set_text(annotation="Gα$_{q}$", locations=[0.04, 0.57, 0.2, 0.2], font_size=7, weight="bold", color="#00BFFF")
    case.set_text(annotation="Nb35", locations=[0.05, 0.23, 0.2, 0.2], font_size=7, weight="bold", color="#00CD00")
    case.set_text(annotation="Gβ", locations=[0.12, 0.19, 0.2, 0.2], font_size=7, weight="bold", color="#8A2BE2")
    case.set_text(annotation="Gγ", locations=[0.16, 0.26, 0.2, 0.2], font_size=7, weight="bold", color="#FFA54F")
    case.set_text(annotation="Gα$_{s}$", locations=[0.23, 0.56, 0.2, 0.2], font_size=7, weight="bold", color="#CD3700")
    case.set_text(annotation="Gα$_{12}$", locations=[0.41, 0.52, 0.2, 0.2], font_size=7, weight="bold", color="#FFB5C5")
    case.set_text(annotation="scFv16", locations=[0.56, 0.27, 0.2, 0.2], font_size=7, weight="bold", color="#00EE00")
    case.set_text(annotation="Gα$_{13}$", locations=[0.61, 0.53, 0.2, 0.2], font_size=7, weight="bold", color="#EE30A7")
    case.set_text(annotation="Gα$_{i}$", locations=[0.81, 0.51, 0.2, 0.2], font_size=7, weight="bold", color="#B0E2FF")
    case.save_figure(save_parent_path + "4.png")


if __name__ == "__main__":
    baseline(file_parent_path="./molecule/4/", save_parent_path="./baseline/")
    designed(file_parent_path="./molecule/4/", temp_parent_path="./temp/", save_parent_path="./designed/")
