import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
import sys
import mpl_toolkits.mplot3d as a3

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def outputVer(grid):

    o_vertex = []
    nr, nc = grid.shape
    o_dict_vert = {}
    i_vert = 0
    for i in range(nr):
        for j in range(nc):
            new_vert = [i, j, grid[i, j]]
            o_vertex.append(new_vert)
            o_dict_vert[i, j] = i_vert
            i_vert = i_vert + 1
    print(len(o_vertex))
    o_vertex = np.asarray(o_vertex)
    return o_vertex, o_dict_vert

def outputTri_Ed(nr, nc, dict_vert):
    edge2vert = {}
    tri2vert = {}
    i_tri = 0
    i_edge = 0
    for i in range(0, nr - 1):
        for j in range(0, nc - 1):
            a_ind = dict_vert[i, j]
            b_ind = dict_vert[i, j + 1]
            c_ind = dict_vert[i + 1, j]
            d_ind = dict_vert[i + 1, j + 1]
            # triangle with no repetition
            tri2vert[i_tri] = [a_ind, b_ind, c_ind]
            tri2vert[i_tri + 1] = [b_ind, c_ind, d_ind]
            i_tri = i_tri + 2
            # edge with repetition
            e1 = (a_ind, b_ind)
            e2 = (b_ind, c_ind)
            e3 = (a_ind, c_ind)
            e4 = (b_ind, d_ind)
            e5 = (c_ind, d_ind)
            edge_list = [e1, e2, e3, e4, e5]
            for ie in range(5):
                newEdge = edge_list[ie]
                if newEdge not in edge2vert:
                    edge2vert[newEdge] = i_edge
                    i_edge = i_edge + 1

    nE = len(edge2vert)
    nT = len(tri2vert)

    triangle = np.zeros([nT, 3])
    edges = np.zeros([nE, 2])

    for i in range(nT):
        triangle[i] = tri2vert[i]

    for key, value in edge2vert.items():
        edges[value, :] = list(key)

    return edges, triangle

def outBinary(vert, edge, triangle, fileName):
    open(fileName, 'wb').close()
    nV = np.asarray(vert.shape[0])
    nE = np.asarray(edge.shape[0])
    nT = np.asarray(triangle.shape[0])
    print("nV:", nV)
    print("nE:", nE)
    print("nT:", nT)
    with open(fileName, 'wb') as f:
        nV.astype(np.int32).tofile(f)
        vert.astype('d').tofile(f)
        nE.astype(np.int32).tofile(f)
        edge.astype(np.int32).tofile(f)
        nT.astype(np.int32).tofile(f)
        triangle.astype(np.int32).tofile(f)
    f.close()

def cmp_dm_img_grid2D(i_grid2d, i_th,i_file_name, i_subsample):
    i_grid2d = i_grid2d[::i_subsample,::i_subsample]
    vert, dict_vert = outputVer(i_grid2d)
    edge, triangle = outputTri_Ed(int(i_grid2d.shape[0]), int(i_grid2d.shape[1]), dict_vert)
    outBinary(vert, edge, triangle, "dataset/"+i_file_name+'/SC.bin')

    if not os.path.exists("result/"+i_file_name+"/"):
        os.makedirs("result/"+i_file_name+"/")

    subprocess.check_call([r"spt_cpp/spt_cpp", "dataset/"+i_file_name+'/SC.bin', "result/"+i_file_name+"/", str(i_th), str(2)])

    o_vert = np.loadtxt("result/"+i_file_name+"/vert.txt")
    o_edge = np.loadtxt("result/"+i_file_name+"/edge.txt")

    if len(o_edge) == 0:
        print('The reconstruction is empty!')
        sys.exit(0)

    o_vert = o_vert[:, :2]

    # visualize result
    stable_vert = o_vert.copy()
    stable_vert[:, 0] = o_vert[:, 1]
    stable_vert[:, 1] = o_vert[:, 0]
    o_vert = stable_vert

    #o_edge = rm_bd_edge(o_edge, o_vert, i_img.shape[0], i_img.shape[1])
    o_vert = o_vert*i_subsample
    return o_vert, o_edge

def outputVer_3d(nx, ny, nz, grid, dicIJK2Index):
    vertex = np.zeros((nx * ny * nz, 4))
    i_vert = 0
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                vertex[i_vert, 0] = i
                vertex[i_vert, 1] = j
                vertex[i_vert, 2] = k
                vertex[i_vert, 3] = grid[i, j, k]
                dicIJK2Index[i, j, k] = i_vert
                i_vert = i_vert + 1
    return vertex

