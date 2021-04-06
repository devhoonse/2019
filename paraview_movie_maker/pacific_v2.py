# encoding: utf-8
# trace generated using paraview version 5.6.0
#
# To ensure correct image size when batch processing, please search
# for and uncomment the line `# renderView*.ViewSize = [*,*]`


# import time module
import time
import datetime

# import os module
import os

# import sys module
import sys

# import json module
import json

#### import the simple module from the paraview
from paraview.simple import *

#### import the servermanager module from the paraview
import paraview.servermanager as sm

#### import the VTK
import vtk


class vtkTimerCallback():
    def __init__(self):
        self.timer_count = 0

    def execute(self, obj, event):
        iren = obj
        event()


class vtkSliderCallback():
    def __init__(self, tk):
        self.tk = tk

    def execute(self, caller, event):
        # sw = caller
        # self.rv.SetPropertyWithName('ViewTime', sw.GetRepresentation().GetValue())
        self.tk.SetPropertyWithName('Time', caller.GetRepresentation().GetValue())
        self.tk.Views[0].ViewTime = caller.GetRepresentation().GetValue()
        self.tk.Views[0].Update()


class vtkSubclassPlaybackRepresentation(vtk.vtkPlaybackRepresentation):
    def __init__(self):
        pass

    def Play(self):
        pass

    def Stop(self):
        pass

    def ForwardOneFrame(self):
        pass

    def BackwardOneFrame(self):
        pass

    def JumpToBeginning(self):
        pass

    def JumpToEnd(self):
        pass


