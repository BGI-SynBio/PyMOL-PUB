from matplotlib import pyplot
from math import cos, sin, pi

if __name__ == "__main__":
    for degree in[0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]:
        x = pi * degree / 180
        fig = pyplot.figure(figsize=(2, 2))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        ax.arrow(0.5 - 0.5 * cos(x), 0.5 - 0.5 * sin(x), 1.0 * cos(x), 1.0 * sin(x), width=0.02, head_width=0.3,
                 head_length=0.4, overhang=0.25, length_includes_head=True, facecolor="black")
        fig.savefig('../mola/supp/widgets/arrow [' + str(degree) + '-degree].png', dpi=600)
