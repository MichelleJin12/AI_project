#
#
# write by kyoung chip ,jang
#
#
# wget http://semanchuk.com/philip/sysv_ipc/sysv_ipc-0.7.0.tar.gz
# tar xvf sysv_ipc-0.7.0.tar.gz
# sudo apt-get install python3-dev
#
# sudo python3 setup.py install
# python3 shmreader.py
#
import sysv_ipc
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import pandas as pd
device = torch.device("cpu")
label_num = 3

class MLP(nn.Module):
    def __init__(self):
        super(MLP,self).__init__()
        self.classifier = nn.Sequential(
            nn.Linear(10, 256),
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(256),
            # nn.Linear(256, 256),
            # nn.ReLU(inplace=True),
            # nn.BatchNorm1d(256),
            # nn.Linear(256, 256),
            # nn.ReLU(inplace=True),
            # nn.BatchNorm1d(256),
            # nn.Linear(256, 256),
            # nn.ReLU(inplace=True),
            # nn.BatchNorm1d(256),
            nn.Linear(256, label_num)
        )

    def forward(self, x):
        result = self.classifier(x)
#         return result
        return F.softmax(result,dim=-1)

    def forward(self, x):
        result = self.classifier(x)
        return F.softmax(result,dim=-1)

class CShmReader :

    def __init__( self ) :

        pass

    def doReadShm( self , key ) :

        memory = sysv_ipc.SharedMemory( key )

        memory_value = memory.read()
        #print ( memory_value )
        return memory_value

if __name__ == '__main__':
    a = []
    temp = ""
    s = CShmReader()
    text = s.doReadShm( 777 )
    text = text.decode('utf-8')
    for i in text:
        if i == '\t':
            a.append(temp)
            temp = ""
        else:
            temp += i
    a = list(map(float, a))
    print(a)
    input = [a, a, a, a]
    input = np.array(input)
    input = torch.from_numpy(input.astype('float32')).to(device)
    model = MLP()
    model.load_state_dict(torch.load("MLP_"))
    model.eval()
    output = model(input)
    lst = output.tolist()
    print("성수호:", lst[0][0]*100)
    print("김재원:", lst[0][1]*100)
    print("진성희:", lst[0][2]*100)