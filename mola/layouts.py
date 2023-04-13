from logging import getLogger, CRITICAL
from matplotlib import pyplot, rcParams
from numpy import zeros, sum, abs, array, linalg
from os import path
# noinspection PyPackageRequirements
from PIL import Image, PngImagePlugin
from pymol2 import PyMOL
from re import search
from types import FunctionType
from warnings import filterwarnings

filterwarnings("ignore")
getLogger("matplotlib").setLevel(CRITICAL)


class DefaultStructureImage:

    def __init__(self, structure_paths: list):
        self.__mol = PyMOL()
        self.__mol.start()
        self.__structure_names = []
        for structure_path in structure_paths:
            self.__mol.cmd.load(structure_path, quiet=1)
            self.__structure_names.append(structure_path[structure_path.rindex("/") + 1: structure_path.rindex(".")])
        self.__mol.cmd.ray(quiet=1)  # make PyMOL run silently.

    def set_cache(self, cache_contents: list):
        """
        Set cache contents of the structure.

        :param cache_contents: hidden contents.
        :type cache_contents: list
        """
        for hidden_information in cache_contents:
            if ":" in hidden_information:
                shading_type, target_information = hidden_information.split(":")
                if shading_type == "position":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_position = target.split("+")
                            if search(pattern=r"^[0-9]*[1-9][0-9]*$", string=selected_position):
                                selection_command = "(c. " + selected_chain + " and i. " + selected_position + ")"
                            else:
                                raise ValueError("Position (" + selected_position + ")  should be a positive integer!")
                        else:
                            if search(pattern=r"^[0-9]*[1-9][0-9]*$", string=target):
                                selection_command = "(i. " + target + ")"
                            else:
                                raise ValueError("Position (" + target + ") should be a positive integer!")
                        self.__mol.cmd.hide(selection=selection_command)

                elif shading_type == "range":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_range = target.split("+")
                            if "-" in selected_range and selected_range.count("-") == 1:
                                former, latter = selected_range.split("-")
                                if int(former) < int(latter):
                                    selection_command = "(c. " + selected_chain + " and i. " + selected_range + ")"
                                else:
                                    raise ValueError("The former position needs to be less than the latter position "
                                                     + "in the Range (" + selected_range + ").")
                            else:
                                raise ValueError("Range (" + selected_range + ") needs to "
                                                 + "meet the \"number-number\" format!")
                        else:
                            if "-" in target and target.count("-") == 1:
                                former, latter = target.split("-")
                                if int(former) < int(latter):
                                    selection_command = "(i. " + target + ")"
                                else:
                                    raise ValueError("The former position needs to be less than the latter position "
                                                     + "in the Range (" + target + ").")
                            else:
                                raise ValueError("Range (" + target + ") needs to meet the \"number-number\" format!")
                        self.__mol.cmd.hide(selection=selection_command)

                elif shading_type == "residue":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_residue = target.split("+")
                            selection_command = "(c. " + selected_chain + " and r. " + selected_residue + ")"
                        else:
                            selection_command = "(r. " + target + ")"
                        self.__mol.cmd.hide(selection=selection_command)

                elif shading_type == "segment":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_segment = target.split("+")
                            if search(pattern=r"^[A-Z]+$", string=selected_segment):
                                selection_command = "(c. " + selected_chain + " and ps. " + selected_segment + ")"
                            else:
                                raise ValueError("Segment (" + selected_segment + ") should be a string "
                                                 + "composed of uppercase letters!")
                        else:
                            if search(pattern=r"^[A-Z]+$", string=target):
                                selection_command = "(ps. " + target + ")"
                            else:
                                raise ValueError("Segment (" + target + ") should be a string "
                                                 + "composed of uppercase letters!")
                        self.__mol.cmd.hide(selection=selection_command)

                elif shading_type == "chain":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_model, selected_chain = target.split("+")
                            selection_command = "(m. " + selected_model + " and c. " + selected_chain + ")"
                        else:
                            selection_command = "(c. " + target + ")"
                        self.__mol.cmd.hide(selection=selection_command)

                elif shading_type == "model":
                    for target in target_information.split(","):
                        selection_command = "(m. " + target + ")"
                        self.__mol.cmd.hide(selection=selection_command)

                else:
                    raise ValueError("No such shading type! We only support "
                                     + "\"position\", \"range\", \"residue\", \"segment\", \"chain\" and \"model\".")
            else:
                raise ValueError("No such representing information! We only support one type of information, i.e. "
                                 + "\"shading type:target,target,...,target\"")

    def set_state(self, rotate_x: float = 0, rotate_y: float = 0, rotate_z: float = 0,
                  inner_align: bool = False, target_name: str = None):
        """
        Set the state of the structure.

        :param rotate_x: rotate degree with x-axis.
        :type rotate_x: float

        :param rotate_y: rotate degree with y-axis.
        :type rotate_y: float

        :param rotate_z: rotate degree with z-axis.
        :type rotate_z: float

        :param inner_align: align multiple structures through built-in interfaces (cmd.align).
        :type inner_align: bool

        :param target_name: the target (or template) name can be specified if the inner align is executed.
        :type target_name: str or None
        """
        self.__mol.cmd.orient()

        if abs(rotate_x - 0) > 1e-3:
            self.__mol.cmd.rotate(axis="x", angle=rotate_x)
        if abs(rotate_y - 0) > 1e-3:
            self.__mol.cmd.rotate(axis="y", angle=rotate_y)
        if abs(rotate_z - 0) > 1e-3:
            self.__mol.cmd.rotate(axis="z", angle=rotate_z)

        if inner_align and len(self.__structure_names) > 1:
            if target_name is not None:
                for mobile_name in self.__structure_names:
                    if mobile_name != target_name:
                        self.__mol.cmd.align(mobile_name, target_name)
            else:
                target_name = self.__structure_names[0]
                for mobile_name in self.__structure_names[1:]:
                    self.__mol.cmd.align(mobile_name, target_name)

        self.__mol.cmd.center()
        self.__mol.cmd.zoom(complete=1)

    def set_shape(self, representation_plan: list, initial_representation: str = "cartoon"):
        """
        Set the shape (or representation in PyMOL) of the structure.

        :param representation_plan: the type of the visual structure.
        :type representation_plan: list

        :param initial_representation: if representation type is index, can optionally operate on the specified chain.
        :type initial_representation: str
        """
        self.__mol.cmd.show(representation=initial_representation, selection="(all)")

        for step, (representing_information, representation) in enumerate(representation_plan):
            if type(representing_information) is not str:
                raise ValueError("The format of representing information at step " + str(step + 1) + " is illegal! "
                                 + "We only support \"str\" format!")

            if ":" in representing_information:
                shading_type, target_information = representing_information.split(":")
                if shading_type == "position":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_position = target.split("+")
                            if search(pattern=r"^[0-9]*[1-9][0-9]*$", string=selected_position):
                                selection_command = "(c. " + selected_chain + " and i. " + selected_position + ")"
                            else:
                                raise ValueError(
                                    "Position (" + selected_position + ")  should be a positive integer!")
                        else:
                            if search(pattern=r"^[0-9]*[1-9][0-9]*$", string=target):
                                selection_command = "(i. " + target + ")"
                            else:
                                raise ValueError("Position (" + target + ") should be a positive integer!")
                        self.__mol.cmd.show(representation=representation, selection=selection_command)

                elif shading_type == "range":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_range = target.split("+")
                            if "-" in selected_range and selected_range.count("-") == 1:
                                former, latter = selected_range.split("-")
                                if int(former) < int(latter):
                                    selection_command = "(c. " + selected_chain + " and i. " + selected_range + ")"
                                else:
                                    raise ValueError(
                                        "The former position needs to be less than the latter position "
                                        + "in the Range (" + selected_range + ").")
                            else:
                                raise ValueError("Range (" + selected_range + ") needs to "
                                                 + "meet the \"number-number\" format!")
                        else:
                            if "-" in target and target.count("-") == 1:
                                former, latter = target.split("-")
                                if int(former) < int(latter):
                                    selection_command = "(i. " + target + ")"
                                else:
                                    raise ValueError(
                                        "The former position needs to be less than the latter position "
                                        + "in the Range (" + target + ").")
                            else:
                                raise ValueError(
                                    "Range (" + target + ") needs to meet the \"number-number\" format!")
                        self.__mol.cmd.show(representation=representation, selection=selection_command)

                elif shading_type == "residue":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_residue = target.split("+")
                            selection_command = "(c. " + selected_chain + " and r. " + selected_residue + ")"
                        else:
                            selection_command = "(r. " + target + ")"
                        self.__mol.cmd.show(representation=representation, selection=selection_command)

                elif shading_type == "segment":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_segment = target.split("+")
                            if search(pattern=r"^[A-Z]+$", string=selected_segment):
                                selection_command = "(c. " + selected_chain + " and ps. " + selected_segment + ")"
                            else:
                                raise ValueError("Segment (" + selected_segment + ") should be a string "
                                                 + "composed of uppercase letters!")
                        else:
                            if search(pattern=r"^[A-Z]+$", string=target):
                                selection_command = "(ps. " + target + ")"
                            else:
                                raise ValueError("Segment (" + target + ") should be a string "
                                                 + "composed of uppercase letters!")
                        self.__mol.cmd.show(representation=representation, selection=selection_command)

                elif shading_type == "chain":
                    for target in target_information.split(","):
                        self.__mol.cmd.show(representation=representation, selection="(c. " + target + ")")

                elif shading_type == "model":
                    for target in target_information.split(","):
                        self.__mol.cmd.show(representation=representation, selection="(m. " + target + ")")

                else:
                    raise ValueError("No such shading type! We only support "
                                     + "\"position\", \"range\", \"residue\", \"segment\", \"chain\" and \"model\".")

            elif representing_information == "all":
                self.__mol.cmd.show(representation=representation, selection="(all)")

            else:
                raise ValueError("No such representing information! We only support two types of information: "
                                 + "(1) \"all\"; and (2) \"shading type:target,target,...,target\"")

    # def set_spectrum_color(self, palette_plan: list, expression: str = "count", initial_palette: str = "white_gray",
    #                        minimum: float = None, maximum: float = None, byres: int = 0, template_structure: str = None,
    #                        color_structure: str = None):
    #     """
    #     Colors atoms with a spectrum of colors based on an atomic property.
    #
    #     :param palette_plan: coloring plan for the structure.
    #     :type palette_plan: list
    #
    #     :param expression: count, b, q or pc: atom count, temperature factor, occupancy or partial charge.
    #     :type expression: str
    #
    #     :param initial_palette: initial palette in the structure.
    #     :type initial_palette: str
    #
    #     :param minimum: minimum value.
    #     :type minimum: float or None
    #
    #     :param maximum: maximum value.
    #     :type maximum: float or None
    #
    #     :param byres: controls whether coloring is applied per-residue.
    #     :type byres: int
    #
    #     :param template_structure: the template structure used to calculate the property.
    #     :type template_structure: str or None
    #
    #     :param color_structure: the color structure used to calculate the property.
    #     :type color_structure: str or None
    #     """
    #     if expression == "RMSD":
    #         if template_structure is None or color_structure is None:
    #             raise ValueError("We need \"template_structure\" and \"color_structure\" to calculate the RMSD!")
    #
    #         self.set_properties(expression=expression, template_structure=template_structure,
    #                             color_structure=color_structure)
    #         expression = "b"
    #
    #     self.__mol.cmd.spectrum(expression=expression, palette=initial_palette, selection="(all)", minimum=minimum,
    #                             maximum=maximum, byres=byres)
    #
    #     for step, (palette_information, palette) in enumerate(palette_plan):
    #         if type(palette_information) is not str:
    #             raise ValueError("The format of palette information at step " + str(step + 1) + " is illegal! "
    #                              + "We only support \"str\" format!")
    #
    #         if ":" in palette_information:
    #             shading_type, target_information = palette_information.split(":")
    #             if shading_type == "range":
    #                 for target in target_information.split(","):
    #                     if "+" in target:
    #                         selected_chain, selected_range = target.split("+")
    #                         if "-" in selected_range and selected_range.count("-") == 1:
    #                             former, latter = selected_range.split("-")
    #                             if int(former) < int(latter):
    #                                 selection_command = "(c. " + selected_chain + " and i. " + selected_range + ")"
    #                             else:
    #                                 raise ValueError("The former position needs to be less than the latter position "
    #                                                  + "in the Range (" + selected_range + ").")
    #                         else:
    #                             raise ValueError("Range (" + selected_range + ") needs to "
    #                                              + "meet the \"number-number\" format!")
    #                     else:
    #                         if "-" in target and target.count("-") == 1:
    #                             former, latter = target.split("-")
    #                             if int(former) < int(latter):
    #                                 selection_command = "(i. " + target + ")"
    #                             else:
    #                                 raise ValueError("The former position needs to be less than the latter position "
    #                                                  + "in the Range (" + target + ").")
    #                         else:
    #                             raise ValueError("Range (" + target + ") needs to meet the \"number-number\" format!")
    #                     self.__mol.cmd.spectrum(expression=expression, palette=palette, selection=selection_command,
    #                                             minimum=minimum, maximum=maximum, byres=byres)
    #
    #             elif shading_type == "segment":
    #                 for target in target_information.split(","):
    #                     if "+" in target:
    #                         selected_chain, selected_segment = target.split("+")
    #                         if search(pattern=r"^[A-Z]+$", string=selected_segment):
    #                             selection_command = "(c. " + selected_chain + " and ps. " + selected_segment + ")"
    #                         else:
    #                             raise ValueError("Segment (" + selected_segment + ") should be a string "
    #                                              + "composed of uppercase letters!")
    #                     else:
    #                         if search(pattern=r"^[A-Z]+$", string=target):
    #                             selection_command = "(ps. " + target + ")"
    #                         else:
    #                             raise ValueError("Segment (" + target + ") should be a string "
    #                                              + "composed of uppercase letters!")
    #                     self.__mol.cmd.spectrum(expression=expression, palette=palette, selection=selection_command,
    #                                             minimum=minimum, maximum=maximum, byres=byres)
    #
    #             elif shading_type == "chain":
    #                 for target in target_information.split(","):
    #                     self.__mol.cmd.spectrum(expression=expression, palette=palette, selection="(c. " + target + ")",
    #                                             minimum=minimum, maximum=maximum, byres=byres)
    #
    #             elif shading_type == "model":
    #                 for target in target_information.split(","):
    #                     self.__mol.cmd.spectrum(expression=expression, palette=palette, selection="(m. " + target + ")",
    #                                             minimum=minimum, maximum=maximum, byres=byres)
    #
    #             else:
    #                 raise ValueError("No such shading type! We only support "
    #                                  + "\"range\", \"segment\", \"chain\" and \"model\".")
    #
    #         elif palette_information == "all":
    #             self.__mol.cmd.spectrum(expression=expression, palette=palette, selection="(all)", minimum=minimum,
    #                                     maximum=maximum, byres=byres)
    #
    #         else:
    #             raise ValueError("No such coloring information! We only support two types of information: "
    #                              + "(1) \"all\"; and (2) \"shading type:target,target,...,target\"")
    #
    # def align_structures(self, structure1: str, structure2: str):
    #     """
    #     Alignment the structure1 and structure2.
    #
    #     :param structure1: the first structure.
    #     :type structure1: str
    #
    #     :param structure2: the first structure.
    #     :type structure2: str
    #     """
    #     self.__mol.cmd.align(structure1, structure2)
    #
    # def set_advance(self, settings: dict = None, cartoon_putty: str = "off"):
    #     """
    #     Creates a ray-traced image of the current frame.
    #
    #     :param settings: set internal renderer configs.
    #     :type settings: dict or None
    #
    #     :param cartoon_putty: to enable the putty view.
    #     :type cartoon_putty: str
    #     """
    #     if cartoon_putty == "on":
    #         self.__mol.cmd.cartoon("putty")
    #
    #     if settings is None:
    #         settings = {"ray_trace_mode": 0}
    #
    #     for function, config in settings.items():
    #         self.__mol.cmd.set(function, config)
    #
    # def set_properties(self, expression: str, template_structure: str = None, color_structure: str = None):
    #     """
    #     Redefine the color property of atoms.
    #
    #     :param expression: atom property.
    #     :type expression: str
    #
    #     :param template_structure: the template structure used to calculate the property.
    #     :type template_structure: str or None
    #
    #     :param color_structure: the color structure used to calculate the property.
    #     :type color_structure: str or None
    #     """
    #     if expression == "RMSD":
    #         self.__mol.stored.s1 = []
    #         if "+" in template_structure:
    #             selected_model, selected_part = template_structure.split("+")
    #             if "-" in selected_part:
    #                 selection_command = "(m. " + selected_model + " and i. " + selected_part + " and (not hetatm))"
    #             else:
    #                 selection_command = "(m. " + selected_model + " and c. " + selected_part + " and (not hetatm))"
    #         else:
    #             selection_command = "(m. " + template_structure + " and (not hetatm))"
    #         self.__mol.cmd.iterate_state(1, selection_command, "stored.s1.append([x,y,z])")
    #         self.__mol.stored.s1 = array(self.__mol.stored.s1)
    #
    #         self.__mol.stored.s2 = []
    #         if "+" in color_structure:
    #             selected_model, selected_part = color_structure.split("+")
    #             if "-" in selected_part:
    #                 selection_command = "(m. " + selected_model + " and i. " + selected_part + " and (not hetatm))"
    #             else:
    #                 selection_command = "(m. " + selected_model + " and c. " + selected_part + " and (not hetatm))"
    #             color_model = selected_model
    #         else:
    #             selection_command = "(m. " + color_structure + " and (not hetatm))"
    #             color_model = color_structure
    #         color_selection = selection_command
    #         self.__mol.cmd.iterate_state(1, selection_command, "stored.s2.append([x,y,z])")
    #         self.__mol.stored.s2 = array(self.__mol.stored.s2)
    #
    #         self.__mol.cmd.alter("(m. " + color_model + ")", "b=0.0")
    #         self.__mol.stored.rmsd = list(linalg.norm((self.__mol.stored.s1 - self.__mol.stored.s2), axis=1, ord=2))
    #         self.__mol.cmd.alter(color_selection, "b=stored.rmsd.pop(0)")

    def save(self, save_path: str, width: int = 640, ratio: float = 0.75, dpi: int = 1200):
        """
        Save the structure image.

        :param save_path: path to save file.
        :type save_path: str

        :param width: width of the structure image.
        :type width: int

        :param ratio: the ratio of width to height.
        :type ratio: float

        :param dpi: dots per inch.
        :type dpi: int
        """
        self.__mol.cmd.png(filename=save_path, width=width, height=width * ratio, dpi=dpi, quiet=1)


