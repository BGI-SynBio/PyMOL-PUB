import shutil
import sys
from collections import Counter
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QWidget, QMessageBox
from numpy import array, min, max, where, zeros, any
from gui import ImageWindow1, ImageWindow2, ImageWindow3, ImageWindow4
from gui import MainWindow, ClickSurface, SelectionWindow, ContentWindow
from molpub import HighlightStructureImage, Figure


class EntryWindow(QMainWindow, MainWindow):
    def __init__(self):
        super(EntryWindow, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.add_history)
        self.layout = [1, 1]
        self.new_buttonlist = [self.push_button1]
        self.detail_buttonlist = []
        self.detail_window = DetailWindow([1, 1], 0)
        self.current_label = ""
        self.combobox_label = ["a"]
        self.case = None
        self.progress = 0.0
        self.draw_number = 0
        self.history_text = []
        self.targets_text = []
        self.occupied_text = []
        self.ratio_text = []
        self.format_text = []

        self.comboBox_3.activated.connect(lambda: self.change_layout(self.comboBox_3.currentIndex()))
        self.pushButton_2.clicked.connect(self.figure_output)
        self.pushButton_3.clicked.connect(self.set_undo)
        self.pushButton_4.clicked.connect(self.set_redo)

    def add_history(self):
        figure_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '.', "Figure (*.png *.pdf)")
        self.textBrowser.append(figure_name)

    def change_layout(self, index):
        self.comboBox_4.clear()
        self.combobox_label = []
        if index == 0:
            self.layout[0] += 1
        elif index == 1:
            self.layout[0] -= 1
        elif index == 2:
            self.layout[1] += 1
        else:
            self.layout[1] -= 1

        width = 625 / self.layout[1]
        height = 265 / self.layout[0]

        button_list = self.button_group.buttons()
        for button in button_list:
            self.button_group.removeButton(button)
            button.setParent(None)

        self.new_buttonlist = []
        self.button_state = []
        for i in range(self.layout[0] * self.layout[1]):
            button = QPushButton(self.centralwidget)
            self.new_buttonlist.append(button)
            self.new_buttonlist[i].resize(width, height)
            self.new_buttonlist[i].move((80 + i % self.layout[1] * (630.0 / self.layout[1])),
                                        (120 + i // self.layout[1] * (270.0 / self.layout[0])))
            font = QFont()
            font.setFamily("Times New Roman")
            font.setPointSize(20)
            self.new_buttonlist[i].setFont(font)
            self.new_buttonlist[i].setObjectName("push_button" + str(i))
            self.new_buttonlist[i].setStyleSheet("border: 3px dashed black;")
            self.new_buttonlist[i].clicked.connect(self.show_detail)
            self.button_group.addButton(self.new_buttonlist[i], i)
            self.button_state.append(0)
            self.new_buttonlist[i].show()

    def check_surface(self, new_index):
        matrix = []
        for order, button in enumerate(self.new_buttonlist):
            matrix.append(button.text())
        matrix[new_index] = self.current_label
        matrix = array(matrix).reshape(self.layout)

        values = []
        for row in matrix:
            for value in row:
                if value != '':
                    values.append(ord(value) - 97)
                else:
                    values.append(-1)
        indices = array(values).reshape(self.layout)
        counter = Counter(indices.reshape(-1))
        order = sorted(list(counter.keys()))
        if order[0] == -1 and len(order) == 1:
            return True
        if order[0] == -1:
            order = order[1:]
        if order[0] != 0:
            return "The label should start from a!"
        if len(order) > 1:
            for former_index, latter_index in zip(order[:-1], order[1:]):
                if latter_index - former_index != 1:
                    return "The labels should be consecutive!"

        for index in order:
            xs, ys = where(indices == index)
            ranges = {"x": (min(xs), max(xs)), "y": (min(ys), max(ys))}
            chuck_matrix = zeros(shape=(ranges["x"][1] - ranges["x"][0] + 1, ranges["y"][1] - ranges["y"][0] + 1))
            for x, y in zip(xs, ys):
                chuck_matrix[x - ranges["x"][0], y - ranges["y"][0]] = 1
            if any(chuck_matrix != 1):
                return "The area covered by this label should be rectangular!"
        return True

    def show_detail(self):
        order = self.new_buttonlist.index(self.sender())
        self.detail_window = DetailWindow(self.layout, order)
        self.detail_window.show()
        self.hide()

        self.detail_window.pushButton.clicked.connect(self.detail_window.hide)
        self.detail_window.pushButton.clicked.connect(self.show)
        self.detail_window.pushButton.clicked.connect(lambda: self.label_set(order))

    def label_set(self, order):
        self.current_label = self.detail_window.textEdit.toPlainText()
        warning_text = self.check_surface(order)

        if warning_text is True:
            if self.current_label == '':
                self.new_buttonlist[order].setText(self.current_label)
                self.new_buttonlist[order].setStyleSheet("border: 3px dashed black; background: #FFFFFF;")
            else:
                self.new_buttonlist[order].setText(self.current_label)
                self.new_buttonlist[order].setStyleSheet("border: 3px dashed black; background: #B4C7E7;")
                self.button_state[order] = 1
                if self.current_label not in self.combobox_label:
                    self.combobox_label.append(self.current_label)
                    self.comboBox_4.addItem(self.current_label)
        else:
            QMessageBox.warning(self, "Illegal Label", warning_text, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def image_set(self):
        global image_list
        global statistical_list

        if len(image_list) > 0 or len(statistical_list) > 0:
            self.progress += 1

            for order, button in enumerate(self.new_buttonlist):
                if button.text() == self.comboBox_4.currentText():
                    button.setStyleSheet("border: 3px dashed black; background: #F8CBAD;")
                    self.button_state[order] = 2

            label_number = self.comboBox_4.count()
            self.progressBar.setValue(self.progress / label_number * 100)

    def calculate_imageratio(self):
        panel_width = 1.0 / self.layout[1]
        panel_hight = 1.0 / self.layout[0]
        panel_list = []

        for order, button in enumerate(self.new_buttonlist):
            if button.text() == self.comboBox_4.currentText():
                x = order % self.layout[1] * panel_width
                y = 1.0 - (order // self.layout[1] + 1) * panel_hight
                coordinate = [x, y, x + panel_width, y + panel_hight]
                panel_list.append(coordinate)
        panel_array = array(panel_list)
        panel_location = [min(panel_array[:, 0]), min(panel_array[:, 1]),
                          max(panel_array[:, 2]) - min(panel_array[:, 0]),
                          max(panel_array[:, 3]) - min(panel_array[:, 1])]
        return panel_location[3] / panel_location[2] / float(self.textEdit_1.toPlainText())

    def figure_output(self):
        manuscript_format = self.comboBox.currentText()
        occupied_columns = int(self.textEdit.toPlainText())
        aspect_ratio = (1, float(self.textEdit_1.toPlainText()))

        if manuscript_format == "Cell":
            column_format = int(self.comboBox_2.currentText())
        else:
            column_format = None

        self.case = Figure(manuscript_format=manuscript_format, column_format=column_format, aspect_ratio=aspect_ratio,
                           occupied_columns=occupied_columns)
        if self.textBrowser.toPlainText() != "":
            self.case.set_image(image_path=self.textBrowser.toPlainText(), locations=[0, 0, 1, 1])

        panel_width = 1.0 / self.layout[1]
        panel_hight = 1.0 / self.layout[0]
        label_number = self.comboBox_4.count()
        image_dict = {}

        for i in range(label_number):
            panel_list = []
            label = self.comboBox_4.itemText(i)
            for order, button in enumerate(self.new_buttonlist):
                if button.text() == label and self.button_state[order] == 2:
                    x = order % self.layout[1] * panel_width
                    y = 1.0 - (order // self.layout[1] + 1) * panel_hight
                    coordinate = [x, y, x + panel_width, y + panel_hight]
                    panel_list.append(coordinate)
            panel_array = array(panel_list)
            if panel_array != []:
                image_dict[label] = [min(panel_array[:, 0]), min(panel_array[:, 1]),
                                     max(panel_array[:, 2]) - min(panel_array[:, 0]),
                                     max(panel_array[:, 3]) - min(panel_array[:, 1])]
        for image_label, locations in image_dict.items():
            self.case.set_image(image_path="./temp/panel_" + image_label + ".png", locations=locations)
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save file', '.')
        self.case.save_figure(save_path)

        if self.draw_number < len(self.history_text):
            self.history_text = self.history_text[:self.draw_number + 1]
            self.history_text[self.draw_number] = self.textBrowser.toPlainText()
        else:
            self.history_text.append(self.textBrowser.toPlainText())

        if self.draw_number < len(self.targets_text):
            self.targets_text = self.targets_text[:self.draw_number + 1]
            self.targets_text[self.draw_number] = self.comboBox.currentText()
        else:
            self.targets_text.append(self.comboBox.currentText())

        if self.draw_number < len(self.occupied_text):
            self.occupied_text = self.occupied_text[:self.draw_number + 1]
            self.occupied_text[self.draw_number] = self.textEdit.toPlainText()
        else:
            self.occupied_text.append(self.textEdit.toPlainText())

        if self.draw_number < len(self.ratio_text):
            self.ratio_text = self.ratio_text[:self.draw_number + 1]
            self.ratio_text[self.draw_number] = self.textEdit_1.toPlainText()
        else:
            self.ratio_text.append(self.textEdit_1.toPlainText())

        if self.draw_number < len(self.format_text):
            self.format_text = self.format_text[:self.draw_number + 1]
            self.format_text[self.draw_number] = self.comboBox_2.currentText()
        else:
            self.format_text.append(self.comboBox_2.currentText())

        self.draw_number += 1

    def set_undo(self):
        if self.draw_number > 1:
            self.textBrowser.setText(self.history_text[self.draw_number - 2])
            self.comboBox.setCurrentText(self.targets_text[self.draw_number - 2])
            self.textEdit.setText(self.occupied_text[self.draw_number - 2])
            self.textEdit_1.setText(self.ratio_text[self.draw_number - 2])
            self.comboBox_2.setCurrentText(self.format_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.textBrowser.setText("")
            self.comboBox.setCurrentIndex(0)
            self.textEdit.setText("")
            self.textEdit_1.setText("")
            self.comboBox_2.setCurrentIndex(0)
            self.draw_number = 0

    def set_redo(self):
        if self.draw_number < len(self.history_text):
            self.textBrowser.setText(self.history_text[self.draw_number])
            self.comboBox.setCurrentText(self.targets_text[self.draw_number])
            self.textEdit.setText(self.occupied_text[self.draw_number])
            self.textEdit_1.setText(self.ratio_text[self.draw_number])
            self.comboBox_2.setCurrentText(self.format_text[self.draw_number])
            self.draw_number += 1
        else:
            self.textBrowser.setText(self.history_text[-1])
            self.comboBox.setCurrentText(self.targets_text[-1])
            self.textEdit.setText(self.occupied_text[-1])
            self.textEdit_1.setText(self.ratio_text[-1])
            self.comboBox_2.setCurrentText(self.format_text[-1])


class DetailWindow(QWidget, ClickSurface):
    def __init__(self, layout, order):
        super(DetailWindow, self).__init__()
        self.setupUi(self)
        self.draw_layout(layout, order)

    def draw_layout(self, layout, order):
        width = 370 / layout[1]
        height = 190 / layout[0]
        self.detail_buttonlist = []

        for i in range(layout[0] * layout[1]):
            button = QPushButton(self)
            self.detail_buttonlist.append(button)
            self.detail_buttonlist[i].resize(width, height)
            self.detail_buttonlist[i].move((12 + i % layout[1] * (375.0 / layout[1])),
                                           (82 + i // layout[1] * (195.0 / layout[0])))
            font = QFont()
            font.setFamily("Times New Roman")
            font.setPointSize(16)
            self.detail_buttonlist[i].setFont(font)
            self.detail_buttonlist[i].setObjectName("push_button" + str(i))
            if i == order:
                self.detail_buttonlist[i].setStyleSheet("border: 3px dashed black; background: #FFE699;")
                self.detail_buttonlist[i].setText("select")
            else:
                self.detail_buttonlist[i].setStyleSheet("border: 3px dashed black;")
            self.button_group.addButton(self.detail_buttonlist[i], i)
            self.detail_buttonlist[i].show()


class SelectWindow(QMainWindow, SelectionWindow):
    def __init__(self):
        super(SelectWindow, self).__init__()
        self.setupUi(self)


class StatisticalWindow(QMainWindow, ContentWindow):
    def __init__(self):
        super(StatisticalWindow, self).__init__()
        self.setupUi(self)
        global statistical_list
        statistical_list = []
        self.draw_number = 0
        self.folder_text = []

        self.pushButton_7.clicked.connect(self.add_statistical)
        self.pushButton_8.clicked.connect(self.show_statistical)
        self.pushButton_3.clicked.connect(self.set_undo)
        self.pushButton_4.clicked.connect(self.set_redo)

    def add_statistical(self):
        figure_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '.', "Figure (*.png *.jpg *.svg *.pdf)")
        self.textBrowser.append(figure_name)

    def show_statistical(self):
        global statistical_list

        statistical_path = self.textBrowser.toPlainText().strip("\n")

        if self.draw_number < len(statistical_list):
            statistical_list = statistical_list[:self.draw_number + 1]
            statistical_list[self.draw_number] = statistical_path
        else:
            statistical_list.append(statistical_path)

        if self.draw_number < len(self.folder_text):
            self.folder_text = self.folder_text[:self.draw_number + 1]
            self.folder_text[self.draw_number] = self.textBrowser.toPlainText()
        else:
            self.folder_text.append(self.textBrowser.toPlainText())

        figure = QPixmap(statistical_path)
        self.scene.clear()
        self.scene.addPixmap(figure)
        self.graphicsView.setScene(self.scene)

        self.draw_number += 1

    def save_image(self, label_text):
        global statistical_list
        if len(statistical_list) > 0:
            newfile_path = "./temp/panel_" + label_text + ".png"
            shutil.copyfile(statistical_list[-1], newfile_path)

    def set_undo(self):
        global statistical_list

        if self.draw_number > 1:
            self.scene.clear()
            figure = QPixmap(statistical_list[self.draw_number - 2])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.scene.clear()
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText("")
            self.draw_number = 0

    def set_redo(self):
        global statistical_list

        if self.draw_number < len(statistical_list):
            self.scene.clear()
            figure = QPixmap(statistical_list[self.draw_number])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[self.draw_number])
            self.draw_number += 1
        else:
            self.scene.clear()
            figure = QPixmap(statistical_list[-1])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[-1])

    def window_clear(self):
        global statistical_list

        statistical_list = []
        self.draw_number = 0
        self.folder_text = []

        self.textBrowser.clear()
        self.scene.clear()
        self.graphicsView.setScene(self.scene)


class StructureImage1(QMainWindow, ImageWindow1):
    def __init__(self):
        super(StructureImage1, self).__init__()
        self.setupUi(self)
        global image_list
        global structure
        image_list = []
        structure = None
        self.draw_number = 0
        self.folder_text = []
        self.remove_text = []

        self.pushButton_8.clicked.connect(self.load_structures)
        self.pushButton_7.clicked.connect(self.draw_structure)
        self.pushButton_3.clicked.connect(self.set_undo)
        self.pushButton_4.clicked.connect(self.set_redo)

    def load_structures(self):
        structure_names, _ = QFileDialog.getOpenFileNames(self, 'Open file', '.', "Structure (*.pdb *.cif)")
        for structure_name in structure_names:
            self.textBrowser.append(structure_name)

    def draw_structure(self):
        global image_list
        global structure

        structure_paths = [file for file in self.textBrowser.toPlainText().split("\n")]
        if self.draw_number == 0:
            structure = HighlightStructureImage(structure_paths=structure_paths)

        if self.textEdit.toPlainText() != "":
            structure.set_cache(cache_contents=[self.textEdit.toPlainText()])

        structure.save(save_path="./temp/image" + str(self.draw_number) + ".png")
        structure.save_pymol(save_path="./temp/image" + str(self.draw_number) + ".pse")

        if self.draw_number < len(image_list):
            image_list = image_list[:self.draw_number + 1]
        else:
            image_list.append("./temp/image" + str(self.draw_number) + ".png")

        if self.draw_number < len(self.folder_text):
            self.folder_text = self.folder_text[:self.draw_number + 1]
            self.folder_text[self.draw_number] = self.textBrowser.toPlainText()
        else:
            self.folder_text.append(self.textBrowser.toPlainText())

        if self.draw_number < len(self.remove_text):
            self.remove_text = self.remove_text[:self.draw_number + 1]
            self.remove_text[self.draw_number] = self.textEdit.toPlainText()
        else:
            self.remove_text.append(self.textEdit.toPlainText())

        figure = QPixmap("./temp/image" + str(self.draw_number) + ".png")
        self.scene.clear()
        self.scene.addPixmap(figure)
        self.graphicsView.setScene(self.scene)

        self.draw_number += 1

    def set_undo(self):
        global image_list
        global structure

        if self.draw_number > 1:
            self.scene.clear()
            figure = QPixmap(image_list[self.draw_number - 2])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.draw_number - 2) + ".pse")
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[self.draw_number - 2])
            self.textEdit.setText(self.remove_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.scene.clear()
            structure.clear()
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText("")
            self.textEdit.setText("")
            self.draw_number = 0

    def set_redo(self):
        global image_list
        global structure

        if self.draw_number < len(image_list):
            self.scene.clear()
            figure = QPixmap(image_list[self.draw_number])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.draw_number) + ".pse")
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[self.draw_number])
            self.textEdit.setText(self.remove_text[self.draw_number])
            self.draw_number += 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[-1])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[-1])
            self.textEdit.setText(self.remove_text[-1])

    def window_clear(self):
        global image_list
        global structure

        image_list = []
        if structure is not None:
            structure.close()
        self.draw_number = 0
        self.folder_text = []
        self.remove_text = []

        self.textBrowser.clear()
        self.textEdit.clear()
        self.scene.clear()
        self.graphicsView.setScene(self.scene)