def minus2odd_or_even(i):
    if i % 2 == 0:
        return 1
    else:
        return -1

def buildTetraGrid(nx, ny, nz, dicIJK2Index):
    STATE1 = 1
    STATE2 = -1
    # (n-1)*(n-1)*n_hight cubes
    nTetra = (nx - 1) * (ny - 1) * (nz - 1) * 5
    tetra = np.zeros([nTetra, 4])
    index_tetra = 0
    cur_state = STATE1
    for i in range(nx - 1):
        for j in range(ny - 1):
            cur_state = STATE1 * minus2odd_or_even(i + j)
            for k in range(nz - 1):
                pt1_ind = dicIJK2Index[i, j, k]
                pt2_ind = dicIJK2Index[i, j + 1, k]
                pt3_ind = dicIJK2Index[i + 1, j, k]
                pt4_ind = dicIJK2Index[i + 1, j + 1, k]
                pt5_ind = dicIJK2Index[i, j, k + 1]
                pt6_ind = dicIJK2Index[i, j + 1, k + 1]
                pt7_ind = dicIJK2Index[i + 1, j, k + 1]
                pt8_ind = dicIJK2Index[i + 1, j + 1, k + 1]
                if cur_state == STATE1:
                    tetra[index_tetra, :] = [pt1_ind, pt2_ind, pt3_ind, pt5_ind]
                    tetra[index_tetra + 1, :] = [pt3_ind, pt5_ind, pt7_ind, pt8_ind]
                    tetra[index_tetra + 2, :] = [pt2_ind, pt3_ind, pt4_ind, pt8_ind]
                    tetra[index_tetra + 3, :] = [pt2_ind, pt5_ind, pt6_ind, pt8_ind]
                    tetra[index_tetra + 4, :] = [pt2_ind, pt3_ind, pt5_ind, pt8_ind]
                if cur_state == STATE2:
                    tetra[index_tetra, :] = [pt1_ind, pt3_ind, pt4_ind, pt7_ind]
                    tetra[index_tetra + 1, :] = [pt1_ind, pt2_ind, pt4_ind, pt6_ind]
                    tetra[index_tetra + 2, :] = [pt4_ind, pt6_ind, pt7_ind, pt8_ind]
                    tetra[index_tetra + 3, :] = [pt1_ind, pt5_ind, pt6_ind, pt7_ind]
                    tetra[index_tetra + 4, :] = [pt1_ind, pt4_ind, pt6_ind, pt7_ind]
                index_tetra = index_tetra + 5
                cur_state = -cur_state
    return tetra

def buildTriFromTetra(tetra):
    tri = {}

    nTe = tetra.shape[0]
    tri_index = 0

    for i in range(nTe):
        for j in range(4):
            # Four triangles
            newTri = []
            for k in range(4):
                # Triangles' three vertices
                if k != j:
                    newTri.append(tetra[i, k])
            newTri = tuple(newTri)
            if newTri not in tri:
                # Add new triangles
                tri[newTri] = tri_index
                tri_index = tri_index + 1

    # Convert everythin into list
    nTri = len(tri)
    tri_array = np.zeros([nTri, 3])
    for key, value in tri.items():
        tri_array[value, :] = list(key)

    return tri_array

def builEdgeFromTri(tri):
    edge = {}
    edge_index = 0

    nTri = len(tri)

    for i in range(nTri):
        for j in range(3):
            # 3 edges
            newEdge = []
            for k in range(3):
                if k != j:
                    newEdge.append(tri[i, k])
            newEdge = tuple(newEdge)
            if newEdge not in edge:
                edge[newEdge] = edge_index
                edge_index = edge_index + 1

    nEdge = len(edge)
    edge_array = np.zeros([nEdge, 2])
    for key, value in edge.items():
        edge_array[value, :] = list(key)

    return edge_array

def outBinary_3d(vert, edge, triangle, nV, nE, nT, file_name):
    open(file_name, 'wb').close()
    with open(file_name, 'wb') as f:
        nV.astype(np.int32).tofile(f)
        vert.astype('d').tofile(f)
        nE.astype(np.int32).tofile(f)
        edge.astype(np.int32).tofile(f)
        nT.astype(np.int32).tofile(f)
        triangle.astype(np.int32).tofile(f)
    f.close()


