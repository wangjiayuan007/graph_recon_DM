Paper on arXiv: https://arxiv.org/abs/1803.05093 <br />

spt_cpp/ contains the source code for graph reconstruction, py_visualization/ contains the source code converting result to Paraview format.<br />

#Compile spt_cpp:<br />

To compile files in spt_cpp/, change directory to spt_cpp/, run the following command in the terminal:<br />

Linux/macOS:<br />
g++ DiMoSC.cpp -I./phat/include -std=c++11 -o spt_cpp<br />

Windows(g++ need installed):<br />
g++ -static DiMoSC.cpp -I./phat/include -std=c++11 -o spt_cpp<br />

#Run spt_cpp:<br />

Usage: ./spt_cpp <input_file> <output_file> <persistence_threshold> <dimension> [use_previous]<br />

For example, running on the test dataset dataset/test3D, change directory to spt_cpp/, run the following command: <br />
3D:<br />
./spt_cpp ../dataset/test_3D/SC.bin ../result/test_3D 20 3<br />
2D:<br />
./spt_cpp ../dataset/Berlin/SC.bin ../result/Berlin 0.01 2<br />

##Input:<br />
SC.bin is a binary file contains the informaiton of the input triangulation and density function defined on the vertices.<br />

##Output:<br />
vert.txt: <br />
x1 y1 (z1) f1<br />
x2 y2 (z2) f2<br />
x3 y3 (z3) f3<br />
...<br />

edge.txt<br />
vertex1_index1 vertex1_index2<br />
vertex2_index1 vertex2_index2<br />
...<br />


#Visualization(python3.6 numpy, sys, vtk package needed):<br />

##Convert output of graph reconstruction to .vtp:<br />
Change directory to py_visualization/ (If not using the same directory structure, the directory location needs to be changed inside the code), run the following command in the terminal:<br />

2D dataset:<br />
python to_vtk_form_recon_2D.py <dataset_name><br />

3D dataset:<br />
python to_vtk_form_recon_3D.py <dataset_name><br />

For example, 'python to_vtk_form_recon_3D.py test_3D' generates the vtp file for test_3D. Then you can open the vtp file in Paraview directly.<br />
'python to_vtk_form_recon_2D.py Berlin' generates the vtp file for Berlin.<br />

##3D volume rendering<br />
.raw files are used for volume rendering.<br />
Open .raw file in Paraview, <br />

test_3D:<br />
Select Raw(binary) files when opening<br />
Data scalar type: float<br />
Data extent <br />
0 49<br />
0 49<br />
0 49<br />

ENZO:<br />
Select Raw(binary) files when opening<br />
Data scalar type: float<br />
Data extent <br />
0 63<br />
0 63<br />
0 63<br />

Bone<br />
Select Raw(binary) files when opening<br />
Data scalar type: unsigned char<br />
Data extent <br />
0 245<br />
0 147<br />
0 146<br />

#Dataset:<br />
https://drive.google.com/open?id=1pnmR66-7MXqwZf9wexPnvtoLB3XAq4Wu<br />
2D datasets: Athens, Berlin<br />
3D datasets: ENZO, bone<br />
sur.vtp is the density terrain of 2D datasets, which can be opened directly in Paraview

