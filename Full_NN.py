import numpy as np
from random import random

class Full_NN(object):
    def __init__(self, X=2, HL=[2,2], Y=2):
        self.X=X #inputs
        self.HL=HL #hidden layers
        self.Y=Y #outputs
        self.activation = self.relu
        self.activation_Der = self.relu_Der

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
    

#test
if __name__ == "__main__": #test what we have done
    training_inputs = np.array([[random()/2 for _ in range(2)] for _ in range(1000)]) #this creates a training set of inputs
    targets = np.array([[i[0] * i[1]] for i in training_inputs]) #this creates a training set of outputs

    nn=Full_NN(2, [5,5], 1) #creates a NN with 2 inputs, 2 hidden layers and 1 output

    nn.train_nn(training_inputs, targets, 10, 0.1) #trains the network with 0.1 learning rate for 10 epochs

    #Testing data to identify if Network trained well
    input = np.array([0.3, 0.2]) #after training this tests the train network
    target = np.array([0.06]) # for this target value

    NN_output = nn.FF(input)

    print("=============== Testing the Network Screen Output ===============")
    print ("Test input is ", input)
    print()
    print("Target output is ",target)
    print()
    print("Neural Network actual output is ",NN_output, "there is an error (not MSQE) of ",target-NN_output)

print("=================================================================")