class HighlightStructureImage(DefaultStructureImage):

    def set_color(self, coloring_plan: list, initial_color: str = "0xFFFFCC", edge_color: str = None):
        """
        Set colors for the structure with the coloring plan in order.

        :param coloring_plan: coloring plan for the structure.
        :type coloring_plan: list

        :param initial_color: initial color in the structure.
        :type initial_color: str

        :param edge_color: edge color of the structure if required.
        :type edge_color: str or None
        """
        self.__mol.cmd.color(color=initial_color, selection="(all)")

        for step, (coloring_information, color) in enumerate(coloring_plan):
            if type(coloring_information) is not str:
                raise ValueError("The format of coloring information at step " + str(step + 1) + " is illegal! "
                                 + "We only support \"str\" format!")

            if ":" in coloring_information:
                shading_type, target_information = coloring_information.split(":")
                if shading_type == "position":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_position = target.split("+")
                            if search(pattern=r"^[0-9]*[1-9][0-9]*$", string=selected_position):
                                selection_command = "(c. " + selected_chain + " and i. " + selected_position + ")"
                            else:
                                raise ValueError("Position (" + selected_position + ")  should be a positive integer!")
                        else:
                            if search(pattern=r"^[0-9]*[1-9][0-9]*$", string=target):
                                selection_command = "(i. " + target + ")"
                            else:
                                raise ValueError("Position (" + target + ") should be a positive integer!")
                        self.__mol.cmd.color(color=color, selection=selection_command)

                elif shading_type == "range":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_range = target.split("+")
                            if "-" in selected_range and selected_range.count("-") == 1:
                                former, latter = selected_range.split("-")
                                if int(former) < int(latter):
                                    selection_command = "(c. " + selected_chain + " and i. " + selected_range + ")"
                                else:
                                    raise ValueError("The former position needs to be less than the latter position "
                                                     + "in the Range (" + selected_range + ").")
                            else:
                                raise ValueError("Range (" + selected_range + ") needs to "
                                                 + "meet the \"number-number\" format!")
                        else:
                            if "-" in target and target.count("-") == 1:
                                former, latter = target.split("-")
                                if int(former) < int(latter):
                                    selection_command = "(i. " + target + ")"
                                else:
                                    raise ValueError("The former position needs to be less than the latter position "
                                                     + "in the Range (" + target + ").")
                            else:
                                raise ValueError("Range (" + target + ") needs to meet the \"number-number\" format!")
                        self.__mol.cmd.color(color=color, selection=selection_command)

                elif shading_type == "residue":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_residue = target.split("+")
                            selection_command = "(c. " + selected_chain + " and r. " + selected_residue + ")"
                        else:
                            selection_command = "(r. " + target + ")"
                        self.__mol.cmd.color(color=color, selection=selection_command)

                elif shading_type == "segment":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_segment = target.split("+")
                            if search(pattern=r"^[A-Z]+$", string=selected_segment):
                                selection_command = "(c. " + selected_chain + " and ps. " + selected_segment + ")"
                            else:
                                raise ValueError("Segment (" + selected_segment + ") should be a string "
                                                 + "composed of uppercase letters!")
                        else:
                            if search(pattern=r"^[A-Z]+$", string=target):
                                selection_command = "(ps. " + target + ")"
                            else:
                                raise ValueError("Segment (" + target + ") should be a string "
                                                 + "composed of uppercase letters!")
                        self.__mol.cmd.color(color=color, selection=selection_command)

                elif shading_type == "chain":
                    for target in target_information.split(","):
                        self.__mol.cmd.color(color=color, selection="(c. " + target + ")")

                elif shading_type == "model":
                    for target in target_information.split(","):
                        self.__mol.cmd.color(color=color, selection="(m. " + target + ")")

                else:
                    raise ValueError("No such shading type! We only support "
                                     + "\"position\", \"range\", \"residue\", \"segment\", \"chain\" and \"model\".")

            elif coloring_information == "all":
                self.__mol.cmd.color(color=color, selection="(all)")

            else:
                raise ValueError("No such coloring information! We only support two types of information: "
                                 + "(1) \"all\"; and (2) \"shading type:target,target,...,target\"")

        if edge_color is not None:
            self.__mol.cmd.set(name="ray_trace_color", value=edge_color)
            self.__mol.cmd.set(name="ray_trace_mode", value=1)


