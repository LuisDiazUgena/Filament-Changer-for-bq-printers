from PySide import QtCore,QtGui
from PySide import QtUiTools
import os, sys

def load_ui(file_name, where=None):
    """
    Loads a .UI file into the corresponding Qt Python object
    :param file_name: UI file path
    :param where: Use this parameter to load the UI into an existing class (i.e. to override methods)
    :return: loaded UI
    """
    # Create a QtLoader
    loader = QtUiTools.QUiLoader()

    # Open the UI file
    ui_file = QtCore.QFile(file_name)
    ui_file.open(QtCore.QFile.ReadOnly)

    # Load the contents of the file
    ui = loader.load(ui_file, where)

    # Close the file
    ui_file.close()

    return ui

class FilamentChanger(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUI()

    def setupUI(self):
        ui_file_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'filamentchanger.ui')
        main_widget = load_ui(ui_file_path, self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(main_widget)
        self.setLayout(layout)
        self.setWindowTitle("Filament Changer for Marlin 3D Printers")
        #Get a reference to all required widgets
        self.BrowseButton = self.findChild(QtGui.QToolButton,'BrowseButton')
        self.FileLineEdit = self.findChild(QtGui.QLineEdit,'FileLineEdit')
        self.LayerSpinBox = self.findChild(QtGui.QSpinBox,'LayerSpinBox')
        self.EnabledCheckBox = self.findChild(QtGui.QCheckBox,'EnabledCheckBox')

        self.ExportBtn = self.findChild(QtGui.QToolButton,'ExportBtn')
        self.ResetBtn = self.findChild(QtGui.QToolButton,'ResetBtn')
        #Configure widget ranges
        #Todo: Change the max value to the last layer of the script.
        #max_layer = sys.float_info.max
        #self.LayerSpinBox.setMaximum(max_layer)

if __name__ == '__main__':

    # Create Qt app
    app = QtGui.QApplication(sys.argv)

    # Create the widget and show it
    gui = FilamentChanger()
    gui.show()

    # Run the app
    sys.exit(app.exec_())
