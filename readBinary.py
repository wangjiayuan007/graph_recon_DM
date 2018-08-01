import struct
import numpy as np
import sys

fileName = sys.argv[1]

# 4
# 8 8 8 8 
# ...
# 8 8 8 8

# 4
# 4 4 
# ...
# 4 4

# 4
# 4 4 4
# ...
# 4 4 4 

with open(fileName, mode='rb') as file:
    fileContent = file.read()

    nV = struct.unpack("i", fileContent[:4])[0]
    print("nV:",nV)
    pt_all =[]
    pointer = 4
    for i in range(nV):
        new_pt = []
        for j in range(4):
            pt_coor = struct.unpack("d", fileContent[pointer:pointer+8])
            pointer = pointer+8
            new_pt.append(pt_coor)
        pt_all.append(new_pt)

    nE = struct.unpack("i", fileContent[pointer:pointer+4])[0]
    pointer = pointer+4
    print("nE:",nE)
    edge_list = []
    for i in range(nE):
        new_edge = []
        for j in range(2):
            v_ind = struct.unpack("i", fileContent[pointer:pointer+4])
            pointer = pointer+4
            new_edge.append(v_ind)
        edge_list.append(new_edge)

    nT = struct.unpack("i", fileContent[pointer:pointer+4])[0]
    pointer = pointer+4
    print("nT:",nT)
    tri_list = []
    for i in range(nT):
        new_tri = []
        for j in range(3):
            v_ind = struct.unpack("i", fileContent[pointer:pointer+4])
            pointer = pointer+4
            new_tri.append(v_ind)
        tri_list.append(new_tri)

        # ptx = struct.unpack("d", fileContent[4+i*32:4+i*32+8])
        # pty = struct.unpack("d", fileContent[4+i*32+8:4+i*32+8+8])
        # ptz = struct.unpack("d", fileContent[4+i*32+8+8:4+i*32+8+8+8])
        # pt_value = struct.unpack("d", fileContent[4+i*32+8+8+8:4+i*32+8+8+8+8])
        # pt_all.append([ptx,pty,ptz,pt_value])

#        ptx = struct.unpack("f", fileContent[4+i*24:4+i*24+4])
#        pty = struct.unpack("f", fileContent[4+i*24+4:4+i*24+4+4])
#        pt_value = struct.unpack("f", fileContent[4+i*24+4+4:4+i*24+4+4+4])
#        pt_all.append([ptx,pty,pt_value])



pt_all = np.asarray(pt_all)
pt_all = pt_all.reshape([pt_all.shape[0],pt_all.shape[1]])
print(pt_all.shape)
edge_list = np.asarray(edge_list)
edge_list = edge_list.reshape([edge_list.shape[0],edge_list.shape[1]])
print(edge_list.shape)
tri_list = np.asarray(tri_list)
tri_list = tri_list.reshape([tri_list.shape[0],tri_list.shape[1]])
print(tri_list.shape)

# print("Max: ", np.max(pt_all[:,3]))
#np.savetxt("ptCloud3.txt",pt_all[:,0:2],fmt='%d %d')
#np.savetxt("value3.txt",pt_all[:,3],fmt='%f ')
np.savetxt("tri_vert.txt",pt_all,fmt='%1.2f %1.2f %1.2f %f')
np.savetxt("tri_edge.txt",edge_list,fmt='%d %d')
np.savetxt("tri_triangle.txt",tri_list,fmt='%d %d %d')
