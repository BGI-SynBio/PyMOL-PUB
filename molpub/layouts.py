from logging import getLogger, CRITICAL
from matplotlib import pyplot, rcParams, patches
from numpy import array, zeros, linspace, deg2rad, sum, cos, sin, sqrt, pi
from os import path
from PIL import Image, PngImagePlugin

try:
    from pymol2 import PyMOL  # Please refer to https://pymol.org/2/ for download of PyMOL library
except ModuleNotFoundError:
    print("PyMOL is not installed!")

from re import search
from types import FunctionType
from warnings import filterwarnings

filterwarnings("ignore")
getLogger("matplotlib").setLevel(CRITICAL)


def obtain_widget_icon(save_path: str, widget_type: str, params: dict, dpi: int = 1200):
    """
    Obtain the widget icon based on the predetermined setting.

    :param save_path: the path of save icon.
    :type save_path: str

    :param widget_type: widget type including "arrow" and "rotation".
    :type widget_type: str

    :param params: parameters of the widget.
    :type params: dict

    :param dpi: dots per inch.
    :type dpi: int
    """
    if widget_type == "line":
        if "degree" in params:
            if 0 <= params["degree"] <= 180:
                x = pi * params["degree"] / 180
                figure = pyplot.figure(figsize=(2, 2))
                if "color" in params:
                    color = params["color"]
                else:
                    color = "black"
                if "linestyle" in params:
                    linestyle = params["linestyle"]
                else:
                    linestyle = "-"
                if "linewidth" in params:
                    linewidth = params["linewidth"]
                else:
                    linewidth = 1.0

                pyplot.xlim(-1, 1)
                pyplot.ylim(-1, 1)
                pyplot.plot([-cos(x), cos(x)], [-sin(x), sin(x)], linewidth=linewidth,
                            color=color, linestyle=linestyle)
                pyplot.axis('off')
                figure.savefig(save_path, dpi=dpi, transparent=True, pad_inches=0, bbox_inches="tight")
                pyplot.close()
            else:
                raise ValueError("The scope of \"degree\" is [0, 360].")
        else:
            raise ValueError("\"degree\" is a parameter that \"arrow\" must specify.")

    elif widget_type == "arrow":
        if "degree" in params:
            if 0 <= params["degree"] <= 360:
                x = pi * params["degree"] / 180
                figure = pyplot.figure(figsize=(2, 2))
                if "color" in params:
                    color = params["color"]
                else:
                    color = "black"
                if "linestyle" in params:
                    linestyle = params["linestyle"]
                else:
                    linestyle = "-"
                if "width" in params:
                    width = params["width"]
                else:
                    width = 0.02
                if "head_width" in params:
                    head_width = params["head_width"]
                else:
                    head_width = 0.3
                if "head_length" in params:
                    head_length = params["head_length"]
                else:
                    head_length = 0.4
                if "overhang" in params:
                    overhang = params["overhang"]
                else:
                    overhang = 0.25
                pyplot.arrow(0.5 - 0.5 * cos(x), 0.5 - 0.5 * sin(x), 1.0 * cos(x), 1.0 * sin(x), width=width,
                             head_width=head_width, head_length=head_length, overhang=overhang,
                             length_includes_head=True, color=color, linestyle=linestyle)
                pyplot.axis('off')
                figure.savefig(save_path, dpi=dpi, transparent=True)
                pyplot.close()
            else:
                raise ValueError("The scope of \"degree\" is [0, 360].")
        else:
            raise ValueError("\"degree\" is a parameter that \"arrow\" must specify.")

    elif widget_type == "rotation":
        # use style 1.
        if "turn" in params and "degree" in params:
            if params["turn"] in ["right", "left"] and 0 <= params["degree"] <= 180:
                major_axis, minor_axis = 1.8, 0.6
                if params["turn"] == "right":
                    x_values = cos(deg2rad(linspace(-90, 270, 361)[::-1])) * major_axis / 2.0
                    y_values = sin(deg2rad(linspace(-90, 270, 361)[::-1])) * minor_axis / 2.0
                else:
                    x_values = cos(deg2rad(linspace(-90, 270, 361))) * major_axis / 2.0
                    y_values = sin(deg2rad(linspace(-90, 270, 361))) * minor_axis / 2.0

                pyplot.figure(figsize=(2, 2))
                ax = pyplot.subplot(1, 1, 1)
                pyplot.vlines(0, -0.6, -1, color="k", lw=3, zorder=0)
                # noinspection PyUnresolvedReferences
                ax.add_patch(patches.Ellipse(xy=(0.0, 0.0), width=major_axis, height=minor_axis, fc="silver"))
                pyplot.vlines(0, 0, +1, color="k", lw=3, zorder=2)
                if params["turn"] == "right":
                    pyplot.fill_between([0.0, +0.3], [-0.45, -0.3], [-0.15, -0.3], color="k", zorder=3)
                else:
                    pyplot.fill_between([-0.3, 0.0], [-0.3, -0.45], [-0.3, -0.15], color="k", zorder=3)

                if params["degree"] != 180:
                    pyplot.plot([0, x_values[params["degree"] + 1]], [0, y_values[params["degree"] + 1]],
                                color="k", lw=2, ls=":", zorder=4)
                pyplot.scatter([0, x_values[params["degree"] + 1]], [0, y_values[params["degree"] + 1]],
                               marker="o", s=40, color="k", zorder=4)
                pyplot.plot(x_values[:params["degree"] + 1], y_values[:params["degree"] + 1], color="k", lw=3, zorder=4)

                pyplot.xlim(-1, +1)
                pyplot.ylim(-1, +1)
                pyplot.axis("off")

                pyplot.savefig(save_path, transparent=True, pad_inches=0, bbox_inches="tight", dpi=1200)
                pyplot.close()

            else:
                raise ValueError("The scope of \"turn\" is \"right\" or \"left\" and that of \"degree\" is [0, 360].")

        # use style 2.
        elif "elevation" in params and "azimuth" in params:
            if -180 <= params["elevation"] <= 180 and -180 <= params["azimuth"] <= 180:
                if params["elevation"] == 0 and params["azimuth"] == 0:
                    raise ValueError("\"elevation\" and \"azimuth\" cannot be both 0.")

                major_axis, minor_axis = 1.2, 1.2 / sqrt(3)
                x_values_1 = cos(deg2rad(linspace(0, 360, 361))) * major_axis / 2.0
                y_values_1 = sin(deg2rad(linspace(0, 360, 361))) * minor_axis / 2.0
                x_values_2 = cos(deg2rad(linspace(-90, 270, 361))) * minor_axis / 2.0
                y_values_2 = sin(deg2rad(linspace(-90, 270, 361))) * major_axis / 2.0
                x_values_3 = cos(deg2rad(linspace(0, 360, 361))) * major_axis / 2.0
                y_values_3 = sin(deg2rad(linspace(0, 360, 361))) * major_axis / 2.0

                # elevation angle in the z plane.
                elevation_x_values = cos(deg2rad(linspace(-150, 210, 361)[::-1])) * minor_axis / 2.0
                elevation_y_values = sin(deg2rad(linspace(-150, 210, 361)[::-1])) * major_axis / 2.0
                line_info, area_info, last_x, last_y = [], None, None, None
                if 0 < params["elevation"] <= 90:
                    addition = int(params["elevation"] / 3 * 4)
                    x, y = elevation_x_values[:addition], elevation_y_values[:addition]
                    line_info.append((x, y, "-"))
                    last_x, last_y = x[-1], y[-1]
                    upper = []
                    for x_value, y_value in zip(x, y):
                        upper.append(x_value if x_value <= 0 else x_value / last_x * last_y)
                    area_info = (array(x.tolist() + [0]), array(y.tolist() + [0]), array(upper + [0]))
                    elevation_data = line_info, area_info, last_x, last_y
                elif params["elevation"] > 90:
                    x_1, y_1 = elevation_x_values[:120], elevation_y_values[:120]
                    addition = int((params["elevation"] - 90) / 3 * 2)
                    x_2, y_2 = elevation_x_values[120:120 + addition], elevation_y_values[120:120 + addition]
                    line_info.append((x_1, y_1, "-"))
                    line_info.append((x_2, y_2, ":"))
                    last_x, last_y = x_2[-1], y_2[-1]
                    area_info = [[], [], []]
                    for x_value, y_value in zip(x_1, y_1):
                        area_info[0].append(x_value)
                        area_info[1].append(x_value)
                        area_info[2].append(y_value)
                    for index in range(addition):
                        area_info[0].append(x_2[index])
                        area_info[1].append(x_2[index] / last_x * last_y)
                        area_info[2].append(y_2[index])
                    area_info = (array(area_info[0]), array(area_info[1]), array(area_info[2]))
                    elevation_data = line_info, area_info, last_x, last_y
                elif -90 < params["elevation"] < 0:
                    addition = int((90 + params["elevation"]) / 3 * 2)
                    x, y = elevation_x_values[300 + addition:], elevation_y_values[300 + addition:]
                    line_info.append((x, y, "-"))
                    last_x, last_y = x[0], y[0]
                    upper = []
                    for x_value, y_value in zip(x, y):
                        upper.append(x_value / last_x * last_y)
                    area_info = (array(x.tolist() + [0]), array(y.tolist() + [0]), array(upper + [0]))
                    elevation_data = line_info, area_info, last_x, last_y
                elif -90 == params["elevation"]:
                    addition = int((90 + params["elevation"]) / 3 * 2)
                    x, y = elevation_x_values[300 + addition:], elevation_y_values[300 + addition:]
                    line_info.append((x, y, "-"))
                    last_x, last_y = x[0], y[0]
                    upper = []
                    for x_value, y_value in zip(x, y):
                        upper.append(x_value)
                    area_info = (x, y, upper)
                    elevation_data = line_info, area_info, last_x, last_y
                elif -90 > params["elevation"]:
                    x_1, y_1 = elevation_x_values[300:], elevation_y_values[300:]
                    addition = int((-params["elevation"] - 90) / 3 * 4)
                    x_2, y_2 = elevation_x_values[300 - addition:300], elevation_y_values[300 - addition:300]
                    line_info.append((x_1, y_1, "-"))
                    line_info.append((x_2, y_2, ":"))
                    last_x, last_y = x_2[0], y_2[0]
                    area_info = [[], [], []]
                    for x_value, y_value in zip(x_1, y_1):
                        area_info[0].append(x_value)
                        area_info[1].append(x_value)
                        area_info[2].append(y_value)
                    for x_value, y_value in zip(x_2[::-1], y_2[::-1]):
                        area_info[0].append(x_value)
                        area_info[1].append(y_value)
                        area_info[2].append(x_value / last_x * last_y)
                    elevation_data = line_info, area_info, last_x, last_y
                else:
                    elevation_data = None

                # azimuth angle for the x,y plane.
                azimuth_x_values = cos(deg2rad(linspace(-120, 240, 361))) * major_axis / 2.0
                azimuth_y_values = sin(deg2rad(linspace(-120, 240, 361))) * minor_axis / 2.0
                line_info, area_info, last_x, last_y = [], None, None, None
                if 0 < params["azimuth"] <= 90:
                    addition = int(params["azimuth"] / 3 * 4)
                    x, y = azimuth_x_values[:addition], azimuth_y_values[:addition]
                    line_info.append((x, y, "-"))
                    last_x, last_y = x[-1], y[-1]
                    upper = []
                    for x_value, y_value in zip(x, y):
                        upper.append(x_value if x_value <= 0 else x_value / last_x * last_y)
                    area_info = (x, y, array(upper))
                    azimuth_data = line_info, area_info, last_x, last_y
                elif params["azimuth"] > 90:
                    x_1, y_1 = azimuth_x_values[:120], azimuth_y_values[:120]
                    addition = int((params["azimuth"] - 90) / 3 * 2)
                    x_2, y_2 = azimuth_x_values[120:120 + addition], azimuth_y_values[120:120 + addition]
                    line_info.append((x_1, y_1, "-"))
                    line_info.append((x_2, y_2, ":"))
                    last_x, last_y = x_2[-1], y_2[-1]
                    area_info = [[], [], []]
                    for index, (x_value, y_value) in enumerate(zip(x_1, y_1)):
                        if index < 120 - addition:
                            upper_value = x_value if x_value < 0 else x_value / last_x * last_y
                        else:
                            upper_value = y_2[::-1][index - 120 + addition]
                        area_info[0].append(x_value)
                        area_info[1].append(y_value)
                        area_info[2].append(upper_value)
                    area_info = (array(area_info[0]), array(area_info[1]), array(area_info[2]))
                    azimuth_data = line_info, area_info, last_x, last_y
                elif -90 <= params["azimuth"] < 0:
                    addition = int((90 + params["azimuth"]) / 3 * 2)
                    x, y = azimuth_x_values[300 + addition:], azimuth_y_values[300 + addition:]
                    line_info.append((x, y, "-"))
                    last_x, last_y = x[0], y[0]
                    upper = []
                    for x_value, y_value in zip(x, y):
                        upper.append(x_value / last_x * last_y)
                    area_info = (array(x.tolist() + [0]), array(y.tolist() + [0]), array(upper + [0]))
                    azimuth_data = line_info, area_info, last_x, last_y
                elif -90 > params["azimuth"]:
                    x_1, y_1 = azimuth_x_values[300:], azimuth_y_values[300:]
                    addition = int((-params["azimuth"] - 90) / 3 * 4)
                    x_2, y_2 = azimuth_x_values[300 - addition:300], azimuth_y_values[300 - addition:300]
                    line_info.append((x_1, y_1, "-"))
                    line_info.append((x_2, y_2, ":"))
                    last_x, last_y = x_2[0], y_2[0]
                    area_info = [[], [], []]
                    for index in range(min(60, addition)):
                        area_info[0].append(x_1[index])
                        area_info[1].append(y_1[index])
                        area_info[2].append(y_2[::-1][index])
                    if addition > 60:
                        for index in range(60, addition):
                            area_info[0].append(x_2[::-1][index])
                            area_info[1].append(x_2[::-1][index] / last_x * last_y)
                            area_info[2].append(y_2[::-1][index])
                    else:
                        for index in range(addition, 60):
                            area_info[0].append(x_1[index])
                            area_info[1].append(y_1[index])
                            area_info[2].append(x_1[index] / last_x * last_y)
                        area_info[0].append(0)
                        area_info[1].append(0)
                        area_info[2].append(0)
                    azimuth_data = line_info, area_info, last_x, last_y
                else:
                    azimuth_data = None

                pyplot.figure(figsize=(2, 2))
                pyplot.plot(x_values_1[:180], y_values_1[:180], color="grey", lw=1, ls=":", zorder=0)
                pyplot.plot(x_values_1[180:], y_values_1[180:], color="grey", lw=1, zorder=0)
                pyplot.plot(x_values_2[:180], y_values_2[:180], color="grey", lw=1, ls=":", zorder=0)
                pyplot.plot(x_values_2[180:], y_values_2[180:], color="grey", lw=1, zorder=0)
                pyplot.plot(x_values_3, y_values_3, color="grey", lw=1, zorder=0)

                if elevation_data is not None:
                    line_info, area_info, last_x, last_y = elevation_data
                    if area_info is not None:
                        if params["elevation"] < 0:
                            pyplot.fill_between(area_info[0], area_info[1], area_info[2],
                                                fc="royalblue", lw=0, alpha=0.5, zorder=2)
                        else:
                            pyplot.fill_between(area_info[0], area_info[1], area_info[2],
                                                fc="royalblue", lw=0, alpha=0.5, zorder=4)
                    for x, y, style in line_info:
                        pyplot.plot(x, y, color="k", lw=3, ls=style, zorder=5)
                    if params["elevation"] > 0:
                        pyplot.fill_between([-0.15, 0, +0.15], [-1, -1, -1], [-1, -0.7, -1], color="k", lw=0, zorder=6)
                    elif params["elevation"] < 0:
                        pyplot.fill_between([-0.15, 0, +0.15], [+1, +1, +1], [+1, 0.7, +1], color="k", lw=0, zorder=6)

                if azimuth_data is not None:
                    line_info, area_info, last_x, last_y = azimuth_data
                    if area_info is not None:
                        pyplot.fill_between(area_info[0], area_info[1], area_info[2],
                                            fc="chocolate", lw=0, alpha=0.5, zorder=3)
                    for x, y, style in line_info:
                        pyplot.plot(x, y, color="k", lw=3, ls=style, zorder=5)

                    if params["azimuth"] > 0:
                        pyplot.fill_between([0.7, 1.0], [0, -0.15], [0, +0.15], color="k", lw=0, zorder=6)
                    elif params["azimuth"] < 0:
                        pyplot.fill_between([-1, -0.7], [-0.15, 0], [+0.15, 0], color="k", lw=0, zorder=6)

                pyplot.xlim(-1, +1)
                pyplot.ylim(-1, +1)
                pyplot.axis("off")

                pyplot.savefig(save_path, transparent=True, pad_inches=0, bbox_inches="tight", dpi=1200)
                pyplot.close()

            else:
                raise ValueError("The scope of \"elevation\" and \"azimuth\" is [-180, +180].")

        else:
            raise ValueError("No such rotation type! "
                             + "You can input \"turn\" and \"degree\" for style 1, "
                             + "or input \"elevation\" and \"azimuth\" for style 2.")

    else:
        raise ValueError("No such widget type (\"arrow\" and \"rotation\" only).")


