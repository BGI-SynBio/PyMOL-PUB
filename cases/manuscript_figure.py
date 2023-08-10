from molpub import DefaultStructureImage, HighlightStructureImage, Figure, obtain_widget_icon


def baseline(file_parent_path, save_parent_path):
    # Initial visualization of the structures in case.
    for structure_name in ["2VU9", "3BTA", "3FFZ", "3QUM", "5JLV", "7UIA", "7UIB", "7UIE"]:
        origin_structure = DefaultStructureImage(structure_paths=[file_parent_path + structure_name + ".pdb"])
        origin_structure.save(save_path=save_parent_path + "manuscript." + structure_name + ".png", width=1280)


def designed(file_parent_path, temp_parent_path, save_parent_path):
    # Alignment of the structure 3FFZ, 3QUM, 7OVW and 7UIA, then visualization.
    complex_e = HighlightStructureImage(structure_paths=[file_parent_path + "3FFZ.pdb", file_parent_path + "3QUM.pdb",
                                                         file_parent_path + "7OVW.cif", file_parent_path + "7UIA.pdb"])
    complex_e.set_state(inner_align=True, target="(3FFZ and chain A)", mobile="(7UIA and chain A)")
    complex_e.set_state(inner_align=True, target="(3FFZ and chain A)", mobile="(7OVW and chain AAA)")
    complex_e.set_state(inner_align=True, target="(7UIA and chain G)", mobile="(3QUM and chain G)")
    complex_e.set_cache(cache_contents=["residue:HOH,ZN,NA,ACT,SO4,PEG,A2G", "chain:7OVW+AAA,7OVW+BBB",
                                        "residue:7UIA+G+NAG,7UIA+C+NAG,7UIA+H+NAG,7UIA+F+NAG", "range:3QUM+G+8-15",
                                        "residue:3QUM+E+NAG,3QUM+E+MAN,3QUM+E+GAL,3QUM+E+SIA,3QUM+E+FUC,3QUM+F+GAL",
                                        "residue:7OVW+HHH+BGC,7OVW+HHH+GAL,7OVW+HHH+NGA,7OVW+HHH+SIA", "chain:3FFZ+B",
                                        "chain:3QUM+A,3QUM+B,3QUM+C,3QUM+D,3QUM+H,3QUM+K,3QUM+L,3QUM+M,3QUM+P,3QUM+Q",
                                        "chain:7UIA+A,7UIA+B,7UIA+D,7UIA+E,7UIA+F,7UIA+H,7UIA+G", "atom:7OVW+GGG+H"])
    complex_e.set_color(coloring_plan=[("range:3FFZ+A+1-400", "0xCAFBFC"), ("range:3FFZ+A+401-800", "0x8C3E97"),
                                       ("range:3FFZ+A+801-1252", "0x00CD00"), ("chain:7UIA+C", "0xE59747"),
                                       ("chain:3QUM+G", "0xA15153"), ("chain:7OVW+GGG", "0x00C5CD"),
                                       ("atom:7OVW+GGG+O,7OVW+GGG+H", "0xC07079")])
    complex_e.set_state(rotate=[280, 5, 240])
    complex_e.set_zoom(zoom_contents=["chain:3FFZ+A"], buffer=5.0)
    complex_e.save(save_path=temp_parent_path + "BoNTE-SV2-gangliosides.png", width=1800, ratio=1.2)
    complex_e.set_zoom(zoom_contents=["chain:3QUM+G"], buffer=1.0)
    complex_e.save(save_path=temp_parent_path + "BoNTE-SV2-gangliosides-zoom(N-glycan).png", width=1800, ratio=1.0)
    complex_e.close()

    # Alignment of the structure 3BTA, 5JLV, 2VU9, then visualization.
    complex_a = HighlightStructureImage(structure_paths=[file_parent_path + "3BTA.pdb", file_parent_path + "5JLV.pdb",
                                                         file_parent_path + "2VU9.pdb"])
    complex_a.set_state(inner_align=True, target="(3BTA)", mobile="(5JLV and chain A)")
    complex_a.set_state(inner_align=True, target="(3BTA)", mobile="(2VU9)")
    complex_a.set_cache(cache_contents=["residue:HOH,MG,ZN,ACT,PO4", "residue:5JLV+F+NAG,5JLV+F+FUC,5JLV+C+NAG",
                                        "chain:5JLV+B,5JLV+A,5JLV+D", "chain:2VU9+A"])
    complex_a.set_color(coloring_plan=[("range:3BTA+A+1-450", "0xFCFC82"), ("range:3BTA+A+451-875", "0x884423"),
                                       ("range:3BTA+A+876-1295", "0x999999"), ("chain:5JLV+C", "0x0989FC"),
                                       ("chain:5JLV+E", "0x3892F3"), ("atom:5JLV+E+O,5JLV+E+H", "0xD55758"),
                                       ("chain:2VU9+B", "0x639592"), ("atom:2VU9+B+O,2VU9+B+H", "0xD55758")])
    complex_a.set_state(rotate=[65, 12.5, 50])
    complex_a.set_zoom(zoom_contents=["model:3BTA"], buffer=20.0)
    complex_a.save(save_path=temp_parent_path + "BoNTA-SV2-gangliosides.png", width=1800, ratio=1.2)
    complex_a.set_zoom(zoom_contents=["chain:5JLV+E"], buffer=10.0)
    complex_a.save(save_path=temp_parent_path + "BoNTA-SV2-gangliosides-zoom(N-glycan).png", width=1800, ratio=1.0)
    complex_a.close()

    # Alignment of the structure 7UIA, 5JLV, 7OVW and 2VU9, then visualization.
    complexsub = HighlightStructureImage(structure_paths=[file_parent_path + "7UIA.pdb", file_parent_path + "5JLV.pdb",
                                                          file_parent_path + "7OVW.cif", file_parent_path + "2VU9.pdb"])
    complexsub.set_state(inner_align=True, target="(7UIA and chain A)", mobile="(5JLV and chain A)")
    complexsub.set_state(inner_align=True, target="(7UIA and chain A)", mobile="(7OVW and chain AAA)")
    complexsub.set_state(inner_align=True, target="(5JLV and chain A)", mobile="(2VU9)")
    complexsub.set_cache(cache_contents=["residue:HOH,MG,ZN,NA,ACT,PO4,SO4,PEG,A2G", "chain:7OVW+AAA,7OVW+BBB",
                                         "residue:7UIA+G+NAG,7UIA+C+NAG,7UIA+H+NAG,7UIA+F+NAG", "chain:5JLV+B,5JLV+D",
                                         "residue:7OVW+HHH+BGC,7OVW+HHH+GAL,7OVW+HHH+NGA,7OVW+HHH+SIA", "chain:2VU9+A",
                                         "residue:5JLV+F+NAG,5JLV+F+FUC,5JLV+C+NAG", "atom:7OVW+GGG+H",
                                         "chain:7UIA+B,7UIA+D,7UIA+E,7UIA+F,7UIA+H,7UIA+G"])
    complexsub.set_color(coloring_plan=[("chain:7UIA+A", "0x00CD00"), ("chain:7UIA+C", "0xE59747"),
                                        ("chain:7OVW+GGG", "0x00C5CD"), ("atom:7OVW+GGG+O,7OVW+GGG+H", "0xC07079"),
                                        ("chain:5JLV+A", "0x999999"), ("chain:5JLV+C", "0x0989FC"),
                                        ("chain:5JLV+E", "0x3892F3"), ("atom:5JLV+E+O,5JLV+E+H", "0xD55758"),
                                        ("chain:2VU9+B", "0x639592"), ("atom:2VU9+B+O,2VU9+B+H", "0xD55758")])
    complexsub.set_state(rotate=[205, 20, 25])
    complexsub.set_zoom(zoom_contents=["range:7UIA+A+1102-1103"], buffer=18.0)
    complexsub.save(save_path=temp_parent_path + "HCE_SV2Ac-HCA_SV2C.png", width=1800, ratio=0.5)
    complexsub.set_state(rotate=[0, 115, 0], only_rotate=True)
    complexsub.set_zoom(zoom_contents=["range:7UIA+C+576-577"], buffer=18.0)
    complexsub.save(save_path=temp_parent_path + "HCE_SV2Ac-HCA_SV2C(115).png", width=1800, ratio=0.5)
    complexsub.close()

    # Construct the case figure.
    case = Figure(manuscript_format="Oxford", occupied_columns=2, aspect_ratio=(1298, 1746), dpi=600, mathtext=True)
    # construct widgets
    widget_icon_dict = {"rotation(115)": {"turn": "right", "degree": 115}, "arrow(45)": {"degree": 45},
                        "arrow(315)": {"degree": 315}, "arrow(85)": {"degree": 85},
                        "line(45)": {"degree": 45, "linestyle": "--", "linewidth": 0.992, "color": "#D9D9D9"},
                        "line(25)": {"degree": 25, "linestyle": "--", "linewidth": 1.2, "color": "#D9D9D9"},
                        "line(155)": {"degree": 155, "linestyle": "--", "linewidth": 2.232, "color": "#D9D9D9"},
                        "line(30)": {"degree": 30, "linestyle": "--", "linewidth": 2.232, "color": "#D9D9D9"}}
    for wname, content in widget_icon_dict.items():
        obtain_widget_icon(save_path=temp_parent_path + wname + ".png", widget_type=wname.split('(')[0], params=content)
    # set structure images
    case.set_image(image_path=temp_parent_path + "BoNTE-SV2-gangliosides.png", locations=[0.075, 0.35, 0.3, 0.65])
    case.set_image(image_path=temp_parent_path + "BoNTA-SV2-gangliosides.png", locations=[0.675, 0.35, 0.3, 0.65])
    case.set_image(image_path=temp_parent_path + "HCE_SV2Ac-HCA_SV2C.png", locations=[0.08, 0.01, 0.38, 0.35],
                   positions=(8, 4, 0, 8, -0.5, 3.25), frame_off=False, linewidth=1.5)
    case.set_image(image_path=temp_parent_path + "HCE_SV2Ac-HCA_SV2C(115).png", locations=[0.56, 0.01, 0.38, 0.35],
                   positions=(8, 4, 0.5, 8.45, -0.5, 3.25), frame_off=False, linewidth=1.5)
    case.set_image(image_path=temp_parent_path + "BoNTE-SV2-gangliosides-zoom(N-glycan).png",
                   locations=[0.375, 0.7, 0.25, 0.25], frame_off=False, linewidth=1.5, linecolor="#D9D9D9")
    case.set_image(image_path=temp_parent_path + "BoNTA-SV2-gangliosides-zoom(N-glycan).png",
                   locations=[0.375, 0.425, 0.25, 0.25], frame_off=False, linewidth=1.5, linecolor="#D9D9D9")
    # set widgets
    widget_image_dict = {1: ("rotation(115)", [0.46, 0.15, 0.1, 0.1]), 2: ("arrow(315)", [0.215, 0.215, 0.025, 0.025]),
                         3: ("arrow(85)", [0.19, 0.09, 0.025, 0.025]), 4: ("arrow(85)", [0.625, 0.12, 0.025, 0.025]),
                         5: ("arrow(45)", [0.795, 0.075, 0.025, 0.025]), 6: ("line(45)", [0.0624, 0.5655, 0.45, 0.45]),
                         7: ("line(25)", [0.115, 0.453, 0.348, 0.348]), 8: ("line(155)", [0.562, 0.5328, 0.2, 0.2]),
                         9: ("line(30)", [0.557, 0.372, 0.21, 0.21])}
    for _, content in widget_image_dict.items():
        case.set_image(image_path=temp_parent_path + content[0] + ".png", locations=content[1], transparent=True)
    # set texts
    case.set_text(annotation="Membrane", locations=[0.05, 0.35, 0.9, 0.05], backgroundcolor="#FEF4E8",
                  positions=(0.5, 0.3), font_size=12)
    case.set_text(annotation="N-glycan", locations=[0.455, 0.82, 0.04, 0.02], font_size=9, weight="bold",
                  color="#A15153", transparent=True)
    case.set_text(annotation="N-glycan", locations=[0.455, 0.49, 0.04, 0.02], font_size=9, weight="bold",
                  color="#3892F3", transparent=True)
    text_dict1 = {1: ("N-glycan", [0.1, 0.575, 0.05, 0.05], "A15153"), 2: ("SV2A", [0.2, 0.425, 0.05, 0.05], "E59747"),
                  3: (r"/ $H_c$A", [0.35, 0.28, 0.04, 0.03], "999999"), 4: ("BoNT/A", [0.8, 0.9, 0.05, 0.05], "000000"),
                  5: ("115°", [0.51, 0.11, 0.04, 0.04], "000000"), 6: (r"/ $H_c$A", [0.75, 0.28, 0.04, 0.03], "999999"),
                  7: (r"$H_c$E", [0.7, 0.28, 0.04, 0.03], "00CD00"), 8: ("BoNT/E", [0.15, 0.9, 0.05, 0.05], "000000"),
                  9: ("GD1a", [0.3, 0.425, 0.05, 0.05], "00C5CD"), 10: (r"$H_c$E", [0.3, 0.28, 0.04, 0.03], "00CD00"),
                  11: ("SV2C", [0.78, 0.425, 0.05, 0.05], "3892F3"), 12: ("GT1b", [0.88, 0.425, 0.05, 0.05], "639592"),
                  13: ("N-glycan", [0.68, 0.555, 0.05, 0.05], "3892F3")}
    for _, content in text_dict1.items():
        case.set_text(annotation=content[0], locations=content[1], font_size=11, weight="bold", color="#" + content[2],
                      transparent=True)
    text_dict2 = {1: ("SV2C", [0.195, 0.24, 0.04, 0.03], "#3892F3"), 2: ("N", [0.13, 0.23, 0.01, 0.05], "#E59747"),
                  3: ("SV2Ac", [0.13, 0.13, 0.02, 0.03], "#E59747"), 4: ("β8", [0.2, 0.075, 0.01, 0.02], "#E59747"),
                  5: ("C", [0.23, 0.095, 0.01, 0.02], "#E59747"), 6: ("GD1a", [0.335, 0.075, 0.02, 0.02], "#00C5CD"),
                  7: ("/GT1b", [0.39, 0.075, 0.02, 0.02], "#639592"), 8: ("SV2C", [0.61, 0.215, 0.02, 0.02], "#3892F3"),
                  9: ("β8", [0.625, 0.105, 0.01, 0.02], "#3892F3"), 10: ("C", [0.685, 0.14, 0.01, 0.02], "#3892F3"),
                  11: ("N", [0.75, 0.15, 0.01, 0.02], "#3892F3"), 12: ("C", [0.745, 0.085, 0.01, 0.02], "#E59747"),
                  13: ("β8", [0.79, 0.07, 0.01, 0.02], "#E59747"), 14: ("SV2Ac", [0.905, 0.14, 0.01, 0.02], "#E59747"),
                  15: ("N", [0.885, 0.215, 0.01, 0.02], "#E59747")}
    for _, content in text_dict2.items():
        case.set_text(annotation=content[0], locations=content[1], font_size=10, color=content[2])
    text_dict3 = {"a": [0.05, 0.95, 0.05, 0.05], "b": [0.05, 0.3, 0.05, 0.05],
                  "c": [0.425, 0.915, 0.02, 0.02], "d": [0.425, 0.635, 0.02, 0.02]}
    for annotation, content in text_dict3.items():
        case.set_text(annotation=annotation, locations=content, weight="bold", transparent=True)
    case.save_figure(save_parent_path + "manuscript_figure.png")


if __name__ == "__main__":
    baseline(file_parent_path="./molecule/manuscript/", save_parent_path="./baseline/")
    designed(file_parent_path="./molecule/manuscript/", temp_parent_path="./temp/", save_parent_path="./designed/")