def cmp_dm_img_grid3D(i_grid3d, i_th,i_file_name, i_subsample):
    i_grid3d = i_grid3d[::i_subsample,::i_subsample]
    [nx, ny, nz] = i_grid3d.shape
    dicIJK2Index = {}
    print("Build vertex from grid.")
    vert = outputVer_3d(nx, ny, nz, i_grid3d, dicIJK2Index)
    print("Build tetrahedron from grid.")
    tetra = buildTetraGrid(nx, ny, nz, dicIJK2Index)
    tetra.sort()
    print("Build tri from tetra.")
    tri = buildTriFromTetra(tetra)
    print("Build edge from tri.")
    edge = builEdgeFromTri(tri)

    nV = vert.shape[0] * np.ones(1)
    nE = edge.shape[0] * np.ones(1)
    nT = tri.shape[0] * np.ones(1)

    outBinary_3d(vert, edge, tri, nV, nE, nT, "dataset/"+i_file_name+'/SC.bin')

    if not os.path.exists("result/"+i_file_name+"/"):
        os.makedirs("result/"+i_file_name+"/")

    subprocess.check_call([r"spt_cpp/spt_cpp", "dataset/"+i_file_name+'/SC.bin', "result/"+i_file_name+"/", str(i_th), str(3)])

    o_vert = np.loadtxt("result/"+i_file_name+"/vert.txt")
    o_edge = np.loadtxt("result/"+i_file_name+"/edge.txt")

    if len(o_edge) == 0:
        print('The reconstruction is empty!')
        sys.exit(0)

    o_vert = o_vert[:, :3]

    o_vert = o_vert*i_subsample
    return o_vert, o_edge

def cmp_dm_img_tri2D(i_file_name,i_th):

    vert = np.loadtxt("dataset/"+i_file_name+'/tri_vert.txt')
    vert[:, 2] = vert[:, 2] / np.max(vert[:, 2])
    edge = np.loadtxt("dataset/" + i_file_name + '/tri_edge.txt')
    triangle = np.loadtxt("dataset/" + i_file_name + '/tri_triangle.txt')

    outBinary(vert, edge, triangle, "dataset/"+i_file_name+'/SC.bin')

    if not os.path.exists("result/"+i_file_name+"/"):
        os.makedirs("result/"+i_file_name+"/")

    subprocess.check_call([r"spt_cpp/spt_cpp", "dataset/"+i_file_name+'/SC.bin', "result/"+i_file_name+"/", str(i_th), str(2)])

    o_vert = np.loadtxt("result/"+i_file_name+"/vert.txt")
    o_edge = np.loadtxt("result/"+i_file_name+"/edge.txt")

    if len(o_edge) == 0:
        print('The reconstruction is empty!')
        sys.exit(0)

    o_vert = o_vert[:, :2]

    # visualize result
    stable_vert = o_vert.copy()
    stable_vert[:, 0] = o_vert[:, 1]
    stable_vert[:, 1] = o_vert[:, 0]
    o_vert = stable_vert

    return o_vert, o_edge

def cmp_dm_img_tri3D(i_file_name,i_th):

    vert = np.loadtxt("dataset/"+i_file_name+'/tri_vert.txt')
    vert[:,3] = vert[:,3]/np.max(vert[:,3])
    edge = np.loadtxt("dataset/" + i_file_name + '/tri_edge.txt')
    triangle = np.loadtxt("dataset/" + i_file_name + '/tri_triangle.txt')

    outBinary(vert, edge, triangle, "dataset/"+i_file_name+'/SC.bin')

    if not os.path.exists("result/"+i_file_name+"/"):
        os.makedirs("result/"+i_file_name+"/")

    subprocess.check_call([r"spt_cpp/spt_cpp", "dataset/"+i_file_name+'/SC.bin', "result/"+i_file_name+"/", str(i_th), str(3)])

    o_vert = np.loadtxt("result/"+i_file_name+"/vert.txt")
    o_edge = np.loadtxt("result/"+i_file_name+"/edge.txt")

    if len(o_edge) == 0:
        print('The reconstruction is empty!')
        sys.exit(0)

    o_vert = o_vert[:, :3]

    return o_vert, o_edge

