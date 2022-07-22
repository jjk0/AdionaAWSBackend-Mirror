import json
import urllib.parse
import boto3
import sys
import numpy as np
import pandas as pd
from timesmash import SymbolicDerivative
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
# from test_nest import test
print('Loading function')

s3 = boto3.client('s3')

def handler(event, context):

    print('Let us test Timesmash. See below.')
    train = [[1, 0, 1, 0, 1, 0], [1, 1, 0, 1, 1, 0]]
    train_label = [[0], [1]]
    test = [[0, 1, 1, 0, 1, 1]]
    train_features, test_features = SymbolicDerivative().fit_transform(
        train=train, test=test, label=train_label
    )
    clf = RandomForestClassifier().fit(train_features, train_label)
    label = clf.predict(test_features)
    print("Predicted label: ", label)
    print('Great! If you see the predicted label, then it worked.')
    print('Now, try pandas and numpy.')
    s = pd.Series([1, 3, 5, np.nan, 6, 8])
    print('pandas and numpy worked!', s)
    print('now try scikit learn')
    iris_X, iris_y = datasets.load_iris(return_X_y=True)
    val = np.unique(iris_y)
    print('sci kit learn worked too!', val)

    print('does nesting work?')
    values = 'placeholder'
    try: 
        confirm = test(values)
        print('if you saw s is here, then yes!', confirm)
    except Exception as e: 
        print(e)
        print('something went wrong')
        raise e 

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda and all the packages ' + label + s + val)
    }