class ActiveView:

    def __init__(self, input_sl_dll_path, input_etopo_south_nc_path, input_sea_2d_nc_path,
                 input_time_font_ttf_path, use_time_label=True, input_view_size_h=880, input_view_size_v=500):
        """Initialize the PIpeLine Object with Default Settings
            PipeLine
               │
               ├─etopo11.nc / netCDFReader() : etopo 자료 READER
               │     │
               │  ExtractSubset1 / ExtractSubset() : etopo Subset 추출
               │     │
               │     ├─Threshold1 / Threshold() : Ocean Area (2D)
               │     │       │
               │     │  Calculator1 / Calculator() : Ocean Bathemetry (3D)
               │     │
               │     └─Threshold2 / Threshold() : Land Area (2D)
               │              │
               │         Calculator2 / Calculator() : Land Topography (3D)
               │
               └─sea_2d.nc / netCDFReader() : sea 표층자료 READER
                        │
                   ExtractSubset2 / ExtractSubset() : sea 표층자료 Subset 추출
                        │
                   ExtractTimeSteps1 / ExtractTimeSteps() : TimeStep Range 제어
                        │
                   Threshold3 / Threshold() : mask_rho Array값이 1인 영역
                        │
                        ├─Calculator3 / Calculator() : uv 벡터 (StreamLine Representation)
                        │
                        ├─Calculator4 / Calculator() : uv 벡터 (유속 Surface Representation)
                        │
                        └─ProgrammableFilter1 / ProgrammableFilter(): TimeStep→String(YYYY년 MM월 DD일) Array 생성
                                    │
                            PythonAnnotation1 / PythonAnnotation() : 생성된 Array 값을 Annotation으로 View에 추가
            """

        self.DATUM = datetime.datetime(1968, 5, 23, 0, 0, 0)

        self.sl_dll_path = u'%s' % input_sl_dll_path
        self.etopo_south_nc_path = u'%s' % input_etopo_south_nc_path
        self.sea_2d_nc_path = u'%s' % input_sea_2d_nc_path
        self.time_font_ttf_path = u'%s' % input_time_font_ttf_path
        self.show_time_label = use_time_label
        self.view_size_h = int(input_view_size_h)
        self.view_size_v = int(input_view_size_v)

        self.current_time_str = os.path.basename(self.sea_2d_nc_path).split(u'.')[0].split(u'_')[-1]

        #### Load Plug-In "StreamLinesRepresentations"
        sm.LoadPlugin(filename=self.sl_dll_path)

        # create a new 'NetCDF Reader'
        self.etopo11nc = NetCDFReader(FileName=[self.etopo_south_nc_path])
        self.etopo11nc.Dimensions = '(latitude, longitude)'

        # Properties modified on etopo11nc
        self.etopo11nc.SphericalCoordinates = 0

        # get active view
        self.renderView1 = GetActiveViewOrCreate('RenderView')

        # Hide the Orientation Axes
        self.renderView1.OrientationAxesVisibility = 0

        # self.renderView1.UseOffscreenRendering = 1

        # uncomment following to set a specific view size
        self.renderView1.ViewSize = [self.view_size_h, self.view_size_v]

        # Set the Center of Rotation for Reder View
        self.renderView1.SetPropertyWithName("CenterOfRotation",
                                             [191.0, 25.0, 0.0])

        self.renderView1.Update()

        # Get Active Renderer
        self.renderer1 = self.renderView1.GetRenderer()

        # Set Interactive Renderer On
        self.renderer1.InteractiveOn()

        # Set DepthPeelingForVolumes Off
        self.renderer1.UseDepthPeelingForVolumesOff()

        # Get Active Renderer
        self.camera1 = self.renderView1.GetActiveCamera()

        # show data in view
        self.etopo11ncDisplay = Show(self.etopo11nc, self.renderView1)

        # get color transfer function/color map for 'Band1'
        self.band1LUT = GetColorTransferFunction('altitude')

        # get opacity transfer function/opacity map for 'Band1'
        self.band1PWF = GetOpacityTransferFunction('altitude')

        # trace defaults for the display properties.
        self.etopo11ncDisplay.Representation = 'Slice'
        self.etopo11ncDisplay.AmbientColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.ColorArrayName = ['POINTS', 'altitude']
        self.etopo11ncDisplay.LookupTable = self.band1LUT
        self.etopo11ncDisplay.OSPRayScaleArray = 'altitude'
        self.etopo11ncDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
        self.etopo11ncDisplay.SelectOrientationVectors = 'altitude'
        self.etopo11ncDisplay.ScaleFactor = 2.8899999999999997
        self.etopo11ncDisplay.SelectScaleArray = 'altitude'
        self.etopo11ncDisplay.GlyphType = 'Arrow'
        self.etopo11ncDisplay.GlyphTableIndexArray = 'altitude'
        self.etopo11ncDisplay.GaussianRadius = 0.1445
        self.etopo11ncDisplay.SetScaleArray = ['POINTS', 'altitude']
        self.etopo11ncDisplay.ScaleTransferFunction = 'PiecewiseFunction'
        self.etopo11ncDisplay.OpacityArray = ['POINTS', 'altitude']
        self.etopo11ncDisplay.OpacityTransferFunction = 'PiecewiseFunction'
        self.etopo11ncDisplay.DataAxesGrid = 'GridAxesRepresentation'
        self.etopo11ncDisplay.SelectionCellLabelFontFile = ''
        self.etopo11ncDisplay.SelectionPointLabelFontFile = ''
        self.etopo11ncDisplay.PolarAxes = 'PolarAxesRepresentation'
        self.etopo11ncDisplay.ScalarOpacityUnitDistance = 0.27958843910525977
        self.etopo11ncDisplay.ScalarOpacityFunction = self.band1PWF
        self.etopo11ncDisplay.InputVectors = [None, '']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.etopo11ncDisplay.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.DataAxesGrid.XTitleFontFile = ''
        self.etopo11ncDisplay.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.DataAxesGrid.YTitleFontFile = ''
        self.etopo11ncDisplay.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.DataAxesGrid.ZTitleFontFile = ''
        self.etopo11ncDisplay.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.DataAxesGrid.XLabelFontFile = ''
        self.etopo11ncDisplay.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.DataAxesGrid.YLabelFontFile = ''
        self.etopo11ncDisplay.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.etopo11ncDisplay.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.PolarAxes.PolarAxisTitleFontFile = ''
        self.etopo11ncDisplay.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.PolarAxes.PolarAxisLabelFontFile = ''
        self.etopo11ncDisplay.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
        self.etopo11ncDisplay.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.etopo11ncDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # reset view to fit data
        self.renderView1.ResetCamera()

        # changing interaction mode based on data extents
        self.renderView1.InteractionMode = '3D'
        self.renderView1.CameraPosition = [191, 25, 173.909]
        self.renderView1.CameraFocalPoint = [191, 25, -225.269]
        self.renderView1.CameraParallelScale = 103.315
        self.renderView1.CameraViewUp = [0, 1, 0]
        self.renderView1.CameraViewAngle = 30

        # get the material library
        self.materialLibrary1 = GetMaterialLibrary()

        # show color bar/color legend
        self.etopo11ncDisplay.SetScalarBarVisibility(self.renderView1, True)

        # hide data in view
        Hide(self.etopo11nc, self.renderView1)

        # update the view to ensure updated data information
        self.renderView1.Update()

        # create a new 'Extract Subset'
        self.extractSubset1 = ExtractSubset(Input=self.etopo11nc)

        # Properties modified on extractSubset1
        self.extractSubset1.VOI = [0, 11160, 0, 5100, 0, 0]
        self.extractSubset1.SampleRateI = 1
        self.extractSubset1.SampleRateJ = 1
        self.extractSubset1.SampleRateK = 1

        # show data in view
        self.extractSubset1Display = Show(self.extractSubset1, self.renderView1)

        # trace defaults for the display properties.
        self.extractSubset1Display.Representation = 'Slice'
        self.extractSubset1Display.AmbientColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.ColorArrayName = ['POINTS', 'altitude']
        self.extractSubset1Display.LookupTable = self.band1LUT
        self.extractSubset1Display.OSPRayScaleArray = 'altitude'
        self.extractSubset1Display.OSPRayScaleFunction = 'PiecewiseFunction'
        self.extractSubset1Display.SelectOrientationVectors = 'altitude'
        self.extractSubset1Display.ScaleFactor = 1.966666666666666
        self.extractSubset1Display.SelectScaleArray = 'altitude'
        self.extractSubset1Display.GlyphType = 'Arrow'
        self.extractSubset1Display.GlyphTableIndexArray = 'altitude'
        self.extractSubset1Display.GaussianRadius = 0.09833333333333329
        self.extractSubset1Display.SetScaleArray = ['POINTS', 'altitude']
        self.extractSubset1Display.ScaleTransferFunction = 'PiecewiseFunction'
        self.extractSubset1Display.OpacityArray = ['POINTS', 'altitude']
        self.extractSubset1Display.OpacityTransferFunction = 'PiecewiseFunction'
        self.extractSubset1Display.DataAxesGrid = 'GridAxesRepresentation'
        self.extractSubset1Display.SelectionCellLabelFontFile = ''
        self.extractSubset1Display.SelectionPointLabelFontFile = ''
        self.extractSubset1Display.PolarAxes = 'PolarAxesRepresentation'
        self.extractSubset1Display.ScalarOpacityUnitDistance = 0.24821281318555447
        self.extractSubset1Display.ScalarOpacityFunction = self.band1PWF
        self.extractSubset1Display.InputVectors = [None, '']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.extractSubset1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.DataAxesGrid.XTitleFontFile = ''
        self.extractSubset1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.DataAxesGrid.YTitleFontFile = ''
        self.extractSubset1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.DataAxesGrid.ZTitleFontFile = ''
        self.extractSubset1Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.DataAxesGrid.XLabelFontFile = ''
        self.extractSubset1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.DataAxesGrid.YLabelFontFile = ''
        self.extractSubset1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.extractSubset1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.PolarAxes.PolarAxisTitleFontFile = ''
        self.extractSubset1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.PolarAxes.PolarAxisLabelFontFile = ''
        self.extractSubset1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.PolarAxes.LastRadialAxisTextFontFile = ''
        self.extractSubset1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.extractSubset1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # show color bar/color legend
        self.extractSubset1Display.SetScalarBarVisibility(self.renderView1, True)

        # hide data in view
        Hide(self.extractSubset1, self.renderView1)

        # update the view to ensure updated data information
        self.renderView1.Update()

        # create a new 'Threshold'
        self.threshold1 = Threshold(Input=self.extractSubset1)
        self.threshold1.Scalars = ['POINTS', 'altitude']
        self.threshold1.ThresholdRange = [-7439.0, 3577.0]

        # Properties modified on threshold1
        self.threshold1.ThresholdRange = [-7439.0, 0.0]
        self.threshold1.AllScalars = 0

        # show data in view
        self.threshold1Display = Show(self.threshold1, self.renderView1)

        # trace defaults for the display properties.
        self.threshold1Display.Representation = 'Surface'
        self.threshold1Display.AmbientColor = [0.0, 0.0, 0.0]
        self.threshold1Display.ColorArrayName = ['POINTS', 'altitude']
        self.threshold1Display.LookupTable = self.band1LUT
        self.threshold1Display.OSPRayScaleArray = 'altitude'
        self.threshold1Display.OSPRayScaleFunction = 'PiecewiseFunction'
        self.threshold1Display.SelectOrientationVectors = 'altitude'
        self.threshold1Display.ScaleFactor = 1.9666656494140626
        self.threshold1Display.SelectScaleArray = 'altitude'
        self.threshold1Display.GlyphType = 'Arrow'
        self.threshold1Display.GlyphTableIndexArray = 'altitude'
        self.threshold1Display.GaussianRadius = 0.09833328247070312
        self.threshold1Display.SetScaleArray = ['POINTS', 'altitude']
        self.threshold1Display.ScaleTransferFunction = 'PiecewiseFunction'
        self.threshold1Display.OpacityArray = ['POINTS', 'altitude']
        self.threshold1Display.OpacityTransferFunction = 'PiecewiseFunction'
        self.threshold1Display.DataAxesGrid = 'GridAxesRepresentation'
        self.threshold1Display.SelectionCellLabelFontFile = ''
        self.threshold1Display.SelectionPointLabelFontFile = ''
        self.threshold1Display.PolarAxes = 'PolarAxesRepresentation'
        self.threshold1Display.ScalarOpacityFunction = self.band1PWF
        self.threshold1Display.ScalarOpacityUnitDistance = 0.27141932816969944
        self.threshold1Display.InputVectors = [None, '']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.threshold1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.threshold1Display.DataAxesGrid.XTitleFontFile = ''
        self.threshold1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.threshold1Display.DataAxesGrid.YTitleFontFile = ''
        self.threshold1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.threshold1Display.DataAxesGrid.ZTitleFontFile = ''
        self.threshold1Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.threshold1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.threshold1Display.DataAxesGrid.XLabelFontFile = ''
        self.threshold1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.threshold1Display.DataAxesGrid.YLabelFontFile = ''
        self.threshold1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.threshold1Display.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.threshold1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.threshold1Display.PolarAxes.PolarAxisTitleFontFile = ''
        self.threshold1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.threshold1Display.PolarAxes.PolarAxisLabelFontFile = ''
        self.threshold1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.threshold1Display.PolarAxes.LastRadialAxisTextFontFile = ''
        self.threshold1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.threshold1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # show color bar/color legend
        self.threshold1Display.SetScalarBarVisibility(self.renderView1, True)

        # hide data in view
        Hide(self.threshold1, self.renderView1)

        # update the view to ensure updated data information
        self.renderView1.Update()

        # create a new 'Calculator'
        self.calculator1 = Calculator(Input=self.threshold1)
        self.calculator1.Function = ''

        # Properties modified on calculator1
        self.calculator1.CoordinateResults = 1
        self.calculator1.Function = 'coordsX*iHat+coordsY*jHat+kHat*altitude/2000'

        # show data in view
        self.calculator1Display = Show(self.calculator1, self.renderView1)

        # trace defaults for the display properties.
        self.calculator1Display.Representation = 'Surface'
        self.calculator1Display.AmbientColor = [0.0, 0.0, 0.0]
        self.calculator1Display.ColorArrayName = ['POINTS', 'altitude']
        self.calculator1Display.LookupTable = self.band1LUT
        self.calculator1Display.OSPRayScaleArray = 'altitude'
        self.calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
        self.calculator1Display.SelectOrientationVectors = 'altitude'
        self.calculator1Display.ScaleFactor = 1.9666656494140626
        self.calculator1Display.SelectScaleArray = 'altitude'
        self.calculator1Display.GlyphType = 'Arrow'
        self.calculator1Display.GlyphTableIndexArray = 'altitude'
        self.calculator1Display.GaussianRadius = 0.09833328247070312
        self.calculator1Display.SetScaleArray = ['POINTS', 'altitude']
        self.calculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
        self.calculator1Display.OpacityArray = ['POINTS', 'altitude']
        self.calculator1Display.OpacityTransferFunction = 'PiecewiseFunction'
        self.calculator1Display.DataAxesGrid = 'GridAxesRepresentation'
        self.calculator1Display.SelectionCellLabelFontFile = ''
        self.calculator1Display.SelectionPointLabelFontFile = ''
        self.calculator1Display.PolarAxes = 'PolarAxesRepresentation'
        self.calculator1Display.ScalarOpacityFunction = self.band1PWF
        self.calculator1Display.ScalarOpacityUnitDistance = 0.2717106773086742
        self.calculator1Display.InputVectors = [None, '']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.calculator1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.calculator1Display.DataAxesGrid.XTitleFontFile = ''
        self.calculator1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.calculator1Display.DataAxesGrid.YTitleFontFile = ''
        self.calculator1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.calculator1Display.DataAxesGrid.ZTitleFontFile = ''
        self.calculator1Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.calculator1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.calculator1Display.DataAxesGrid.XLabelFontFile = ''
        self.calculator1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.calculator1Display.DataAxesGrid.YLabelFontFile = ''
        self.calculator1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.calculator1Display.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.calculator1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.calculator1Display.PolarAxes.PolarAxisTitleFontFile = ''
        self.calculator1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.calculator1Display.PolarAxes.PolarAxisLabelFontFile = ''
        self.calculator1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.calculator1Display.PolarAxes.LastRadialAxisTextFontFile = ''
        self.calculator1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.calculator1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # hide data in view
        # Hide(self.threshold1, self.renderView1)

        # show color bar/color legend
        self.calculator1Display.SetScalarBarVisibility(self.renderView1, True)

        # hide data in view
        Hide(self.calculator1, self.renderView1)

        # update the view to ensure updated data information
        self.renderView1.Update()

        # turn off scalar coloring
        ColorBy(self.calculator1Display, None)

        # Hide the scalar bar for this color map if no visible data is colored by it.
        HideScalarBarIfNotNeeded(self.band1LUT, self.renderView1)

        # change solid color
        self.calculator1Display.DiffuseColor = [0.3333333333333333, 0.6666666666666666, 1.0]

        # set active source
        SetActiveSource(self.extractSubset1)

        # create a new 'Threshold'
        self.threshold2 = Threshold(Input=self.extractSubset1)
        self.threshold2.Scalars = ['POINTS', 'altitude']
        self.threshold2.ThresholdRange = [-7439.0, 3577.0]

        # Properties modified on threshold2
        self.threshold2.ThresholdRange = [0, 3577.0]

        # show data in view
        self.threshold2Display = Show(self.threshold2, self.renderView1)

        # trace defaults for the display properties.
        self.threshold2Display.Representation = 'Surface'
        self.threshold2Display.AmbientColor = [0.0, 0.0, 0.0]
        self.threshold2Display.ColorArrayName = ['POINTS', 'altitude']
        self.threshold2Display.LookupTable = self.band1LUT
        self.threshold2Display.OSPRayScaleArray = 'altitude'
        self.threshold2Display.OSPRayScaleFunction = 'PiecewiseFunction'
        self.threshold2Display.SelectOrientationVectors = 'altitude'
        self.threshold2Display.ScaleFactor = 1.9666656494140626
        self.threshold2Display.SelectScaleArray = 'altitude'
        self.threshold2Display.GlyphType = 'Arrow'
        self.threshold2Display.GlyphTableIndexArray = 'altitude'
        self.threshold2Display.GaussianRadius = 0.09833328247070312
        self.threshold2Display.SetScaleArray = ['POINTS', 'altitude']
        self.threshold2Display.ScaleTransferFunction = 'PiecewiseFunction'
        self.threshold2Display.OpacityArray = ['POINTS', 'altitude']
        self.threshold2Display.OpacityTransferFunction = 'PiecewiseFunction'
        self.threshold2Display.DataAxesGrid = 'GridAxesRepresentation'
        self.threshold2Display.SelectionCellLabelFontFile = ''
        self.threshold2Display.SelectionPointLabelFontFile = ''
        self.threshold2Display.PolarAxes = 'PolarAxesRepresentation'
        self.threshold2Display.ScalarOpacityFunction = self.band1PWF
        self.threshold2Display.ScalarOpacityUnitDistance = 0.4004217339813561
        self.threshold2Display.InputVectors = [None, '']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.threshold2Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.threshold2Display.DataAxesGrid.XTitleFontFile = ''
        self.threshold2Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.threshold2Display.DataAxesGrid.YTitleFontFile = ''
        self.threshold2Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.threshold2Display.DataAxesGrid.ZTitleFontFile = ''
        self.threshold2Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.threshold2Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.threshold2Display.DataAxesGrid.XLabelFontFile = ''
        self.threshold2Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.threshold2Display.DataAxesGrid.YLabelFontFile = ''
        self.threshold2Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.threshold2Display.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.threshold2Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.threshold2Display.PolarAxes.PolarAxisTitleFontFile = ''
        self.threshold2Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.threshold2Display.PolarAxes.PolarAxisLabelFontFile = ''
        self.threshold2Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.threshold2Display.PolarAxes.LastRadialAxisTextFontFile = ''
        self.threshold2Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.threshold2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # show color bar/color legend
        self.threshold2Display.SetScalarBarVisibility(self.renderView1, True)

        # hide data in view
        Hide(self.threshold2, self.renderView1)

        # update the view to ensure updated data information
        self.renderView1.Update()

        # create a new 'Calculator'
        self.calculator2 = Calculator(Input=self.threshold2)
        self.calculator2.Function = ''

        # Properties modified on calculator2
        self.calculator2.CoordinateResults = 1
        self.calculator2.Function = 'coordsX*iHat+coordsY*jHat+kHat*altitude/10000'

        # show data in view
        self.calculator2Display = Show(self.calculator2, self.renderView1)

        # trace defaults for the display properties.
        self.calculator2Display.Representation = 'Surface'
        self.calculator2Display.AmbientColor = [0.0, 0.0, 0.0]
        self.calculator2Display.ColorArrayName = ['POINTS', 'altitude']
        self.calculator2Display.LookupTable = self.band1LUT
        self.calculator2Display.OSPRayScaleArray = 'altitude'
        self.calculator2Display.OSPRayScaleFunction = 'PiecewiseFunction'
        self.calculator2Display.SelectOrientationVectors = 'altitude'
        self.calculator2Display.ScaleFactor = 1.9666656494140626
        self.calculator2Display.SelectScaleArray = 'altitude'
        self.calculator2Display.GlyphType = 'Arrow'
        self.calculator2Display.GlyphTableIndexArray = 'altitude'
        self.calculator2Display.GaussianRadius = 0.09833328247070312
        self.calculator2Display.SetScaleArray = ['POINTS', 'altitude']
        self.calculator2Display.ScaleTransferFunction = 'PiecewiseFunction'
        self.calculator2Display.OpacityArray = ['POINTS', 'altitude']
        self.calculator2Display.OpacityTransferFunction = 'PiecewiseFunction'
        self.calculator2Display.DataAxesGrid = 'GridAxesRepresentation'
        self.calculator2Display.SelectionCellLabelFontFile = ''
        self.calculator2Display.SelectionPointLabelFontFile = ''
        self.calculator2Display.PolarAxes = 'PolarAxesRepresentation'
        self.calculator2Display.ScalarOpacityFunction = self.band1PWF
        self.calculator2Display.ScalarOpacityUnitDistance = 0.4004556146647298
        self.calculator2Display.InputVectors = [None, '']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.calculator2Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.calculator2Display.DataAxesGrid.XTitleFontFile = ''
        self.calculator2Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.calculator2Display.DataAxesGrid.YTitleFontFile = ''
        self.calculator2Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.calculator2Display.DataAxesGrid.ZTitleFontFile = ''
        self.calculator2Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.calculator2Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.calculator2Display.DataAxesGrid.XLabelFontFile = ''
        self.calculator2Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.calculator2Display.DataAxesGrid.YLabelFontFile = ''
        self.calculator2Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.calculator2Display.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.calculator2Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.calculator2Display.PolarAxes.PolarAxisTitleFontFile = ''
        self.calculator2Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.calculator2Display.PolarAxes.PolarAxisLabelFontFile = ''
        self.calculator2Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.calculator2Display.PolarAxes.LastRadialAxisTextFontFile = ''
        self.calculator2Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.calculator2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # hide data in view
        Hide(self.threshold2, self.renderView1)

        # show color bar/color legend
        self.calculator2Display.SetScalarBarVisibility(self.renderView1, True)

        # update the view to ensure updated data information
        self.renderView1.Update()

        # turn off scalar coloring
        ColorBy(self.calculator2Display, None)

        # Hide the scalar bar for this color map if no visible data is colored by it.
        HideScalarBarIfNotNeeded(self.band1LUT, self.renderView1)

        # change solid color
        self.calculator2Display.DiffuseColor = [0.0, 0.6666666666666666, 0.4980392156862745]

        # set active source
        SetActiveSource(None)

        # create a new 'NetCDF Reader'
        self.sea_2dnc = NetCDFReader(FileName=[self.sea_2d_nc_path])
        self.sea_2dnc.Dimensions = '(eta_rho, xi_rho)'

        # get animation scene
        self.animationScene1 = GetAnimationScene()

        # update animation scene based on data timesteps
        self.animationScene1.UpdateAnimationUsingDataTimeSteps()

        # get the time-keeper
        self.timeKeeper1 = GetTimeKeeper()

        # Properties modified on sea_2dnc
        self.sea_2dnc.SphericalCoordinates = 0

        # Get the Timestep Values from sea_2dnc
        self.sea_2dnc_TimeStepValues = sorted([ts for ts in self.sea_2dnc.TimestepValues])

        # get the Initial StartTime and EndTime Value from animationScene1
        self.animationScene1StartTime = min(self.sea_2dnc_TimeStepValues)
        self.animationScene1EndTime = max(self.sea_2dnc_TimeStepValues)
        self.animationScene1IntervalLen \
            = (float(self.animationScene1EndTime) - float(self.animationScene1StartTime)) \
              / (len(self.sea_2dnc_TimeStepValues) - 1)

        # Convert the Initial StartTimeStep Value to Date Type
        startHours = datetime.timedelta(seconds=self.animationScene1StartTime)
        self.start_time_value = self.DATUM + startHours

        # show data in view
        self.sea_2dncDisplay = Show(self.sea_2dnc, self.renderView1)

        # trace defaults for the display properties.
        self.sea_2dncDisplay.Representation = 'Surface'
        self.sea_2dncDisplay.AmbientColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.ColorArrayName = [None, '']
        self.sea_2dncDisplay.OSPRayScaleArray = 'h'
        self.sea_2dncDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
        self.sea_2dncDisplay.SelectOrientationVectors = 'None'
        self.sea_2dncDisplay.ScaleFactor = 1.9468032786887122
        self.sea_2dncDisplay.SelectScaleArray = 'None'
        self.sea_2dncDisplay.GlyphType = 'Arrow'
        self.sea_2dncDisplay.GlyphTableIndexArray = 'None'
        self.sea_2dncDisplay.GaussianRadius = 0.0973401639344356
        self.sea_2dncDisplay.SetScaleArray = ['POINTS', 'h']
        self.sea_2dncDisplay.ScaleTransferFunction = 'PiecewiseFunction'
        self.sea_2dncDisplay.OpacityArray = ['POINTS', 'h']
        self.sea_2dncDisplay.OpacityTransferFunction = 'PiecewiseFunction'
        self.sea_2dncDisplay.DataAxesGrid = 'GridAxesRepresentation'
        self.sea_2dncDisplay.SelectionCellLabelFontFile = ''
        self.sea_2dncDisplay.SelectionPointLabelFontFile = ''
        self.sea_2dncDisplay.PolarAxes = 'PolarAxesRepresentation'
        self.sea_2dncDisplay.ScalarOpacityUnitDistance = 0.3719322908004742
        self.sea_2dncDisplay.InputVectors = [None, '']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.sea_2dncDisplay.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.DataAxesGrid.XTitleFontFile = ''
        self.sea_2dncDisplay.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.DataAxesGrid.YTitleFontFile = ''
        self.sea_2dncDisplay.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.DataAxesGrid.ZTitleFontFile = ''
        self.sea_2dncDisplay.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.DataAxesGrid.XLabelFontFile = ''
        self.sea_2dncDisplay.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.DataAxesGrid.YLabelFontFile = ''
        self.sea_2dncDisplay.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.sea_2dncDisplay.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.PolarAxes.PolarAxisTitleFontFile = ''
        self.sea_2dncDisplay.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.PolarAxes.PolarAxisLabelFontFile = ''
        self.sea_2dncDisplay.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
        self.sea_2dncDisplay.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.sea_2dncDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # update the view to ensure updated data information
        self.renderView1.Update()

        # create a new 'Extract Subset'
        self.extractSubset2 = ExtractSubset(Input=self.sea_2dnc)
        self.extractSubset2.VOI = [0, 744, 0, 427, 0, 0]

        # Properties modified on extractSubset2
        self.extractSubset2.SampleRateI = 1
        self.extractSubset2.SampleRateJ = 1
        self.extractSubset2.SampleRateK = 1

        # show data in view
        self.extractSubset2Display = Show(self.extractSubset2, self.renderView1)

        # trace defaults for the display properties.
        self.extractSubset2Display.Representation = 'Surface'
        self.extractSubset2Display.AmbientColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.ColorArrayName = [None, '']
        self.extractSubset2Display.OSPRayScaleArray = 'h'
        self.extractSubset2Display.OSPRayScaleFunction = 'PiecewiseFunction'
        self.extractSubset2Display.SelectOrientationVectors = 'None'
        self.extractSubset2Display.ScaleFactor = 1.943606557377234
        self.extractSubset2Display.SelectScaleArray = 'None'
        self.extractSubset2Display.GlyphType = 'Arrow'
        self.extractSubset2Display.GlyphTableIndexArray = 'None'
        self.extractSubset2Display.GaussianRadius = 0.0971803278688617
        self.extractSubset2Display.SetScaleArray = ['POINTS', 'h']
        self.extractSubset2Display.ScaleTransferFunction = 'PiecewiseFunction'
        self.extractSubset2Display.OpacityArray = ['POINTS', 'h']
        self.extractSubset2Display.OpacityTransferFunction = 'PiecewiseFunction'
        self.extractSubset2Display.DataAxesGrid = 'GridAxesRepresentation'
        self.extractSubset2Display.SelectionCellLabelFontFile = ''
        self.extractSubset2Display.SelectionPointLabelFontFile = ''
        self.extractSubset2Display.PolarAxes = 'PolarAxesRepresentation'
        self.extractSubset2Display.ScalarOpacityUnitDistance = 0.590138016519659
        self.extractSubset2Display.InputVectors = [None, '']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.extractSubset2Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.DataAxesGrid.XTitleFontFile = ''
        self.extractSubset2Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.DataAxesGrid.YTitleFontFile = ''
        self.extractSubset2Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.DataAxesGrid.ZTitleFontFile = ''
        self.extractSubset2Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.DataAxesGrid.XLabelFontFile = ''
        self.extractSubset2Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.DataAxesGrid.YLabelFontFile = ''
        self.extractSubset2Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.extractSubset2Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.PolarAxes.PolarAxisTitleFontFile = ''
        self.extractSubset2Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.PolarAxes.PolarAxisLabelFontFile = ''
        self.extractSubset2Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.PolarAxes.LastRadialAxisTextFontFile = ''
        self.extractSubset2Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.extractSubset2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # update the view to ensure updated data information
        self.renderView1.Update()

        # hide data in view
        Hide(self.sea_2dnc, self.renderView1)

        # create a new 'Extract Time Steps'
        self.extractTimeSteps1 = ExtractTimeSteps(Input=self.extractSubset2)
        self.extractTimeSteps1.TimeStepIndices = [0]
        self.extractTimeSteps1.TimeStepRange = [0, len(self.sea_2dnc_TimeStepValues) - 1]

        # Properties modified on extractTimeSteps1
        self.extractTimeSteps1.SelectionMode = 'Select Time Range'

        # show data in view
        self.extractTimeSteps1Display = Show(self.extractTimeSteps1, self.renderView1)

        # trace defaults for the display properties.
        self.extractTimeSteps1Display.Representation = 'Surface'
        self.extractTimeSteps1Display.AmbientColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.ColorArrayName = [None, '']
        self.extractTimeSteps1Display.OSPRayScaleArray = 'h'
        self.extractTimeSteps1Display.OSPRayScaleFunction = 'PiecewiseFunction'
        self.extractTimeSteps1Display.SelectOrientationVectors = 'None'
        self.extractTimeSteps1Display.ScaleFactor = 1.9436065573771601
        self.extractTimeSteps1Display.SelectScaleArray = 'None'
        self.extractTimeSteps1Display.GlyphType = 'Arrow'
        self.extractTimeSteps1Display.GlyphTableIndexArray = 'None'
        self.extractTimeSteps1Display.GaussianRadius = 0.097180327868858
        self.extractTimeSteps1Display.SetScaleArray = ['POINTS', 'h']
        self.extractTimeSteps1Display.ScaleTransferFunction = 'PiecewiseFunction'
        self.extractTimeSteps1Display.OpacityArray = ['POINTS', 'h']
        self.extractTimeSteps1Display.OpacityTransferFunction = 'PiecewiseFunction'
        self.extractTimeSteps1Display.DataAxesGrid = 'GridAxesRepresentation'
        self.extractTimeSteps1Display.SelectionCellLabelFontFile = ''
        self.extractTimeSteps1Display.SelectionPointLabelFontFile = ''
        self.extractTimeSteps1Display.PolarAxes = 'PolarAxesRepresentation'
        self.extractTimeSteps1Display.ScalarOpacityUnitDistance = 0.6558511127405765
        self.extractTimeSteps1Display.InputVectors = [None, '']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.extractTimeSteps1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.DataAxesGrid.XTitleFontFile = ''
        self.extractTimeSteps1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.DataAxesGrid.YTitleFontFile = ''
        self.extractTimeSteps1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.DataAxesGrid.ZTitleFontFile = ''
        self.extractTimeSteps1Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.DataAxesGrid.XLabelFontFile = ''
        self.extractTimeSteps1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.DataAxesGrid.YLabelFontFile = ''
        self.extractTimeSteps1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.extractTimeSteps1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.PolarAxes.PolarAxisTitleFontFile = ''
        self.extractTimeSteps1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.PolarAxes.PolarAxisLabelFontFile = ''
        self.extractTimeSteps1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.PolarAxes.LastRadialAxisTextFontFile = ''
        self.extractTimeSteps1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.extractTimeSteps1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # hide data in view
        Hide(self.extractSubset2, self.renderView1)

        # update the view to ensure updated data information
        self.renderView1.Update()

        # create a new 'Threshold'
        self.threshold3 = Threshold(Input=self.extractTimeSteps1)
        self.threshold3.Scalars = ['POINTS', 'h']
        self.threshold3.ThresholdRange = [0.00451, 5.438802115069695]

        # Properties modified on threshold3
        self.threshold3.Scalars = ['POINTS', 'mask_rho']
        self.threshold3.ThresholdRange = [1.0, 1.0]

        # show data in view
        self.threshold3Display = Show(self.threshold3, self.renderView1)

        # trace defaults for the display properties.
        self.threshold3Display.Representation = 'Surface'
        self.threshold3Display.AmbientColor = [0.0, 0.0, 0.0]
        self.threshold3Display.ColorArrayName = [None, '']
        self.threshold3Display.OSPRayScaleArray = 'h'
        self.threshold3Display.OSPRayScaleFunction = 'PiecewiseFunction'
        self.threshold3Display.SelectOrientationVectors = 'None'
        self.threshold3Display.ScaleFactor = 1.9436065573771601
        self.threshold3Display.SelectScaleArray = 'None'
        self.threshold3Display.GlyphType = 'Arrow'
        self.threshold3Display.GlyphTableIndexArray = 'None'
        self.threshold3Display.GaussianRadius = 0.097180327868858
        self.threshold3Display.SetScaleArray = ['POINTS', 'h']
        self.threshold3Display.ScaleTransferFunction = 'PiecewiseFunction'
        self.threshold3Display.OpacityArray = ['POINTS', 'h']
        self.threshold3Display.OpacityTransferFunction = 'PiecewiseFunction'
        self.threshold3Display.DataAxesGrid = 'GridAxesRepresentation'
        self.threshold3Display.SelectionCellLabelFontFile = ''
        self.threshold3Display.SelectionPointLabelFontFile = ''
        self.threshold3Display.PolarAxes = 'PolarAxesRepresentation'
        self.threshold3Display.ScalarOpacityUnitDistance = 0.6558511127405765
        self.threshold3Display.InputVectors = [None, '']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.threshold3Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.threshold3Display.DataAxesGrid.XTitleFontFile = ''
        self.threshold3Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.threshold3Display.DataAxesGrid.YTitleFontFile = ''
        self.threshold3Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.threshold3Display.DataAxesGrid.ZTitleFontFile = ''
        self.threshold3Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.threshold3Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.threshold3Display.DataAxesGrid.XLabelFontFile = ''
        self.threshold3Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.threshold3Display.DataAxesGrid.YLabelFontFile = ''
        self.threshold3Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.threshold3Display.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.threshold3Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.threshold3Display.PolarAxes.PolarAxisTitleFontFile = ''
        self.threshold3Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.threshold3Display.PolarAxes.PolarAxisLabelFontFile = ''
        self.threshold3Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.threshold3Display.PolarAxes.LastRadialAxisTextFontFile = ''
        self.threshold3Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.threshold3Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # hide data in view
        Hide(self.extractTimeSteps1, self.renderView1)

        # update the view to ensure updated data information
        self.renderView1.Update()

        ###########################
        if True:
            # create a new 'Programmable Filter'
            self.programmableFilter1 = ProgrammableFilter(Input=self.threshold3)

            # Properties modified on programmableFilter1
            self.programmableFilter1.Script = """
            import time
            import datetime

            DATUM = datetime.datetime(1968,5,23,0,0,0)
            t = inputs[0].GetInformation().Get(vtk.vtkDataObject.DATA_TIME_STEP())
            hours = datetime.timedelta(seconds=t)
            time_value = DATUM + hours

            outputarray = vtk.vtkStringArray()
            outputarray.SetName("datestr")
            outputarray.SetNumberOfTuples(1)
            outputarray.SetValue(0, "{}년 {}월 {}일 {}시"
                                    .format(time_value.year, 
                                            \'%02d\' % time_value.month, 
                                            \'%02d\' % time_value.day, 
                                            \'%02d\' % time_value.hour)
                                )

            output.FieldData.AddArray(outputarray)
            """
            self.programmableFilter1.RequestInformationScript = ''
            self.programmableFilter1.RequestUpdateExtentScript = ''
            # self.programmableFilter1.PythonPath = ''

            # show data in view
            self.programmableFilter1Display = Show(self.programmableFilter1, self.renderView1)

            # trace defaults for the display properties.
            self.programmableFilter1Display.Representation = 'Surface'
            self.programmableFilter1Display.AmbientColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.ColorArrayName = [None, '']
            self.programmableFilter1Display.OSPRayScaleFunction = 'PiecewiseFunction'
            self.programmableFilter1Display.SelectOrientationVectors = 'None'
            self.programmableFilter1Display.ScaleFactor = 1.946803278688637
            self.programmableFilter1Display.SelectScaleArray = 'None'
            self.programmableFilter1Display.GlyphType = 'Arrow'
            self.programmableFilter1Display.GlyphTableIndexArray = 'None'
            self.programmableFilter1Display.GaussianRadius = 0.09734016393443184
            self.programmableFilter1Display.SetScaleArray = [None, '']
            self.programmableFilter1Display.ScaleTransferFunction = 'PiecewiseFunction'
            self.programmableFilter1Display.OpacityArray = [None, '']
            self.programmableFilter1Display.OpacityTransferFunction = 'PiecewiseFunction'
            self.programmableFilter1Display.DataAxesGrid = 'GridAxesRepresentation'
            self.programmableFilter1Display.SelectionCellLabelFontFile = ''
            self.programmableFilter1Display.SelectionPointLabelFontFile = ''
            self.programmableFilter1Display.PolarAxes = 'PolarAxesRepresentation'
            self.programmableFilter1Display.ScalarOpacityUnitDistance = 0.4117377971501411
            self.programmableFilter1Display.InputVectors = [None, '']

            # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
            self.programmableFilter1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.DataAxesGrid.XTitleFontFile = ''
            self.programmableFilter1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.DataAxesGrid.YTitleFontFile = ''
            self.programmableFilter1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.DataAxesGrid.ZTitleFontFile = ''
            self.programmableFilter1Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.DataAxesGrid.XLabelFontFile = ''
            self.programmableFilter1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.DataAxesGrid.YLabelFontFile = ''
            self.programmableFilter1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.DataAxesGrid.ZLabelFontFile = ''

            # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
            self.programmableFilter1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.PolarAxes.PolarAxisTitleFontFile = ''
            self.programmableFilter1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.PolarAxes.PolarAxisLabelFontFile = ''
            self.programmableFilter1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.PolarAxes.LastRadialAxisTextFontFile = ''
            self.programmableFilter1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
            self.programmableFilter1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

            # update the view to ensure updated data information
            self.renderView1.Update()

            # create a new 'Python Annotation'
            self.pythonAnnotation1 = PythonAnnotation(Input=self.programmableFilter1)

            # Properties modified on pythonAnnotation1
            self.pythonAnnotation1.Expression = "'%s' % datestr.GetValue(0)"

            # show data in view
            self.pythonAnnotation1Display = Show(self.pythonAnnotation1, self.renderView1)

            # trace defaults for the display properties.
            self.pythonAnnotation1Display.Color = [0.0, 0.0, 0.0]

            # Properties modified on pythonAnnotation1Display
            self.pythonAnnotation1Display.FontFamily = 'File'

            # Properties modified on pythonAnnotation1Display
            self.pythonAnnotation1Display.FontFile = input_time_font_ttf_path

            # Properties modified on pythonAnnotation1Display
            self.pythonAnnotation1Display.WindowLocation = 'LowerCenter'

            # Properties modified on pythonAnnotation1Display
            self.pythonAnnotation1Display.FontSize = 10

        # update the view to ensure updated data information
        self.renderView1.Update()

        # create a new 'Calculator'
        self.calculator3 = Calculator(Input=self.threshold3)
        self.calculator3.Function = 'u*iHat+v*jHat'

        # show data in view
        self.calculator3Display = Show(self.calculator3, self.renderView1)

        # trace defaults for the display properties.
        self.calculator3Display.Representation = 'Surface'
        self.calculator3Display.AmbientColor = [0.0, 0.0, 0.0]
        self.calculator3Display.ColorArrayName = [None, '']
        self.calculator3Display.OSPRayScaleArray = 'Result'
        self.calculator3Display.OSPRayScaleFunction = 'PiecewiseFunction'
        self.calculator3Display.SelectOrientationVectors = 'Result'
        self.calculator3Display.ScaleFactor = 1.9436065573771601
        self.calculator3Display.SelectScaleArray = 'None'
        self.calculator3Display.GlyphType = 'Arrow'
        self.calculator3Display.GlyphTableIndexArray = 'None'
        self.calculator3Display.GaussianRadius = 0.097180327868858
        self.calculator3Display.SetScaleArray = ['POINTS', 'Result']
        self.calculator3Display.ScaleTransferFunction = 'PiecewiseFunction'
        self.calculator3Display.OpacityArray = ['POINTS', 'Result']
        self.calculator3Display.OpacityTransferFunction = 'PiecewiseFunction'
        self.calculator3Display.DataAxesGrid = 'GridAxesRepresentation'
        self.calculator3Display.SelectionCellLabelFontFile = ''
        self.calculator3Display.SelectionPointLabelFontFile = ''
        self.calculator3Display.PolarAxes = 'PolarAxesRepresentation'
        self.calculator3Display.ScalarOpacityUnitDistance = 0.6558511127405765
        self.calculator3Display.InputVectors = ['POINTS', 'Result']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.calculator3Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.calculator3Display.DataAxesGrid.XTitleFontFile = ''
        self.calculator3Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.calculator3Display.DataAxesGrid.YTitleFontFile = ''
        self.calculator3Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.calculator3Display.DataAxesGrid.ZTitleFontFile = ''
        self.calculator3Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.calculator3Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.calculator3Display.DataAxesGrid.XLabelFontFile = ''
        self.calculator3Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.calculator3Display.DataAxesGrid.YLabelFontFile = ''
        self.calculator3Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.calculator3Display.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.calculator3Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.calculator3Display.PolarAxes.PolarAxisTitleFontFile = ''
        self.calculator3Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.calculator3Display.PolarAxes.PolarAxisLabelFontFile = ''
        self.calculator3Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.calculator3Display.PolarAxes.LastRadialAxisTextFontFile = ''
        self.calculator3Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.calculator3Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # hide data in view
        Hide(self.threshold3, self.renderView1)

        ############# NEW
        # create a new 'Calculator'
        self.calculator4 = Calculator(Input=self.threshold3)
        self.calculator4.Function = 'sqrt(u^2+v^2)'

        # show data in view
        self.calculator4Display = Show(self.calculator4, self.renderView1)

        # trace defaults for the display properties.
        self.calculator4Display.Representation = 'Surface'
        self.calculator4Display.AmbientColor = [0.0, 0.0, 0.0]
        self.calculator4Display.ColorArrayName = [None, '']
        self.calculator4Display.OSPRayScaleArray = 'Result'
        self.calculator4Display.OSPRayScaleFunction = 'PiecewiseFunction'
        self.calculator4Display.SelectOrientationVectors = 'Result'
        self.calculator4Display.ScaleFactor = 1.946803278688637
        self.calculator4Display.SelectScaleArray = 'None'
        self.calculator4Display.GlyphType = 'Arrow'
        self.calculator4Display.GlyphTableIndexArray = 'None'
        self.calculator4Display.GaussianRadius = 0.09734016393443184
        self.calculator4Display.SetScaleArray = ['POINTS', 'Result']
        self.calculator4Display.ScaleTransferFunction = 'PiecewiseFunction'
        self.calculator4Display.OpacityArray = ['POINTS', 'Result']
        self.calculator4Display.OpacityTransferFunction = 'PiecewiseFunction'
        self.calculator4Display.DataAxesGrid = 'GridAxesRepresentation'
        self.calculator4Display.SelectionCellLabelFontFile = ''
        self.calculator4Display.SelectionPointLabelFontFile = ''
        self.calculator4Display.PolarAxes = 'PolarAxesRepresentation'
        self.calculator4Display.ScalarOpacityUnitDistance = 0.4117377971501411
        self.calculator4Display.InputVectors = ['POINTS', 'Result']

        # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
        self.calculator4Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
        self.calculator4Display.DataAxesGrid.XTitleFontFile = ''
        self.calculator4Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
        self.calculator4Display.DataAxesGrid.YTitleFontFile = ''
        self.calculator4Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
        self.calculator4Display.DataAxesGrid.ZTitleFontFile = ''
        self.calculator4Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
        self.calculator4Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
        self.calculator4Display.DataAxesGrid.XLabelFontFile = ''
        self.calculator4Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
        self.calculator4Display.DataAxesGrid.YLabelFontFile = ''
        self.calculator4Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
        self.calculator4Display.DataAxesGrid.ZLabelFontFile = ''

        # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
        self.calculator4Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
        self.calculator4Display.PolarAxes.PolarAxisTitleFontFile = ''
        self.calculator4Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
        self.calculator4Display.PolarAxes.PolarAxisLabelFontFile = ''
        self.calculator4Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
        self.calculator4Display.PolarAxes.LastRadialAxisTextFontFile = ''
        self.calculator4Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
        self.calculator4Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

        # set scalar coloring
        ColorBy(self.calculator4Display, ('POINTS', 'Result', 'Magnitude'))

        # update the view to ensure updated data information
        self.renderView1.Update()

        # change representation type
        self.calculator3Display.SetRepresentationType('Stream Lines')

        #### saving camera placements for all active views

        # current camera placement for renderView1
        self.renderView1.InteractionMode = '3D'
        self.renderView1.CameraPosition = [191, 25, 173.909]
        self.renderView1.CameraFocalPoint = [191, 25, -225.269]
        self.renderView1.CameraParallelScale = 103.315
        self.renderView1.CameraViewUp = [0, 1, 0]
        self.renderView1.CameraViewAngle = 30

        #### uncomment the following to render all views
        # RenderAllViews()
        # alternatively, if you want to write images, you can use SaveScreenshot(...).

        # Insert the Logo in the View
        """import vtk
        self.logo_img = vtk.vtkPNGReader()
        self.logo_img.SetFileName(self.logo_path)
        self.logo_img.Update()
        self.logo_rep = vtk.vtkLogoRepresentation()
        self.logo_rep.SetImage(self.logo_img.GetOutput())
        self.logo_rep.SetRenderer(self.renderer1)
        self.logo_rep.GetImageProperty().SetOpacity(0.95)
        self.logo_rep.SetPosition(0.04, 0.9)
        self.logo_widget = vtk.vtkLogoWidget()
        self.logo_widget.SetRepresentation(self.logo_rep)
        self.logo_widget.SetCurrentRenderer(self.renderer1)
        self.renderView1.GetInteractor().Initialize()
        self.logo_widget.SetInteractor(self.renderView1.GetInteractor())
        self.logo_widget.On()"""

    def m00_01_set_all_filters_visibility_off(self):

        Hide(self.etopo11nc, self.renderView1)
        Hide(self.extractSubset1, self.renderView1)
        Hide(self.threshold1, self.renderView1)
        Hide(self.calculator1, self.renderView1)
        Hide(self.threshold2, self.renderView1)
        Hide(self.calculator2, self.renderView1)
        Hide(self.sea_2dnc, self.renderView1)
        Hide(self.extractSubset2, self.renderView1)
        Hide(self.extractTimeSteps1, self.renderView1)
        Hide(self.threshold3, self.renderView1)
        Hide(self.programmableFilter1, self.renderView1)
        Hide(self.pythonAnnotation1, self.renderView1)
        Hide(self.calculator3, self.renderView1)
        Hide(self.calculator4, self.renderView1)

    def m00_02_00_set_view_graphics_background(self, use_gradient=True, *params):

        # Set the Background Color
        if use_gradient:
            self.renderView1.UseGradientBackground = 1
            if not len(params) == 2:
                self.renderView1.Background = [0.5, 0.5, 0.5]
                self.renderView1.Background2 = [0.0, 0.0, 0.0]
            else:
                if not sum([(type(p).__name__ == 'tuple' and len(p) == 3
                             and sum([(type(e).__name__ == 'float') for e in p]) == 3)
                            for p in params]) == 2:
                    self.renderView1.Background = [0.5, 0.5, 0.5]
                    self.renderView1.Background2 = [0.0, 0.0, 0.0]
                else:
                    self.renderView1.Background = list(params[0])
                    self.renderView1.Background2 = list(params[1])
        else:
            self.renderView1.UseGradientBackground = 0
            if not len(params) == 1:
                self.renderView1.Background = [0.5, 0.5, 0.5]
            else:
                param = params[0]
                if not (type(param).__name__ == 'tuple' and len(param) == 3):
                    self.renderView1.Background = [0.5, 0.5, 0.5]
                else:
                    self.renderView1.Background = list(param)
        self.renderView1.Update()

    def m00_02_01_set_view_graphics_land(self, input_land_colorbar_font_ttf_path,
                                         scale_min, scale_max, dim='3D', use_scalar_bar=True, ambient=0.5, **params):
        self.land_colorbar_font_ttf_path = u'%s' % input_land_colorbar_font_ttf_path

        if dim == '3D':
            # calculator2Display ( Colored by Scalar ) ::: LAND AREA ( 3D )
            Show(self.calculator2, self.renderView1)
            self.calculator2Display.Ambient = ambient
            if len({'COLOR', 'color', 'C', 'c'}.intersection(params.keys())) == 1 \
                    and type(
                params[list({'COLOR', 'color', 'C', 'c'}.intersection(params.keys()))[0]]).__name__ == 'tuple' \
                    and len(params[list({'COLOR', 'color', 'C', 'c'}.intersection(params.keys()))[0]]) == 3 \
                    and sum([(type(e).__name__ == 'float')
                             for e in params[list({'COLOR', 'color', 'C', 'c'}.intersection(params.keys()))[0]]]) == 3:
                ColorBy(self.threshold2Display, None)
                self.band1LUT = GetColorTransferFunction('altitude', self.threshold2Display)
                self.band1PWF = GetOpacityTransferFunction('altitude', self.threshold2Display)
                self.threshold2Display.DiffuseColor = \
                    params[list({'COLOR', 'color', 'C', 'c'}.intersection(params.keys()))[0]]
                HideScalarBarIfNotNeeded(self.band1LUT, self.renderView1)
            elif 'colormap_json_path' in params.keys() and type(params['colormap_json_path']).__name__ == 'str' \
                    and os.path.isfile(params['colormap_json_path']):
                with open(params['colormap_json_path']) as json_file:
                    palette_nm = json.load(json_file)[0]["Name"]
                ImportPresets(filename=params['colormap_json_path'])
                if False:
                    ColorBy(self.calculator2Display, ('POINTS', 'altitude'))
                    self.band1LUT = GetColorTransferFunction('altitude', self.calculator2Display)
                    self.band1PWF = GetOpacityTransferFunction('altitude', self.calculator2Display)
                    self.calculator2Display.RescaleTransferFunctionToDataRange(True, False)
                    self.band1PWF.RescaleTransferFunction(scale_min, scale_max)
                    self.band1LUT.RescaleTransferFunction(scale_min, scale_max)
                    self.band1LUT.ApplyPreset(palette_nm, True)  # sample5_land_topo_color
                    self.band1LUTColorBar = GetScalarBar(self.band1LUT, self.renderView1)
                    self.band1LUTColorBar.TitleFontFamily = 'File'
                    self.band1LUTColorBar.TitleFontFile = self.land_colorbar_font_ttf_path
                    self.band1LUTColorBar.Title = '고도'
                    self.band1LUTColorBar.ComponentTitle = ' (m)'
                    self.band1LUTColorBar.TitleColor = [1.0, 1.0, 1.0]
                    self.band1LUTColorBar.LabelColor = [1.0, 1.0, 1.0]
                    self.band1LUTColorBar.WindowLocation = 'LowerRightCorner'
                    self.band1LUTColorBar.AddRangeAnnotations = 0
                    self.band1LUTColorBar.DrawTickMarks = 1
                    self.band1LUTColorBar.DrawTickLabels = 1
                    self.band1LUTColorBar.RangeLabelFormat = '%.0f'
                    self.band1LUTColorBar.LabelFormat = '%.0f'
                    self.calculator2Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)
                if False:
                    ColorBy(self.calculator2Display, ('POINTS', 'altitude'))
                    self.separate_calculator2Display_Band1LUT = \
                        GetColorTransferFunction('altitude', self.calculator2Display, separate=True)
                    self.separate_calculator2Display_Band1PWF = \
                        GetOpacityTransferFunction('altitude', self.calculator2Display, separate=True)
                    self.calculator2Display.RescaleTransferFunctionToDataRange(True, False)
                    self.separate_calculator2Display_Band1PWF.RescaleTransferFunction(scale_min, scale_max)
                    self.separate_calculator2Display_Band1LUT.RescaleTransferFunction(scale_min, scale_max)
                    self.separate_calculator2Display_Band1LUT.ApplyPreset(palette_nm, True)  # sample5_land_topo_color
                    self.separate_calculator2Display_Band1LUT_ColorBar = \
                        GetScalarBar(self.separate_calculator2Display_Band1LUT, self.renderView1)
                    self.separate_calculator2Display_Band1LUT_ColorBar.TitleFontFamily = 'File'
                    self.separate_calculator2Display_Band1LUT_ColorBar.TitleFontFile = self.land_colorbar_font_ttf_path
                    self.separate_calculator2Display_Band1LUT_ColorBar.Title = '고도'
                    self.separate_calculator2Display_Band1LUT_ColorBar.ComponentTitle = ' (m)'
                    self.separate_calculator2Display_Band1LUT_ColorBar.TitleColor = [1.0, 1.0, 1.0]
                    self.separate_calculator2Display_Band1LUT_ColorBar.LabelColor = [1.0, 1.0, 1.0]
                    self.separate_calculator2Display_Band1LUT_ColorBar.WindowLocation = 'LowerRightCorner'
                    self.separate_calculator2Display_Band1LUT_ColorBar.AddRangeAnnotations = 0
                    self.separate_calculator2Display_Band1LUT_ColorBar.DrawTickMarks = 1
                    self.separate_calculator2Display_Band1LUT_ColorBar.DrawTickLabels = 1
                    self.separate_calculator2Display_Band1LUT_ColorBar.RangeLabelFormat = '%.0f'
                    self.separate_calculator2Display_Band1LUT_ColorBar.LabelFormat = '%.0f'
                    self.calculator2Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)
                if True:
                    ColorBy(self.calculator2Display, ('POINTS', 'altitude'), True)
                    self.band1LUT = GetColorTransferFunction('altitude', self.calculator2Display)
                    self.band1PWF = GetOpacityTransferFunction('altitude', self.calculator2Display)
                    self.calculator2Display.RescaleTransferFunctionToDataRange(True, False)
                    self.calculator2Display.Opacity = 0.8
                    self.band1LUT.RescaleTransferFunction(scale_min, scale_max)
                    self.band1PWF.RescaleTransferFunction(scale_min, scale_max)
                    self.band1LUT.ApplyPreset(palette_nm, True)  # sample5_land_topo_color
                    self.band1LUTColorBar = GetScalarBar(self.band1LUT, self.renderView1)
                    self.band1LUTColorBar.TitleFontFamily = 'File'
                    self.band1LUTColorBar.TitleFontFile = self.land_colorbar_font_ttf_path
                    self.band1LUTColorBar.Title = '고도'
                    self.band1LUTColorBar.ComponentTitle = ' (m)'
                    self.band1LUTColorBar.TitleColor = [1.0, 1.0, 1.0]
                    self.band1LUTColorBar.LabelColor = [1.0, 1.0, 1.0]
                    self.band1LUTColorBar.WindowLocation = 'LowerRightCorner'
                    self.band1LUTColorBar.AddRangeAnnotations = 0
                    self.band1LUTColorBar.DrawTickMarks = 1
                    self.band1LUTColorBar.DrawTickLabels = 1
                    self.band1LUTColorBar.RangeLabelFormat = '%.0f'
                    self.band1LUTColorBar.LabelFormat = '%.0f'
                    self.calculator2Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)
                if False:
                    Show(self.calculator2, self.renderView1)
                    ColorBy(self.calculator2Display, ('POINTS', 'altitude'), True)
                    self.band1LUT = GetColorTransferFunction('altitude', self.calculator2Display)
                    self.band1PWF = GetOpacityTransferFunction('altitude', self.calculator2Display)
                    self.calculator2Display.RescaleTransferFunctionToDataRange(True, False)
                    self.band1LUT.RescaleTransferFunction(scale_min, scale_max)
                    self.band1PWF.RescaleTransferFunction(scale_min, scale_max)
                    self.band1LUT.ApplyPreset(palette_nm, True)  # Land_Scandinavia
                    self.band1LUTColorBar = GetScalarBar(self.band1LUT, self.renderView1)
                    self.band1LUTColorBar.TitleFontFamily = 'File'
                    self.band1LUTColorBar.TitleFontFile = self.land_colorbar_font_ttf_path
                    self.band1LUTColorBar.Title = '고도'
                    self.band1LUTColorBar.ComponentTitle = ' (m)'
                    self.band1LUTColorBar.TitleColor = [1.0, 1.0, 1.0]
                    self.band1LUTColorBar.LabelColor = [1.0, 1.0, 1.0]
                    self.band1LUTColorBar.WindowLocation = 'LowerRightCorner'
                    self.band1LUTColorBar.AddRangeAnnotations = 0
                    self.band1LUTColorBar.DrawTickMarks = 1
                    self.band1LUTColorBar.DrawTickLabels = 1
                    self.band1LUTColorBar.RangeLabelFormat = '%.0f'
                    self.band1LUTColorBar.LabelFormat = '%.0f'
                    self.calculator2Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)
            else:
                pass
        elif dim == '2D':
            Show(self.threshold2, self.renderView1)
            Hide(self.calculator2, self.renderView1)
            self.threshold2Display.Ambient = ambient
            if len({'COLOR', 'color', 'C', 'c'}.intersection(params.keys())) == 1 \
                    and type(
                params[list({'COLOR', 'color', 'C', 'c'}.intersection(params.keys()))[0]]).__name__ == 'tuple' \
                    and len(params[list({'COLOR', 'color', 'C', 'c'}.intersection(params.keys()))[0]]) == 3 \
                    and sum([(type(e).__name__ == 'float')
                             for e in params[list({'COLOR', 'color', 'C', 'c'}.intersection(params.keys()))[0]]]) == 3:
                ColorBy(self.threshold2Display, None)
                self.band1LUT = GetColorTransferFunction('altitude', self.threshold2Display)
                self.band1PWF = GetOpacityTransferFunction('altitude', self.threshold2Display)
                self.threshold2Display.DiffuseColor = \
                    params[list({'COLOR', 'color', 'C', 'c'}.intersection(params.keys()))[0]]
                HideScalarBarIfNotNeeded(self.band1LUT, self.renderView1)
            elif 'colormap_json_path' in params.keys() and type(params['colormap_json_path']) == 'str' \
                    and os.path.isfile(params['colormap_json_path']):
                with open(params['colormap_json_path']) as json_file:
                    palette_nm = json.load(json_file)[0]["Name"]
                ImportPresets(filename=params['colormap_json_path'])
                self.band1LUT = GetColorTransferFunction('altitude', self.threshold2Display)
                self.band1PWF = GetOpacityTransferFunction('altitude', self.threshold2Display)
                self.threshold2Display.RescaleTransferFunctionToDataRange(True, False)
                self.band1PWF.RescaleTransferFunction(scale_min, scale_max)
                self.band1LUT.RescaleTransferFunction(scale_min, scale_max)
                self.band1LUT.ApplyPreset(palette_nm, True)  # sample5_land_topo_color
                self.band1LUTColorBar = GetScalarBar(self.band1LUT, self.renderView1)
                self.band1LUTColorBar.TitleFontFamily = 'File'
                self.band1LUTColorBar.TitleFontFile = self.land_colorbar_font_ttf_path
                self.band1LUTColorBar.Title = '고도'
                self.band1LUTColorBar.ComponentTitle = ' (m)'
                self.band1LUTColorBar.TitleColor = [1.0, 1.0, 1.0]
                self.band1LUTColorBar.LabelColor = [1.0, 1.0, 1.0]
                self.band1LUTColorBar.WindowLocation = 'LowerRightCorner'
                self.band1LUTColorBar.AddRangeAnnotations = 0
                self.band1LUTColorBar.DrawTickMarks = 1
                self.band1LUTColorBar.DrawTickLabels = 1
                self.band1LUTColorBar.RangeLabelFormat = '%.0f'
                self.band1LUTColorBar.LabelFormat = '%.0f'
                self.threshold2Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)
            else:
                pass
        elif dim == 'None':
            Hide(self.threshold2, self.renderView1)
            Hide(self.calculator2, self.renderView1)
        else:
            pass

        self.renderView1.Update()

    def m00_02_02_set_view_graphics_ocean(self, input_ocean_colorbar_font_ttf_path, scale_min, scale_max,
                                          dim='3D', use_scalar_bar=True, ambient=0, opacity=0.5, **params):

        self.ocean_colorbar_font_ttf_path = u'%s' % input_ocean_colorbar_font_ttf_path
        self.ocean_graphic = ''

        if dim == '2D':
            if params == dict():
                Show(self.threshold1, self.renderView1)
                self.threshold1Display.Ambient = ambient
                self.ocean_graphic = '%s_BATHEMETRY' % dim
                self.threshold1Display.Opacity = opacity
                ColorBy(self.threshold1Display, ('POINTS', 'altitude'), True)
                self.separate_threshold1Display_Band1LUT = \
                    GetColorTransferFunction('altitude', self.threshold1Display, separate=True)
                self.separate_threshold1Display_Band1PWF = \
                    GetOpacityTransferFunction('altitude', self.threshold1Display, separate=True)
                self.threshold1Display.RescaleTransferFunctionToDataRange(True, False)
                self.separate_threshold1Display_Band1PWF.RescaleTransferFunction(scale_min, scale_max)
                self.separate_threshold1Display_Band1LUT.RescaleTransferFunction(scale_min, scale_max)
                self.separate_threshold1Display_Band1LUT.ApplyPreset('Ocean_Scandinavia', True)
                self.separate_threshold1Display_Band1LUT_ColorBar = \
                    GetScalarBar(self.separate_threshold1Display_Band1LUT, self.renderView1)
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleFontFamily = 'File'
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleFontFile = self.ocean_colorbar_font_ttf_path
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleFontSize = 20
                self.separate_threshold1Display_Band1LUT_ColorBar.Title = '수심'
                self.separate_threshold1Display_Band1LUT_ColorBar.ComponentTitle = ' (m)'
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleColor = [0.0, 0.0, 0.0]
                self.separate_threshold1Display_Band1LUT_ColorBar.LabelColor = [0.0, 0.0, 0.0]
                self.separate_threshold1Display_Band1LUT_ColorBar.WindowLocation = 'UpperRightCorner'
                self.separate_threshold1Display_Band1LUT_ColorBar.AddRangeAnnotations = 0
                self.separate_threshold1Display_Band1LUT_ColorBar.DrawTickMarks = 1
                self.separate_threshold1Display_Band1LUT_ColorBar.DrawTickLabels = 1
                self.separate_threshold1Display_Band1LUT_ColorBar.RangeLabelFormat = '%.0f'
                self.separate_threshold1Display_Band1LUT_ColorBar.LabelFormat = '%.0f'
                self.separate_threshold1Display_Band1LUT_ColorBar.HorizontalTitle = 1
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleJustification = 'Left'
                self.separate_threshold1Display_Band1LUT_ColorBar.ScalarBarThickness = 40
                self.separate_threshold1Display_Band1LUT_ColorBar.ScalarBarLength = 0.6
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleBold = 1
                self.separate_threshold1Display_Band1LUT_ColorBar.LabelBold = 1
                self.threshold1Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)
            elif len({'VARIABLE', 'VAR', 'var', 'V', 'v'}.intersection(params.keys())) == 0:
                self.ocean_graphic = 'None'
            else:
                if len({'VARIABLE', 'VAR', 'var', 'V', 'v'}.intersection(params.keys())) > 1:
                    self.ocean_graphic = 'None'
                else:
                    param = list({'VARIABLE', 'VAR', 'var', 'V', 'v'}.intersection(params.keys()))[0]
                    if params[param] not in ['S', 'T', 'U', 'Z', 'V', 's', 't', 'u', 'z', 'v',
                                             'SALT', 'TEMP', 'UNIFORM', 'ZETA', 'VELOCITY',
                                             'salt', 'temp', 'uniform', 'zeta', 'velocity']:
                        self.ocean_graphic = 'None'
                    else:
                        if 'colormap_json_path' in params.keys() \
                                and type(params['colormap_json_path']).__name__ == 'str' \
                                and os.path.isfile(params['colormap_json_path']):
                            with open(params['colormap_json_path']) as json_file:
                                palette_nm = json.load(json_file)[0]["Name"]
                            ImportPresets(filename=params['colormap_json_path'])
                            if params[param] in ['S', 's', 'SALT', 'salt', 'T', 't', 'TEMP', 'temp',
                                                 'Z', 'z', 'ZETA', 'zeta', 'V', 'v', 'VELOCITY', 'velocity']:
                                Show(self.calculator1, self.renderView1)
                                ColorBy(self.calculator1Display, None)
                                self.cal1LUT = GetColorTransferFunction('altitude', self.calculator1Display)
                                self.cal1PWF = GetOpacityTransferFunction('altitude', self.calculator1Display)
                                self.calculator1Display.DiffuseColor = [1.0, 1.0, 1.0]
                                self.calculator1Display.Opacity = 0.25
                                self.calculator1Display.Ambient = ambient
                                HideScalarBarIfNotNeeded(self.cal1LUT, self.renderView1)
                                if params[param] in ['S', 's', 'SALT', 'salt']:
                                    self.ocean_graphic = '%s_SALT' % dim
                                    Hide(self.threshold1, self.renderView1)
                                    Show(self.threshold3, self.renderView1)
                                    self.threshold3Display.Ambient = ambient
                                    self.threshold3Display.Opacity = opacity
                                    ColorBy(self.threshold3Display, ('POINTS', 'salt'))
                                    self.saltLUT = GetColorTransferFunction('salt', self.threshold3Display)
                                    self.saltPWF = GetOpacityTransferFunction('salt', self.threshold3Display)
                                    self.threshold3Display.ColorArrayName = ['POINTS', 'salt']
                                    self.threshold3Display.LookupTable = self.saltLUT
                                    self.threshold3Display.RescaleTransferFunctionToDataRange(True, False)
                                    self.saltLUT.RescaleTransferFunction(scale_min, scale_max)
                                    self.saltPWF.RescaleTransferFunction(scale_min, scale_max)
                                    self.saltLUT.ApplyPreset(palette_nm, True)  # Salinity_Palette_1
                                    self.saltLUTColorBar = GetScalarBar(self.saltLUT, self.renderView1)
                                    self.saltLUTColorBar.TitleFontFamily = 'File'
                                    self.saltLUTColorBar.TitleFontFile = self.ocean_colorbar_font_ttf_path
                                    self.saltLUTColorBar.TitleFontSize = 20
                                    self.saltLUTColorBar.Title = '염분'
                                    self.saltLUTColorBar.ComponentTitle = ' (‰)'
                                    self.saltLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
                                    self.saltLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
                                    self.saltLUTColorBar.WindowLocation = 'UpperRightCorner'
                                    self.saltLUTColorBar.AddRangeAnnotations = 0
                                    self.saltLUTColorBar.DrawTickMarks = 1
                                    self.saltLUTColorBar.DrawTickLabels = 1
                                    self.saltLUTColorBar.RangeLabelFormat = '%.0f'
                                    self.saltLUTColorBar.LabelFormat = '%.0f'
                                    self.saltLUTColorBar.HorizontalTitle = 1
                                    self.saltLUTColorBar.TitleJustification = 'Left'
                                    self.saltLUTColorBar.ScalarBarThickness = 40
                                    self.saltLUTColorBar.ScalarBarLength = 0.6
                                    self.saltLUTColorBar.TitleBold = 1
                                    self.saltLUTColorBar.LabelBold = 1
                                    self.threshold3Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)
                                elif params[param] in ['T', 't', 'TEMP', 'temp']:
                                    self.ocean_graphic = '%s_TEMP' % dim
                                    Hide(self.threshold1, self.renderView1)
                                    Show(self.threshold3, self.renderView1)
                                    self.threshold3Display.Ambient = ambient
                                    self.threshold3Display.Opacity = opacity
                                    ColorBy(self.threshold3Display, ('POINTS', 'temp'), True)
                                    self.separate_threshold3Display_tempLUT = \
                                        GetColorTransferFunction('temp', self.threshold3Display, separate=True)
                                    self.separate_threshold3Display_tempPWF = \
                                        GetOpacityTransferFunction('temp', self.threshold3Display, separate=True)
                                    self.threshold3Display.ColorArrayName = ['POINTS', 'temp']
                                    self.threshold3Display.LookupTable = self.separate_threshold3Display_tempLUT
                                    self.threshold3Display.RescaleTransferFunctionToDataRange(True, False)
                                    self.threshold3Display.SetScalarBarVisibility(self.renderView1, True)
                                    self.separate_threshold3Display_tempLUT.RescaleTransferFunction(scale_min,
                                                                                                    scale_max)
                                    self.separate_threshold3Display_tempPWF.RescaleTransferFunction(scale_min,
                                                                                                    scale_max)
                                    self.separate_threshold3Display_tempLUT.ApplyPreset(palette_nm,
                                                                                        True)  # Temperature_Palette_1
                                    self.separate_threshold3Display_tempLUTColorBar = \
                                        GetScalarBar(self.separate_threshold3Display_tempLUT, self.renderView1)
                                    self.separate_threshold3Display_tempLUTColorBar.TitleFontFamily = 'File'
                                    self.separate_threshold3Display_tempLUTColorBar.TitleFontFile = self.ocean_colorbar_font_ttf_path
                                    self.separate_threshold3Display_tempLUTColorBar.TitleFontSize = 20
                                    self.separate_threshold3Display_tempLUTColorBar.Title = '수온'
                                    self.separate_threshold3Display_tempLUTColorBar.ComponentTitle = ' (℃)'
                                    self.separate_threshold3Display_tempLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
                                    self.separate_threshold3Display_tempLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
                                    self.separate_threshold3Display_tempLUTColorBar.WindowLocation = 'UpperRightCorner'
                                    self.separate_threshold3Display_tempLUTColorBar.AddRangeAnnotations = 0
                                    self.separate_threshold3Display_tempLUTColorBar.DrawTickMarks = 1
                                    self.separate_threshold3Display_tempLUTColorBar.DrawTickLabels = 1
                                    self.separate_threshold3Display_tempLUTColorBar.RangeLabelFormat = '%.0f'
                                    self.separate_threshold3Display_tempLUTColorBar.LabelFormat = '%.0f'
                                    self.separate_threshold3Display_tempLUTColorBar.HorizontalTitle = 1
                                    self.separate_threshold3Display_tempLUTColorBar.TitleJustification = 'Left'
                                    self.separate_threshold3Display_tempLUTColorBar.ScalarBarThickness = 40
                                    self.separate_threshold3Display_tempLUTColorBar.ScalarBarLength = 0.6
                                    self.separate_threshold3Display_tempLUTColorBar.TitleBold = 1
                                    self.separate_threshold3Display_tempLUTColorBar.LabelBold = 1
                                    self.threshold3Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)
                                elif params[param] in ['Z', 'z', 'ZETA', 'zeta']:
                                    self.ocean_graphic = '%s_ZETA' % dim
                                    Hide(self.threshold1, self.renderView1)
                                    Show(self.threshold3, self.renderView1)
                                    self.threshold3Display.Ambient = ambient
                                    self.threshold3Display.Opacity = opacity
                                    ColorBy(self.threshold3Display, ('POINTS', 'zeta'))
                                    self.zetaLUT = GetColorTransferFunction('zeta', self.threshold3Display)
                                    self.zetaPWF = GetOpacityTransferFunction('zeta', self.threshold3Display)
                                    self.threshold3Display.ColorArrayName = ['POINTS', 'zeta']
                                    self.threshold3Display.LookupTable = self.zetaLUT
                                    self.threshold3Display.RescaleTransferFunctionToDataRange(True, False)
                                    self.zetaLUT.RescaleTransferFunction(scale_min, scale_max)
                                    self.zetaPWF.RescaleTransferFunction(scale_min, scale_max)
                                    self.zetaLUT.ApplyPreset(palette_nm, True)  # Zeta_Palette_1
                                    self.zetaLUTColorBar = GetScalarBar(self.zetaLUT, self.renderView1)
                                    self.zetaLUTColorBar.TitleFontFamily = 'File'
                                    self.zetaLUTColorBar.TitleFontFile = self.ocean_colorbar_font_ttf_path
                                    self.zetaLUTColorBar.TitleFontSize = 20
                                    self.zetaLUTColorBar.Title = '해수면 높이'
                                    self.zetaLUTColorBar.ComponentTitle = ' (m)'
                                    self.zetaLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
                                    self.zetaLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
                                    self.zetaLUTColorBar.WindowLocation = 'UpperRightCorner'
                                    self.zetaLUTColorBar.AddRangeAnnotations = 0
                                    self.zetaLUTColorBar.DrawTickMarks = 1
                                    self.zetaLUTColorBar.DrawTickLabels = 1
                                    self.zetaLUTColorBar.RangeLabelFormat = '%.0f'
                                    self.zetaLUTColorBar.LabelFormat = '%.0f'
                                    self.zetaLUTColorBar.HorizontalTitle = 1
                                    self.zetaLUTColorBar.TitleJustification = 'Left'
                                    self.zetaLUTColorBar.ScalarBarThickness = 40
                                    self.zetaLUTColorBar.ScalarBarLength = 0.6
                                    self.zetaLUTColorBar.TitleBold = 1
                                    self.zetaLUTColorBar.LabelBold = 1
                                    self.threshold3Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)
                                elif params[param] in ['V', 'v', 'VELOCITY', 'velocity']:
                                    self.ocean_graphic = '%s_velo' % dim
                                    Show(self.calculator4, self.renderView1)
                                    self.calculator4Display.Opacity = opacity
                                    self.calculator4Display.Ambient = ambient
                                    ColorBy(self.calculator4Display, ('POINTS', 'Result', 'Magnitude'))

                                    # rescale color and/or opacity maps used to exactly fit the current data range
                                    self.calculator4Display.RescaleTransferFunctionToDataRange(False, False)

                                    # Get the Color Setting Functions
                                    self.veloLUT = GetColorTransferFunction('Result', self.calculator4Display)
                                    self.veloPWF = GetOpacityTransferFunction('Result', self.calculator4Display)

                                    # Update a scalar bar component title.
                                    UpdateScalarBarsComponentTitle(self.veloLUT, self.calculator4Display)

                                    self.calculator4Display.ColorArrayName = ['POINTS', 'Result']
                                    self.calculator4Display.LookupTable = self.veloLUT
                                    self.calculator4Display.RescaleTransferFunctionToDataRange(True, False)
                                    self.veloLUT.RescaleTransferFunction(scale_min, scale_max)
                                    self.veloPWF.RescaleTransferFunction(scale_min, scale_max)
                                    self.veloLUT.ApplyPreset(palette_nm, True)  # UVVelocity
                                    self.veloLUTColorBar = GetScalarBar(self.veloLUT, self.renderView1)
                                    self.veloLUTColorBar.TitleFontFamily = 'File'
                                    self.veloLUTColorBar.TitleFontFile = self.ocean_colorbar_font_ttf_path
                                    self.veloLUTColorBar.TitleFontSize = 20
                                    self.veloLUTColorBar.Title = '유속'
                                    self.veloLUTColorBar.ComponentTitle = ' (m/s)'
                                    self.veloLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
                                    self.veloLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
                                    self.veloLUTColorBar.WindowLocation = 'UpperRightCorner'
                                    self.veloLUTColorBar.AddRangeAnnotations = 0
                                    self.veloLUTColorBar.DrawTickMarks = 1
                                    self.veloLUTColorBar.DrawTickLabels = 1
                                    self.veloLUTColorBar.RangeLabelFormat = '%.1f'
                                    self.veloLUTColorBar.LabelFormat = '%.1f'
                                    self.veloLUTColorBar.HorizontalTitle = 1
                                    self.veloLUTColorBar.TitleJustification = 'Left'
                                    self.veloLUTColorBar.ScalarBarThickness = 40
                                    self.veloLUTColorBar.ScalarBarLength = 0.6
                                    self.veloLUTColorBar.TitleBold = 1
                                    self.veloLUTColorBar.LabelBold = 1
                                    self.calculator4Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)
                            else:
                                pass
                        else:
                            if len({'C', 'c', 'COLOR', 'color'}.intersection(params.keys())) == 0:
                                uniform_ocean_color = [0.0, 0.3333333333333333, 1.0]
                            else:
                                if len({'C', 'c', 'COLOR', 'color'}.intersection(params.keys())) > 0:
                                    uniform_ocean_color = [0.0, 0.3333333333333333, 1.0]
                                else:
                                    color_parameter = list({'C', 'c', 'COLOR', 'color'}.intersection(params.keys()))[0]
                                    if not (type(params[color_parameter]).__name__ == 'list'
                                            and len(params[color_parameter]) == 3):
                                        uniform_ocean_color = [0.0, 0.3333333333333333, 1.0]
                                    else:
                                        uniform_ocean_color = params[color_parameter]
                            Hide(self.threshold3, self.renderView1)
                            Show(self.threshold1, self.renderView1)
                            self.ocean_graphic = '%s_UNIFORM' % dim
                            ColorBy(self.threshold1Display, None)
                            self.band1LUT = GetColorTransferFunction('altitude', self.threshold1Display)
                            self.band1PWF = GetOpacityTransferFunction('altitude', self.threshold1Display)
                            self.threshold1Display.Ambient = ambient
                            self.threshold1Display.DiffuseColor = uniform_ocean_color
                            HideScalarBarIfNotNeeded(self.band1LUT, self.renderView1)
        elif dim == '3D':
            Show(self.threshold1, self.renderView1)
            Show(self.calculator1, self.renderView1)
            self.ocean_graphic = '%s_BATHEMETRY' % dim
            if 'colormap_json_path' in params.keys() \
                    and type(params['colormap_json_path']).__name__ == 'str' \
                    and os.path.isfile(params['colormap_json_path']):
                with open(params['colormap_json_path']) as json_file:
                    palette_nm = json.load(json_file)[0]["Name"]
                ImportPresets(filename=params['colormap_json_path'])

                # threshold1Display ( Colored by Scalar ) ::: OCEAN AREA ( 2D )
                self.threshold1Display.Ambient = ambient
                self.threshold1Display.Opacity = opacity
                ColorBy(self.threshold1Display, ('POINTS', 'altitude'), True)
                self.separate_threshold1Display_Band1LUT = \
                    GetColorTransferFunction('altitude', self.threshold1Display, separate=True)
                self.separate_threshold1Display_Band1PWF = \
                    GetOpacityTransferFunction('altitude', self.threshold1Display, separate=True)
                self.threshold1Display.RescaleTransferFunctionToDataRange(True, False)
                self.separate_threshold1Display_Band1PWF.RescaleTransferFunction(scale_min, scale_max)
                self.separate_threshold1Display_Band1LUT.RescaleTransferFunction(scale_min, scale_max)
                self.separate_threshold1Display_Band1LUT.ApplyPreset(palette_nm, True)  # Ocean_Scandinavia
                self.separate_threshold1Display_Band1LUT_ColorBar = \
                    GetScalarBar(self.separate_threshold1Display_Band1LUT, self.renderView1)
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleFontFamily = 'File'
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleFontFile = self.ocean_colorbar_font_ttf_path
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleFontSize = 20
                self.separate_threshold1Display_Band1LUT_ColorBar.Title = '수심'
                self.separate_threshold1Display_Band1LUT_ColorBar.ComponentTitle = ' (m)'
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleColor = [0.0, 0.0, 0.0]
                self.separate_threshold1Display_Band1LUT_ColorBar.LabelColor = [0.0, 0.0, 0.0]
                self.separate_threshold1Display_Band1LUT_ColorBar.WindowLocation = 'UpperRightCorner'
                self.separate_threshold1Display_Band1LUT_ColorBar.AddRangeAnnotations = 0
                self.separate_threshold1Display_Band1LUT_ColorBar.DrawTickMarks = 1
                self.separate_threshold1Display_Band1LUT_ColorBar.DrawTickLabels = 1
                self.separate_threshold1Display_Band1LUT_ColorBar.RangeLabelFormat = '%.0f'
                self.separate_threshold1Display_Band1LUT_ColorBar.LabelFormat = '%.0f'
                self.separate_threshold1Display_Band1LUT_ColorBar.HorizontalTitle = 1
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleJustification = 'Left'
                self.separate_threshold1Display_Band1LUT_ColorBar.ScalarBarThickness = 40
                self.separate_threshold1Display_Band1LUT_ColorBar.ScalarBarLength = 0.6
                self.separate_threshold1Display_Band1LUT_ColorBar.TitleBold = 1
                self.separate_threshold1Display_Band1LUT_ColorBar.LabelBold = 1
                self.threshold1Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)

                # calculator1Display ( Not Colored by Scalar ) ::: OCEAN AREA ( 3D )
                self.calculator1Display.Opacity = opacity
                self.calculator1Display.Ambient = ambient
                ColorBy(self.calculator1Display, None)
                HideScalarBarIfNotNeeded(self.band1LUT, self.renderView1)
                self.calculator1Display.DiffuseColor = [80.0 / 255 * 1, 100.0 / 255 * 1, 127.0 / 255 * 1]
            else:
                pass
        elif dim == 'None':
            Hide(self.threshold3, self.renderView1)
            Hide(self.threshold1, self.renderView1)
            Hide(self.calculator1, self.renderView1)
        else:
            pass

    def m00_02_03_set_view_graphics_streamline(self, input_streamline_colorbar_font_ttf_path, scale_min=0,
                                               scale_max=1.4, use_scalar_bar=True, line_width=2, n_of_particles=1500,
                                               opacity=1, max_time_to_live=100, step_len=0.025, alpha=0.1,
                                               color_setting='MAGNITUDE', **params):
        self.streamline_colorbar_font_ttf_path = u'%s' % input_streamline_colorbar_font_ttf_path

        # calculator3Display ( Not Colored by Scalar ) ::: sea_2d.nc AREA ( StreamLine )
        self.calculator3Display.Opacity = opacity
        self.calculator3Display.LineWidth = line_width
        self.calculator3Display.NumberOfParticles = n_of_particles
        self.calculator3Display.MaxTimeToLive = max_time_to_live
        self.calculator3Display.StepLength = step_len
        self.calculator3Display.Alpha = alpha

        if color_setting == 'UNIFORM':
            Show(self.calculator3, self.renderView1)
            ColorBy(self.calculator3Display, None)
            if len({'C', 'c', 'COLOR', 'color'}.intersection(set(params.keys()))) == 1 \
                    and type(params[params.keys()[0]]).__name__ in ['tuple', 'list'] \
                    and len(params[params.keys()[0]]) == 3 \
                    and sum([type(e).__name__ in ['int', 'float'] for e in params[params.keys()[0]]]) == 3:
                self.calculator3Display.DiffuseColor = params[params.keys()[0]]
            else:
                self.calculator3Display.DiffuseColor = [255.0, 255.0, 255.0]

        elif color_setting == 'MAGNITUDE':
            if 'colormap_json_path' in params.keys() \
                    and type(params['colormap_json_path']).__name__ == 'str' \
                    and os.path.isfile(params['colormap_json_path']):
                with open(params['colormap_json_path']) as json_file:
                    palette_nm = json.load(json_file)[0]["Name"]
                ImportPresets(filename=params['colormap_json_path'])
                Show(self.calculator3, self.renderView1)
                ColorBy(self.calculator3Display, ('POINTS', 'Result', 'Magnitude'))
                self.resultLUT = GetColorTransferFunction('Result', self.calculator3Display)
                self.resultPWF = GetOpacityTransferFunction('Result', self.calculator3Display)
                self.resultLUT.RescaleTransferFunction(scale_min, scale_max)
                self.resultPWF.RescaleTransferFunction(scale_min, scale_max)
                self.resultLUT.ApplyPreset(palette_nm, True)  # UVVelocity
                self.resultLUTColorBar = GetScalarBar(self.resultLUT, self.renderView1)
                self.resultLUTColorBar.TitleFontFamily = 'File'
                self.resultLUTColorBar.TitleFontFile = self.streamline_colorbar_font_ttf_path
                self.resultLUTColorBar.TitleFontSize = 20
                self.resultLUTColorBar.Title = '유속'
                self.resultLUTColorBar.ComponentTitle = ' (m/s)'
                self.resultLUTColorBar.TitleColor = [1.0, 1.0, 1.0]
                self.resultLUTColorBar.LabelColor = [1.0, 1.0, 1.0]
                self.resultLUTColorBar.WindowLocation = 'LowerRightCorner'
                self.resultLUTColorBar.AddRangeAnnotations = 0
                self.resultLUTColorBar.DrawTickMarks = 1
                self.resultLUTColorBar.DrawTickLabels = 1
                self.resultLUTColorBar.RangeLabelFormat = '%.0f'
                self.resultLUTColorBar.LabelFormat = '%.0f'
                self.resultLUTColorBar.HorizontalTitle = 1
                self.resultLUTColorBar.TitleJustification = 'Left'
                self.calculator3Display.SetScalarBarVisibility(self.renderView1, use_scalar_bar)
            else:
                pass
        elif color_setting == 'None':
            Hide(self.calculator3, self.renderView1)
        else:
            pass

        self.renderView1.Update()

    def m01_create_avi_by_time_steps(self, input_out_avi_dir, camera_setting="ENTIRE", ts_start=0, ts_end=6,
                                     nof_frames=100, fps=20):
        """Create .avi Format Movie Files for Each Time Steps"""

        # current camera placement for renderView1
        self.renderView1.InteractionMode = '3D'
        self.renderView1.CameraPosition = [191, 25, 173.909]
        self.renderView1.CameraFocalPoint = [191, 25, -225.269]
        self.renderView1.CameraParallelScale = 103.315

        # update the view to ensure updated data information
        self.renderView1.Update()

        import vtk.numpy_interface.dataset_adapter as dsa
        import paraview.numpy_support as pvn
        import numpy as np

        ndArrs = {'SALT': np.array([]), 'TEMP': np.array([]), 'ZETA': np.array([]), 'VELO': np.array([])}

        for ts in sorted(self.sea_2dnc_TimeStepValues):
            tsIdx = sorted(self.sea_2dnc_TimeStepValues).index(ts)
            self.extractTimeSteps1.TimeStepRange = [tsIdx, tsIdx]
            stzData = paraview.servermanager.Fetch(self.threshold3)
            stzWdo = dsa.WrapDataObject(stzData)

            npSaltPts = pvn.vtk_to_numpy(stzWdo.GetPointData().GetArray('salt'))
            ndArrs['SALT'] = np.concatenate((ndArrs['SALT'], npSaltPts), axis=0)
            npTempPts = pvn.vtk_to_numpy(stzWdo.GetPointData().GetArray('temp'))
            ndArrs['TEMP'] = np.concatenate((ndArrs['TEMP'], npTempPts), axis=0)
            npZetaPts = pvn.vtk_to_numpy(stzWdo.GetPointData().GetArray('zeta'))
            ndArrs['ZETA'] = np.concatenate((ndArrs['ZETA'], npZetaPts), axis=0)

            uvMagData = paraview.servermanager.Fetch(self.calculator4)
            npMagPts = pvn.vtk_to_numpy(uvMagData.GetPointData().GetArray('Result'))
            ndArrs['VELO'] = np.concatenate((ndArrs['VELO'], npMagPts), axis=0)

        if self.ocean_graphic not in ["2D_SALT", "2D_TEMP", "2D_ZETA", "2D_VELO"]:
            pass
        else:
            if self.ocean_graphic == "2D_SALT":
                self.saltLUT.RescaleTransferFunction(np.percentile(ndArrs['SALT'], 1),
                                                     np.percentile(ndArrs['SALT'], 100))
                self.saltPWF.RescaleTransferFunction(np.percentile(ndArrs['SALT'], 1),
                                                     np.percentile(ndArrs['SALT'], 100))
            elif self.ocean_graphic == "2D_TEMP":
                self.separate_threshold3Display_tempLUT.RescaleTransferFunction(np.percentile(ndArrs['TEMP'], 0.1),
                                                                                np.percentile(ndArrs['TEMP'], 100))
                self.separate_threshold3Display_tempPWF.RescaleTransferFunction(np.percentile(ndArrs['TEMP'], 0.1),
                                                                                np.percentile(ndArrs['TEMP'], 100))
            elif self.ocean_graphic == "2D_ZETA":
                self.zetaLUT.RescaleTransferFunction(np.percentile(ndArrs['ZETA'], 0.01),
                                                     np.percentile(ndArrs['ZETA'], 99.99))
                self.zetaPWF.RescaleTransferFunction(np.percentile(ndArrs['ZETA'], 0.01),
                                                     np.percentile(ndArrs['ZETA'], 99.99))
            elif self.ocean_graphic == "2D_VELO":
                self.veloLUT.RescaleTransferFunction(np.percentile(ndArrs['VELO'], 0),
                                                     np.percentile(ndArrs['VELO'], 99.5))
                self.veloPWF.RescaleTransferFunction(np.percentile(ndArrs['VELO'], 0),
                                                     np.percentile(ndArrs['VELO'], 99.5))
            else:
                pass
        self.renderView1.Update()

        if self.show_time_label:
            Show(self.pythonAnnotation1, self.renderView1)

        # Properties modified on animationScene1
        self.animationScene1.PlayMode = 'Sequence'

        # Properties modified on animationScene1
        self.animationScene1.NumberOfFrames = nof_frames

        # Set the Animation Loop On
        self.animationScene1.Loop = 1

        # update animation scene based on data timesteps !!
        # self.animationScene1.UpdateAnimationUsingDataTimeSteps()

        # Not Using AnimationTime ( Equivalent to Toggle  the TimeKeeper Check Box )
        self.animationScene1.Cues[0].UseAnimationTime = 0
        self.animationScene1.Cues[0].Enabled = 0

        # save animation
        for time_step in sorted(self.sea_2dnc_TimeStepValues):
            time_step_idx = self.sea_2dnc_TimeStepValues.index(time_step)

            if not (ts_start <= time_step_idx <= ts_end):
                pass
            else:
                hours = datetime.timedelta(seconds=time_step)
                time_value = self.DATUM + hours
                self.extractTimeSteps1.TimeStepRange = [time_step_idx, time_step_idx]
                print(time_value)

                # update the view to ensure updated data information
                self.renderView1.Update()

                input_out_avi_path = \
                    os.path.join(input_out_avi_dir, self.current_time_str,
                                 u'sea_{}_streamline{}_{}{}{}{}.ogv'
                                 .format(self.current_time_str,
                                         "_" + camera_setting.lower() if camera_setting in ["WEST", "EAST", "SOUTH"] else "",
                                         time_value.year, u'%02d' % time_value.month, u'%02d' % time_value.day,
                                         u'%02d' % time_value.hour,
                                         ))
                if not os.path.exists(os.path.dirname(input_out_avi_path)):
                    os.makedirs(os.path.dirname(input_out_avi_path))

                SaveAnimation(filename=input_out_avi_path, View=self.renderView1, scene=self.animationScene1,
                              ImageResolution=[self.view_size_h, self.view_size_v],
                              ImageQuality=2,
                              FontScaling="Scale fonts proportionally",
                              FrameRate=fps,
                              FrameWindow=[0, self.animationScene1.NumberOfFrames - 1])

        # current camera placement for renderView1
        # self.renderView1.InteractionMode = '3D'
        self.renderView1.ResetCamera()

    def m01_create_avi(self, input_out_avi_dir, ts_start=0, ts_end=23,
                       nof_frames=720, fps=10):
        """Create .avi Format Movie Files for Each Time Steps"""

        # current camera placement for renderView1
        self.renderView1.InteractionMode = '3D'
        self.renderView1.CameraPosition = [191, 25, 173.909]
        self.renderView1.CameraFocalPoint = [191, 25, -225.269]
        self.renderView1.CameraParallelScale = 103.315

        # update the view to ensure updated data information
        self.renderView1.Update()

        import vtk.numpy_interface.dataset_adapter as dsa
        import paraview.numpy_support as pvn
        import numpy as np

        ndArrs = {'SALT': np.array([]), 'TEMP': np.array([]), 'ZETA': np.array([]), 'VELO': np.array([])}

        for ts in sorted(self.sea_2dnc_TimeStepValues):
            tsIdx = sorted(self.sea_2dnc_TimeStepValues).index(ts)
            self.extractTimeSteps1.TimeStepRange = [tsIdx, tsIdx]
            stzData = paraview.servermanager.Fetch(self.threshold3)
            stzWdo = dsa.WrapDataObject(stzData)

            npSaltPts = pvn.vtk_to_numpy(stzWdo.GetPointData().GetArray('salt'))
            ndArrs['SALT'] = np.concatenate((ndArrs['SALT'], npSaltPts), axis=0)
            npTempPts = pvn.vtk_to_numpy(stzWdo.GetPointData().GetArray('temp'))
            ndArrs['TEMP'] = np.concatenate((ndArrs['TEMP'], npTempPts), axis=0)
            npZetaPts = pvn.vtk_to_numpy(stzWdo.GetPointData().GetArray('zeta'))
            ndArrs['ZETA'] = np.concatenate((ndArrs['ZETA'], npZetaPts), axis=0)

            uvMagData = paraview.servermanager.Fetch(self.calculator4)
            npMagPts = pvn.vtk_to_numpy(uvMagData.GetPointData().GetArray('Result'))
            ndArrs['VELO'] = np.concatenate((ndArrs['VELO'], npMagPts), axis=0)

        if self.ocean_graphic not in ["2D_SALT", "2D_TEMP", "2D_ZETA", "2D_VELO"]:
            pass
        else:
            if self.ocean_graphic == "2D_SALT":
                self.saltLUT.RescaleTransferFunction(np.percentile(ndArrs['SALT'], 0.05),
                                                     np.percentile(ndArrs['SALT'], 100))
                self.saltPWF.RescaleTransferFunction(np.percentile(ndArrs['SALT'], 0.05),
                                                     np.percentile(ndArrs['SALT'], 100))
            elif self.ocean_graphic == "2D_TEMP":
                self.separate_threshold3Display_tempLUT.RescaleTransferFunction(np.percentile(ndArrs['TEMP'], 0.01),
                                                                                np.percentile(ndArrs['TEMP'], 100) + 5)
                self.separate_threshold3Display_tempPWF.RescaleTransferFunction(np.percentile(ndArrs['TEMP'], 0.01),
                                                                                np.percentile(ndArrs['TEMP'], 100) + 5)
            elif self.ocean_graphic == "2D_ZETA":
                self.zetaLUT.RescaleTransferFunction(np.percentile(ndArrs['ZETA'], 0.01),
                                                     np.percentile(ndArrs['ZETA'], 100))
                self.zetaPWF.RescaleTransferFunction(np.percentile(ndArrs['ZETA'], 0.01),
                                                     np.percentile(ndArrs['ZETA'], 100))
            elif self.ocean_graphic == "2D_VELO":
                self.veloLUT.RescaleTransferFunction(np.percentile(ndArrs['VELO'], 0),
                                                     np.percentile(ndArrs['VELO'], 99.5))
                self.veloPWF.RescaleTransferFunction(np.percentile(ndArrs['VELO'], 0),
                                                     np.percentile(ndArrs['VELO'], 99.5))
            else:
                pass
        self.renderView1.Update()

        if self.show_time_label:
            Show(self.pythonAnnotation1, self.renderView1)

        # Set the TimeStep Range
        self.extractTimeSteps1.TimeStepRange = [ts_start, ts_end]
        self.animationScene1.StartTime = sorted(self.sea_2dnc_TimeStepValues)[ts_start]
        self.animationScene1.EndTime = sorted(self.sea_2dnc_TimeStepValues)[ts_end]

        # update the view to ensure updated data information
        self.renderView1.Update()

        # Properties modified on animationScene1
        self.animationScene1.PlayMode = 'Sequence'

        # Properties modified on animationScene1
        self.animationScene1.NumberOfFrames = nof_frames

        # Set the Animation Loop On
        self.animationScene1.Loop = 1

        hours = datetime.timedelta(seconds=self.animationScene1StartTime)
        time_value = self.DATUM + hours

        input_out_avi_path = \
            os.path.join(input_out_avi_dir, self.current_time_str,
                         u'npac_{}.ogv'
                         .format(u'salt' if self.ocean_graphic == u'2D_SALT'
                                 else u'temp' if self.ocean_graphic == u'2D_TEMP'
                                 else u'zeta' if self.ocean_graphic == u'2D_ZETA'
                                 else u'velo' if self.ocean_graphic == u'2D_VELO'
                                 else u''
                                 ))
        if not os.path.exists(os.path.dirname(input_out_avi_path)):
            os.makedirs(os.path.dirname(input_out_avi_path))

        SaveAnimation(filename=input_out_avi_path, View=self.renderView1, scene=self.animationScene1,
                      ImageResolution=[self.view_size_h, self.view_size_v],
                      ImageQuality=2,
                      FontScaling="Scale fonts proportionally",
                      FrameRate=fps,
                      FrameWindow=[0, self.animationScene1.NumberOfFrames - 1])

        # update animation scene based on data timesteps !!
        # self.animationScene1.UpdateAnimationUsingDataTimeSteps()

    def m02_start_interactive_window(self, input_slider_ttf_path, use_time_step_slider=True):

        self.extractSubset1.VOI = [0, 11160, 0, 5100, 0, 0]  # etopo
        self.extractSubset2.VOI = [0, 744, 0, 427, 0, 0]  # sea
        self.renderView1.Update()

        if self.show_time_label:
            Show(self.pythonAnnotation1, self.renderView1)
            self.pythonAnnotation1Display.WindowLocation = 'AnyLocation'
            self.pythonAnnotation1Display.Position = [0.421, 0.06]

        # current camera placement for renderView1
        self.renderView1.InteractionMode = '3D'
        self.renderView1.CameraPosition = [191, 25, 173.909]
        self.renderView1.CameraFocalPoint = [191, 25, -225.269]
        self.renderView1.CameraParallelScale = 103.315

        # update the view to ensure updated data information
        self.renderView1.Update()

        # Set Rendering on Interaction Enabled
        self.renderView1.EnableRenderOnInteraction = 1

        # Get the Interactor And Render Window
        self.interactor1 = self.renderView1.GetInteractor()
        self.interactor1_rw1 = self.interactor1.GetRenderWindow()

        # Register the Current Renderer to the Current Render Window
        self.interactor1_rw1.AddRenderer(self.renderer1)

        # Get the Interactor Helper
        self.interactor1_helper1 = self.renderView1.GetInteractorHelper()  # vtkSMViewProxyInteractorHelper

        # Set the Interacting Option On
        self.interactor1_helper1.Interacting = True

        # Setting Up the Interactor to the Current View Proxy
        self.view_proxy1 = self.interactor1_helper1.GetViewProxy()  # vtkSMRenderViewProxy
        self.view_proxy1.EnableOn()
        self.view_proxy1.SetupInteractor(self.interactor1)

        # Set the Interactive Window Title
        self.interactor1_rw1.SetWindowName(os.path.basename(self.sea_2d_nc_path))

        # Make InteractiveRendererWindow Current
        self.interactor1_rw1.MakeCurrent()

        # Set Current Renderer
        self.interactor1.GetInteractorStyle().SetCurrentRenderer(self.renderer1)

        # Get the Interactor Style Handler
        self.interactor1_style1 = self.interactor1.GetInteractorStyle()

        # Set the Current Renderer as Interactor Style Handler's Current Renderer
        self.interactor1_style1.SetCurrentRenderer(self.renderer1)

        # Start Animating the StreamLine Flow
        self.interactor1_style1.StartAnimate()

        # Get the Render Window Interactor
        self.view_proxy_interactor1 = self.view_proxy1.GetInteractor()

        #### uncomment the following to render all views
        # RenderAllViews()
        # alternatively, if you want to write images, you can use SaveScreenshot(...).

        #### import the VTK
        import vtk

        # Add the Mapping Actor's Event as Observer Named 'AutoReplay' to the Interactor
        self.actor1 = vtk.vtkActor()
        self.mapper1 = vtk.vtkPolyDataMapper()
        self.actor1.SetMapper(self.mapper1)
        self.cb1 = vtkTimerCallback()
        self.cb1.actor = self.actor1
        self.interactor1.AddObserver('AutoReplay', self.cb1.execute)
        self.loopPlayerId = self.interactor1.CreateRepeatingTimer(1)

        # Add the TimeStep Slider Inside the View
        if use_time_step_slider:
            self.sliderRep1 = vtk.vtkSliderRepresentation2D()
            self.sliderRep1.SetMinimumValue(min(self.sea_2dnc_TimeStepValues))
            self.sliderRep1.SetMaximumValue(max(self.sea_2dnc_TimeStepValues))
            self.sliderRep1.SetValue(self.renderView1.ViewTime)
            # self.sliderRep1.SetSliderWidth(1)

            self.sliderRep1.GetSliderProperty().SetColor(0, 0, 0)
            self.sliderRep1.GetTitleProperty().SetColor(1, 1, 1)
            self.sliderRep1.GetTitleProperty().SetFontFamilyAsString('File')
            self.sliderRep1.GetTitleProperty().SetFontFile(input_slider_ttf_path)
            self.sliderRep1.SetTitleText("")
            self.sliderRep1.SetShowSliderLabel(False)
            self.sliderRep1.GetLabelProperty().SetColor(1, 1, 1)
            self.sliderRep1.GetSelectedProperty().SetColor(0, 0, 1)
            self.sliderRep1.GetTubeProperty().SetColor(1, 1, 1)
            self.sliderRep1.GetCapProperty().SetColor(1, 1, 1)
            self.sliderRep1.GetCapProperty().SetOpacity(0)
            self.sliderRep1.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
            self.sliderRep1.GetPoint1Coordinate().SetValue(600, 50)
            self.sliderRep1.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
            self.sliderRep1.GetPoint2Coordinate().SetValue(1000, 50)
            self.sliderRep1.SetRenderer(self.renderer1)

            self.sliderWidget1 = vtk.vtkSliderWidget()
            self.sliderWidget1.SetInteractor(self.view_proxy_interactor1)
            self.sliderWidget1.SetRepresentation(self.sliderRep1)
            self.sliderWidget1.SetAnimationModeToAnimate()
            self.sliderWidget1.EnabledOn()

            self.actor2 = vtk.vtkActor()
            self.mapper2 = vtk.vtkPolyDataMapper()
            self.actor2.SetMapper(self.mapper2)
            self.cb2 = vtkSliderCallback(tk=self.timeKeeper1)
            self.cb2.actor = self.actor2
            self.sliderWidget1.AddObserver(vtk.vtkCommand.InteractionEvent, self.cb2.execute)

        # Add the Playback Widget Inside the View
        """self.playBackRep1 = vtkSubclassPlaybackRepresentation()
        self.playBackRep1.SetRenderer(self.renderer1)
        self.playBackRep1.SetShowBorderToActive()
        # self.playBackRep1.SetPosition(120, 110)
        # self.playBackRep1.SetPosition2(420, 50)
        # self.playBackRep1.StartWidgetInteraction()
        self.playBackWidget1 = vtk.vtkPlaybackWidget()
        self.playBackWidget1.SetInteractor(self.view_proxy_interactor1)
        self.playBackWidget1.SetCurrentRenderer(self.renderer1)
        self.playBackWidget1.SetRepresentation(self.playBackRep1)
        self.playBackWidget1.On()
        self.playBackWidget1.SetEnabled(True)
        self.playBackWidget1.EnabledOn()
        self.playBackWidget1.SetProcessEvents(True)
        self.playBackWidget1.KeyPressActivationOn()
        # self.playBackWidget1.AddObserver(vtk.vtkCommand.InteractionEvent, self.cb2.execute)
        self.recorder1 = vtk.vtkInteractorEventRecorder()
        self.recorder1.SetInteractor(self.view_proxy_interactor1)
        self.recorder1.SetCurrentRenderer(self.renderer1)
        self.recorder1.SetFileName('record.log')
        self.recorder1.Record()"""

        # self.playButtonRep = vtk.vtkButtonRepresentation()

        self.playButtonWidget = vtk.vtkButtonWidget()
        self.playButtonWidget.SetInteractor(self.interactor1)
        # self.playButtonWidget.SetRepresentation(self.playButtonRep)
        self.playButtonWidget.CreateDefaultRepresentation()
        self.playButtonWidget.SetEnabled(1)

        self.playButtonRep = self.playButtonWidget.GetSliderRepresentation()

        # Pop Up Interactive Window
        self.view_proxy1.StreamingUpdate(True)
        self.view_proxy_interactor1.Initialize()

        # Set the Logo Widget Interaction On
        """self.logo_widget.SetInteractor(self.interactor1)
        self.logo_widget.On()"""

        self.interactor1_rw1.Render()
        # self.recorder1.Off()
        self.view_proxy_interactor1.Start()

    def m03_start_animation_window(self):

        # Set Visibility of Time Label Annotation
        if self.show_time_label:
            Show(self.pythonAnnotation1, self.renderView1)

        # Set the Whole Time Step Range
        self.extractTimeSteps1.TimeStepRange = [0, len(self.sea_2dnc_TimeStepValues) - 1]

        # Set the Animation Window Name
        self.renderView1.GetInteractor().GetRenderWindow().SetWindowName('AnimationView')

        # Set the Camera
        self.renderView1.InteractionMode = '2D'
        self.renderView1.CameraPosition = [127.133, 31.525, 43.6186]
        self.renderView1.CameraFocalPoint = [127.133, 31.525, -0.381325]
        self.renderView1.CameraParallelScale = 11.0

        # Update the Render View
        self.renderView1.Update()

        # Play the Animation Scene
        self.animationScene1.Loop = 1
        self.animationScene1.Play()


