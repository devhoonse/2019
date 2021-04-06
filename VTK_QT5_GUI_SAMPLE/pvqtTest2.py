# encoding: utf-8


from __future__ import print_function
import os
import vtk
from paraview import simple

from PyQt5 import QtCore, QtGui, uic, QtWidgets
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class ViewerApp(QtWidgets.QMainWindow):
    def __init__(self):
        # Parent Constructor
        super(ViewerApp, self).__init__()

        self.ui = None
        self.vtk_widget = None
        self.setup()

    def setup(self):
        import pyqtUI2

        self.ui = pyqtUI2.Ui_MainWindow()
        self.ui.setupUi(self)

        self.vtk_widget = QViewer(self.ui.vtk_panel)

        self.ui.vtk_layout = QtWidgets.QHBoxLayout()
        self.ui.vtk_layout.addWidget(self.vtk_widget)
        self.ui.vtk_layout.setContentsMargins(0, 0, 0, 0)

        self.ui.vtk_panel.setLayout(self.ui.vtk_layout)

        self.ui.opacity_slider.setValue(50)
        self.ui.opacity_slider.valueChanged.connect(self.vtk_widget.set_opacity)

        self.ui.shrink_slider.setValue(50)
        self.ui.shrink_slider.valueChanged.connect(self.vtk_widget.set_shrink)

    def initialize(self):
        self.vtk_widget.start()


class QViewer(QtWidgets.QFrame):
    def __init__(self, parent):
        # Parent Constructor
        super(QViewer, self).__init__(parent)

        # Set QVTKRenderWindowInteractor
        self.interactor = QVTKRenderWindowInteractor(self)

        # Initialize LayOut Object
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.interactor)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Set Layout
        self.setLayout(self.layout)

        # ===================== Construct ParaView PipeLine =====================
        # Set RenderView and Renderer
        self.renderView = simple.GetActiveViewOrCreate('RenderView')

        # Get Renderer
        self.renderer = self.renderView.GetRenderer()

        # Set RenderWindow
        self.renderWindow = self.interactor.GetRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)

        # Get InteractorStyle
        self.interactorStyle = self.interactor.GetInteractorStyle()

        # Set Interactor
        self.renderWindow.SetInteractor(self.interactor)

        # Set Background
        self.renderer.SetBackground(0.2, 0.2, 0.2)

        # Make Sphere Source
        self.sphere = simple.Sphere(Radius=1.0, Center=[0, 1, 0])
        self.sphereDisplay = simple.Show(self.sphere, self.renderView)

        # Set Opacity of Sphere Source
        self.sphereDisplay.Opacity = 0.5

        # Make Shrink Filter to Sphere Source
        self.sphereShrink = simple.Shrink(Input=self.sphere, ShrinkFactor=0.5)
        self.sphereShrinkDisplay = simple.Show(self.sphereShrink, self.renderView)

        simple.Render()
        # =======================================================================

    def start(self):
        self.interactor.Initialize()
        self.interactor.Start()

    def set_opacity(self, new_value):
        float_value = new_value/100.0
        self.sphereDisplay.Opacity = float_value
        self.renderWindow.Render()

    def set_shrink(self, new_value):
        float_value = new_value/100.0
        self.sphereShrink.SetPropertyWithName('ShrinkFactor', float_value)
        self.sphereShrinkDisplay = simple.Show(self.sphereShrink, self.renderView)
        self.renderView.Update()
        self.renderWindow.Render()


if __name__ == "__main__":

    os.chdir(os.path.dirname(__file__))

    # Recompile UI
    """with open("untitled.ui") as ui_file:
        with open("pyqtUI2.py", 'w') as py_ui_file:
            uic.compileUi(ui_file, py_ui_file)
    print(u'>> {}'.format("pyqtUI2.py"))"""

    app = QtWidgets.QApplication([])
    main_window = ViewerApp()
    main_window.show()
    main_window.initialize()
    app.exec_()
