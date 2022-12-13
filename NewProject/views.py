# -*- coding: utf-8 -*-

""" Loading Necessary Dependencies """
#Importing Required Library
import pandas as pd
import numpy as np
import requests
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


""" Data Collection Stage"""
# Loading The Dataset into the Pandas Dataframe
mail_data = pd.read_csv(r'https://github.com/mubarakebb/Email-Spam-Detection-System/blob/main/static/file/dataset.csv')
#print(mail_data)

"""Data Evaluation and Validation"""
# Replacing the null values(i.e empty cells) with a null string
# Storing the validated data in a new variable
valid_mail_data = mail_data.where((pd.notnull(mail_data)), '')


""" Date Encoding Stage """
# Encoding Dataset with label (spam as 1 and not_spam as 0)
# Spam = 1 and Not_Spam = 0
valid_mail_data.loc[valid_mail_data['Label'] == 'spam', 'Label'] = 1
valid_mail_data.loc[valid_mail_data['Label'] == 'not_spam', 'Label'] = 0

""" Data Tokenization - Seperation of the Data into 'EmailText' and 'Label' """
# Seperating the dataset into meaningful smaller set for proper processing
# Creating a variable X to store the "EmailText" and variable Y to store the "Label"
X = valid_mail_data['EmailText']
Y = valid_mail_data['Label']

""" Pre-Processing Stage - Data Slipting """
#Spliting the data into "Training Data" and "Test Data"
# Traning Data = 80% of Dataset
# Test Data = 20% of the Dataset
# Creating new variable X_train, X_test, Y_train and Y_test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=3)

""" Data Transformation - Feature Extraction """
# Transforming the Data to a Feature Vector
# Vectorized data will be used as input to the logistic Regression model
feature_extraction = TfidfVectorizer(min_df = 1, stop_words = 'english', lowercase = 'true')
X_train_features = feature_extraction.fit_transform (X_train)
X_test_features = feature_extraction.transform (X_test)

# Converting Y_train and Y_test Data from Object to Integers
Y_train = Y_train.astype ('int')
Y_test = Y_test.astype ('int')

""" Data Processing Phase - Logistics Regression Model """
# Logistics Regression Model
model = LogisticRegression ()
# Traing the Logistics Regression Model with the Data
model.fit(X_train_features, Y_train)

""" Model Evaluation """
# Prediction using the Train data
pred_on_train_data = model.predict(X_train_features)

# Accuracy Check on the Trained Model
accuracy_on_train_data = accuracy_score(Y_train, pred_on_train_data)

""" Prediction Using the Test data """
pred_on_test_data = model.predict(X_test_features)

# Accuracy Check on the Trained Model
accuracy_on_test_data = accuracy_score(Y_test, pred_on_test_data)


def homePage (request):
     
    return render (request, 'index.html', {})


def createModel (request):
    
    # Evaluation Report
    classificationReport = classification_report (Y_train, pred_on_train_data )
    classificationReport2 = classification_report (Y_test, pred_on_test_data )

    # Accuracy Check on the Trained Model
    accuracy_on_train_data = accuracy_score(Y_train, pred_on_train_data)

    # Accuracy Check using Test data
    accuracy_on_test_data = accuracy_score(Y_test, pred_on_test_data)

    print(classificationReport2)
    print (classificationReport)
    
    report = {
        'data' : classificationReport,
        'data2': classificationReport2,
        'data3' : accuracy_on_train_data,
        'data4' : accuracy_on_test_data,
    }

    return render (request, 'index.html', report)

def single (request):

    """ User Input Section """
    raw_input_mail = request.POST.get('singleInput')
    input_mail = [raw_input_mail]
    print (input_mail)
    
    # Converting Text to feature extraction vector
    input_mail_vector = feature_extraction.transform (input_mail)
    prediction = model.predict (input_mail_vector)

    pred = prediction
    if pred [0] == 1:
        statusReport = 'Spam Content'
        commentReport = 'This input is a spam, trust the content at your own risk'
        #print ('The input mail is SPAM - Trust the content at your own risk')

    else:
        statusReport = 'Not-Spam Content'
        commentReport = 'This input is safe, you can trust the content'
        #print ('This is not a SPAM Mail')

    classificationReport = classification_report (Y_train, pred_on_train_data )
    classificationReport2 = classification_report (Y_test, pred_on_test_data )
    accuracy_on_train_data = accuracy_score(Y_train, pred_on_train_data)
    accuracy_on_test_data = accuracy_score(Y_test, pred_on_test_data)
    
    report = {
        'data' : classificationReport,
        'data2': classificationReport2,
        'data3' : accuracy_on_train_data,
        'data4' : accuracy_on_test_data,
        'status' : statusReport,
        'comment' : commentReport
    }

    return render (request, 'index.html', report)
