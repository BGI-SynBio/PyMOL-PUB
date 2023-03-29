from logging import getLogger, CRITICAL
from matplotlib import pyplot, rcParams
from numpy import zeros, sum
from os import path
from PIL import Image, PngImagePlugin
from pymol2 import PyMOL
from types import FunctionType
from warnings import filterwarnings

filterwarnings("ignore")
getLogger("matplotlib").setLevel(CRITICAL)


class StructureImage:

    def __init__(self, structure_path: str):

        self.__mol = PyMOL()
        self.__mol.start()
        self.__mol.cmd.load(structure_path, quiet=1)
        self.__mol.cmd.ray(quiet=1)  # make PyMOL run silently.

    def set_state(self, representation_type: str = None, chain_select: str = None, representations: dict = None,
                  hides: list = None):
        """
        Set the initial state of a structure.

        :param representation_type: the type of the visual structure.
        :type representation_type: str or None

        :param chain_select: if representation_type is index, can optionally operate on the specified chain.
        :type chain_select: str or None

        :param representations: pair of the class and its corresponding representation.
        :type representations: dict or None

        :param hides: hided molecules.
        :type hides: list or None
        """
        if representation_type is None and representations is None:
            representation = "cartoon"
            self.__mol.cmd.show(representation=representation)

        elif representation_type is not None and representations is not None:
            if representation_type == "residue":
                for residue, representation in representations.items():
                    self.__mol.cmd.show(representation=representation, selection="(r. " + residue + ")")

            elif representation_type == "chain":
                for chain, representation in representations.items():
                    self.__mol.cmd.show(representation=representation, selection="(c. " + chain + ")")

            elif representation_type == "index":
                for index, representation in representations.items():
                    if chain_select is not None:
                        self.__mol.cmd.show(representation=representation,
                                            selection="(c. " + chain_select + " and i. " + index + ")")
                    else:
                        self.__mol.cmd.show(representation=representation, selection="(i. " + index + ")")

            elif representation_type == "segment":
                for segment, representation in representations.items():
                    self.__mol.cmd.show(representation=representation, selection="(ps. " + segment + ")")

            elif representation_type == "all":
                self.__mol.cmd.show(representation=list(representations.values())[0], selection="(all)")

            else:
                raise ValueError("No such representation type!")

        else:
            raise ValueError("We need \'representation_type\' and \'representations\'!")

        if hides is not None:
            for hide_selection in hides:
                self.__mol.cmd.hide(selection=hide_selection)

        self.__mol.cmd.orient()
        self.__mol.cmd.center()
        self.__mol.cmd.zoom(complete=1)

    def set_color(self, shading_type: str = None, chain_select: str = None, colors: dict = None):
        """
        Set color for the structure.

        :param shading_type: type of color shading for the structure.
        :type shading_type: str or None

        :param chain_select: if shading_type is index, can optionally operate on the specified chain.
        :type chain_select: str or None

        :param colors: pair of the class and its corresponding color.
        :type colors: dict or None
        """
        if shading_type is None and colors is None:
            residue_colors = {"ALA": "0x8A685C", "ARG": "0x402F42", "ASN": "0x7fA9C2", "ASP": "0x632D3B",
                              "CYS": "0x7D779D", "GLN": "0x853D2F", "GLU": "0x88191F", "GLY": "0x945A4F",
                              "HIS": "0xA29DB3", "ILE": "0x645D87", "LEU": "0x82A293", "LYS": "0xA58121",
                              "MET": "0x6273A1", "PHE": "0xB33C24", "PRO": "0x73584D", "SER": "0x4F698A",
                              "THR": "0xB9B9BB", "TRP": "0x686C47", "TYR": "0x674E3A", "VAL": "0x9D491B",
                              "DA": "0xF2521B", "DC": "0x81CC28", "DG": "0x00AEF0", "DT": "0xFABC09", "DU": "0xFABC09",
                              "A": "0xF2521B", "C": "0x81CC28", "G": "0x00AEF0", "T": "0xFABC09", "U": "0xFABC09"}

            for residue, color in residue_colors.items():
                self.__mol.cmd.color(color=color, selection="(r. " + residue + ")")

        elif shading_type is not None and colors is not None:
            if shading_type == "residue":
                for residue, color in colors.items():
                    self.__mol.cmd.color(color=color, selection="(r. " + residue + ")")

            elif shading_type == "chain":
                for chain, color in colors.items():
                    self.__mol.cmd.color(color=color, selection="(c. " + chain + ")")

            elif shading_type == "index":
                for index, color in colors.items():
                    if chain_select is not None:
                        self.__mol.cmd.color(color=color, selection="(c. " + chain_select + " and i. " + index + ")")
                    else:
                        self.__mol.cmd.color(color=color, selection="(i. " + index + ")")

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

    def rotate_structure(self, rotate_dict: dict):
        """
        Rotate the structure.

        :param rotate_dict: pair of the axis and its corresponding rotation angle.
        :type rotate_dict: dict
        """
        for axis, degree in rotate_dict.items():
            self.__mol.cmd.rotate(axis=axis, angle=degree)

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
        assert save_path[-4:] == ".png"  # TODO consider the SVG output.
        self.__mol.cmd.png(filename=save_path, width=width, height=width * ratio, dpi=dpi, quiet=1)


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
        elif image_format == ".svg":
            # TODO we need to find a suitable svg loader.
            self.paste_vector(image=image_path, locations=locations, layout=layout, zorder=zorder)
        else:
            raise ValueError("Only PNG files and SVG files are support!")

    def set_text(self, annotation: str, fontsize: int = 16, horizontalalignment: str = 'center', locations: list = None,
                 layout: tuple = None, zorder: int = None):
        """
        Put the text box with a specific size in a specific position of a panel.

        :param annotation: text content.
        :type annotation: str

        :param fontsize: font size.
        :type fontsize: str

        :param horizontalalignment: horizontal alignment('center' | 'right' | 'left' ).
        :type horizontalalignment: str

        :param locations: location in the panel (x,y,dx and dy: the scale of the whole picture).
        :type locations: list or None

        :param layout: picture segmentation method and specified location(x,y,order).
        :type layout: tuple or None

        :param zorder: order in which components are superimposed on each other.
        :type zorder: int or None
        """
        if locations is not None and layout is not None:
            raise ValueError("We can't choose between \'locations\' and \'layout\'!")

        if layout is not None and locations is None:
            locations = self.calculate_locations(layout=layout)

        if locations is not None:
            if zorder is not None:
                ax = self.fig.add_axes(locations)
                ax.axis("off")
                ax.text(0, 0, annotation, fontsize=fontsize, horizontalalignment=horizontalalignment, zorder=zorder)
            else:
                ax = self.fig.add_axes(locations)
                ax.axis("off")
                ax.text(0, 0, annotation, fontsize=fontsize, horizontalalignment=horizontalalignment)
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
    def paste_vector(image, locations: list = None, layout: tuple = None, zorder: int = None):
        # TODO no suitable pasting (or painting) rules found temporarily.
        pass

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

    @staticmethod
    def save_figure(save_path: str):
        """
        Save the whole figure.

        :param save_path: the path of save figure.
        :type save_path: str
        """
        pyplot.savefig(save_path)
