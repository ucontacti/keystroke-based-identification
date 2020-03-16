# import pandas as pd
import joblib
import pandas as pd

import torch 
import torch.nn as nn
import torch.nn.functional as F#our class must extend nn.Module

class NNClassifier(nn.Module):
    def __init__(self, input_size):
        super(NNClassifier,self).__init__()
        #Our network consists of 3 layers. 1 input, 1 hidden and 1 output layer
        #This applies Linear transformation to input data. 
        self.fc1 = nn.Linear(input_size,100)

        #This applies linear transformation to produce output data
        self.fc2 = nn.Linear(100,100)

        #This applies linear transformation to produce output data
        self.fc3 = nn.Linear(100,2)
        
    #This must be implemented
    def forward(self,x):
        #Output of the first layer
        x = self.fc1(x)
        #Activation function is Relu. Feel free to experiment with this
        x = torch.tanh(x)
        #This produces output
        x = self.fc2(x)
        return x
        
    #This function takes an input and predicts the class, (0 or 1)        
    def predict(self,x):
        #Apply softmax to output. 
        pred = F.softmax(self.forward(x),dim=1)
        ans = []
        #Pick the class with maximum weight
        for t in pred:
            if t[0]>t[1]:
                ans.append(0)
            else:
                ans.append(1)
        return torch.tensor(ans)

if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')

# models loader
nn_model = NNClassifier(34).to(device)
nn_model.load_state_dict(torch.load("Modules/nn_model.pkl"))
svm_model = joblib.load('Modules/svm_model.pkl')
knn_model = joblib.load('Modules/svm_model.pkl')

def tester(data_up, data_down):
    new_data = []
    for i in range(len(data_up) - 1):
        new_data.append(data_up[i] - data_down[i])
        new_data.append(data_down[i+1] - data_down[i])
        new_data.append(data_down[i+1] - data_up[i])
    new_data.append(data_up[-1] - data_down[-1])
    new_data_1gram = pd.DataFrame([new_data])
    new_data = []
    for i in range(len(data_up)):
        new_data.append(data_up[i] - data_down[i])
        if (i+1) < len(data_up):
            new_data.append(data_down[i+1] - data_down[i])
            new_data.append(data_down[i+1] - data_up[i])
        if (i+2) < len(data_up):
            new_data.append(data_down[i+2] - data_down[i])
            new_data.append(data_down[i+2] - data_up[i])
        if (i+3) < len(data_up):
            new_data.append(data_down[i+3] - data_down[i])
            new_data.append(data_down[i+3] - data_up[i])
    new_data_3gram = pd.DataFrame([new_data])
    result = 0
    if not svm_model.predict(new_data_3gram):
        result += 2 ** 0
    if not knn_model.predict(new_data_3gram):
        result += 2 ** 1
    if not nn_model.predict(torch.from_numpy(new_data_1gram.to_numpy()).type(torch.FloatTensor).to(device)):
        result += 2 ** 2
    
    # print("Our test result: " + str(result))

    # test_true = [66,404,338,66,113,47,122,136,14,54,68,14,121,89,-32,100,90,-10,88,67,-21,100,156,56,90,158,68,101,112,11,78,68,-10,78]
    # test_true = pd.DataFrame([test_true])
    # result = 0
    # if not svm_model.predict(test_true):
    #     result += 2 ** 0
    # if not knn_model.predict(test_true):
    #     result += 2 ** 1
    # if not nn_model.predict(torch.from_numpy(test_true.to_numpy()).type(torch.FloatTensor).to(device)):
    #     result += 2 ** 2
    # print("True possitive result: " + str(result))

    # test_false = [119, 80, -39, 119, 80, -39, 112, 56, -56, 104, 120, 16, 80, 128, 48, 104, 80, -24, 79, 128, 49, 95, 80, -15, 120, 80, -40, 96, 56, -40, 103, 80, -23, 103]
    # test_false = pd.DataFrame([test_false])
    # result = 0
    # if not svm_model.predict(test_false):
    #     result += 2 ** 0
    # if not knn_model.predict(test_false):
    #     result += 2 ** 1
    # if not nn_model.predict(torch.from_numpy(test_false.to_numpy()).type(torch.FloatTensor).to(device)):
    #     result += 2 ** 2

    # print("True negative result: " + str(result))

    return result