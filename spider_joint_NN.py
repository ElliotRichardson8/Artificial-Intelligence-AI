import numpy as np
from random import random
import matplotlib.pyplot as plt
import plot_spider_pose as pt

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
        losses = []
        for epoch in range(epochs):
            S_errors = 0
            for j, sample in enumerate(x):
                t = target[j]
                output = self.FF(sample)
                e = t - output
                self.BP(e)
                self.GD(lr)
                S_errors += self.msqe(t, output)
            avg_loss = S_errors / len(x)
            losses.append(avg_loss)

            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {avg_loss}")
        return losses

    def GD(self, lr): #gradient descent
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
        return np.tanh(x)
    
    def tanh_Der(self, out): #tanh derivative method
        return 1 - out ** 2

    def msqe(self, t, output): #mean square error (loss function)
        msq = np.average((t-output) ** 2)
        return msq
    

#Generate Training Data (sinusoidal gait)
samples = 500

t = np.linspace(0, 1, samples).reshape(-1, 1)

Y=np.zeros((samples, 24))
for x in range(24):
    phase = x * (np.pi/8)
    Y[:, x] = np.sin(2 * np.pi * t[:, 0] + phase)

#creating and training the neural network
nn = Full_NN(1, [32], 24)

losses = nn.train_nn(t, Y, 2000, 0.01)

#plot training loss
plt.plot(losses)
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss Curve")
plt.show()

# Compare predicted outputs vs target configurations
test_times = np.linspace(0, 1, 5)  # 5 sample time points

for ti in test_times:
    # Predict joint angles
    pred = nn.FF(np.array([ti]))
    
    # Compute true joint angles
    true = np.array([np.sin(2 * np.pi * ti + x * np.pi / 8) for x in range(24)])
    
    # Print comparison
    print(f"t = {ti:.2f}")
    print("Predicted:", np.round(pred, 3))
    print("Target:   ", np.round(true, 3), "\n")
    
    # Plot comparison
    plt.figure(figsize=(10, 4))
    plt.plot(true, label="Target")
    plt.plot(pred, '--', label="Predicted")
    plt.title(f"Predicted vs Target Joint Angles at t={ti:.2f}")
    plt.xlabel("Joint Index")
    plt.ylabel("Angle")
    plt.legend()
    plt.show()
    
    # Plot spider pose for this prediction
    pt.plot_spider_pose(pred)

#model test
test_t = np.array([0.5])
prediction = nn.FF(test_t)
print("Predicted 24 joint angles:", prediction)
pt.plot_spider_pose(prediction)