def createLines(Lines, edge, vert):
    nLine = edge.shape[0]
    for i in range(nLine):
        v1_ind = int(edge[i, 0])
        v2_ind = int(edge[i, 1])
        vert1 = vert[v1_ind, :]
        vert2 = vert[v2_ind, :]
        vert1_coor = (vert1[0], vert1[1])
        vert2_coor = (vert2[0], vert2[1])
        newLine = [vert1, vert2]
        Lines.append(newLine)

def drawLines(lines, color, width, order, ax):
    lc = mc.LineCollection(lines, colors=color, linewidths=width, zorder=order)
    ax.add_collection(lc)

def read_grid3d(i_file_name):
    with open("dataset/"+i_file_name+"/grid.txt") as f:
        first_line = f.readline()
    grid_shape = [int(ele) for ele in first_line.split()]
    grid_flat = np.loadtxt("dataset/"+i_file_name+"/grid.txt", skiprows=1)
    if grid_shape[0]*grid_shape[1]*grid_shape[2] != len(grid_flat):
        print("Dimension doesn't match!")
        sys.exit(0)
    grid3d = grid_flat.reshape([grid_shape[0], grid_shape[1], grid_shape[2]])
    #print(grid3d)
    return grid3d

def cmp_by_pre2D(i_file_name,i_th):
    subprocess.check_call(
        [r"spt_cpp/spt_cpp", "dataset/" + i_file_name + '/SC.bin', "result/" + i_file_name + "/", str(i_th),
         str(2), 'result/' + i_file_name + '/presave.bin'])

    o_vert = np.loadtxt("result/"+i_file_name+"/vert.txt")
    o_edge = np.loadtxt("result/"+i_file_name+"/edge.txt")

    if len(o_edge) == 0:
        print('The reconstruction is empty!')
        sys.exit(0)

    o_vert = o_vert[:, :2]

    # visualize result
    stable_vert = o_vert.copy()
    stable_vert[:, 0] = o_vert[:, 1]
    stable_vert[:, 1] = o_vert[:, 0]
    o_vert = stable_vert

    return o_vert, o_edge

def cmp_by_pre3D(i_file_name,i_th):
    subprocess.check_call(
        [r"spt_cpp/spt_cpp", "dataset/" + i_file_name + '/SC.bin', "result/" + i_file_name + "/", str(i_th),
         str(3), 'result/' + i_file_name + '/presave.bin'])

    o_vert = np.loadtxt("result/"+i_file_name+"/vert.txt")
    o_edge = np.loadtxt("result/"+i_file_name+"/edge.txt")

    if len(o_edge) == 0:
        print('The reconstruction is empty!')
        sys.exit(0)

    o_vert = o_vert[:, :3]

    return o_vert, o_edge

# file_name = 'Berlin'
# input_arg = '-t'
# dimension = 2
# threshold = 0.1

#test
#python graphRecon.py Berlin -t 2 0.1
#python graphRecon.py grid2D -g 2 0.6
#python graphRecon.py test_3D -g 3 0.05
#python graphRecon.py test_3D -t 3 0.05

print(sys.argv)

if len(sys.argv) != 5:
    print("python graphRecon.py <dataset_name> <dataset_form> <dimension> <threshold>")
    print("<dataset_form>   -g input grid")
    print("<dataset_form>   -t input triangulation")
    sys.exit(0)

file_name = sys.argv[1]
input_arg = sys.argv[2]
dimension = int(sys.argv[3])
threshold = float(sys.argv[4])

subsample_grid = 1
flip = False

