import numpy as np
from scipy import io

mat = io.loadmat('E:\\try\\keyboard\\Pp.mat')
#mat_t = np.transpose(mat['P'])
print(mat['P'].shape)
np.save('P.npy', mat['P'])
matrix = np.load('P.npy')
print(matrix.shape)
