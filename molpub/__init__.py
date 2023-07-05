from matplotlib import font_manager
from os import path

# load required font formats.
font_files = font_manager.findSystemFonts(path.abspath(__file__).replace("\\", "/")[:-11] + "fonts/")
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)
