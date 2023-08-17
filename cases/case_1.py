from molpub import DefaultStructureImage, HighlightStructureImage, Figure, obtain_widget_icon


def baseline(file_parent_path, save_parent_path):
    # Initial visualization of the structures in case.
    for structure_name in ["1F34", "1AY7", "1YCR"]:
        origin_structure = DefaultStructureImage(structure_paths=[file_parent_path + structure_name + ".pdb"])
        origin_structure.save(save_path=save_parent_path + "1." + structure_name + ".png", width=1280)


def designed(file_parent_path, temp_parent_path, save_parent_path):
    # Visualization of the structure 1F34.
    s1f34 = HighlightStructureImage(structure_paths=[file_parent_path + "1F34.pdb"])
    s1f34.set_cache(cache_contents=["residue:HOH"])
    s1f34.set_shape(representation_plan=[("chain:A", "surface"), ("chain:B", "cartoon")],
                    independent_color=True, closed_surface=True)
    s1f34.set_state(rotate=[330, 10, 270])
    s1f34.set_color(coloring_plan=[("chain:A", "0xF2F2F2"), ("chain:B", "0x2D2F82"),
                                   ("range:A+1-30,A+65-80,A+90-100,A+108-115,A+120-140", "0xF08080"),
                                   ("range:A+150-160,A+170-180,A+185-195,A+280-310", "0xF08080")])
    s1f34.save(save_path=temp_parent_path + "1F34.png", width=1280, ratio=0.9)
    s1f34.close()

    # Visualization of the structure 1AY7.
    s1ay7 = HighlightStructureImage(structure_paths=[file_parent_path + "1AY7.pdb"])
    s1ay7.set_cache(cache_contents=["residue:HOH"])
    s1ay7.set_shape(representation_plan=[("chain:A", "cartoon"), ("chain:B", "surface")],
                    independent_color=True, closed_surface=True)
    s1ay7.set_state(rotate=[110, 30, 325])
    s1ay7.set_color(coloring_plan=[("chain:A", "0x2D2F82"), ("chain:B", "0xF2F2F2"), ("range:B+25-45", "0xF08080")])
    s1ay7.save(save_path=temp_parent_path + "1AY7.png", width=1280, ratio=1.2)
    s1ay7.close()

    # Visualization of the structure 1YCR.
    s1ycr = HighlightStructureImage(structure_paths=[file_parent_path + "1YCR.pdb"])
    s1ycr.set_shape(representation_plan=[("chain:A", "surface"), ("chain:B", "cartoon")],
                    independent_color=True, closed_surface=True)
    s1ycr.set_state(rotate=[250, 330, 255])
    s1ycr.set_color(coloring_plan=[("chain:A", "0xF2F2F2"), ("chain:B", "0x2D2F82"), ("position:A+96", "0xF08080"),
                                   ("range:A+25-30,A+50-55,A+58-65,A+70-73,A+93-94,A+99-100", "0xF08080")])
    s1ycr.save(save_path=temp_parent_path + "1YCR.png", width=1280, ratio=0.75)
    s1ycr.close()

    # Construct the case figure.
    case = Figure(manuscript_format="Nature", aspect_ratio=(606, 358), mathtext=False)
    case.set_image(image_path=temp_parent_path + "1F34.png", layout=(1, 2, 1))
    case.set_image(image_path=temp_parent_path + "1AY7.png", layout=(2, 2, 3))
    case.set_image(image_path=temp_parent_path + "1YCR.png", layout=(2, 2, 4))
    case.set_text(annotation="Stable Complex", locations=[0.5, 0.96, 0.4, 0.05])
    case.set_text(annotation="Transient\nDomain Domain", locations=[0.25, 0.05, 0.4, 0.1])
    case.set_text(annotation="Transient\nDomain Motif", locations=[0.75, 0.05, 0.4, 0.1])
    case.set_text(annotation="Protein-Protein\nInteractions", locations=[0.5, 0.4, 0.4, 0.1])
    obtain_widget_icon(save_path=temp_parent_path + "arrow(90).png", widget_type="arrow", params={"degree": 90})
    case.set_image(image_path=temp_parent_path + "arrow(90).png", locations=[0.422, 0.44, 0.15, 0.15], transparent=True)
    obtain_widget_icon(save_path=temp_parent_path + "arrow(225).png", widget_type="arrow", params={"degree": 225})
    case.set_image(image_path=temp_parent_path + "arrow(225).png", locations=[0.325, 0.27, 0.15, 0.15], transparent=True)
    obtain_widget_icon(save_path=temp_parent_path + "arrow(315).png", widget_type="arrow", params={"degree": 315})
    case.set_image(image_path=temp_parent_path + "arrow(315).png", locations=[0.525, 0.27, 0.15, 0.15], transparent=True)
    case.save_figure(save_parent_path + "1.png")


if __name__ == "__main__":
    baseline(file_parent_path="./molecule/1/", save_parent_path="./baseline/")
    designed(file_parent_path="./molecule/1/", temp_parent_path="./temp/", save_parent_path="./designed/")