class DefaultStructureImage:

    def __init__(self, structure_paths: list):
        self._mol = PyMOL()
        self._mol.start()
        self.__structure_names = []
        for structure_path in structure_paths:
            self._mol.cmd.load(structure_path, quiet=1)
            self.__structure_names.append(structure_path[structure_path.rindex("/") + 1: structure_path.rindex(".")])
        self._mol.cmd.ray(quiet=1)  # make PyMOL run silently.

    def set_cache(self, cache_contents: list):
        """
        Set cache contents of the structure.

        :param cache_contents: hidden contents.
        :type cache_contents: list
        """
        for hidden_information in cache_contents:
            if ":" in hidden_information:
                shading_type, target_information = hidden_information.split(":")
                if shading_type == "atom":
                    for target in target_information.split(","):
                        if "+" in target:
                            if target.count("+") > 1:
                                selected_model, selected_chain, selected_atom = target.split("+")
                                selection_command = "(m. " + selected_model + " and c. " + selected_chain
                                selection_command = selection_command + " and e. " + selected_atom + ")"
                            else:
                                selected_chain, selected_atom = target.split("+")
                                selection_command = "(c. " + selected_chain + " and e. " + selected_atom + ")"
                        else:
                            selection_command = "(e. " + target + ")"
                        self._mol.cmd.hide(selection=selection_command)

                elif shading_type == "position":
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
                        self._mol.cmd.hide(selection=selection_command)

                elif shading_type == "range":
                    for target in target_information.split(","):
                        if "+" in target:
                            if target.count("+") > 1:
                                selected_model, selected_chain, selected_range = target.split("+")
                                if "-" in selected_range and selected_range.count("-") == 1:
                                    former, latter = selected_range.split("-")
                                    if int(former) < int(latter):
                                        selection_command = "(m. " + selected_model + " and c. " + selected_chain
                                        selection_command = selection_command + " and i. " + selected_range + ")"
                                    else:
                                        raise ValueError("The former position needs to be less than the latter position"
                                                         + " in the Range (" + selected_range + ").")
                                else:
                                    raise ValueError("Range (" + selected_range + ") needs to "
                                                     + "meet the \"number-number\" format!")
                            else:
                                selected_chain, selected_range = target.split("+")
                                if "-" in selected_range and selected_range.count("-") == 1:
                                    former, latter = selected_range.split("-")
                                    if int(former) < int(latter):
                                        selection_command = "(c. " + selected_chain + " and i. " + selected_range + ")"
                                    else:
                                        raise ValueError("The former position needs to be less than the latter position"
                                                         + " in the Range (" + selected_range + ").")
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
                        self._mol.cmd.hide(selection=selection_command)

                elif shading_type == "residue":
                    for target in target_information.split(","):
                        if "+" in target:
                            if target.count("+") > 1:
                                selected_model, selected_chain, selected_residue = target.split("+")
                                selection_command = "(m. " + selected_model + " and c. " + selected_chain
                                selection_command = selection_command + " and r. " + selected_residue + ")"
                            else:
                                selected_chain, selected_residue = target.split("+")
                                selection_command = "(c. " + selected_chain + " and r. " + selected_residue + ")"
                        else:
                            selection_command = "(r. " + target + ")"
                        self._mol.cmd.hide(selection=selection_command)

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
                        self._mol.cmd.hide(selection=selection_command)

                elif shading_type == "chain":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_model, selected_chain = target.split("+")
                            selection_command = "(m. " + selected_model + " and c. " \
                                                + selected_chain + " and (not hetatm))"
                        else:
                            selection_command = "(c. " + target + " and (not hetatm))"
                        self._mol.cmd.hide(selection=selection_command)

                elif shading_type == "model":
                    for target in target_information.split(","):
                        selection_command = "(m. " + target + ")"
                        self._mol.cmd.hide(selection=selection_command)

                else:
                    raise ValueError("No such shading type! We only support "
                                     + "\"position\", \"range\", \"residue\", \"segment\", \"chain\" and \"model\".")
            else:
                raise ValueError("No such representing information! We only support one type of information, i.e. "
                                 + "\"shading type:target,target,...,target\"")

    def set_zoom(self, zoom_contents: list, buffer: float = 0.0):
        """
        Set zoom contents of the structure.

        :param zoom_contents: structure content that needs to be zoomed.
        :type zoom_contents: list

        :param buffer: the buffer area size of the target structure.
        :type buffer: float
        """
        for zoom_information in zoom_contents:
            if ":" in zoom_information:
                shading_type, target_information = zoom_information.split(":")
                if shading_type == "atom":
                    for target in target_information.split(","):
                        if "+" in target:
                            if target.count("+") > 1:
                                selected_model, selected_chain, selected_atom = target.split("+")
                                selection_command = "(m. " + selected_model + " and c. " + selected_chain
                                selection_command = selection_command + " and e. " + selected_atom + ")"
                            else:
                                selected_chain, selected_atom = target.split("+")
                                selection_command = "(c. " + selected_chain + " and e. " + selected_atom + ")"
                        else:
                            selection_command = "(e. " + target + ")"
                        self._mol.cmd.zoom(selection=selection_command, buffer=buffer)

                elif shading_type == "position":
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
                        self._mol.cmd.zoom(selection=selection_command, buffer=buffer)

                elif shading_type == "range":
                    for target in target_information.split(","):
                        if "+" in target:
                            if target.count("+") > 1:
                                selected_model, selected_chain, selected_range = target.split("+")
                                if "-" in selected_range and selected_range.count("-") == 1:
                                    former, latter = selected_range.split("-")
                                    if int(former) < int(latter):
                                        selection_command = "(m. " + selected_model + " and c. " + selected_chain
                                        selection_command = selection_command + " and i. " + selected_range + ")"
                                    else:
                                        raise ValueError("The former position needs to be less than the latter position"
                                                         + " in the Range (" + selected_range + ").")
                                else:
                                    raise ValueError("Range (" + selected_range + ") needs to "
                                                     + "meet the \"number-number\" format!")
                            else:
                                selected_chain, selected_range = target.split("+")
                                if "-" in selected_range and selected_range.count("-") == 1:
                                    former, latter = selected_range.split("-")
                                    if int(former) < int(latter):
                                        selection_command = "(c. " + selected_chain + " and i. " + selected_range + ")"
                                    else:
                                        raise ValueError("The former position needs to be less than the latter position"
                                                         + " in the Range (" + selected_range + ").")
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
                        self._mol.cmd.zoom(selection=selection_command, buffer=buffer)

                elif shading_type == "residue":
                    for target in target_information.split(","):
                        if "+" in target:
                            if target.count("+") > 1:
                                selected_model, selected_chain, selected_residue = target.split("+")
                                selection_command = "(m. " + selected_model + " and c. " + selected_chain
                                selection_command = selection_command + " and r. " + selected_residue + ")"
                            else:
                                selected_chain, selected_residue = target.split("+")
                                selection_command = "(c. " + selected_chain + " and r. " + selected_residue + ")"
                        else:
                            selection_command = "(r. " + target + ")"
                        self._mol.cmd.zoom(selection=selection_command, buffer=buffer)

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
                        self._mol.cmd.zoom(selection=selection_command, buffer=buffer)

                elif shading_type == "chain":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_model, selected_chain = target.split("+")
                            selection_command = "(m. " + selected_model + " and c. " + selected_chain + ")"
                        else:
                            selection_command = "(c. " + target + ")"
                        self._mol.cmd.zoom(selection=selection_command, buffer=buffer)

                elif shading_type == "model":
                    for target in target_information.split(","):
                        selection_command = "(m. " + target + ")"
                        self._mol.cmd.zoom(selection=selection_command, buffer=buffer)

                else:
                    raise ValueError("No such shading type! We only support "
                                     + "\"position\", \"range\", \"residue\", \"segment\", \"chain\" and \"model\".")
            else:
                raise ValueError("No such representing information! We only support one type of information, i.e. "
                                 + "\"shading type:target,target,...,target\"")

    def set_state(self, translate: list = None, rotate: list = None, inner_align: bool = False, target: str = None,
                  mobile: str = None, only_rotate: bool = False):
        """
        Set the state of the structure.

        :param translate: translate distances with x/y/z-axis.
        :type translate: list or None

        :param rotate: rotate degree with x/y/z-axis.
        :type rotate: list or None

        :param inner_align: align multiple structures through built-in interfaces (cmd.align).
        :type inner_align: bool

        :param target: the target (or template) name can be specified if the inner align is executed.
        :type target: str or None

        :param mobile: the mobile name can be specified if the inner align is executed.
        :type mobile: str or None

        :param only_rotate: only rotation, no initialization.
        :type only_rotate: bool
        """
        if inner_align and len(self.__structure_names) > 1:
            if target is not None:
                if mobile is not None:
                    self._mol.cmd.align(mobile, target)
                else:
                    for mobile in self.__structure_names:
                        if mobile != target:
                            self._mol.cmd.align(mobile, target)
            else:
                target = self.__structure_names[0]
                for mobile in self.__structure_names[1:]:
                    self._mol.cmd.align(mobile, target)

        if only_rotate:
            self._mol.cmd.rotate(axis="x", angle=rotate[0])
            self._mol.cmd.rotate(axis="y", angle=rotate[1])
            self._mol.cmd.rotate(axis="z", angle=rotate[2])

        else:
            if translate is not None:
                self._mol.cmd.translate(vector=translate)
            else:
                self._mol.cmd.center()

            self._mol.cmd.orient()

            self._mol.cmd.zoom(complete=1)

            if rotate is not None:
                self._mol.cmd.rotate(axis="x", angle=rotate[0])
                self._mol.cmd.rotate(axis="y", angle=rotate[1])
                self._mol.cmd.rotate(axis="z", angle=rotate[2])

    def set_shape(self, representation_plan: list, initial_representation: str = "cartoon",
                  independent_color: bool = False, closed_surface: bool = False):
        """
        Set the shape (or representation in PyMOL) of the structure.

        :param representation_plan: the type of the visual structure.
        :type representation_plan: list

        :param initial_representation: if representation type is index, can optionally operate on the specified chain.
        :type initial_representation: str

        :param independent_color: if independent_color is False, colors can leak into the open surface edge.
        :type independent_color: bool

        :param closed_surface: if closed_surface is True, create a closed surface.
        :type closed_surface: bool
        """
        if initial_representation is not None:
            self._mol.cmd.show(representation=initial_representation, selection="(all)")

        if independent_color:
            self._mol.cmd.set(name="surface_proximity", value="off")

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
                        if representation == "surface" and closed_surface:
                            self._mol.cmd.create("new_entity", selection_command)
                            self._mol.cmd.show(representation=representation, selection="new_entity")
                        else:
                            self._mol.cmd.show(representation=representation, selection=selection_command)

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
                        if representation == "surface" and closed_surface:
                            self._mol.cmd.create("new_entity", selection_command)
                            self._mol.cmd.show(representation=representation, selection="new_entity")
                        else:
                            self._mol.cmd.show(representation=representation, selection=selection_command)

                elif shading_type == "residue":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_residue = target.split("+")
                            selection_command = "(c. " + selected_chain + " and r. " + selected_residue + ")"
                        else:
                            selection_command = "(r. " + target + ")"
                        if representation == "surface" and closed_surface:
                            self._mol.cmd.create("new_entity", selection_command)
                            self._mol.cmd.show(representation=representation, selection="new_entity")
                        else:
                            self._mol.cmd.show(representation=representation, selection=selection_command)

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
                        if representation == "surface" and closed_surface:
                            self._mol.cmd.create("new_entity", selection_command)
                            self._mol.cmd.show(representation=representation, selection="new_entity")
                        else:
                            self._mol.cmd.show(representation=representation, selection=selection_command)

                elif shading_type == "chain":
                    for target in target_information.split(","):
                        if representation == "surface" and closed_surface:
                            self._mol.cmd.create("new_entity", "(c. " + target + ")")
                            self._mol.cmd.show(representation=representation, selection="new_entity")
                        else:
                            self._mol.cmd.show(representation=representation, selection="(c. " + target + ")")

                elif shading_type == "model":
                    for target in target_information.split(","):
                        self._mol.cmd.show(representation=representation, selection="(m. " + target + ")")

                else:
                    raise ValueError("No such shading type! We only support "
                                     + "\"position\", \"range\", \"residue\", \"segment\", \"chain\" and \"model\".")

            elif representing_information == "all":
                self._mol.cmd.show(representation=representation, selection="(all)")

            else:
                raise ValueError("No such representing information! We only support two types of information: "
                                 + "(1) \"all\"; and (2) \"shading type:target,target,...,target\"")

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
        self._mol.cmd.png(filename=save_path, width=width, height=width * ratio, dpi=dpi, quiet=1)

    def save_pymol(self, save_path: str):
        """
        Save the PyMOL state.

        :param save_path: path to save file.
        :type save_path: str
        """
        self._mol.cmd.save(filename=save_path)

    def load_pymol(self, load_path: str):
        """
        Load the PyMOL state.

        :param load_path: path to save file.
        :type load_path: str
        """
        self.clear()
        self._mol.cmd.load(filename=load_path)

    def clear(self):
        """
        Clear the PyMOL.
        """
        self._mol.cmd.delete("all")

    def close(self):
        """
        Close the PyMOL.
        """
        self._mol.stop()


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
        if initial_color is not None:
            self._mol.cmd.color(color=initial_color, selection="(all)")

        for step, (coloring_information, color) in enumerate(coloring_plan):
            if type(coloring_information) is not str:
                raise ValueError("The format of coloring information at step " + str(step + 1) + " is illegal! "
                                 + "We only support \"str\" format!")

            if ":" in coloring_information:
                shading_type, target_information = coloring_information.split(":")
                if shading_type == "atom":
                    for target in target_information.split(","):
                        if "+" in target:
                            if target.count("+") > 1:
                                selected_model, selected_chain, selected_atom = target.split("+")
                                selection_command = "(m. " + selected_model + " and c. " + selected_chain
                                selection_command = selection_command + " and e. " + selected_atom + ")"
                            else:
                                selected_chain, selected_atom = target.split("+")
                                selection_command = "(c. " + selected_chain + " and e. " + selected_atom + ")"
                        else:
                            selection_command = "(e. " + target + ")"
                        self._mol.cmd.color(color=color, selection=selection_command)

                elif shading_type == "position":
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
                        self._mol.cmd.color(color=color, selection=selection_command)

                elif shading_type == "range":
                    for target in target_information.split(","):
                        if "+" in target:
                            if target.count("+") > 1:
                                selected_model, selected_chain, selected_range = target.split("+")
                                if "-" in selected_range and selected_range.count("-") == 1:
                                    former, latter = selected_range.split("-")
                                    if int(former) < int(latter):
                                        selection_command = "(m. " + selected_model + " and c. " + selected_chain
                                        selection_command = selection_command + " and i. " + selected_range + ")"
                                    else:
                                        raise ValueError(
                                            "The former position needs to be less than the latter position "
                                            + "in the Range (" + selected_range + ").")
                                else:
                                    raise ValueError("Range (" + selected_range + ") needs to "
                                                     + "meet the \"number-number\" format!")
                            else:
                                selected_chain, selected_range = target.split("+")
                                if "-" in selected_range and selected_range.count("-") == 1:
                                    former, latter = selected_range.split("-")
                                    if int(former) < int(latter):
                                        selection_command = "(c. " + selected_chain + " and i. " + selected_range + ")"
                                    else:
                                        raise ValueError("The former position needs to be less than the latter position"
                                                         + " in the Range (" + selected_range + ").")
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
                        self._mol.cmd.color(color=color, selection=selection_command)

                elif shading_type == "residue":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_chain, selected_residue = target.split("+")
                            selection_command = "(c. " + selected_chain + " and r. " + selected_residue + ")"
                        else:
                            selection_command = "(r. " + target + ")"
                        self._mol.cmd.color(color=color, selection=selection_command)

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
                        self._mol.cmd.color(color=color, selection=selection_command)

                elif shading_type == "chain":
                    for target in target_information.split(","):
                        if "+" in target:
                            selected_model, selected_chain = target.split("+")
                            selection_command = "(m. " + selected_model + " and c. " + selected_chain + ")"
                        else:
                            selection_command = "(c. " + target + ")"
                        self._mol.cmd.color(color=color, selection=selection_command)

                elif shading_type == "model":
                    for target in target_information.split(","):
                        self._mol.cmd.color(color=color, selection="(m. " + target + ")")

                else:
                    raise ValueError("No such shading type! We only support "
                                     + "\"position\", \"range\", \"residue\", \"segment\", \"chain\" and \"model\".")

            elif coloring_information == "all":
                self._mol.cmd.color(color=color, selection="(all)")

            else:
                raise ValueError("No such coloring information! We only support two types of information: "
                                 + "(1) \"all\"; and (2) \"shading type:target,target,...,target\"")

        if edge_color is not None:
            self._mol.cmd.set(name="ray_trace_color", value=edge_color)
            self._mol.cmd.set(name="ray_trace_mode", value=1)