class PropertyStructureImage(DefaultStructureImage):

    def set_color(self, target: str, properties: list = None,
                  color_map: str = "rainbow", initial_color: str = "0xFFFFCC", edge_color: str = None,
                  gauge_strengthen: bool = False):
        """
        Set colors for the structure with its element properties.

        :param target: coloring

        :param properties: element properties of the structure.
        :type properties: list or None

        :param color_map:

        :param initial_color: initial color in the structure.
        :type initial_color: str

        :param edge_color: edge color of the structure if required.
        :type edge_color: str or None

        :param gauge_strengthen: strengthen property differences through gauge changes (available in "cartoon").
        :type gauge_strengthen: bool
        """
        self.__mol.cmd.color(color=initial_color, selection="(all)")

        if gauge_strengthen and properties is not None:
            self.__mol.cmd.show(representation="cartoon", selection="(all)")
            self.__mol.cmd.cartoon("putty")

        if properties is None:
            self.__mol.cmd.spectrum(expression="count", palette=color_map, selection="(all)", byres=0)

        else:
            shading_type, target_information = target.split(":")
            # TODO
            if shading_type == "range":
                pass
            elif shading_type == "segment":
                pass
            elif shading_type == "chain":
                pass
            elif shading_type == "model":
                pass

            else:
                raise ValueError("No such shading type! We only support "
                                 + "\"range\", \"segment\", \"chain\" and \"model\".")

        if edge_color is not None:
            self.__mol.cmd.set(name="ray_trace_color", value=edge_color)
            self.__mol.cmd.set(name="ray_trace_mode", value=1)


