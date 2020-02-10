
def checkUsingKNN(base_dir, data:list):
    import pickle
    loaded_model = pickle.load(open(base_dir+'/../diabetesModel/knnModel', 'rb'))
    print("model imported")
    result = str((loaded_model.predict([data]))[0])
    print('The result for KNN is '+str(result))
    return 'Positive' if result == '1' else 'Negative'



def checkUsingNaiveBayes(base_dir, data:list):
    import pickle
    loaded_model = pickle.load(open(base_dir + '/../diabetesModel/naiveBayesModel', 'rb'))
    print("model imported")
    result = str((loaded_model.predict([data]))[0])
    print('The result for NB is ' + result)
    return 'Positive' if result == '1' else 'Negative'


def checkUsingDT(base_dir, data:list):
    import pickle
    loaded_model = pickle.load(open(base_dir + '/../diabetesModel/decisionTreeModel', 'rb'))
    print("model imported")
    result = str((loaded_model.predict([data]))[0])
    print('The result for DT is ' + result)
    return 'Positive' if result == '1' else 'Negative'
    
    
# def importModules():
#     import pickle
#     import pandas as pd
#     from sklearn.naive_bayes import GaussianNB 
#     from sklearn.metrics import accuracy_score 
#     from sklearn.preprocessing import StandardScaler
#     from sklearn.neighbors import KNeighborsClassifier  
#     from sklearn.model_selection import train_test_split