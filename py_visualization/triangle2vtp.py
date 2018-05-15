import numpy as np
import sys
import vtk

multi = 25e2
dataName = sys.argv[1]
vert = np.loadtxt("../dataset/"+dataName+"/tri_vert.txt")
tri = np.loadtxt("../dataset/"+dataName+"/tri_triangle.txt")

vert[:,2] = np.max(vert[:,2])-vert[:,2]

Points = vtk.vtkPoints()
Triangles = vtk.vtkCellArray()

value = vtk.vtkFloatArray()
value.SetNumberOfComponents(1)
value.SetName("value")

print("write points:")
nv = len(vert)
for i in range(nv):
    Points.InsertNextPoint(vert[i, 0], vert[i, 1], vert[i, 2]*multi)
    value.InsertNextValue(vert[i, 2])

print("write triangles:")
nt = len(tri)
for i in range(nt):
    #new_tri = vtk.vtkTriangle()
    tri_ind = tri[i,:]
    ind1 = int(tri_ind[0])
    ind2 = int(tri_ind[1])
    ind3 = int(tri_ind[2])
    Triangles.InsertNextCell(3)
    Triangles.InsertCellPoint(ind1)
    Triangles.InsertCellPoint(ind2)
    Triangles.InsertCellPoint(ind3)

    # new_tri.GetPointIds().SetId(ind1, ind1)
    # new_tri.GetPointIds().SetId(ind2, ind2)
    # new_tri.GetPointIds().SetId(ind3, ind3)
    #Triangles.InsertNextCell(new_tri)

polydata = vtk.vtkPolyData()
polydata.SetPoints(Points)
polydata.SetPolys(Triangles)
polydata.GetPointData().SetScalars(value)

gw = vtk.vtkXMLPolyDataWriter()
gw.SetFileName("../result/"+dataName+"/suf.vtp")
gw.SetInputData(polydata)
gw.Write()