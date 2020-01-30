

def check():
	import pickle
	import pandas as pd
	import seaborn as sns
	from sklearn.model_selection import train_test_split
	from sklearn.neighbors import KNeighborsClassifier  


	diabetes = pd.read_csv('/home/resham/Downloads/diabetes.csv')   #importing dataset.
	X_train, X_test, y_train, y_test = train_test_split(
		diabetes.loc[:, diabetes.columns != 'Outcome'], 
		diabetes['Outcome'], 
		stratify=diabetes['Outcome'],
		random_state=66
	)

	training_accuracy = []
	test_accuracy = []
	# try n_neighbors from 1 to 10
	neighbors_settings = range(1, 11)

	for n_neighbors in neighbors_settings:
	    # build the model
	    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
	    knn.fit(X_train, y_train)
	    # record training set accuracy
	    training_accuracy.append(knn.score(X_train, y_train))
	    # record test set accuracy
	    test_accuracy.append(knn.score(X_test, y_test))


	knn = KNeighborsClassifier(n_neighbors=9)
	knn.fit(X_train, y_train)
	#print('Exporting model.')
	# pickle.dump(knn, open('/home/resham/projects/tsheri/flask/diabetesModel/knnModel','wb'))
	loaded_model = pickle.load(open('/home/resham/projects/tsheri/flask/diabetesModel/knnModel', 'rb'))
	# print("model imported")
	result = loaded_model.score(X_test,y_test)
	return 'The result is '+ str(result)
