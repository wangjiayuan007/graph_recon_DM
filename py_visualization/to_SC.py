import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import sys
#import seaborn as sns;

#sns.set()

def outBinary(i_filenmae, vert,edge,triangle):
    open(i_filenmae, 'wb').close()
    with open(i_filenmae, 'wb') as f:
        nV.astype(np.int32).tofile(f)
        vert.astype('d').tofile(f)
        nE.astype(np.int32).tofile(f)
        edge.astype(np.int32).tofile(f)
        nT.astype(np.int32).tofile(f)
        triangle.astype(np.int32).tofile(f)
    f.close()

dataName = sys.argv[1]
vert = np.loadtxt("../dataset/" + dataName + "/tri_vert.txt")
edge = np.loadtxt("../dataset/" + dataName + "/tri_edge.txt")
triangle = np.loadtxt("../dataset/" + dataName + "/tri_triangle.txt")
vert[:,2] = vert[:,2] /np.max(vert[:,2])
nV = len(vert)
nE = len(edge)
nT = len(triangle)
nV = np.asarray(nV)
nE = np.asarray(nE)
nT = np.asarray(nT)
outBinary("../dataset/" + dataName + "/SC.bin",vert,edge,triangle)
# np.savetxt("tri_vert.txt", newPTall, fmt='%d %d %f')
# np.savetxt("tri_edge.txt", edges, fmt='%d')
# np.savetxt("tri_triangle.txt",triangle,fmt='%d')










