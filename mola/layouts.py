from logging import getLogger, CRITICAL
from PIL import Image
from pymol2 import PyMOL
from matplotlib import pyplot, rcParams
from numpy import zeros, sum
from types import FunctionType
from warnings import filterwarnings

filterwarnings("ignore")
getLogger("matplotlib").setLevel(CRITICAL)


class StructureImage:

    def __init__(self):
        self.__mol = PyMOL()
        self.__mol.cmd.ray(quiet=1)  # make PyMOL run silently.

    def set_title(self, title: str):
        """
        Set title of structure image.

        :param title: title of structure.
        :type title: str
        """
        self.__mol.set_title(object="structure", state=1, text=title)

    def set_state(self, representation: str = "cartoon", hides: list = None):
        """
        Set the initial state of a structure.

        :param representation: representation type.
        :type representation: str

        :param hides: hided molecules.
        :type hides: list or None
        """
        if representation is None:
            representation = "cartoon"

        if representation is not "cartoon":
            self.__mol.cmd.hide(representation="cartoon")
            self.__mol.cmd.show(representation=representation)

        if hides is not None:
            for hide_selection in hides:
                self.__mol.cmd.hide(selection=hide_selection)

        self.__mol.cmd.orient()
        self.__mol.cmd.center()
        self.__mol.cmd.zoom(complete=1)

    def set_color(self, shading_type: str = None, colors: dict = None):
        """
        Set color for the structure.

        :param shading_type: type of color shading for the structure.
        :type shading_type: str or None

        :param colors: pair of the class and its corresponding color.
        :type colors: dict or None
        """
        if shading_type is None and colors is None:
            residue_colors = {"ALA": "0x8A685C", "ARG": "0x402F42", "ASN": "0x7fA9C2", "ASP": "0x632D3B",
                              "CYS": "0x7D779D", "GLN": "0x853D2F", "GLU": "0x88191F", "GLY": "0x945A4F",
                              "HIS": "0xA29DB3", "ILE": "0x645D87", "LEU": "0x82A293", "LYS": "0xA58121",
                              "MET": "0x6273A1", "PHE": "0xB33C24", "PRO": "0x73584D", "SER": "0x4F698A",
                              "THR": "0xB9B9BB", "TRP": "0x686C47", "TYR": "0x674E3A", "VAL": "0x9D491B",
                              "DA": "0xF2521B", "DC": "0x81CC28", "DG": "0x00AEF0", "DT": "0xFABC09", "DU": "0xFABC09"}

            for residue, color in residue_colors.items():
                self.__mol.cmd.color(color=color, selection="(r. " + residue + ")")

        elif shading_type is not None and colors is not None:
            if shading_type == "residue":
                for residue, color in colors.items():
                    self.__mol.cmd.color(color=color, selection="(r. " + residue + ")")

            elif shading_type == "segment":
                for segment, color in colors.items():
                    self.__mol.cmd.color(color=color, selection="(ps. " + segment + ")")

            elif shading_type == "all":
                self.__mol.cmd.color(color=list(colors.values())[0], selection="(all)")

            else:
                raise ValueError("No such shading type!")

        else:
            raise ValueError("We need \'shading_type\' and \'colors\'!")

    def clean_color(self, neglect_color: str = "0xFFFFCC"):
        """
        Clean color through neglecting.

        :param neglect_color: color to neglect.
        :type neglect_color: str
        """
        self.set_color(shading_type="all", colors={"all": neglect_color})

    def save(self, save_path: str, dpi: int = 600):
        """
        Save the structure image.

        :param save_path: path to save file.
        :type save_path: str

        :param dpi: dots per inch.
        :type dpi: int
        """
        assert save_path[-4:] == ".png"
        self.__mol.cmd.png(filename=save_path, dpi=dpi, quiet=1)


