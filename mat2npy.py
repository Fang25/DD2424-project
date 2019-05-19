import numpy as np
from scipy import io

trdmat= io.loadmat('C:\\Study\\A2\\trd.mat')
#mat_t = np.transpose(mat['P'])
#print(mat['P'].shape)
np.save('trd.npy', trdmat['traindata'])
trd = np.load('trd.npy')
print('traindata shape: ',trd.shape)

trlmat= io.loadmat('C:\\Study\\A2\\trl.mat')
np.save('trl.npy', trlmat['trainlabel'])
trl = np.load('trl.npy')
print('trainlabel shape: ',trl.shape)

trlmat= io.loadmat('C:\\Study\\A2\\ted.mat')
np.save('ted.npy', trlmat['testdata'])
ted = np.load('ted.npy')
print('testdata shape: ',ted.shape)

trlmat= io.loadmat('C:\\Study\\A2\\tel.mat')
np.save('tel.npy', trlmat['testlabel'])
tel = np.load('tel.npy')
print('testlabel shape: ',tel.shape)