class StructureImage2(QMainWindow, ImageWindow2):
    def __init__(self):
        super(StructureImage2, self).__init__()
        self.setupUi(self)
        global image_list
        global structure
        self.draw_number = 0
        self.start_number = 0
        self.style_text = []
        self.class_text = []
        self.range_text = []

        self.pushButton_7.clicked.connect(self.draw_structure)
        self.pushButton_3.clicked.connect(self.set_undo)
        self.pushButton_4.clicked.connect(self.set_redo)

    def start_image(self):
        if len(image_list) > 0:
            self.scene.addPixmap(QPixmap(image_list[-1]))
            self.graphicsView.setScene(self.scene)
            self.start_number = len(image_list)

    def draw_structure(self):
        global structure
        global image_list

        representation = self.comboBox_2.currentText()
        shading_type = self.comboBox_3.currentText()
        content = self.textEdit.toPlainText()

        structure.set_shape(representation_plan=[(shading_type + ":" + content, representation)],
                            initial_representation=None, independent_color=True, closed_surface=True)
        structure.save(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".png")
        structure.save_pymol(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")

        if self.start_number + self.draw_number < len(image_list):
            image_list = image_list[:self.start_number + self.draw_number + 1]
        else:
            image_list.append("./temp/image" + str(self.start_number + self.draw_number) + ".png")

        if self.draw_number < len(self.style_text):
            self.style_text = self.style_text[:self.draw_number + 1]
            self.style_text[self.draw_number] = representation
        else:
            self.style_text.append(representation)

        if self.draw_number < len(self.class_text):
            self.class_text = self.class_text[:self.draw_number + 1]
            self.class_text[self.draw_number] = shading_type
        else:
            self.class_text.append(shading_type)

        if self.draw_number < len(self.range_text):
            self.range_text = self.range_text[:self.draw_number + 1]
            self.range_text[self.draw_number] = content
        else:
            self.range_text.append(content)

        figure = QPixmap("./temp/image" + str(self.start_number + self.draw_number) + ".png")
        self.scene.clear()
        self.scene.addPixmap(figure)
        self.graphicsView.setScene(self.scene)

        self.draw_number += 1

    def set_undo(self):
        global image_list
        global structure

        if self.draw_number > 1:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number - 2])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 2) + ".pse")
            self.graphicsView.setScene(self.scene)
            self.comboBox_2.setCurrentText(self.style_text[self.draw_number - 2])
            self.comboBox_3.setCurrentText(self.class_text[self.draw_number - 2])
            self.textEdit.setText(self.range_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number - 1])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")
            self.graphicsView.setScene(self.scene)
            self.comboBox_2.setCurrentIndex(0)
            self.comboBox_3.setCurrentIndex(0)
            self.textEdit.setText("")
            self.draw_number = 0

    def set_redo(self):
        global image_list
        global structure

        if self.start_number + self.draw_number < len(image_list):
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")
            self.graphicsView.setScene(self.scene)
            self.comboBox_2.setCurrentText(self.style_text[self.draw_number])
            self.comboBox_3.setCurrentText(self.class_text[self.draw_number])
            self.textEdit.setText(self.range_text[self.draw_number])
            self.draw_number += 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[-1])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 1) + ".pse")
            self.comboBox_2.setCurrentText(self.style_text[-1])
            self.comboBox_3.setCurrentText(self.class_text[-1])
            self.textEdit.setText(self.range_text[-1])

    def window_clear(self):
        self.draw_number = 0
        self.start_number = 0
        self.style_text = []
        self.class_text = []
        self.range_text = []

        self.textEdit.clear()
        self.scene.clear()
        self.graphicsView.setScene(self.scene)

    def window_initialization(self):
        global structure
        global image_list

        if len(image_list) > 0:
            self.draw_number = 0
            self.style_text = []
            self.class_text = []
            self.range_text = []
            image_list = image_list[:self.start_number]

            self.textEdit.clear()
            self.scene.clear()
            self.scene.addPixmap(QPixmap(image_list[self.start_number - 1]))
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")