class Figure:

    def __init__(self, manuscript_format: str = "Nature", occupied_columns: int = 1, aspect_ratio: tuple = (1, 2),
                 row_number: int = 1, column_number: int = 1, interval: tuple = (0, 0)):
        """
        Initialize a manuscript figure.

        :param manuscript_format: format of the manuscript (or the publisher of the manuscript).
        :type manuscript_format: str

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
                pyplot.figure(figsize=(3.54, 3.54 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                pyplot.figure(figsize=(7.08, 7.08 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("Nature's standard figures allow single or double column.")

            rcParams["font.family"] = "Times New Roman"

        elif manuscript_format == "Science":
            if occupied_columns == 1:
                pyplot.figure(figsize=(2.24, 2.24 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                pyplot.figure(figsize=(4.76, 4.76 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 3:
                pyplot.figure(figsize=(7.24, 7.24 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("Science's standard figures allow 1 ~ 3 column(s).")

            rcParams["font.family"] = "sans-serif"
            rcParams["font.sans-serif"] = "Helvetica"

        elif manuscript_format == "ACS":
            if occupied_columns == 1:
                pyplot.figure(figsize=(3.30, 3.30 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                pyplot.figure(figsize=(7.00, 7.00 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("ACS standard figures allow single or double column.")

            rcParams["font.family"] = "Times New Roman"

        elif manuscript_format == "Oxford":
            if occupied_columns == 1:
                pyplot.figure(figsize=(3.35, 3.35 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                pyplot.figure(figsize=(6.70, 6.70 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("Oxford standard figures allow single or double column.")

            rcParams["font.family"] = "Arial"

        elif manuscript_format == "IEEE":
            if occupied_columns == 1:
                pyplot.figure(figsize=(3.50, 3.50 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                pyplot.figure(figsize=(7.16, 7.16 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("IEEE standard figures allow single or double column.")

            rcParams["font.family"] = "Times New Roman"

        elif manuscript_format == "ACM":
            if occupied_columns == 1:
                pyplot.figure(figsize=(2.50, 2.50 / aspect_ratio[1] * aspect_ratio[0]))
            elif occupied_columns == 2:
                pyplot.figure(figsize=(6.02, 6.02 / aspect_ratio[1] * aspect_ratio[0]))
            else:
                raise ValueError("ACM standard figures allow single or double column.")

            rcParams["font.family"] = "Linux Libertine"

        rcParams["mathtext.fontset"] = "custom"
        rcParams["mathtext.rm"] = "Linux Libertine"
        rcParams["mathtext.cal"] = "Lucida Calligraphy"
        rcParams["mathtext.it"] = "Linux Libertine:italic"
        rcParams["mathtext.bf"] = "Linux Libertine:bold"

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
        self.occupy_locations[grid_params["l"]: grid_params["l"] + grid_params["w"],
                              grid_params["t"]: grid_params["t"] + grid_params["h"]] = 1

    # noinspection PyMethodMayBeStatic
    def set_panel(self, function: FunctionType = None, function_params: dict = None, image_path: str = None):
        """
        Draw a panel in a specific location.

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

    # noinspection PyMethodMayBeStatic
    def set_structure_image(self, image_path: str, locations: tuple, size: tuple, zorder: int = None):
        """
        Put the structure image with a specific size in a specific position of a panel.

        :param image_path: path of structure image.
        :type image_path: str

        :param locations: location in the panel (x and y).
        :type locations: tuple

        :param size: display size of the structure image.
        :type size: tuple

        :param zorder: order in which components are superimposed on each other.
        :type zorder: int or None
        """
        image_data = Image.open(fp=image_path)
        if zorder is not None:
            pyplot.imshow(X=image_data, extent=[locations[0], size[0], locations[1], size[1]], zorder=zorder)
        else:
            pyplot.imshow(X=image_data, extent=[locations[0], size[0], locations[1], size[1]])

    def set_widget_image(self, widget_info: tuple, locations: tuple, size: tuple, zorder: int = None):
        """
        Put the widget with a specific size in a specific position of a panel.

        :param widget_info: the painting information of the widget.
        :type widget_info: tuple

        :param locations: location in the panel (x and y).
        :type locations: tuple

        :param size: display size of the widget.
        :type size: tuple

        :param zorder: order in which components are superimposed on each other.
        :type zorder: int or None
        """
        pass  # TODO
