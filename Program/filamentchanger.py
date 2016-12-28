from PySide import QtCore,QtGui
from PySide import QtUiTools
import os, sys
import os.path as osp
import ctypes #For adding the icon to windows taskbar

#Add icon info
icon_path = osp.join(osp.dirname(sys.modules[__name__].__file__), 'icon_filament.png')
myappid = u'DrMaker.filamentchanger' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

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
        self.setWindowIcon(QtGui.QIcon(icon_path))
        #Get a reference to all required widgets
        #LineEdits
        self.FileLineEdit = self.findChild(QtGui.QLineEdit,'FileLineEdit')

        #SpinBoxs
        self.LayerSpinBox = self.findChild(QtGui.QSpinBox,'LayerSpinBox')

        #CheckBox
        self.EnabledCheckBox = self.findChild(QtGui.QCheckBox,'EnabledCheckBox')
        self.CuraCheckBox = self.findChild(QtGui.QCheckBox,'CuraCheckBox')
        self.Simplify3DCheckBox = self.findChild(QtGui.QCheckBox,'Simplify3DCheckBox')
        self.Slic3rCheckBox = self.findChild(QtGui.QCheckBox,'Slic3rCheckBox')

        #Buttons
        self.ExportBtn = self.findChild(QtGui.QPushButton,'ExportBtn')
        self.ResetBtn = self.findChild(QtGui.QPushButton,'ResetBtn')
        self.BrowseButton = self.findChild(QtGui.QPushButton,'BrowseButton')

        #Configure widget ranges
        #TODO: Change the max value to the last layer of the script.
        #max_layer = sys.float_info.max
        #self.LayerSpinBox.setMaximum(max_layer)

        #Connect slot and signals
        #CheckBoxs
        self.EnabledCheckBox.stateChanged.connect(self.onEnabledCheckBoxChangedState)
        self.CuraCheckBox.stateChanged.connect(self.onCuraCheckBoxChangedState)
        self.Simplify3DCheckBox.stateChanged.connect(self.onSimplify3DCheckBoxChangedState)
        self.Slic3rCheckBox.stateChanged.connect(self.onSlic3rCheckBoxChangedState)
        #Buttons
        self.ExportBtn.clicked.connect(self.onExportBtnClicked)
        self.ResetBtn.clicked.connect(self.onResetBtnClicked)
        self.BrowseButton.clicked.connect(self.OnBrowseButtonClicked)

    #functions

    #buttons related functions
    def onSaveButtonClicked(self):
        reply = QtGui.QMessageBox.question(parent=self, title='Attention',
                                           text='File will be overwritten.\nDo you still want to proceed?',
                                           buttons=QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                           defaultButton=QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            print("response is yes")
            #TODO Add save function

    def OnBrowseButtonClicked(self):
        print("OnBrowseButtonClicked")
        #TODO Create browse routine
        filename, filter = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.', filter='gcode files(*.gcode)')
        if filename:
            self.FileLineEdit.setText(filename)
            LookForLayers(filename)

    def onExportBtnClicked(self):
        print("onExportBtnClicked")
        #TODO Create export routine
        filename, filter = QtGui.QFileDialog.getSaveFileName(parent=self, caption='Select output file', dir='.', filter='*.gcode')
        if filename:
            if '.gcode' != filename[-6]:
                filename += '.gcode'

            print("File saved!")

    def onResetBtnClicked(self):
        print("onResetBtnClicked")
        #TODO Create reset routine

    #Checkbox related functions
    def onCuraCheckBoxChangedState(self,checked):
        self.CuraCheckBox.setChecked(bool(checked))
        if self.CuraCheckBox.isChecked():
            self.Simplify3DCheckBox.setChecked(False)
            self.Slic3rCheckBox.setChecked(False)
    def onSimplify3DCheckBoxChangedState(self,checked):
        self.Simplify3DCheckBox.setChecked(bool(checked))
        if self.Simplify3DCheckBox.isChecked():
            self.CuraCheckBox.setChecked(False)
            self.Slic3rCheckBox.setChecked(False)
    def onSlic3rCheckBoxChangedState(self,checked):
        self.Slic3rCheckBox.setChecked(bool(checked))
        if self.Slic3rCheckBox.isChecked():
            self.Simplify3DCheckBox.setChecked(False)
            self.CuraCheckBox.setChecked(False)
    def onEnabledCheckBoxChangedState(self, checked):
        self.EnabledCheckBox.setChecked(bool(checked))

def LookForLayers(filename):
    filename = os.path.abspath(os.path.realpath(filename))
    datafile = open(filename,'r')
    count = 0
    for line in datafile:
        if 'layer' in line:
            count += 1

    print("Found layer " + repr(count) +" times")
if __name__ == '__main__':

    # Create Qt app
    app = QtGui.QApplication(sys.argv)

    # Create the widget and show it
    gui = FilamentChanger()
    gui.show()

    # Run the app
    sys.exit(app.exec_())
