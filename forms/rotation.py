from matplotlib import pyplot, patches
from numpy import array, linspace, deg2rad, sin, cos, sqrt

from forms import parent_path, optimize_format

if __name__ == "__main__":
    # style 1
    major_axis, minor_axis = 1.8, 0.6
    for turn in ["right", "left"]:
        if turn == "right":
            x_values = cos(deg2rad(linspace(-90, 270, 361)[::-1])) * major_axis / 2.0
            y_values = sin(deg2rad(linspace(-90, 270, 361)[::-1])) * minor_axis / 2.0
        else:
            x_values = cos(deg2rad(linspace(-90, 270, 361))) * major_axis / 2.0
            y_values = sin(deg2rad(linspace(-90, 270, 361))) * minor_axis / 2.0

        for degree in [30, 60, 90, 120, 180]:
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
                pyplot.plot([0, x_values[degree + 1]], [0, y_values[degree + 1]],
                            color="k", lw=2, ls=":", zorder=4)
            pyplot.scatter([0, x_values[degree + 1]], [0, y_values[degree + 1]], marker="o",
                           s=40, color="k", zorder=4)
            pyplot.plot(x_values[:degree + 1], y_values[:degree + 1], color="k", lw=3, zorder=4)

            pyplot.xlim(-1, +1)
            pyplot.ylim(-1, +1)
            pyplot.axis("off")

            flag_1 = "-" if turn == "right" else "+"
            flag_2 = "1pi" + str(int(180 / degree)) if degree != 120 else "2pi3"

            save_path = parent_path + "rotation [" + flag_1 + "." + flag_2 + "].svg"
            pyplot.savefig(save_path, transparent=True, pad_inches=0, bbox_inches="tight", dpi=1200)
            pyplot.close()

            optimize_format(image_path=save_path)

    # style 2.
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
    elevation_data = {}
    for elevation in [-180, -120, -90, -60, -30, 0, 30, 60, 90, 120, 180]:
        line_info, area_info, last_x, last_y = [], None, None, None
        if 0 < elevation <= 90:
            addition = int(elevation / 3 * 4)
            x, y = elevation_x_values[:addition], elevation_y_values[:addition]
            line_info.append((x, y, "-"))
            last_x, last_y = x[-1], y[-1]
            upper = []
            for x_value, y_value in zip(x, y):
                upper.append(x_value if x_value <= 0 else x_value / last_x * last_y)
            area_info = (array(x.tolist() + [0]), array(y.tolist() + [0]), array(upper + [0]))
            elevation_data[elevation] = line_info, area_info, last_x, last_y
        elif elevation > 90:
            x_1, y_1 = elevation_x_values[:120], elevation_y_values[:120]
            addition = int((elevation - 90) / 3 * 2)
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
            elevation_data[elevation] = line_info, area_info, last_x, last_y
        elif -90 < elevation < 0:
            addition = int((90 + elevation) / 3 * 2)
            x, y = elevation_x_values[300 + addition:], elevation_y_values[300 + addition:]
            line_info.append((x, y, "-"))
            last_x, last_y = x[0], y[0]
            upper = []
            for x_value, y_value in zip(x, y):
                upper.append(x_value / last_x * last_y)
            area_info = (array(x.tolist() + [0]), array(y.tolist() + [0]), array(upper + [0]))
            elevation_data[elevation] = line_info, area_info, last_x, last_y
        elif -90 == elevation:
            addition = int((90 + elevation) / 3 * 2)
            x, y = elevation_x_values[300 + addition:], elevation_y_values[300 + addition:]
            line_info.append((x, y, "-"))
            last_x, last_y = x[0], y[0]
            upper = []
            for x_value, y_value in zip(x, y):
                upper.append(x_value)
            area_info = (x, y, upper)
            elevation_data[elevation] = line_info, area_info, last_x, last_y
        elif -90 > elevation:
            x_1, y_1 = elevation_x_values[300:], elevation_y_values[300:]
            addition = int((-elevation - 90) / 3 * 4)
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
            elevation_data[elevation] = line_info, area_info, last_x, last_y

    # azimuth angle for the x,y plane.
    azimuth_x_values = cos(deg2rad(linspace(-120, 240, 361))) * major_axis / 2.0
    azimuth_y_values = sin(deg2rad(linspace(-120, 240, 361))) * minor_axis / 2.0
    azimuth_data = {}
    for azimuth in [-180, -120, -90, -60, -30, 0, 30, 60, 90, 120, 180]:
        line_info, area_info, last_x, last_y = [], None, None, None
        if 0 < azimuth <= 90:
            addition = int(azimuth / 3 * 4)
            x, y = azimuth_x_values[:addition], azimuth_y_values[:addition]
            line_info.append((x, y, "-"))
            last_x, last_y = x[-1], y[-1]
            upper = []
            for x_value, y_value in zip(x, y):
                upper.append(x_value if x_value <= 0 else x_value / last_x * last_y)
            area_info = (x, y, array(upper))
            azimuth_data[azimuth] = line_info, area_info, last_x, last_y
        elif azimuth > 90:
            x_1, y_1 = azimuth_x_values[:120], azimuth_y_values[:120]
            addition = int((azimuth - 90) / 3 * 2)
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
            azimuth_data[azimuth] = line_info, area_info, last_x, last_y
        elif -90 <= azimuth < 0:
            addition = int((90 + azimuth) / 3 * 2)
            x, y = azimuth_x_values[300 + addition:], azimuth_y_values[300 + addition:]
            line_info.append((x, y, "-"))
            last_x, last_y = x[0], y[0]
            upper = []
            for x_value, y_value in zip(x, y):
                upper.append(x_value / last_x * last_y)
            area_info = (array(x.tolist() + [0]), array(y.tolist() + [0]), array(upper + [0]))
            azimuth_data[azimuth] = line_info, area_info, last_x, last_y
        elif -90 > azimuth:
            x_1, y_1 = azimuth_x_values[300:], azimuth_y_values[300:]
            addition = int((-azimuth - 90) / 3 * 4)
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
            azimuth_data[azimuth] = line_info, area_info, last_x, last_y

    for elevation in [-180, -120, -90, -60, -30, 0, 30, 60, 90, 120, 180]:
        for azimuth in [-180, -120, -90, -60, -30, 0, 30, 60, 90, 120, 180]:
            if elevation == 0 and azimuth == 0:
                continue

            pyplot.figure(figsize=(2, 2))
            pyplot.plot(x_values_1[:180], y_values_1[:180], color="grey", lw=1, ls=":", zorder=0)
            pyplot.plot(x_values_1[180:], y_values_1[180:], color="grey", lw=1, zorder=0)
            pyplot.plot(x_values_2[:180], y_values_2[:180], color="grey", lw=1, ls=":", zorder=0)
            pyplot.plot(x_values_2[180:], y_values_2[180:], color="grey", lw=1, zorder=0)
            pyplot.plot(x_values_3, y_values_3, color="grey", lw=1, zorder=0)
            pyplot.plot([azimuth_x_values[0], 0], [azimuth_y_values[0], 0], color="k", lw=3, ls=":", zorder=1)

            if elevation in elevation_data:
                line_info, area_info, last_x, last_y = elevation_data[elevation]
                if area_info is not None:
                    if elevation < 0:
                        pyplot.fill_between(area_info[0], area_info[1], area_info[2],
                                            fc="royalblue", lw=0, alpha=0.5, zorder=2)
                    else:
                        pyplot.fill_between(area_info[0], area_info[1], area_info[2],
                                            fc="royalblue", lw=0, alpha=0.5, zorder=4)
                for x, y, style in line_info:
                    pyplot.plot(x, y, color="k", lw=3, ls=style, zorder=5)
                pyplot.plot([0, last_x], [0, last_y], color="k", lw=3, ls=":", zorder=5)
                if elevation > 0:
                    pyplot.fill_between([-0.15, 0, +0.15],
                                        [-1, -1, -1], [-1, -0.7, -1], color="k", lw=0, zorder=6)
                elif elevation < 0:
                    pyplot.fill_between([-0.15, 0, +0.15],
                                        [+1, +1, +1], [+1, 0.7, +1], color="k", lw=0, zorder=6)

            if azimuth in azimuth_data:
                line_info, area_info, last_x, last_y = azimuth_data[azimuth]
                if area_info is not None:
                    pyplot.fill_between(area_info[0], area_info[1], area_info[2],
                                        fc="chocolate", lw=0, alpha=0.5, zorder=3)
                for x, y, style in line_info:
                    pyplot.plot(x, y, color="k", lw=3, ls=style, zorder=5)
                pyplot.plot([0, last_x], [0, last_y], color="k", lw=3, ls=":", zorder=5)
                if azimuth > 0:
                    pyplot.fill_between([0.7, 1.0], [0, -0.15], [0, +0.15], color="k", lw=0, zorder=6)
                elif azimuth < 0:
                    pyplot.fill_between([-1, -0.7], [-0.15, 0], [+0.15, 0], color="k", lw=0, zorder=6)

            pyplot.xlim(-1, +1)
            pyplot.ylim(-1, +1)
            pyplot.axis("off")

            if elevation > 0:
                flag_1 = "+" + ("1pi" + str(int(180 / elevation)) if elevation != 120 else "2pi3")
            elif elevation < 0:
                flag_1 = "-" + ("1pi" + str(int(180 / -elevation)) if elevation != -120 else "2pi3")
            else:
                flag_1 = "+0pi1"

            if azimuth > 0:
                flag_2 = "+" + ("1pi" + str(int(180 / azimuth)) if azimuth != 120 else "2pi3")
            elif azimuth < 0:
                flag_2 = "-" + ("1pi" + str(int(180 / -azimuth)) if azimuth != -120 else "2pi3")
            else:
                flag_2 = "+0pi1"

            save_path = parent_path + "rotation [" + flag_1 + "." + flag_2 + "].svg"
            pyplot.savefig(save_path, transparent=True, pad_inches=0, bbox_inches="tight")
            pyplot.close()

            optimize_format(image_path=save_path)
