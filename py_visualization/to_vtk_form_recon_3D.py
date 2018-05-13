import numpy as np
import sys
import vtk

dataName = sys.argv[1]
vert = np.loadtxt("../result/" + dataName + "/vert.txt")
edge = np.loadtxt("../result/" + dataName + "/edge.txt")

nv = len(vert)
pts = vtk.vtkPoints()
for i in range(nv):
    pts.InsertNextPoint(vert[i,1],vert[i,0],vert[i,2])

ne = len(edge)
lines = vtk.vtkCellArray()
for i in range(ne):
    v1_ind = int(edge[i,0])
    v2_ind = int(edge[i,1])
    new_line = vtk.vtkLine()
    new_line.GetPointIds().SetId(0, v1_ind)
    new_line.GetPointIds().SetId(1, v2_ind)
    lines.InsertNextCell(new_line)

linesPolyData = vtk.vtkPolyData()
linesPolyData.SetPoints(pts)
linesPolyData.SetLines(lines)

gw = vtk.vtkXMLPolyDataWriter()
gw.SetFileName("../result/" + dataName + "/reconstruction.vtp")
gw.SetInputData(linesPolyData)
gw.Write()

