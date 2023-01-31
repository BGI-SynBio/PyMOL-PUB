from matplotlib import pyplot, patches
from numpy import linspace, deg2rad, sin, cos

from forms import parent_path, optimize_format

if __name__ == "__main__":
    # style 1
    major_axis, minor_axis, scale = 1.8, 0.6, 1
    for turn in ["right", "left"]:
        if turn == "right":
            x_values = cos(deg2rad(linspace(-90, 270, 360 * scale + 1)[::-1])) * major_axis / 2.0
            y_values = sin(deg2rad(linspace(-90, 270, 360 * scale + 1)[::-1])) * minor_axis / 2.0
        else:
            x_values = cos(deg2rad(linspace(-90, 270, 360 * scale + 1))) * major_axis / 2.0
            y_values = sin(deg2rad(linspace(-90, 270, 360 * scale + 1))) * minor_axis / 2.0

        for degree in [30, 60, 90, 120]:
            pyplot.figure(figsize=(2, 2))
            ax = pyplot.subplot(1, 1, 1)
            pyplot.vlines(0, -0.6, -1, color="k", lw=3, zorder=0)
            # noinspection PyUnresolvedReferences
            ax.add_patch(patches.Ellipse(xy=(0.0, 0.0), width=major_axis, height=minor_axis, fc="silver"))
            pyplot.vlines(0, 0, +1, color="k", lw=3, zorder=2)
            if turn == "right":
                pyplot.fill_between([0.0, +0.3], [-0.45, -0.3], [-0.15, -0.3], color="k", zorder=3)
            else:
                pyplot.fill_between([-0.3, 0.0], [-0.3, -0.45], [-0.3, -0.15], color="k", zorder=3)

            if degree != 180:
                pyplot.plot([0, x_values[degree * scale + 1]], [0, y_values[degree * scale + 1]],
                            color="k", lw=2, ls=":", zorder=4)
            pyplot.scatter([0, x_values[degree * scale + 1]], [0, y_values[degree * scale + 1]], marker="o",
                           s=40, color="k", zorder=4)
            pyplot.plot(x_values[:degree * scale + 1], y_values[:degree * scale + 1], color="k", lw=3, zorder=4)

            pyplot.xlim(-1, +1)
            pyplot.ylim(-1, +1)
            pyplot.axis("off")

            flag_1 = "-" if turn == "right" else "+"
            flag_2 = "1pi" + str(int(180 / degree)) if degree != 120 else "2pi3"

            save_path = parent_path + "rotation [" + flag_1 + "." + flag_2 + "].svg"
            pyplot.savefig(save_path, transparent=True, pad_inches=0, bbox_inches="tight", dpi=1200)
            pyplot.close()

            optimize_format(image_path=save_path)