class Figure:

    def __init__(self, manuscript_format: str = "Nature", column_format: int = None, occupied_columns: int = 1,
                 aspect_ratio: tuple = (1, 2), row_number: int = 1, column_number: int = 1, interval: tuple = (0, 0)):
        """
        Initialize a manuscript figure.

        :param manuscript_format: format of the manuscript (or the publisher of the manuscript).
        :type manuscript_format: str

        :param column_format: column format of manuscript (only support for Cell format).
        :type column_format: int or None

        :param occupied_columns: occupied column number of the manuscript.
        :type occupied_columns: int

        :param aspect_ratio: aspect ratio of figure in the manuscript (height : width).
        :type aspect_ratio: tuple

        :param row_number: number of grid row in the figure.
        :type row_number: int

        :param column_number: number of grid column in the figure.
        :type column_number: int

        :param interval: horizontal (width) and vertical (height) space interval between panels.
        :type interval: tuple
        """
        if manuscript_format == "Nature":
            if occupied_columns == 1:
                self.fig = pyplot.figure(figsize=(3.54, 3.54 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                self.fig = pyplot.figure(figsize=(7.08, 7.08 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("Nature's standard figures allow single or double column.")

            self.minimum_dpi = 300
            rcParams["font.family"] = "Arial"

        elif manuscript_format == "Science":
            if occupied_columns == 1:
                self.fig = pyplot.figure(figsize=(2.24, 2.24 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                self.fig = pyplot.figure(figsize=(4.76, 4.76 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 3:
                self.fig = pyplot.figure(figsize=(7.24, 7.24 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("Science's standard figures allow 1 ~ 3 column(s).")

            self.minimum_dpi = 300
            rcParams["font.family"] = "sans-serif"
            rcParams["font.sans-serif"] = "Helvetica"

        elif manuscript_format == "Cell":
            if column_format is None:
                raise ValueError("The column format for Cell's standard figures should be specified!")

            if column_format == 2:
                if occupied_columns == 1:
                    self.fig = pyplot.figure(figsize=(3.35, 3.35 / aspect_ratio[1] * aspect_ratio[0]))
                elif occupied_columns == 2:
                    self.fig = pyplot.figure(figsize=(6.85, 6.85 / aspect_ratio[1] * aspect_ratio[0]))
                else:
                    raise ValueError("Cell's standard figures allow 1 and 2 column(s).")

            elif column_format == 3:
                if occupied_columns == 1:
                    self.fig = pyplot.figure(figsize=(2.17, 2.17 / aspect_ratio[1] * aspect_ratio[0]))
                elif occupied_columns == 2:
                    self.fig = pyplot.figure(figsize=(4.49, 4.49 / aspect_ratio[1] * aspect_ratio[0]))
                elif occupied_columns == 3:
                    self.fig = pyplot.figure(figsize=(6.85, 6.85 / aspect_ratio[1] * aspect_ratio[0]))
                else:
                    raise ValueError("Cell's standard figures allow 1 ~ 3 column(s).")

            else:
                raise ValueError("No such column format (allowing 2 and 3)!")

            if occupied_columns == 1:
                self.fig = pyplot.figure(figsize=(3.54, 3.54 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                self.fig = pyplot.figure(figsize=(7.08, 7.08 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("Cell's standard figures allow 1 and 2 column(s).")

            self.minimum_dpi = 300
            rcParams["font.family"] = "Arial"

        elif manuscript_format == "PNAS":
            if occupied_columns == 1:
                self.fig = pyplot.figure(figsize=(3.43, 3.43 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                self.fig = pyplot.figure(figsize=(7.08, 7.08 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("PNAS's standard figures allow 1 and 2 column(s).")

            self.minimum_dpi = 600
            rcParams["font.family"] = "sans-serif"
            rcParams["font.sans-serif"] = "Helvetica"

        elif manuscript_format == "ACS":
            if occupied_columns == 1:
                self.fig = pyplot.figure(figsize=(3.30, 3.30 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                self.fig = pyplot.figure(figsize=(7.00, 7.00 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("ACS standard figures allow 1 and 2 column(s).")

            self.minimum_dpi = 600
            rcParams["font.family"] = "Arial"

        elif manuscript_format == "Oxford":
            if occupied_columns == 1:
                self.fig = pyplot.figure(figsize=(3.35, 3.35 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                self.fig = pyplot.figure(figsize=(6.70, 6.70 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("Oxford standard figures allow 1 and 2 column(s).")

            self.minimum_dpi = 350
            rcParams["font.family"] = "Arial"

        elif manuscript_format == "PLOS":
            if occupied_columns == 1:
                self.fig = pyplot.figure(figsize=(5.20, 5.20 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("PLOS standard figures allow single column.")

            self.minimum_dpi = 300
            rcParams["font.family"] = "Arial"

        elif manuscript_format == "IEEE":
            if occupied_columns == 1:
                self.fig = pyplot.figure(figsize=(3.50, 3.50 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                self.fig = pyplot.figure(figsize=(7.16, 7.16 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("IEEE standard figures allow 1 and 2 column(s).")

            self.minimum_dpi = 300
            rcParams["font.family"] = "Times New Roman"

        elif manuscript_format == "ACM":
            if occupied_columns == 1:
                self.fig = pyplot.figure(figsize=(2.50, 2.50 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                self.fig = pyplot.figure(figsize=(6.02, 6.02 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("ACM standard figures allow 1 and 2 column(s).")

            self.minimum_dpi = 300
            rcParams["font.family"] = "Linux Libertine"

        rcParams["mathtext.fontset"] = "custom"
        rcParams["mathtext.rm"] = "Linux Libertine"
        rcParams["mathtext.cal"] = "Lucida Calligraphy"
        rcParams["mathtext.bf"] = "Linux Libertine:bold"
        rcParams["mathtext.it"] = "Linux Libertine:italic"

        if row_number > 1 or column_number > 1:
            self.grid = pyplot.GridSpec(row_number, column_number)
            self.occupy_locations = zeros(shape=(row_number, column_number), dtype=bool)
            pyplot.subplots_adjust(wspace=interval[0], hspace=interval[1])

    def set_panel_grid(self, grid_params):
        """
        Set panel grid for the figure.

        :param grid_params: grid location and occupy of figure.
        :type grid_params: dict
        """
        occupied_parts = sum(self.occupy_locations[grid_params["l"]: grid_params["l"] + grid_params["w"],
                             grid_params["t"]: grid_params["t"] + grid_params["h"]])
        if occupied_parts > 0:
            raise ValueError(str(occupied_parts) + " / " + str(grid_params["w"] * grid_params["h"]) + " were "
                             + "occupied before!")

        pyplot.subplot(self.grid[grid_params["l"]: grid_params["l"] + grid_params["w"],
                       grid_params["t"]: grid_params["t"] + grid_params["h"]])
        self.occupy_locations[grid_params["l"]: (grid_params["l"] + grid_params["w"]),
                              grid_params["t"]: (grid_params["t"] + grid_params["h"])] = 1

    # noinspection PyMethodMayBeStatic
    def set_panel(self, function: FunctionType = None, function_params: dict = None, image_path: str = None):
        """
        Paint a panel in a specific location.

        :param function: painting function.
        :type function: types.FunctionType or None

        :param function_params: parameters of the painting function.
        :type function_params: dict or None

        :param image_path: path of structure image.
        :type image_path: str or None
        """
        if function is not None and image_path is None:
            function(function_params)  # a normal panel function using pyplot statements.

        elif function is None and image_path is not None:
            image_data = Image.open(fp=image_path)
            pyplot.imshow(X=image_data)
            pyplot.xlim(0, image_data.width)
            pyplot.ylim(image_data.height, 0)
            pyplot.axis("off")

        elif function is not None and image_path is not None:
            raise ValueError("We can't choose between \'function\' and \'image_path\'!")

        else:
            raise ValueError("We need to input \'function\' or \'image_path\'!")

    def set_image(self, image_path: str = None, widget_type: str = None, widget_attributes: str = None,
                  image_format: str = ".png", locations: list = None, layout: tuple = None, zorder: int = None):
        """
        Put the structure image or widget with a specific size in a specific position of a panel.

        :param image_path: path of structure image.
        :type image_path: str or None

        :param widget_type: widget type for painting.
        :type widget_type: str or None

        :param widget_attributes: attributes of the selected widget.
        :type widget_attributes: tuple or None

        :param image_format: format of structure image.
        :type image_format: str or None

        :param locations: location in the panel (x,y,dx and dy: the scale of the whole picture).
        :type locations: list or None

        :param layout: picture segmentation method and specified location(x,y,order).
        :type layout: tuple or None

        :param zorder: order in which components are superimposed on each other.
        :type zorder: int or None
        """
        if image_path is not None and (widget_type is not None or widget_attributes is not None):
            raise ValueError("We can't choose between \'image_path\' and \'widget_type|widget_attributes\'!")

        if image_path is None and (widget_type is not None and widget_attributes is not None):
            root_path, image_path = path.abspath(__file__).replace("\\", "/")[:-10] + "supp/widgets/", None
            image_path = root_path + widget_type + " [" + widget_attributes.replace(", ", ".") + "]"
            image_path += image_format

        if image_path is None:
            raise ValueError("We need to input \'image_path\' or \'widget_type|widget_attributes\'!")

        image_format = image_path[image_path.rfind("."):].lower()

        if image_format == ".png":
            image_data = Image.open(fp=image_path)
            self.paste_bitmap(image=image_data, locations=locations, layout=layout, zorder=zorder)
        else:
            raise ValueError("Only PNG files are support!")

    def set_text(self, annotation: str, font_size: int = 16, alignment: str = "center", locations: list = None,
                 layout: tuple = None, zorder: int = None, weight: str = "normal", color: str = "#000000"):
        """
        Put the text box with a specific size in a specific position of a panel.

        :param annotation: text content.
        :type annotation: str

        :param font_size: font size.
        :type font_size: str

        :param alignment: horizontal alignment, accepting "center", "right" and "left".
        :type alignment: str

        :param locations: location in the panel (x,y, dx and dy: the scale of the whole image).
        :type locations: list or None

        :param layout: picture segmentation method and specified location(x,y,order).
        :type layout: tuple or None

        :param zorder: order in which components are superimposed on each other.
        :type zorder: int or None

        :param weight: font weight.
        :type weight: str

        :param color: font color.
        :type color: str
        """
        if locations is not None and layout is not None:
            raise ValueError("We can't choose between \'locations\' and \'layout\'!")

        if layout is not None and locations is None:
            locations = self.calculate_locations(layout=layout)

        if locations is not None:
            if zorder is not None:
                ax = self.fig.add_axes(locations)
                ax.axis("off")
                ax.text(0, 0, annotation, fontsize=font_size, horizontalalignment=alignment, weight=weight, color=color,
                        zorder=zorder)
            else:
                ax = self.fig.add_axes(locations)
                ax.axis("off")
                ax.text(0, 0, annotation, fontsize=font_size, horizontalalignment=alignment, weight=weight, color=color)
        else:
            raise ValueError("We need to input \'locations\' or \'layout\'!")

    def paste_bitmap(self, image: PngImagePlugin.PngImageFile, locations: list = None, layout: tuple = None,
                     zorder: int = None):
        """
        Paste a bitmap in the figure or the panel in figure.

        :param image: bitmap image.
        :type image: PIL.PngImagePlugin.PngImageFile

        :param locations: location in the panel (x,y,dx and dy: the scale of the whole picture).
        :type locations: list or None

        :param layout: picture segmentation method and specified location(x,y,order).
        :type layout: tuple or None

        :param zorder: order in which components are superimposed on each other.
        :type zorder: int or None
        """
        if image.info["dpi"][0] < self.minimum_dpi:
            raise ValueError("The dpi of image is less than the minimum dpi requirement!")

        if locations is not None and layout is not None:
            raise ValueError("We can't choose between \'locations\' and \'layout\'!")

        if layout is not None and locations is None:
            locations = self.calculate_locations(layout=layout)

        if locations is not None:
            if zorder is not None:
                ax = self.fig.add_axes(locations)
                ax.axis("off")
                ax.imshow(X=image, zorder=zorder)
            else:
                ax = self.fig.add_axes(locations)
                ax.axis("off")
                ax.imshow(X=image)
        else:
            raise ValueError("We need to input \'locations\' or \'layout\'!")

    @staticmethod
    def calculate_locations(layout: tuple):
        """
        Calculate the panel locations from layout.

        :param layout: picture segmentation method and specified location(x,y,order).
        :type layout: tuple
        """
        dx = 1.0 / layout[0]
        dy = 1.0 / layout[1]

        if layout[2] % layout[0] == 0:
            x = (layout[0] - 1) * dx
            y = (layout[1] - layout[2] // layout[0]) * dy
        else:
            x = (layout[2] % layout[0] - 1) * dx
            y = (layout[1] - layout[2] // layout[0] - 1) * dy

        return [x, y, dx, dy]

    def save_figure(self, save_path: str):
        """
        Save the whole figure.

        :param save_path: the path of save figure.
        :type save_path: str
        """
        pyplot.savefig(save_path, dpi=self.minimum_dpi)