class StructureImage3(QMainWindow, ImageWindow3):
    def __init__(self):
        super(StructureImage3, self).__init__()
        self.setupUi(self)
        global image_list
        global structure
        self.draw_number = 0
        self.start_number = 0
        self.rotatex_text = []
        self.rotatey_text = []
        self.rotatez_text = []
        self.movex_text = []
        self.movey_text = []
        self.movez_text = []

        self.pushButton_7.clicked.connect(self.draw_structure)
        self.pushButton_3.clicked.connect(self.set_undo)
        self.pushButton_4.clicked.connect(self.set_redo)

    def start_image(self):
        if len(image_list) > 0:
            self.scene.addPixmap(QPixmap(image_list[-1]))
            self.graphicsView.setScene(self.scene)
            self.start_number = len(image_list)

    def draw_structure(self):
        global structure
        global image_list

        rotate_x = int(self.textEdit_2.toPlainText()) if self.textEdit_2.toPlainText() != "" else 0
        rotate_y = int(self.textEdit_1.toPlainText()) if self.textEdit_1.toPlainText() != "" else 0
        rotate_z = int(self.textEdit.toPlainText()) if self.textEdit.toPlainText() != "" else 0
        move_x = int(self.textEdit_3.toPlainText()) if self.textEdit_3.toPlainText() != "" else 0
        move_y = int(self.textEdit_4.toPlainText()) if self.textEdit_4.toPlainText() != "" else 0
        move_z = int(self.textEdit_5.toPlainText()) if self.textEdit_5.toPlainText() != "" else 0
        rotate = [rotate_x, rotate_y, rotate_z]

        if move_x == 0 and move_y == 0 and move_z == 0:
            if self.draw_number > 0:
                structure.set_state(rotate=rotate, only_rotate=True)
            else:
                structure.set_state(rotate=rotate)
        else:
            translate = [move_x, move_y, move_z]
            structure.set_state(rotate=rotate, translate=translate)

        structure.save(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".png")
        structure.save_pymol(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")

        if self.start_number + self.draw_number < len(image_list):
            image_list = image_list[:self.start_number + self.draw_number + 1]
        else:
            image_list.append("./temp/image" + str(self.start_number + self.draw_number) + ".png")

        if self.draw_number < len(self.rotatex_text):
            self.rotatex_text = self.rotatex_text[:self.draw_number + 1]
            self.rotatex_text[self.draw_number] = self.textEdit_2.toPlainText()
        else:
            self.rotatex_text.append(self.textEdit_2.toPlainText())

        if self.draw_number < len(self.rotatey_text):
            self.rotatey_text = self.rotatey_text[:self.draw_number + 1]
            self.rotatey_text[self.draw_number] = self.textEdit_1.toPlainText()
        else:
            self.rotatey_text.append(self.textEdit_1.toPlainText())

        if self.draw_number < len(self.rotatez_text):
            self.rotatez_text = self.rotatez_text[:self.draw_number + 1]
            self.rotatez_text[self.draw_number] = self.textEdit.toPlainText()
        else:
            self.rotatez_text.append(self.textEdit.toPlainText())

        if self.draw_number < len(self.movex_text):
            self.movex_text = self.movex_text[:self.draw_number + 1]
            self.movex_text[self.draw_number] = self.textEdit_3.toPlainText()
        else:
            self.movex_text.append(self.textEdit_3.toPlainText())

        if self.draw_number < len(self.movey_text):
            self.movey_text = self.movey_text[:self.draw_number + 1]
            self.movey_text[self.draw_number] = self.textEdit_4.toPlainText()
        else:
            self.movey_text.append(self.textEdit_4.toPlainText())

        if self.draw_number < len(self.movez_text):
            self.movez_text = self.movez_text[:self.draw_number + 1]
            self.movez_text[self.draw_number] = self.textEdit_5.toPlainText()
        else:
            self.movez_text.append(self.textEdit_5.toPlainText())

        figure = QPixmap("./temp/image" + str(self.start_number + self.draw_number) + ".png")
        self.scene.clear()
        self.scene.addPixmap(figure)
        self.graphicsView.setScene(self.scene)

        self.draw_number += 1

    def set_undo(self):
        global image_list
        global structure

        if self.draw_number > 1:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number - 2])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 2) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit_2.setText(self.rotatex_text[self.draw_number - 2])
            self.textEdit_1.setText(self.rotatey_text[self.draw_number - 2])
            self.textEdit.setText(self.rotatez_text[self.draw_number - 2])
            self.textEdit_3.setText(self.movex_text[self.draw_number - 2])
            self.textEdit_4.setText(self.movey_text[self.draw_number - 2])
            self.textEdit_5.setText(self.movez_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number - 1])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit.setText("")
            self.textEdit_1.setText("")
            self.textEdit_2.setText("")
            self.textEdit_3.setText("")
            self.textEdit_4.setText("")
            self.textEdit_5.setText("")
            self.draw_number = 0

    def set_redo(self):
        global image_list
        global structure

        if self.start_number + self.draw_number < len(image_list):
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit_2.setText(self.rotatex_text[self.draw_number])
            self.textEdit_1.setText(self.rotatey_text[self.draw_number])
            self.textEdit.setText(self.rotatez_text[self.draw_number])
            self.textEdit_3.setText(self.movex_text[self.draw_number])
            self.textEdit_4.setText(self.movey_text[self.draw_number])
            self.textEdit_5.setText(self.movez_text[self.draw_number])
            self.draw_number += 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[-1])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 1) + ".pse")

            self.textEdit_2.setText(self.rotatex_text[-1])
            self.textEdit_1.setText(self.rotatey_text[-1])
            self.textEdit.setText(self.rotatez_text[-1])
            self.textEdit_3.setText(self.movex_text[-1])
            self.textEdit_4.setText(self.movey_text[-1])
            self.textEdit_5.setText(self.movez_text[-1])

    def window_clear(self):
        self.draw_number = 0
        self.start_number = 0
        self.rotatex_text = []
        self.rotatey_text = []
        self.rotatez_text = []
        self.movex_text = []
        self.movey_text = []
        self.movez_text = []

        self.textEdit.clear()
        self.textEdit_1.clear()
        self.textEdit_2.clear()
        self.textEdit_3.clear()
        self.textEdit_4.clear()
        self.textEdit_5.clear()
        self.scene.clear()
        self.graphicsView.setScene(self.scene)

    def window_initialization(self):
        global structure
        global image_list
        if len(image_list) > 0:
            self.draw_number = 0
            self.rotatex_text = []
            self.rotatey_text = []
            self.rotatez_text = []
            self.movex_text = []
            self.movey_text = []
            self.movez_text = []
            image_list = image_list[:self.start_number]

            self.textEdit.clear()
            self.textEdit_1.clear()
            self.textEdit_2.clear()
            self.textEdit_3.clear()
            self.textEdit_4.clear()
            self.textEdit_5.clear()
            self.scene.clear()
            self.scene.addPixmap(QPixmap(image_list[self.start_number - 1]))
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")


