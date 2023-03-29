from mola.layouts import StructureImage, Figure

if __name__ == "__main__":
    # Visualization of the structure 1F34.
    s1f34 = StructureImage(structure_path='../cases/molecule/1/1F34.pdb')
    s1f34.set_state(representation_type="chain", representations={"A": "surface", "B": "cartoon"}, hides=["(r. HOH)"])
    s1f34.set_color(shading_type="chain", colors={"A": "0xF2F2F2", "B": "0x2D2F82"})
    s1f34.set_color(shading_type="index", chain_select="A",
                    colors={"1-30": "0xF08080", "65-80": "0xF08080", "90-100": "0xF08080", "108-115": "0xF08080",
                            "120-140": "0xF08080", "150-160": "0xF08080", "170-180": "0xF08080", "185-195": "0xF08080",
                            "280-310": "0xF08080"})
    s1f34.rotate_structure(rotate_dict={"x": 240, "y": 340, "z": 90})
    s1f34.save(save_path='../cases/output/case1/1F34.png', ratio=0.8)

    # Visualization of the structure 1AY7.
    s1ay7 = StructureImage(structure_path='../cases/molecule/1/1AY7.pdb')
    s1ay7.set_state(representation_type="chain", representations={"A": "cartoon", "B": "surface"}, hides=["(r. HOH)"])
    s1ay7.set_color(shading_type="chain", colors={"A": "0x2D2F82", "B": "0xF2F2F2"})
    s1ay7.set_color(shading_type="index", chain_select="B", colors={"25-45": "0xF08080"})
    s1ay7.rotate_structure(rotate_dict={"x": 120, "y": 30, "z": 325})
    s1ay7.save(save_path='../cases/output/case1/1AY7.png', ratio=1.2)

    # Visualization of the structure 1YCR.
    s1ycr = StructureImage(structure_path='../cases/molecule/1/1YCR.pdb')
    s1ycr.set_state(representation_type="chain", representations={"A": "surface", "B": "cartoon"})
    s1ycr.set_color(shading_type="chain", colors={"A": "0xF2F2F2", "B": "0x2D2F82"})
    s1ycr.set_color(shading_type="index", chain_select="A",
                    colors={"25-30": "0xF08080", "50-55": "0xF08080", "58-65": "0xF08080", "70-73": "0xF08080",
                            "93-94": "0xF08080", "96": "0xF08080", "99-100": "0xF08080"})
    s1ycr.rotate_structure(rotate_dict={"x": 270, "y": 330, "z": 255})
    s1ycr.save(save_path='../cases/output/case1/1YCR.png', ratio=0.75)

    # Construct case1 figure
    case1 = Figure(manuscript_format="Nature", aspect_ratio=(606, 358))

    case1.set_image(image_path='../cases/output/case1/1F34.png', layout=(1, 2, 1))
    case1.set_image(image_path='../cases/output/case1/1AY7.png', layout=(2, 2, 3))
    case1.set_image(image_path='../cases/output/case1/1YCR.png', layout=(2, 2, 4))

    case1.set_text(annotation="Stable Complex", locations=[0.5, 0.96, 0.4, 0.05])
    case1.set_text(annotation="Transient\nDomain Domain", locations=[0.25, 0.05, 0.4, 0.1])
    case1.set_text(annotation="Transient\nDomain Motif", locations=[0.75, 0.05, 0.4, 0.1])
    case1.set_text(annotation="Protein-Protein\nInteractions", locations=[0.5, 0.4, 0.4, 0.1])

    case1.set_image(widget_type='arrow', widget_attributes='90-degree', locations=[0.425, 0.44, 0.15, 0.15])
    case1.set_image(widget_type='arrow', widget_attributes='225-degree', locations=[0.325, 0.27, 0.15, 0.15])
    case1.set_image(widget_type='arrow', widget_attributes='315-degree', locations=[0.525, 0.27, 0.15, 0.15])

    case1.save_figure('../cases/output/case1/case1.png')

    # Initial visualization of the structures in case1.
    structures_name = ['1F34', '1AY7', '1YCR']
    for stru_name in structures_name:
        orign_stru = StructureImage(structure_path='../cases/molecule/1/' + stru_name + '.pdb')
        orign_stru.save(save_path='../cases/output/case1/orign-' + stru_name + '.png')
