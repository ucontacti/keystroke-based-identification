# In[1]: Headerimport matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score  #for accuracy_score



# In[3]: Read data and split train and test data
import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split #for split the data

df_features=pd.read_csv("features/dataset_3gram.csv")
# Drop some data
# print(df_features.shape)
# drop_indices = np.random.choice(df_features.index, 110, replace=False)
# df_features = df_features.drop(drop_indices)

df_features.loc[df_features['Label'] > 0, 'Label'] = 1
df_features.drop("Unnamed: 0", axis=1, inplace = True)
df_features.to_csv("features/dataset_3gram_binary.csv")
X = df_features.drop("Label",axis=1)
y = df_features["Label"]

# Train/test splitter
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)



# In[]: Plot Data
import matplotlib.pyplot as plt
df_features=pd.read_csv("features/dataset_3gram.csv")
fig, axes = plt.subplots(nrows=3, ncols=3)

cols = ['Subject {}'.format(col) for col in range(1, 4)]
rows = ['Session {}'.format(row) for row in ['A', 'B', 'C']]

for ax, col in zip(axes[0], cols):
    ax.set_title(col)

for ax, row in zip(axes[:,0], rows):
    ax.set_ylabel(row, rotation=0, size='large')

df_plot = df_features.loc[df_features['Label'] == 0].drop(["Label", "Unnamed: 0"],axis=1)
df_plot[10:20].T.plot(legend=False, color='blue', ax=axes[0, 0])
df_plot[20:30].T.plot(legend=False, color='blue', ax=axes[1, 0])
df_plot[30:40].T.plot(legend=False, color='blue', ax=axes[2, 0])

ylim = []
ylim.append(df_plot[10:40].values.min()) 
ylim.append(df_plot[10:40].values.max())

df_plot = df_features.loc[df_features['Label'] == 3].drop(["Label", "Unnamed: 0"],axis=1)
df_plot[10:20].T.plot(legend=False, color='red', ax=axes[0, 1])
df_plot[20:30].T.plot(legend=False, color='red', ax=axes[1, 1])
df_plot[30:40].T.plot(legend=False, color='red', ax=axes[2, 1])

ylim.append(df_plot[10:40].values.min()) 
ylim.append(df_plot[10:40].values.max())

df_plot = df_features.loc[df_features['Label'] == 2].drop(["Label", "Unnamed: 0"],axis=1)
df_plot[10:20].T.plot(legend=False, color='green', ax=axes[0, 2])
df_plot[20:30].T.plot(legend=False, color='green', ax=axes[1, 2])
df_plot[30:40].T.plot(legend=False, color='green', ax=axes[2, 2])

ylim.append(df_plot[10:40].values.min()) 
ylim.append(df_plot[10:40].values.max())

