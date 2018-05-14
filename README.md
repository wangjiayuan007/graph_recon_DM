spt_cpp/ contains the source code for graph reconstruction, py_visualization/ contains the source code converting result to paraview format.<br />

#Compile spt_cpp:<br />

To compile files in spt_cpp/, change directory to spt_cpp/, run the following command in the terminal:<br />

Linux/macOS:<br />
g++ DiMoSC.cpp -I./phat/include -std=c++11 -o spt_cpp<br />

Windows(g++ need installed):<br />
g++ -static DiMoSC.cpp -I./phat/include -std=c++11 -o spt_cpp<br />

#Run spt_cpp:<br />

Usage: ./spt_cpp <input_file> <output_file> <persistence_threshold> <dimension> [use_previous]<br />

For example, running on the test dataset dataset/test3D, change directory to spt_cpp/, run the following command: <br />

./spt_cpp ../dataset/test_3D/SC.bin ../result/test_3D 20 3<br />

#Visualization(python3.6 numpy, sys, vtk package needed):<br />

##Convert output of graph reconstruction to .vtp:<br />
Change directory to py_visualization/ (If not using the same directory structure, the directory location needs to be changed inside the code), run the following command in the terminal:<br />

python to_vtk_form_recon_2D.py <dataset_name><br />

For example, 'python to_vtk_form_recon_2D.py test_3D' generates the vtp file for test_3D. Then you can open the vtp file in preview directly.<br />

##3D volume rendering<br />
.raw files are used for volume rendering.<br />
Open .raw file in preview, <br />

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
sur.vtp is the density terrain of 2D datasets

