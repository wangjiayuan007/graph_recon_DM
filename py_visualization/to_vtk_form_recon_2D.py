import numpy as np
import sys
import vtk

multi = 25e2
dataName = sys.argv[1]
# all_vert = np.loadtxt("Input/sigma40_step10/tri_vert.txt")
#vert = np.loadtxt("../result/Athens_vert.txt")
# vert[:,2] = np.max(all_vert[:,2])-vert[:,2]
#edge = np.loadtxt("../result/Athens_edge.txt")
vert = np.loadtxt("../result/" + dataName + "/vert.txt")
edge = np.loadtxt("../result/" + dataName + "/edge.txt")
# edge = edge - 1
# all_vert = np.loadtxt("Input/tri_vert.txt")
nv = len(vert)
pts = vtk.vtkPoints()
for i in range(nv):
    pts.InsertNextPoint(vert[i,0],vert[i,1],vert[i,2]*multi-10)

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
gw.SetFileName("../result/"+dataName+"/reconstruction.vtp")
gw.SetInputData(linesPolyData)
gw.Write()