plt.setp(axes, ylim=(min(ylim), max(ylim)))
plt.subplots_adjust(top=0.92, bottom=0.12, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
plt.show()



# In[3]: Feature Selection
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

#apply SelectKBest class to extract top 10 best features
bestfeatures = SelectKBest(score_func=f_classif, k=10)
fit = bestfeatures.fit(X_train,y_train)
dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(X_train.columns)
#concat two dataframes for better visualization 
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','Score']
print('-------------- Univariate Selection Feature Selection----------------------------')
print(featureScores.nlargest(10,'Score'))  #print 10 best features
#plot graph of feature importances for better visualization
feat_importances = pd.Series(fit.scores_, index=X_train.columns)
feat_importances.nlargest(10).plot(kind='barh', title="Univariate Selection Feature Selection")
plt.show()


# In[2]: Calculate eer rate
from sklearn.metrics import make_scorer, roc_curve #for eer
from scipy.optimize import brentq #for eer
from scipy.interpolate import interp1d #for eer
def calculate_eer(y_true, y_score):
    fpr, tpr, thresholds = roc_curve(y_true, y_score, pos_label=1)
    eer = brentq(lambda x : 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
    return eer


# In[5]: KNN classifier
print('\n\n---------------------KNN Classifier-------------------------------')
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

accuracy_list = []
err_list = []
for i in range(len(X_train.columns)):
    X_train_feature_less = X_train.drop([X_train.columns[i]], axis='columns')    
    X_test_feature_less = X_test.drop([X_test.columns[i]], axis='columns')    
    clf = KNeighborsClassifier(metric='manhattan').fit(X_train_feature_less, y_train)
    prediction_rm=clf.predict(X_test_feature_less)
    accuracy_list.append(round(accuracy_score(prediction_rm,y_test)*100,2))
    err_list.append(round(calculate_eer(prediction_rm, y_test)*100,2))
# dfscores = pd.DataFrame(accuracy_list)
# dfcolumns = pd.DataFrame(X_train.columns)
# featureScores = pd.concat([dfcolumns,dfscores],axis=1)
# featureScores.columns = ['Specs','Score']  #naming the dataframe columns
# print('--------------Feature Selection by accuracy----------------------------')
# print(featureScores.nsmallest(10,'Score'))  #print 10 best features
# feat_importances = pd.Series(accuracy_list, index=X_train.columns)
# feat_importances.nlargest(10).plot(kind='barh')
# plt.show()


dfscores = pd.DataFrame(err_list)
dfcolumns = pd.DataFrame(X_train.columns)
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','Score']  #naming the dataframe columns
print('--------------Feature Selection by EER----------------------------')
print(featureScores.nlargest(10,'Score'))  #print 10 best features
feat_importances = pd.Series(err_list, index=X_train.columns)
feat_importances.nlargest(10).plot(kind='barh', title="Feature Importance by Masking")
plt.show()



knn_model = KNeighborsClassifier(metric='manhattan').fit(X_train, y_train)
prediction_rm=knn_model.predict(X_test)
print('The accuracy of the KNN is ', round(accuracy_score(prediction_rm, y_test)*100,2))
print('The EER value of the KNN is ', round(calculate_eer(prediction_rm, y_test)*100,2))


from sklearn.model_selection import KFold #for K-fold cross validation
from sklearn.model_selection import cross_val_score #score evaluation
kfold = KFold(n_splits=10) # k=10, split the data into 10 equal parts
result_rm=cross_val_score(knn_model, X, y, cv=10, scoring='accuracy')
print('The cross validated score of the KNN is ',round(result_rm.mean()*100,2))

import joblib
joblib.dump(knn_model, 'model/knn_model.pkl', compress=9)
joblib.dump(knn_model, '../Modules/knn_model.pkl', compress=9)

# In[4]: SVM classifier
print('\n\n--------------SVM Classifier----------------------------')
from sklearn import svm
accuracy_list = []
err_list = []
for i in range(len(X_train.columns)):
    X_train_feature_less = X_train.drop([X_train.columns[i]], axis='columns')    
    X_test_feature_less = X_test.drop([X_test.columns[i]], axis='columns')    
    clf = svm.SVC(gamma='scale').fit(X_train_feature_less, y_train)
    prediction_rm=clf.predict(X_test_feature_less)
    accuracy_list.append(round(accuracy_score(prediction_rm,y_test)*100,2))
    err_list.append(round(calculate_eer(prediction_rm, y_test)*100,2))
dfscores = pd.DataFrame(accuracy_list)
dfcolumns = pd.DataFrame(X_train.columns)
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','Score']  #naming the dataframe columns
print('--------------Feature Selection by accuracy----------------------------')
print(featureScores.nsmallest(10,'Score'))  #print 10 best features

dfscores = pd.DataFrame(err_list)
dfcolumns = pd.DataFrame(X_train.columns)
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','Score']  #naming the dataframe columns
print('--------------Feature Selection by eer----------------------------')
print(featureScores.nlargest(10,'Score'))  #print 10 best features

svm_model = svm.SVC(kernel='rbf', gamma='auto').fit(X_train, y_train)
prediction_rm=svm_model.predict(X_test)
print('The accuracy: ', round(accuracy_score(prediction_rm, y_test)*100,2))
print('The EER value:', round(calculate_eer(prediction_rm, y_test)*100,2))
    

kfold = KFold(n_splits=10) # k=10, split the data into 10 equal parts
result_rm=cross_val_score(svm_model, X, y, cv=10,scoring='accuracy')
print('The cross validated score for SVM Classifier is:',round(result_rm.mean()*100,2))

joblib.dump(svm_model, 'model/svm_model.pkl', compress=9)
joblib.dump(svm_model, '../Modules/svm_model.pkl', compress=9)



# In[]: Neural Network
print('\n\n-----------------Neural Network Classifier------------------------')

df_features=pd.read_csv("features/dataset_1gram.csv")
# Drop some data
# print(df_features.shape)
# drop_indices = np.random.choice(df_features.index, 110, replace=False)
# df_features = df_features.drop(drop_indices)

df_features.loc[df_features['Label'] > 0, 'Label'] = 1
df_features.drop("Unnamed: 0", axis=1, inplace = True)
df_features.to_csv("features/dataset_1gram_binary.csv")
X = df_features.drop("Label",axis=1)
y = df_features["Label"]

# Train/test splitter
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

import torch
# Use cuda if available
if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')

# From_numpy takes a numpy element and returns torch.tensor
X_train = torch.from_numpy(X_train.to_numpy()).type(torch.FloatTensor).to(device)
y_train = torch.from_numpy(y_train.to_numpy()).type(torch.LongTensor).to(device)
X_test = torch.from_numpy(X_test.to_numpy()).type(torch.FloatTensor).to(device)
y_test = torch.from_numpy(y_test.to_numpy()).type(torch.LongTensor).to(device)


import torch.nn as nn
import torch.nn.functional as F
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

#Initialize the model        
nn_model = NNClassifier(X_test.shape[1]).to(device)
#Define loss criterion
criterion = nn.CrossEntropyLoss()
#Define the optimizer
optimizer = torch.optim.Adam(nn_model.parameters(), lr=0.01)

#Number of epochs
epochs = 10000
#List to store losses
losses = []
for i in range(epochs):
    #Precit the output for Given input
    y_pred = nn_model.forward(X_train)
    #Compute Cross entropy loss
    loss = criterion(y_pred,y_train)
    #Add loss to the list
    losses.append(loss.item())
    #Clear the previous gradients
    optimizer.zero_grad()
    #Compute gradients
    loss.backward()
    #Adjust weights
    optimizer.step()

print('The accuracy of the Neural Network is', round(accuracy_score(nn_model.predict(X_test), y_test)*100,2))
print('The EER value of the Neural Network is', round(calculate_eer(nn_model.predict(X_test), y_test)*100,2))

torch.save(nn_model.state_dict(), "model/nn_model.pkl")
torch.save(nn_model.state_dict(), "../Modules/nn_model.pkl")