class PropertyStructureImage(DefaultStructureImage):

    def set_color(self, target: str, properties: list = None,
                  color_map: str = "rainbow", initial_color: str = "0xAAAAAA", edge_color: str = None,
                  gauge_strengthen: bool = False):
        """
        Set colors for the structure with its element properties.

        :param target: coloring target select, including "range", "segment", "chain" and "model".
        :type target: str

        :param properties: element properties of the structure.
        :type properties: list or None

        :param color_map: coloring palette.
        :type color_map: str

        :param initial_color: initial color in the structure.
        :type initial_color: str

        :param edge_color: edge color of the structure if required.
        :type edge_color: str or None

        :param gauge_strengthen: strengthen property differences through gauge changes (available in "cartoon").
        :type gauge_strengthen: bool
        """
        self._mol.cmd.color(color=initial_color, selection="(all)")

        shading_type, target_information = target.split(":")
        if shading_type == "range":
            if "+" in target_information:
                selected_model, selected_range = target_information.split("+")
                selection_command = "(m. " + selected_model + " and i. " + selected_range + ")"
            else:
                selection_command = "(i. " + target_information + ")"
        elif shading_type == "segment":
            if "+" in target_information:
                selected_model, selected_segment = target_information.split("+")
                selection_command = "(m. " + selected_model + " and ps. " + selected_segment + ")"
            else:
                selection_command = "(ps. " + target_information + ")"
        elif shading_type == "chain":
            if "+" in target_information:
                selected_model, selected_chain = target_information.split("+")
                selection_command = "(m. " + selected_model + " and c. " + selected_chain + ")"
            else:
                selection_command = "(c. " + target_information + ")"
        elif shading_type == "model":
            selection_command = "(m. " + target_information + ")"
        else:
            raise ValueError("No such shading type! We only support "
                             + "\"range\", \"segment\", \"chain\" and \"model\".")

        if properties is None:
            self._mol.cmd.spectrum(expression="count", palette=color_map, selection=selection_command, byres=0)
        else:
            if len(properties) == self._mol.cmd.count_atoms(selection_command):
                self._mol.stored.properties = properties
                self._mol.cmd.alter(selection_command, "b=stored.properties.pop(0)")
                self._mol.cmd.spectrum(expression="b", palette=color_map, selection=selection_command, byres=0)
            else:
                raise ValueError("We need one-to-one atomic properties.")

        if gauge_strengthen and properties is not None:
            self._mol.cmd.show(representation="cartoon", selection=selection_command)
            self._mol.cmd.cartoon("putty")
            self._mol.cmd.set(name="cartoon_putty_transform", value=7)

        if edge_color is not None:
            self._mol.cmd.set(name="ray_trace_color", value=edge_color)
            self._mol.cmd.set(name="ray_trace_mode", value=1)


