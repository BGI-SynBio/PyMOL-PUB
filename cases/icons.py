from matplotlib import pyplot
from molpub import obtain_widget_icon
from os import remove
from PIL import Image


def combination_1():
    pyplot.figure(figsize=(5, 10), tight_layout=True)
    grid = pyplot.GridSpec(1, 10)
    index = 0

    turn = "right"
    for degree in [30, 60, 90, 120, 180][::-1]:
        pyplot.subplot(grid[0, index])
        obtain_widget_icon(save_path="./temp/comb1.png",
                           widget_type="rotation", params={"turn": turn, "degree": degree})
        image_data = Image.open(fp="./temp/comb1.png")
        pyplot.imshow(X=image_data)
        pyplot.xlim(-100, image_data.width + 100)
        pyplot.ylim(image_data.height + 100, -100)
        pyplot.xticks([])
        pyplot.yticks([])
        pyplot.xlabel(turn + "\n" + str(degree), fontsize=6)
        remove("./temp/comb1.png")
        index += 1

    turn = "left"
    for degree in [30, 60, 90, 120, 180]:
        pyplot.subplot(grid[0, index])
        obtain_widget_icon(save_path="./temp/comb1.png",
                           widget_type="rotation", params={"turn": turn, "degree": degree})
        image_data = Image.open(fp="./temp/comb1.png")
        pyplot.imshow(X=image_data)
        pyplot.xlim(-100, image_data.width + 100)
        pyplot.ylim(image_data.height + 100, -100)
        pyplot.xticks([])
        pyplot.yticks([])
        pyplot.xlabel(turn + "\n" + str(degree), fontsize=6)
        remove("./temp/comb1.png")
        index += 1

    pyplot.savefig("./widgets/style1.png", bbox_inches="tight", dpi=1200)


def combination_2():
    figure = pyplot.figure(figsize=(10, 10), tight_layout=True)
    grid = pyplot.GridSpec(11, 11)

    for e_index, elevation in enumerate([-180, -120, -90, -60, -30, 0, 30, 60, 90, 120, 180]):
        for a_index, azimuth in enumerate([-180, -120, -90, -60, -30, 0, 30, 60, 90, 120, 180]):
            if elevation != 0 or azimuth != 0:
                pyplot.subplot(grid[10 - e_index, a_index])

                obtain_widget_icon(save_path="./temp/comb2.png",
                                   widget_type="rotation", params={"elevation": elevation, "azimuth": azimuth})

                image_data = Image.open(fp="./temp/comb2.png")
                pyplot.imshow(X=image_data)
                pyplot.xlim(-100, image_data.width + 100)
                pyplot.ylim(image_data.height + 100, -100)
                pyplot.xticks([])
                pyplot.yticks([])
                if elevation == -180:
                    if azimuth <= 0:
                        pyplot.xlabel(str(azimuth), fontsize=10)
                    else:
                        pyplot.xlabel("+" + str(azimuth), fontsize=10)
                if azimuth == -180:
                    if elevation <= 0:
                        pyplot.ylabel(str(elevation), fontsize=10)
                    else:
                        pyplot.ylabel("+" + str(elevation), fontsize=10)
                remove("./temp/comb2.png")

    figure.text(0.51, 0.00, "azimuth", va="center", ha="center", fontsize=12)
    figure.text(0.00, 0.51, "elevation", va="center", ha="center", fontsize=12, rotation=90)

    pyplot.savefig("./widgets/style2.png", bbox_inches="tight", dpi=1200)


if __name__ == "__main__":
    combination_1()
    combination_2()
