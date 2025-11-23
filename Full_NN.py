import numpy as np
from random import random

class Full_NN(object):
    def __init__(self, X=2, HL=[2,2], Y=2):
        self.X=X #inputs
        self.HL=HL #hidden layers
        self.Y=Y

        L=[X]+HL+[Y] #total number of layers

        W=[] #weight array
        for x in range(len(L)-1):
            w=np.random.rand(L[x], L[x+1])
            W.append(w)
        self.W=W

        Der=[] #derivative array
        for x in range (len(L)-1):
            d=np.zeros((L[x], L[x+1]))
            Der.append(d)
            self.Der=Der

        out=[] #output array
        for x in range(len(L)):
            o=np.zeros(L[x])
            out.append(o)
            self.out=out

    def FF(self,x): #feed forward method
        out = x
        self.out[0] = x
        for x, w in enumerate(self.W):
            Xnext = np.dot(out, w)
            out=self.sigmoid(Xnext)
            self.out[x+1]=out
        return out
    
    def BP(self, Er): #back propagation method
        for x in reversed (range(len(self.Der))):
            out = self.out[x+1]
            D = Er*self.sigmoid_Der(out)
            D_fixed = D.reshape(D.shape[0],-1)
            this_out = self.out[x]
            this_out = this_out.reshape(this_out.shape[0],-1)
            self.Der[x]=np.dot(this_out, D_fixed)
            Er=np.dot(D, self.W[x].T)

    def train_nn(self, x, target, epochs, lr): #training method
        for x in range(epochs):
            S_errors = 0
            for j, input in enumerate(x):
                t = target[j]
                output = self.FF(input)
                e = t-output
                self.BP(e)
                self.GD(lr)
                S_errors += self.msqe(t, output)

    def GD(self, lr=0.05): #gradient descent, change lr later
        for x in range(len(self.W)):
            W = self.W[x]
            Der = self.Der[x]
            W += Der*lr

    def sigmoid(self, x): #sigmoid activation method
        y= 1.0 / (1 + np.exp(-x))
        return y
    
    def sigmoid_Der(self, x): #sigmoid method derivative
        sig_der = x * (1.0 - x)
        return sig_der
    
    def msqe(self, t, output): #mean square error
        msq = np.average((t-output) ** 2)
        return msq
    

