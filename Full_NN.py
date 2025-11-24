import numpy as np
from random import random

class Full_NN(object):
    def __init__(self, X, HL, Y):
        self.X=X #inputs
        self.HL=HL #hidden layers
        self.Y=Y #outputs
        self.activation = self.tanh
        self.activation_Der = self.tanh_Der

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
            out=self.activation(Xnext)
            self.out[x+1]=out
        return out
    
    def BP(self, Er): #backpropagation method
        for x in reversed(range(len(self.Der))):
            out = self.out[x+1]
            D = Er * self.activation_Der(out)
            # compute weight derivatives as outer product of previous layer outputs and deltas
            this_out = self.out[x]
            self.Der[x] = np.outer(this_out, D)
            Er = np.dot(D, self.W[x].T)

    def train_nn(self, x, target, epochs, lr): #training method
        for epoch in range(epochs):
            S_errors = 0
            for j, sample in enumerate(x):
                t = target[j]
                output = self.FF(sample)
                e = t - output
                self.BP(e)
                self.GD(lr)
                S_errors += self.msqe(t, output)

    def GD(self, lr=0.05): #gradient descent, change lr later
        for x in range(len(self.W)):
            W = self.W[x]
            Der = self.Der[x]
            W += Der * lr

    def sigmoid(self, x): #sigmoid activation method
        y= 1.0 / (1 + np.exp(-x))
        return y
    
    def sigmoid_Der(self, x): #sigmoid method derivative
        sig_der = x * (1.0 - x)
        return sig_der
    
    def relu(self, x): #reLU activation method
        return np.maximum(0,x)
    
    def relu_Der(self, x): #reLU derivative method
        return (x > 0).astype(float)
    
    def tanh(self, x): #tanh activation method
        return 2 * self.sigmoid(2 * x) - 1
    
    def tanh_Der(self, x): #tanh derivative method
        return 1 - self.tanh(x) ** 2

    def msqe(self, t, output): #mean square error
        msq = np.average((t-output) ** 2)
        return msq
    

#Generate Training Data

samples = 500

t = np.linspace(0, 1, samples).reshape(-1, 1)

Y=np.zeros((samples, 24))
for x in range(24):
    phase = x * (np.pi/8)
    Y[:, x] = np.sin(2 * np.pi * t[:, 0] + phase)

#creating and training the neural network

nn = Full_NN(1, [32], 24)

losses = nn.train_nn(t, Y, 2000, 0.01)


#model test

test_t = np.array([0.5])
prediction = nn.FF(test_t)
print("Predicted 24 joint angles:", prediction)