class Figure:

    def __init__(self, manuscript_format: str = "Nature", column_format: int = None, occupied_columns: int = 1,
                 aspect_ratio: tuple = (1, 2), row_number: int = 1, column_number: int = 1, interval: tuple = (0, 0),
                 dpi: int = None, mathtext: bool = True):
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

        :param dpi: customized dpi from user (users to improve figure clarity).
        :type dpi: int or None

        :param mathtext: use mathtext if required.
        :type mathtext: bool
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
                self.fig = pyplot.figure(figsize=(3.42, 3.42 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                self.fig = pyplot.figure(figsize=(7.00, 7.00 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("PNAS's standard figures allow 1 and 2 column(s).")

            self.minimum_dpi = 600
            rcParams["font.family"] = "sans-serif"
            rcParams["font.sans-serif"] = "Helvetica"

        elif manuscript_format == "ACS":
            if occupied_columns == 1:
                self.fig = pyplot.figure(figsize=(3.25, 3.25 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                self.fig = pyplot.figure(figsize=(7.00, 7.00 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("ACS standard figures allow 1 and 2 column(s).")

            self.minimum_dpi = 600
            rcParams["font.family"] = "Arial"

        elif manuscript_format == "Oxford":
            if occupied_columns == 1:
                self.fig = pyplot.figure(figsize=(3.39, 3.39 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                self.fig = pyplot.figure(figsize=(7.00, 7.00 / aspect_ratio[1] * aspect_ratio[0]))
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
                self.fig = pyplot.figure(figsize=(7.25, 7.25 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("IEEE standard figures allow 1 and 2 column(s).")

            self.minimum_dpi = 300
            rcParams["font.family"] = "Times New Roman"

        if mathtext:
            rcParams["mathtext.default"] = "regular"
        else:
            rcParams["mathtext.fontset"] = "custom"
            rcParams["mathtext.rm"] = "Linux Libertine"
            rcParams["mathtext.cal"] = "Lucida Calligraphy"
            rcParams["mathtext.bf"] = "Linux Libertine:bold"
            rcParams["mathtext.it"] = "Linux Libertine:italic"

        if dpi is not None and dpi >= self.minimum_dpi:
            self.minimum_dpi = dpi

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
                  image_format: str = ".png", locations: list = None, layout: tuple = None, zorder: int = None,
                  frame_off: bool = True, backgroundcolor: str = "#FFFFFF", positions: tuple = None,
                  linewidth: float = 1.0, transparent: bool = False, linecolor: str = "#000000"):
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

        :param frame_off: draw frame for the image, no frame by default.
        :type frame_off: bool

        :param backgroundcolor: the background color for image panel.
        :type backgroundcolor: str

        :param positions: set the position of the image in the panel.
        :type positions: tuple or None

        :param linewidth: the width of the frame.
        :type linewidth: float

        :param transparent: set a transparent background.
        :type transparent: bool

        :param linecolor: the color of the frame.
        :type linecolor: str
        """
        if image_path is not None and (widget_type is not None or widget_attributes is not None):
            raise ValueError("We can't choose between \'image_path\' and \'widget_type|widget_attributes\'!")

        if image_path is None and (widget_type is not None and widget_attributes is not None):
            root_path = path.abspath(__file__).replace("\\", "/")[:-17] + "docs/source/_static/widgets/"
            image_path = root_path + widget_type + "[" + widget_attributes.replace(", ", ".") + "]"
            image_path += image_format

        if image_path is None:
            raise ValueError("We need to input \'image_path\' or \'widget_type|widget_attributes\'!")

        image_format = image_path[image_path.rfind("."):].lower()

        if image_format == ".png":
            image_data = Image.open(fp=image_path)
            self.paste_bitmap(image=image_data, locations=locations, layout=layout, zorder=zorder, frame_off=frame_off,
                              backgroundcolor=backgroundcolor, positions=positions, linewidth=linewidth,
                              transparent=transparent, linecolor=linecolor)
        else:
            raise ValueError("Only PNG files are support!")

    def set_text(self, annotation: str, font_size: int = 16, alignment: str = "center", locations: list = None,
                 layout: tuple = None, zorder: int = None, weight: str = "normal", color: str = "#000000",
                 backgroundcolor: str = "#FFFFFF", positions: tuple = (0.0, 0.0), frame_off: bool = True,
                 transparent: bool = False):
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

        :param backgroundcolor: background color.
        :type backgroundcolor: str

        :param positions: set the position of the text in the panel.
        :type positions: tuple

        :param frame_off: draw frame for the text, no frame by default.
        :type frame_off: bool

        :param transparent: set a transparent background.
        :type transparent: bool
        """
        if locations is not None and layout is not None:
            raise ValueError("We can't choose between \'locations\' and \'layout\'!")

        if layout is not None and locations is None:
            locations = self.calculate_locations(layout=layout)

        if transparent:
            alpha = 0.01
        else:
            alpha = 0.5

        if locations is not None:
            ax = self.fig.add_axes(locations, facecolor=backgroundcolor)
            ax.patch.set_alpha(alpha)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            if frame_off:
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
                ax.spines['left'].set_visible(False)

            if zorder is not None:
                ax.text(positions[0], positions[1], annotation, fontsize=font_size, horizontalalignment=alignment,
                        weight=weight, color=color, zorder=zorder)
            else:
                ax.text(positions[0], positions[1], annotation, fontsize=font_size, horizontalalignment=alignment,
                        weight=weight, color=color)
        else:
            raise ValueError("We need to input \'locations\' or \'layout\'!")

    def paste_bitmap(self, image: PngImagePlugin.PngImageFile, locations: list = None, layout: tuple = None,
                     zorder: int = None, frame_off: bool = True, backgroundcolor: str = "#FFFFFF",
                     positions: tuple = None, linewidth: float = 1.0, transparent: bool = False,
                     linecolor: str = "#000000"):
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

        :param frame_off: draw frame for the image, no frame by default.
        :type frame_off: bool

        :param backgroundcolor: the background color for image panel.
        :type backgroundcolor: str

        :param positions: set the position of the image in the panel.
        :type positions: tuple or None

        :param linewidth: the width of the frame.
        :type linewidth: float

        :param transparent: set a transparent background.
        :type transparent: bool

        :param linecolor: the color of the frame.
        :type linecolor: str
        """
        if image.info["dpi"][0] < self.minimum_dpi:
            raise ValueError("The dpi of image is less than the minimum dpi requirement!")

        if locations is not None and layout is not None:
            raise ValueError("We can't choose between \'locations\' and \'layout\'!")

        if layout is not None and locations is None:
            locations = self.calculate_locations(layout=layout)

        if transparent:
            alpha = 0.01
        else:
            alpha = 0.5

        if locations is not None:
            ax = self.fig.add_axes(locations, facecolor=backgroundcolor)
            ax.patch.set_alpha(alpha)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            if positions is not None:
                ax.set_xlim(0, positions[0])
                ax.set_ylim(0, positions[1])
                extent = (positions[2], positions[3], positions[4], positions[5])
            else:
                extent = None
            if frame_off:
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
                ax.spines['left'].set_visible(False)
            else:
                ax.spines['top'].set_linewidth(linewidth)
                ax.spines['right'].set_linewidth(linewidth)
                ax.spines['bottom'].set_linewidth(linewidth)
                ax.spines['left'].set_linewidth(linewidth)
                ax.spines['top'].set_edgecolor(linecolor)
                ax.spines['right'].set_edgecolor(linecolor)
                ax.spines['bottom'].set_edgecolor(linecolor)
                ax.spines['left'].set_edgecolor(linecolor)

            if zorder is not None:
                ax.imshow(X=image, extent=extent, zorder=zorder)
            else:
                ax.imshow(X=image, extent=extent)
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
