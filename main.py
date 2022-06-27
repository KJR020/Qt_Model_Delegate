import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel
from listviewCRUD_ui import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore


class Model(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self.items = []

    def addItems(self, items):
        self.beginInsertRows(
            QtCore.QModelIndex(), len(self.items), len(self.items) + len(items) - 1
        )
        self.items.extend(items)
        self.endInsertRows()

    def columnCount(self, parent):
        return 1

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            return self.items[index.row()]

    def flags(self, index):
        return (
            QtCore.Qt.ItemIsEditable
            | QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsSelectable
        )

    def headerData(self, i, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return i
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return i

    def index(self, row, column=0, parent=QtCore.QModelIndex()):
        return self.createIndex(row, column, parent)

    def parent(self, index):
        return QtCore.QModelIndex()

    def removeItems(self, rows):
        sec = [[rows[0], rows[0] + 1]]
        for row in rows[1:]:
            if sec[-1][1] == row:
                sec[-1][1] = sec[-1][1] + 1
                continue
            sec.append([row, row + 1])

        for s in sec[::-1]:
            self.beginRemoveRows(QtCore.QModelIndex(), s[0], s[1])
            del self.items[s[0] : s[1]]
            self.endRemoveRows()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.items)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCOre.Qt.EditRole:
            self.items[index.row()] = value
            return True
        return False


class Delegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None, setModelDataEvent=None):
        super(Delegate, self).__init__(parent)
        self.setModelDataEvent = setModelDataEvent

    def createEditor(self, parent, option, index):
        return QtWidgets.QLineEdit(parent)

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        editor.setText(str(value))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())
        if not self.setModelDataEvent is None:
            self.setModelDataEvent()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = Model(self)
        self.ui.listView.setModel(self.model)
        self.ui.listView.setItemDelegate(Delegate())
        self.ui.listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.listView.customContextMenuRequested.connect(self.contextMenu)
        self.ui.listView.setAlternatingRowColors(True)

        self.ui.pushButton_2.clicked.connect(self.addItem)
        self.ui.pushButton_3.clicked.connect(self.delItem)

    def contextMenu(self, point):
        self.menu = QtWidgets.QMenu(self)
        self.menu.addAction("追加", self.addItem)
        self.menu.addAction("削除", self.delItem)
        self.menu.exec_(self.ui.listView.mapToGlobal(point))

    def addItem(self):
        self.model.addItems([str(self.model.rowCount())])

    def delItem(self):
        if len(self.ui.listView.selectedIndexes()) == 0:
            return
        rows = [index.row() for index in self.ui.listView.selectedIndexes()]
        self.model.removeItems(rows)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