class StructureImage4(QMainWindow, ImageWindow4):
    def __init__(self):
        super(StructureImage4, self).__init__()
        self.setupUi(self)
        global image_list
        global structure
        self.draw_number = 0
        self.start_number = 0
        self.color_text = []
        self.class_text = []
        self.range_text = []

        self.pushButton_7.clicked.connect(self.draw_structure)
        self.pushButton_3.clicked.connect(self.set_undo)
        self.pushButton_4.clicked.connect(self.set_redo)

    def start_image(self):
        if len(image_list) > 0:
            self.scene.addPixmap(QPixmap(image_list[-1]))
            self.graphicsView.setScene(self.scene)
            self.start_number = len(image_list)

    def draw_structure(self):
        global structure
        global image_list

        color = self.textEdit_1.toPlainText()
        shading_type = self.comboBox_3.currentText()
        range = self.textEdit.toPlainText()

        structure.set_color(coloring_plan=[(shading_type + ":" + range, color)], initial_color=None)
        structure.save(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".png")
        structure.save_pymol(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")

        if self.start_number + self.draw_number < len(image_list):
            image_list = image_list[:self.start_number + self.draw_number + 1]
        else:
            image_list.append("./temp/image" + str(self.start_number + self.draw_number) + ".png")

        if self.draw_number < len(self.color_text):
            self.color_text = self.color_text[:self.draw_number + 1]
            self.color_text[self.draw_number] = color
        else:
            self.color_text.append(color)

        if self.draw_number < len(self.class_text):
            self.class_text = self.class_text[:self.draw_number + 1]
            self.class_text[self.draw_number] = shading_type
        else:
            self.class_text.append(shading_type)

        if self.draw_number < len(self.range_text):
            self.range_text = self.range_text[:self.draw_number + 1]
            self.range_text[self.draw_number] = range
        else:
            self.range_text.append(range)

        figure = QPixmap("./temp/image" + str(self.start_number + self.draw_number) + ".png")
        self.scene.clear()
        self.scene.addPixmap(figure)
        self.graphicsView.setScene(self.scene)

        self.draw_number += 1

    def save_image(self, label_text, ratio):
        global structure
        global image_list
        if len(image_list) > 0:
            structure.save(save_path="./temp/panel_" + label_text + ".png", ratio=ratio)

    def set_undo(self):
        global image_list
        global structure

        if self.draw_number > 1:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number - 2])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 2) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit_1.setText(self.color_text[self.draw_number - 2])
            self.comboBox_3.setCurrentText(self.class_text[self.draw_number - 2])
            self.textEdit.setText(self.range_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number - 1])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit_1.setText("")
            self.comboBox_3.setCurrentIndex(0)
            self.textEdit.setText("")
            self.draw_number = 0

    def set_redo(self):
        global image_list
        global structure

        if self.start_number + self.draw_number < len(image_list):
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit_1.setText(self.color_text[self.draw_number])
            self.comboBox_3.setCurrentText(self.class_text[self.draw_number])
            self.textEdit.setText(self.range_text[self.draw_number])
            self.draw_number += 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[-1])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 1) + ".pse")

            self.textEdit_1.setText(self.color_text[-1])
            self.comboBox_3.setCurrentText(self.class_text[-1])
            self.textEdit.setText(self.range_text[-1])

    def window_clear(self):
        self.draw_number = 0
        self.start_number = 0
        self.color_text = []
        self.class_text = []
        self.range_text = []

        self.textEdit.clear()
        self.textEdit_1.clear()
        self.scene.clear()
        self.graphicsView.setScene(self.scene)

    def window_initialization(self):
        global structure
        global image_list

        if len(image_list) > 0:
            self.draw_number = 0
            self.color_text = []
            self.class_text = []
            self.range_text = []
            image_list = image_list[:self.start_number]

            self.textEdit.clear()
            self.textEdit_1.clear()
            self.scene.clear()
            self.scene.addPixmap(QPixmap(image_list[self.start_number - 1]))
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    entry_window = EntryWindow()
    select_window = SelectWindow()
    statistical_window = StatisticalWindow()
    structure_window1 = StructureImage1()
    structure_window2 = StructureImage2()
    structure_window3 = StructureImage3()
    structure_window4 = StructureImage4()

    entry_window.show()

    entry_window.comboBox_4.activated.connect(select_window.show)
    entry_window.comboBox_4.activated.connect(entry_window.hide)

    select_window.pushButton.clicked.connect(structure_window1.show)
    select_window.pushButton.clicked.connect(select_window.hide)
    select_window.pushButton_2.clicked.connect(statistical_window.show)
    select_window.pushButton_2.clicked.connect(select_window.hide)
    select_window.pushButton_3.clicked.connect(select_window.hide)
    select_window.pushButton_3.clicked.connect(entry_window.show)

    statistical_window.pushButton_5.clicked.connect(statistical_window.hide)
    statistical_window.pushButton_5.clicked.connect(select_window.show)
    statistical_window.pushButton_5.clicked.connect(statistical_window.window_clear)
    statistical_window.pushButton_6.clicked.connect(entry_window.show)
    statistical_window.pushButton_6.clicked.connect(statistical_window.hide)
    statistical_window.pushButton_6.clicked.connect(
        lambda: statistical_window.save_image(entry_window.comboBox_4.currentText()))
    statistical_window.pushButton_6.clicked.connect(entry_window.image_set)
    statistical_window.pushButton_6.clicked.connect(statistical_window.window_clear)

    structure_window1.pushButton_5.clicked.connect(structure_window1.hide)
    structure_window1.pushButton_5.clicked.connect(select_window.show)
    structure_window1.pushButton_5.clicked.connect(structure_window1.window_clear)
    structure_window1.pushButton_6.clicked.connect(structure_window2.show)
    structure_window1.pushButton_6.clicked.connect(structure_window1.hide)
    structure_window1.pushButton_6.clicked.connect(structure_window2.start_image)

    structure_window2.pushButton_5.clicked.connect(structure_window2.hide)
    structure_window2.pushButton_5.clicked.connect(structure_window1.show)
    structure_window2.pushButton_5.clicked.connect(structure_window2.window_initialization)
    structure_window2.pushButton_6.clicked.connect(structure_window3.show)
    structure_window2.pushButton_6.clicked.connect(structure_window2.hide)
    structure_window2.pushButton_6.clicked.connect(structure_window3.start_image)

    structure_window3.pushButton_5.clicked.connect(structure_window3.hide)
    structure_window3.pushButton_5.clicked.connect(structure_window2.show)
    structure_window3.pushButton_5.clicked.connect(structure_window3.window_initialization)
    structure_window3.pushButton_6.clicked.connect(structure_window4.show)
    structure_window3.pushButton_6.clicked.connect(structure_window3.hide)
    structure_window3.pushButton_6.clicked.connect(structure_window4.start_image)

    structure_window4.pushButton_5.clicked.connect(structure_window4.hide)
    structure_window4.pushButton_5.clicked.connect(structure_window3.show)
    structure_window4.pushButton_5.clicked.connect(structure_window4.window_initialization)
    structure_window4.pushButton_6.clicked.connect(entry_window.show)
    structure_window4.pushButton_6.clicked.connect(structure_window4.hide)
    structure_window4.pushButton_6.clicked.connect(
        lambda: structure_window4.save_image(entry_window.comboBox_4.currentText(),
                                             entry_window.calculate_imageratio()))
    structure_window4.pushButton_6.clicked.connect(entry_window.image_set)
    structure_window4.pushButton_6.clicked.connect(structure_window1.window_clear)
    structure_window4.pushButton_6.clicked.connect(structure_window2.window_clear)
    structure_window4.pushButton_6.clicked.connect(structure_window3.window_clear)
    structure_window4.pushButton_6.clicked.connect(structure_window4.window_clear)

    sys.exit(app.exec_())
