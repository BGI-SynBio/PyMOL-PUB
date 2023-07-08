from matplotlib import font_manager
from molpub.layouts import DefaultStructureImage, PropertyStructureImage, HighlightStructureImage
from molpub.layouts import obtain_widget_icon, Figure
from molpub.handles import Monitor, Score, similar, cluster, align, set_properties, set_difference, kmer
from molpub.handles import load_structure_from_file, save_structure_to_file
from os import path

# load required font formats.
font_files = font_manager.findSystemFonts(path.abspath(__file__).replace("\\", "/")[:-11] + "fonts/")
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)