if __name__ == '__main__':

    activeView1 = ActiveView(
        input_sl_dll_path="C:\\Program Files\\ParaView 5.6.0-MPI-Windows-msvc2015-64bit\\bin\\plugins\\StreamLinesRepresentation\\StreamLinesRepresentation.dll",
        input_etopo_south_nc_path="E:\\PARAVIEW\\NORTH_PACIFIC\\etopo0_360.nc",
        input_sea_2d_nc_path="E:\\PARAVIEW\\NORTH_PACIFIC\\npac_2d.nc",
        input_time_font_ttf_path='D:\\PARAVIEW\\01_sea\\DATA\\fonts\\NanumBarunGothicBold.ttf',
        use_time_label=True,
        input_view_size_h=1600,
        input_view_size_v=900)
    activeView1.m00_02_00_set_view_graphics_background(False, (0.4, 0.4, 0.4))

    ########## 1. SALT ##########
    activeView1.m00_01_set_all_filters_visibility_off()
    activeView1.m00_02_01_set_view_graphics_land(
        dim="3D", use_scalar_bar=False, scale_min=-1000, scale_max=5000,
        input_land_colorbar_font_ttf_path='D:\\PARAVIEW\\01_sea\\DATA\\fonts\\NanumBarunGothic.ttf',
        colormap_json_path='D:\\PARAVIEW\\01_sea\\DATA\\colormaps\\sample5_land_topo_color.json'
    )
    activeView1.m00_02_02_set_view_graphics_ocean(
        dim='2D', var='salt', scale_min=20, scale_max=36, opacity=1,
        input_ocean_colorbar_font_ttf_path='D:\\PARAVIEW\\01_sea\\DATA\\fonts\\NanumBarunGothic.ttf',
        colormap_json_path='D:\\PARAVIEW\\01_sea\\DATA\\colormaps\\sample5_1_Salinity_Palette_1.json'
    )
    """activeView1.m01_create_avi(input_out_avi_dir=u"C:\\Users\\bntcsh\\Documents\\190826", ts_start=0, ts_end=6,
                               nof_frames=70, fps=10)"""

    ########## 2. TEMP ##########
    activeView1.m00_01_set_all_filters_visibility_off()
    activeView1.m00_02_01_set_view_graphics_land(
        dim="3D", use_scalar_bar=False, scale_min=-1000, scale_max=5000,
        input_land_colorbar_font_ttf_path='D:\\PARAVIEW\\01_sea\\DATA\\fonts\\NanumBarunGothic.ttf',
        colormap_json_path='D:\\PARAVIEW\\01_sea\\DATA\\colormaps\\sample5_land_topo_color.json'
    )
    activeView1.m00_02_02_set_view_graphics_ocean(
        dim='2D', var='temp', scale_min=5, scale_max=34, opacity=1,
        input_ocean_colorbar_font_ttf_path='D:\\PARAVIEW\\01_sea\\DATA\\fonts\\NanumBarunGothic.ttf',
        colormap_json_path='D:\\PARAVIEW\\01_sea\\DATA\\colormaps\\sample5_1_Temperature_Palette_1.json'
    )
    """activeView1.m01_create_avi(input_out_avi_dir=u"C:\\Users\\bntcsh\\Documents\\190826", ts_start=0, ts_end=6,
                               nof_frames=70, fps=10)"""

    ########## 3. ZETA ##########
    activeView1.m00_01_set_all_filters_visibility_off()
    activeView1.m00_02_01_set_view_graphics_land(
        dim="3D", use_scalar_bar=False, scale_min=-1000, scale_max=5000,
        input_land_colorbar_font_ttf_path='D:\\PARAVIEW\\01_sea\\DATA\\fonts\\NanumBarunGothic.ttf',
        colormap_json_path='D:\\PARAVIEW\\01_sea\\DATA\\colormaps\\sample5_land_topo_color.json'
    )
    activeView1.m00_02_02_set_view_graphics_ocean(
        dim='2D', var='zeta', scale_min=-2.3, scale_max=3.4, opacity=1,
        input_ocean_colorbar_font_ttf_path='D:\\PARAVIEW\\01_sea\\DATA\\fonts\\NanumBarunGothic.ttf',
        colormap_json_path='D:\\PARAVIEW\\01_sea\\DATA\\colormaps\\sample5_1_Salinity_Palette_1.json'
    )
    """activeView1.m01_create_avi(input_out_avi_dir=u"C:\\Users\\bntcsh\\Documents\\190826", ts_start=0, ts_end=6,
                               nof_frames=70, fps=10)"""

    ########## 4-2. StreamLine ::: ENTIRE ##########
    activeView1.m00_01_set_all_filters_visibility_off()
    activeView1.m00_02_01_set_view_graphics_land(
        dim="3D", use_scalar_bar=False, scale_min=-1000, scale_max=5000,
        input_land_colorbar_font_ttf_path='D:\\PARAVIEW\\01_sea\\DATA\\fonts\\NanumBarunGothic.ttf',
        colormap_json_path='D:\\PARAVIEW\\01_sea\\DATA\\colormaps\\sample5_land_topo_color.json'
    )
    activeView1.m00_02_02_set_view_graphics_ocean(
        dim='2D', var='velocity', scale_min=0, scale_max=2, opacity=0.5,
        input_ocean_colorbar_font_ttf_path='D:\\PARAVIEW\\01_sea\\DATA\\fonts\\NanumBarunGothic.ttf',
        colormap_json_path='D:\\PARAVIEW\\01_sea\\DATA\\colormaps\\sample5_1_Salinity_Palette_1.json'
    )
    activeView1.m00_02_03_set_view_graphics_streamline(
        color_setting='UNIFORM', line_width=2, n_of_particles=7500, max_time_to_live=60, step_len=0.1, alpha=0.2,
        opacity=1,
        input_streamline_colorbar_font_ttf_path='D:\\PARAVIEW\\01_sea\\DATA\\fonts\\NanumBarunGothic.ttf',
        color=[255, 255, 255]
    )
    activeView1.m01_create_avi_by_time_steps(
        input_out_avi_dir=u"C:\\Users\\bntcsh\\Documents\\190826",
        nof_frames=100, fps=20)
    activeView1.m02_start_interactive_window(input_slider_ttf_path='D:\\PavaViewBaseMaps\\fonts\\NanumBarunGothic.ttf')
