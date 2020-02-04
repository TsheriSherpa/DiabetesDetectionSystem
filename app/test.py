
def check(base_dir, data:list):
    import pickle
    import pandas as pd
    import seaborn as sns
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier  

    diabetes = pd.read_csv(base_dir+'/../diabetesModel/diabetes.csv')   #importing dataset.
    X_train, X_test, y_train, y_test = train_test_split(
        diabetes.loc[:, diabetes.columns != 'Outcome'], 
        diabetes['Outcome'], 
        stratify=diabetes['Outcome'],
        random_state=66
    )

    # training_accuracy = []
    # test_accuracy = []
    # # try n_neighbors from 1 to 10
    # neighbors_settings = range(1, 11)

    # for n_neighbors in neighbors_settings:
    #     # build the model
    #     knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    #     knn.fit(X_train, y_train)
    #     # record training set accuracy
    #     training_accuracy.append(knn.score(X_train, y_train))
    #     # record test set accuracy
    #     test_accuracy.append(knn.score(X_test, y_test))
    # knn = KNeighborsClassifier(n_neighbors=9)
    # knn.fit(X_train, y_train)
    #print('Exporting model.')
    # pickle.dump(knn, open(base_dir+'/../diabetesModel/knnModel','wb'))
    loaded_model = pickle.load(open(base_dir+'/../diabetesModel/knnModel', 'rb'))
    # print("model imported")
    # result = loaded_model.score(X_test,y_test)
    result = str((loaded_model.predict([data]))[0])
    if result == "1":
        return "Positive"
    else:
        return "Negative"