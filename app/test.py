
def checkUsingKNN(base_dir, data:list):
    import pickle
    # import pandas as pd
    # from sklearn.model_selection import train_test_split
    # from sklearn.neighbors import KNeighborsClassifier 
    
    
    # diabetes = pd.read_csv(base_dir+'/../diabetesModel/diabetes.csv')   #importing dataset.
    # X_train, X_test, y_train, y_test = train_test_split(
    #     diabetes.loc[:, diabetes.columns != 'Outcome'], 
    #     diabetes['Outcome'], 
    #     stratify=diabetes['Outcome'],
    #     random_state=66
    # )

    # training_accuracy = []
    # test_accuracy = []
    # # try n_neighbors from 1 to 10
    # neighbors_settings = range(1, 11)

    # for n_neighbors in neighbors_settings:  #finding the best neighbour for knn model.
    #     # build the model
    #     knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    #     knn.fit(X_train, y_train)
    #     # record training set accuracy
    #     training_accuracy.append(knn.score(X_train, y_train))
    #     # record test set accuracy
    #     test_accuracy.append(knn.score(X_test, y_test))
    # knn = KNeighborsClassifier(n_neighbors=9)   # neightbour 9 has best accuracy
    # knn.fit(X_train, y_train)
    #print('Exporting model.')
    # pickle.dump(knn, open(base_dir+'/../diabetesModel/knnModel','wb'))
    
    loaded_model = pickle.load(open(base_dir+'/../diabetesModel/knnModel', 'rb'))
    print("model imported")
    result = str((loaded_model.predict([data]))[0])

    print('The result for KNN is '+str(result))
    return 'Positive' if result == '1' else 'Negative'



def checkUsingNaiveBayes(base_dir, data:list):
    import pickle
    # import pandas as pd
    # from sklearn.naive_bayes import GaussianNB 
    # from sklearn.metrics import accuracy_score 
    # from sklearn.preprocessing import StandardScaler
    # from sklearn.model_selection import train_test_split
    
    
    # diabetes = pd.read_csv(base_dir+'/../diabetesModel/diabetes.csv')   #importing dataset.
    # X_train, X_test, y_train, y_test = train_test_split(
    #     diabetes.loc[:, diabetes.columns != 'Outcome'], 
    #     diabetes['Outcome'], 
    #     stratify=diabetes['Outcome'],
    #     random_state=66
    # )
    # naiveBayes = GaussianNB()
    # naiveBayes.fit(X_train, y_train)
    # pickle.dump(naiveBayes, open(base_dir + '/../diabetesModel/naiveBayesModel','wb'))

    loaded_model = pickle.load(open(base_dir + '/../diabetesModel/naiveBayesModel', 'rb'))
    print("model imported")
    result = str((loaded_model.predict([data]))[0])
    print('The result for naive bayes is ' + result)

    return 'Positive' if result == '1' else 'Negative'


def checkUsingDT(base_dir, data:list):
    import pickle
    import pandas as pd
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    
    
    # diabetes = pd.read_csv(base_dir+'/../diabetesModel/diabetes.csv') 
    # tree = DecisionTreeClassifier(max_depth=3, random_state=66)
    # X_train, X_test, y_train, y_test = train_test_split(
    #                                             diabetes.loc[:, diabetes.columns != 'Outcome'],
    #                                             diabetes['Outcome'], stratify=diabetes['Outcome'],
    #                                             random_state=66)
    # tree.fit(X_train, y_train)
    # pickle.dump(tree, open(base_dir + '/../diabetesModel/decisionTreeModel','wb'))

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