# 2D
if dimension == 2:
    ## input grid
    if os.path.isfile('result/'+file_name+'/presave.bin') and os.path.isfile('dataset/'+file_name+'/SC.bin'):
        print('Use presaved data.')
        recon_vert, recon_edge = cmp_by_pre2D(file_name,threshold)

        if len(recon_edge)>0:
            # visualize vert and edge
            recon_lines = []
            createLines(recon_lines, recon_edge, recon_vert)
            fig = plt.figure()
            plt.clf()

            ax1 = fig.add_subplot(111)
            #ax1.imshow(grid2d, cmap='gray')
            #drawLines(h0_lines, 'blue', 0.5, 1, ax1)
            drawLines(recon_lines, 'red', 0.5, 2, ax1)

            x_min = np.min(recon_vert[:,0])
            x_max = np.max(recon_vert[:,0])
            y_min = np.min(recon_vert[:,1])
            y_max = np.max(recon_vert[:,1])

            ax1.set_xlim(x_min, x_max)
            ax1.set_ylim(y_max, y_min)
            plt.savefig('result/'+file_name+'/visualization.png', dpi=200)

    elif input_arg=='-g':
        grid2d = np.loadtxt('dataset/'+file_name+'/grid.txt')
        # flip
        #grid2d = np.max(grid2d)- grid2d
        grid2d = grid2d/np.max(np.abs(grid2d))

        recon_vert, recon_edge = cmp_dm_img_grid2D(grid2d, threshold, file_name,subsample_grid)


        if len(recon_edge)>0:
            # visualize vert and edge
            recon_lines = []
            createLines(recon_lines, recon_edge, recon_vert)
            fig = plt.figure()
            plt.clf()

            ax1 = fig.add_subplot(111)
            ax1.imshow(grid2d, cmap='gray')
            #drawLines(h0_lines, 'blue', 0.5, 1, ax1)
            drawLines(recon_lines, 'red', 0.5, 2, ax1)

            plt.savefig('result/'+file_name+'/visualization.png', dpi=200)
    ## input triangulation
    elif input_arg=='-t':
        recon_vert, recon_edge = cmp_dm_img_tri2D(file_name, threshold)

        if len(recon_edge)>0:
            # visualize vert and edge
            recon_lines = []
            createLines(recon_lines, recon_edge, recon_vert)
            fig = plt.figure()
            plt.clf()

            ax1 = fig.add_subplot(111)
            #ax1.imshow(grid2d, cmap='gray')
            #drawLines(h0_lines, 'blue', 0.5, 1, ax1)
            drawLines(recon_lines, 'red', 0.5, 2, ax1)

            x_min = np.min(recon_vert[:,0])
            x_max = np.max(recon_vert[:,0])
            y_min = np.min(recon_vert[:,1])
            y_max = np.max(recon_vert[:,1])

            ax1.set_xlim(x_min, x_max)
            ax1.set_ylim(y_max, y_min)
            plt.savefig('result/'+file_name+'/visualization.png', dpi=200)
# 3D
elif dimension == 3:
    if os.path.isfile('result/'+file_name+'/presave.bin') and os.path.isfile('dataset/'+file_name+'/SC.bin'):
        print('Use presaved data.')
        recon_vert, recon_edge = cmp_by_pre3D(file_name,threshold)

        # 3d plot
        if len(recon_edge) > 0:
            fig = plt.figure()
            ax = a3.Axes3D(fig)
            for e in recon_edge:
                v1_ind = int(e[0])
                v2_ind = int(e[1])
                v1 = recon_vert[v1_ind]
                v2 = recon_vert[v2_ind]
                ax.plot([v1[0],v2[0]],[v1[1],v2[1]],[v1[2],v2[2]], color='red', alpha=1, linewidth=1)
            #plt.show()
            fig.savefig('result/'+file_name+'/visualization.png', dpi=200)
    elif input_arg == '-g':
        grid3d = read_grid3d(file_name)
        grid3d = grid3d/np.max(grid3d)

        recon_vert, recon_edge = cmp_dm_img_grid3D(grid3d, threshold, file_name,subsample_grid)

        # 3d plot
        if len(recon_edge) > 0:
            fig = plt.figure()
            ax = a3.Axes3D(fig)
            for e in recon_edge:
                v1_ind = int(e[0])
                v2_ind = int(e[1])
                v1 = recon_vert[v1_ind]
                v2 = recon_vert[v2_ind]
                ax.plot([v1[0],v2[0]],[v1[1],v2[1]],[v1[2],v2[2]], color='red', alpha=1, linewidth=1)
            #plt.show()
            fig.savefig('result/'+file_name+'/visualization.png', dpi=200)

    elif input_arg == '-t':

        print("3d triangulation")
        recon_vert, recon_edge = cmp_dm_img_tri3D(file_name, threshold)

        # 3d plot
        if len(recon_edge) > 0:
            fig = plt.figure()
            ax = a3.Axes3D(fig)
            for e in recon_edge:
                v1_ind = int(e[0])
                v2_ind = int(e[1])
                v1 = recon_vert[v1_ind]
                v2 = recon_vert[v2_ind]
                ax.plot([v1[0],v2[0]],[v1[1],v2[1]],[v1[2],v2[2]], color='red', alpha=1, linewidth=1)
            #plt.show()
            fig.savefig('result/'+file_name+'/visualization.png', dpi=200)
