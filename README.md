spt_cpp/ contains the source code for graph reconstruction, py_visualization/ contains the source code converting result to paraview format.

#Compile spt_cpp:

To compile files in spt_cpp/, change directory to spt_cpp/, run the following command in the terminal:

Linux/macOS:
g++ DiMoSC.cpp -I./phat/include -std=c++11 -o spt_cpp

Windows(g++ need installed):
g++ -static DiMoSC.cpp -I./phat/include -std=c++11 -o spt_cpp

#Run spt_cpp:

Usage: ./spt_cpp <input_file> <output_file> <persistence_threshold> <dimension> [use_previous]

For example, running on the test dataset dataset/test3D, change directory to spt_cpp/, run the following command: 

./spt_cpp ../dataset/test_3D/SC.bin ../result/test_3D 20 3

#Visualization(python3.6 numpy, sys, vtk package needed):

##Convert output of graph reconstruction to .vtp:
Change directory to py_visualization/ (If not using the same directory structure, the directory location needs to be changed inside the code), run the following command in the terminal:

python to_vtk_form_recon_2D.py <dataset_name>

For example, 'python to_vtk_form_recon_2D.py test_3D' generates the vtp file for test_3D. Then you can open the vtp file in preview directly.

##3D volume rendering
.raw files are used for volume rendering.
Open .raw file in preview, 

test_3D:
Select Raw(binary) files when opening
Data scalar type: float
Data extent 0 49
            0 49
            0 49

ENZO:
Select Raw(binary) files when opening
Data scalar type: float
Data extent 0 63
            0 63
            0 63

Bone
Select Raw(binary) files when opening
Data scalar type: unsigned char
Data extent 0 245
            0 147
            0 146

#Dataset:
https://drive.google.com/open?id=1pnmR66-7MXqwZf9wexPnvtoLB3XAq4Wu

