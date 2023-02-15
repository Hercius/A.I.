from numpy import *

def sigmoid(x):
    return 1 / (1+exp(-x))

def dsigmoid(x):
    return x * (1 - x)

class NeuralNet:
    def __init__(self):
        self.hiddenLayerW = None
        self.outputLayerW = None
        self.output = None
        self.MSE = None
        self.trained = False
        
    def predict( self, X ):
        ### ... YOU FILL IN THIS CODE ....
        X1 = hstack((1,X)) ##adding a 0 to the start of the list
        
        return sigmoid(sigmoid(X1.dot(self.hiddenLayerW)).dot(self.outputLayerW))
        
    def train(self,X,Y,hiddenLayerSize,epochs):    
        ## size of input layer (number of inputs plus bias)
        ni = X.shape[1] + 1

        ## size of hidden layer (number of hidden nodes plus bias)
        nh = hiddenLayerSize + 1

        # size of output layer
        no = 10

        ## initialize weight matrix for hidden layer
        self.hiddenLayerW = 2*random.random((ni,nh)) - 1

        ## initialize weight matrix for output layer
        self.outputLayerW = 2*random.random((nh,no)) - 1

        ## learning rate
        alpha = 0.001

        ## Mark as not trained
        self.trained = False
        ## Set up MSE array
        self.MSE = [0]*epochs

        for epoch in range(epochs):

            ### ... YOU FILL IN THIS CODE ....
            
            aNi = hstack((array([[1]*X.shape[0]]).T,X)) ##although we can fill the first column with 0's, mine works better with a column of 1s
            
            InH = dot(aNi,self.hiddenLayerW) ## taking dot product of the input layer and the weighted hidden layer
            aNh = sigmoid(InH) 
            aNh[:,0] = 1 #changing first column to 1s
            aNi1 = dot(aNh,self.outputLayerW) ## taking dot product of the hidden layer and the weighted output layer
            aNi2 = sigmoid(aNi1)
            error_out = Y - aNi2
            direction = error_out*dsigmoid(aNi2) #finding the change in my error
            ## Record MSE
            self.MSE[epoch] = mean(list(map(lambda x:x**2,error_out)))
            errorHidden = direction.dot(self.outputLayerW.T)
            hiddenDirection = errorHidden*dsigmoid(aNh) #finding the change in my error for hidden
            self.hiddenLayerW = self.hiddenLayerW + alpha*aNi.T.dot(hiddenDirection) #updating the hidden and output weighted matrix to match accordingly
            self.outputLayerW = self.outputLayerW + alpha*aNh.T.dot(direction)
            

        ## Update trained flag
        self.trained = True

