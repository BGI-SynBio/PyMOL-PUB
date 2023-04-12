from mola.layouts import StructureImage, Figure


def baseline(file_parent_path, save_parent_path):
    # Initial visualization of the structures in case.
    for structure_name in ["1F34", "1AY7", "1YCR"]:
        origin_structure = StructureImage(structure_path=[file_parent_path + structure_name + ".pdb"])
        origin_structure.save(save_path=save_parent_path + "1." + structure_name + ".png", width=1280)


def designed(file_parent_path, temp_parent_path, save_parent_path):
    # Visualization of the structure 1F34.
    s1f34 = StructureImage(structure_path=[file_parent_path + "1F34.pdb"])
    s1f34.set_hidden(hidden_contents=["residue:HOH"])
    s1f34.set_state(representation_plan=[("chain:A", "surface"), ("chain:B", "cartoon")],
                    rotate_x=240, rotate_y=340, rotate_z=90)
    s1f34.set_color(coloring_plan=[("chain:A", "0xF2F2F2"), ("chain:B", "0x2D2F82"),
                                   ("range:A+1-30,A+65-80,A+90-100,A+108-115,A+120-140", "0xF08080"),
                                   ("range:A+150-160,A+170-180,A+185-195,A+280-310", "0xF08080")])
    s1f34.save(save_path=temp_parent_path + "1F34.png", width=1280, ratio=0.8)

    # Visualization of the structure 1AY7.
    s1ay7 = StructureImage(structure_path=[file_parent_path + "1AY7.pdb"])
    s1ay7.set_hidden(hidden_contents=["residue:HOH"])
    s1ay7.set_state(representation_plan=[("chain:A", "cartoon"), ("chain:B", "surface")],
                    rotate_x=120, rotate_y=30, rotate_z=325)
    s1ay7.set_color(coloring_plan=[("chain:A", "0x2D2F82"), ("chain:B", "0xF2F2F2"), ("range:B+25-45", "0xF08080")])
    s1ay7.save(save_path=temp_parent_path + "1AY7.png", width=1280, ratio=1.2)

    # Visualization of the structure 1YCR.
    s1ycr = StructureImage(structure_path=[file_parent_path + "1YCR.pdb"])
    s1ycr.set_state(representation_plan=[("chain:A", "surface"), ("chain:B", "cartoon")],
                    rotate_x=270, rotate_y=330, rotate_z=255)
    s1ycr.set_color(coloring_plan=[("chain:A", "0xF2F2F2"), ("chain:B", "0x2D2F82"), ("position:A+96", "0xF08080"),
                                   ("range:A+25-30,A+50-55,A+58-65,A+70-73,A+93-94,A+99-100", "0xF08080")])
    s1ycr.save(save_path=temp_parent_path + "1YCR.png", width=1280, ratio=0.75)

    # Construct the case figure.
    case = Figure(manuscript_format="Nature", aspect_ratio=(606, 358))
    case.set_image(image_path=temp_parent_path + "1F34.png", layout=(1, 2, 1))
    case.set_image(image_path=temp_parent_path + "1AY7.png", layout=(2, 2, 3))
    case.set_image(image_path=temp_parent_path + "1YCR.png", layout=(2, 2, 4))
    case.set_text(annotation="Stable Complex", locations=[0.5, 0.96, 0.4, 0.05])
    case.set_text(annotation="Transient\nDomain Domain", locations=[0.25, 0.05, 0.4, 0.1])
    case.set_text(annotation="Transient\nDomain Motif", locations=[0.75, 0.05, 0.4, 0.1])
    case.set_text(annotation="Protein-Protein\nInteractions", locations=[0.5, 0.4, 0.4, 0.1])
    case.set_image(widget_type="arrow", widget_attributes="90-degree", locations=[0.425, 0.44, 0.15, 0.15])
    case.set_image(widget_type="arrow", widget_attributes="225-degree", locations=[0.325, 0.27, 0.15, 0.15])
    case.set_image(widget_type="arrow", widget_attributes="315-degree", locations=[0.525, 0.27, 0.15, 0.15])
    case.save_figure(save_parent_path + "1.png")


if __name__ == "__main__":
    baseline(file_parent_path="./molecule/1/", save_parent_path="./baseline/")
    designed(file_parent_path="./molecule/1/", temp_parent_path="./temp/", save_parent_path="./designed/")
