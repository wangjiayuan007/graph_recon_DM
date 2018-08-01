# Graph reconstruction

Paper on arXiv: https://arxiv.org/abs/1803.05093 

## Introduction

spt_cpp/ contains the source code for graph reconstruction, py_visualization/ contains the source code converting result to Paraview format. You need to compile spt_cpp first and call it from graphRecon.py. Please maintain the given directory structure. 

## Compile spt_cpp

To compile files in spt_cpp/, change directory to spt_cpp/, run the following command in the terminal:

Linux/macOS:
```
g++ DiMoSC.cpp -I./phat/include -std=c++11 -o spt_cpp
```

Windows(g++ need installed):
```
g++ -static DiMoSC.cpp -I./phat/include -std=c++11 -o spt_cpp
```

## Running the tests

Usage: 

python graphRecon.py <dataset_name> <dataset_form> <dimension> <threshold>

<dataset_form>   -g input grid

<dataset_form>   -t input triangulation

2D triangulation as input:
```
python graphRecon.py Berlin -t 2 0.1
```
2D grid as input:
```
python graphRecon.py grid2D -g 2 0.6
```
3D triangulation as input:
```
python graphRecon.py test_3D -t 3 0.05
```
3D grid as input:
```
python graphRecon.py test_3D -g 3 0.05
```

All datasets can be downloaded [here](https://drive.google.com/drive/u/1/folders/1pnmR66-7MXqwZf9wexPnvtoLB3XAq4Wu).

## Input

The input could be 2D/3D grids or trianglations from density functions.

### 2D grid: 

the input text file should store the 2D grid as a matrixs. You can simply store your 2D array in python using np.savetxt(). 

### 3D grid:

the first line of the input text file is the dimension of the 3D grid m,n,l. And the 3D array is stored as 1D array after being flattened with np.reshape([m* n* l]).

### 2D/3D triangulations:

The triangulation is stored in three files: tri_vert.txt, tri_edge.txt and tri_triangle.txt

**tri_vert.txt**:

x1 y1 (z1) f1 

x2 y2 (z2) f2 

x3 y3 (z3) f3 

...

**tri_edge.txt**:

e1_adjacent_vertex_index1 e1_adjacent_vertex_index2

e2_adjacent_vertex_index1 e2_adjacent_vertex_index2

...

**tri_triangle.txt**:

t1_adjacent_vertex_index1 t1_adjacent_vertex_index2 t1_adjacent_vertex_index3

t2_adjacent_vertex_index1 t2_adjacent_vertex_index2 t2_adjacent_vertex_index3

...


## Output

The output graph is stored in two files: vert.txt and edge.txt

**vert.txt**: 

x1 y1 (z1) f1

x2 y2 (z2) f2

x3 y3 (z3) f3

...

**edge.txt**:

e1_adjacent_vertex_index1 e1_adjacent_vertex_index2

e2_adjacent_vertex_index1 e2_adjacent_vertex_index2

...


## Visualization by paraview(python3.6 numpy, sys, vtk package needed):

### Convert output of graph reconstruction to .vtp:

Change directory to py_visualization/ (If not using the same directory structure, the directory location needs to be changed inside the code), run the following command in the terminal:

2D dataset:
```
python to_vtk_form_recon_2D.py <dataset_name>
```
3D dataset:
```
python to_vtk_form_recon_3D.py <dataset_name>
```
For example, 'python to_vtk_form_recon_3D.py test_3D' generates the vtp file for test_3D. Then you can open the vtp file in Paraview directly.

'python to_vtk_form_recon_2D.py Berlin' generates the vtp file for Berlin.

### 3D volume rendering

Instructions on volume rendering see [here](http://wiki.rac.manchester.ac.uk/community/ParaView/Tips/LoadImageStack).

.raw files are used for volume rendering.

Open .raw file in Paraview, 

test_3D:


Select Raw(binary) files when opening

Data scalar type: float

Data extent

0 49

0 49

0 49

ENZO:


Select Raw(binary) files when opening

Data scalar type: float

Data extent

0 63

0 63

0 63

Bone


Select Raw(binary) files when opening

Data scalar type: unsigned char

Data extent

0 245

0 147

0 146


## Dataset:

All datasets can be downloaded [here](https://drive.google.com/drive/u/1/folders/1pnmR66-7MXqwZf9wexPnvtoLB3XAq4Wu).

2D datasets: Athens, Berlin

3D datasets: ENZO, bone,test_3D 

sur.vtp is the density terrain of 2D datasets, which can be opened directly in Paraview

