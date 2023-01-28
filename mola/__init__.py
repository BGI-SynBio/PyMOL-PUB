from matplotlib.font_manager import fontManager

existing_fonts = []
for font_info in fontManager.ttflist:
    existing_fonts.append(font_info.name)

needed_fonts = ["Times New Roman", "Helvetica", "Arial", "Linux Libertine", "Lucida Calligraphy"]
for needed_font in needed_fonts:
    if needed_font not in existing_fonts:
        pass  # TODO install fonts
