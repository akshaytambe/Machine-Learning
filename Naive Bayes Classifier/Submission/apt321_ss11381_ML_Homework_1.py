# coding: utf-8
# Author - Akshay Tambe (apt321) & Snahil Singh (ss11381)
# Importing Packages
import pandas as pd
import numpy as np

# Loading Comma Seperated Data using read_table pandas function in 'spam_train' dataframe
spam_train = pd.read_table("spambasetrain.csv", sep=",", header=None)

# Adding Headers to Data
spam_train.columns = ["char_freq_;", "char_freq_(", "char_freq_[", "char_freq_!", "char_freq_$", "char_freq_#", "capital_run_length_average", "capital_run_length_longest", "capital_run_length_total", "spam_label"]


# Training

# Counting Total Labels
total_labels = spam_train["spam_label"].count()
#print("Total Label Count:", total_labels)

# Count Per Label
value_counts = spam_train["spam_label"].value_counts()
class0_count = value_counts[0]
class1_count = value_counts[1]
#print("Class 0 Label Count:", class0_count)
#print("Class 1 Label Count:", class1_count)


# Estimation of P(C): 
# To estimate the P(C) values, just calculate the fraction of the training examples that are in class C. For example, to estimate P(C = 1) calculate:

# Estimation of P(C)
prob_spam = class1_count/total_labels
prob_not_spam = class0_count/total_labels


# 1. What was the estimated value of P(C) for C = 1?
print("\nP(Spam)=", prob_spam)

# 2. What was the estimated value of P(C) for C = 0?
print("\nP(Not Spam)=", prob_not_spam)

# Seperating Data According to Class Labels
class0 = spam_train[spam_train['spam_label']==0]
class1 = spam_train[spam_train['spam_label']==1]
del class0['spam_label']
del class1['spam_label']


# Estimation of parameters of Gaussian pdf

# Calculation of Class 0 Mean
class0_mean = class0.describe().T['mean']
print("\nClass 0 Mean Calculation:")
print(class0_mean)

# Calculation of Class 1 Mean
class1_mean = class1.describe().T['mean']
print("\nClass 1 Mean Calculation:")
print(class1_mean)

# Calculation of Variance according to the given formula in assignment
def cal_variance(column, mean, count):
    return (column.apply(lambda x: (x-mean)**2).sum())/(count-1)

class0_variance_list = []
class1_variance_list = []

for column in class0:
    class0_variance_list.append(cal_variance(class0[column], class0_mean[column], class0_count))
for column in class1:
    class1_variance_list.append(cal_variance(class1[column], class1_mean[column], class1_count))

# Calculation of Class 0 Variance
class0_variance = pd.Series(class0_variance_list, index=class0.columns)
print("\nClass 0 Variance Calculation:")
print(class0_variance)

# Calculation of Class 1 Variance
class1_variance = pd.Series(class1_variance_list, index=class1.columns)
print("\nClass 1 Variance Calculation:")
print(class1_variance)

# 3. What were the estimated values for (mean, variance) for the Gaussian corresponding to attribute capital run length longest and class 1 (Spam).
#print("\nMean for capital run length longest and class 1=",class1_mean['capital_run_length_longest'])
#print("\nVariance for capital run length longest and class 1=",class1_variance['capital_run_length_longest'])

# 4. What were the estimated values for (mean, variance) for the Gaussian corresponding to attribute char freq ; and Class 0.
#print("\nMean for char_freq_; and class 0=",class0_mean['char_freq_;'])
#print("\nVariance for char_freq_; and class 0=",class0_variance['char_freq_;'])

# Gaussian PDF Formula
import math
def normpdf(x, mean, var):
    pi = 3.1415926
    denom = (2*pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

# Testing

# Loading Comma Seperated Data using read_table pandas function in 'spam_test' dataframe
spam_test = pd.read_table("spambasetest.csv", sep=",", header=None)

# Adding Headers to Data
spam_test.columns = ["char_freq_;", "char_freq_(", "char_freq_[", "char_freq_!", "char_freq_$", "char_freq_#", "capital_run_length_average", "capital_run_length_longest", "capital_run_length_total", "spam_label"]
spam_test

# Predictions for Test Dataset
import math
import xlwt

workbook = xlwt.Workbook()  
sheet = workbook.add_sheet("programanswers")

i = 0
correct_count =0
answer_list = []

if prob_not_spam > prob_spam:
    zero_r_label = 0
else:
    zero_r_label = 1

c_label =0 

for index, row in spam_test.iterrows():
      # Taking Natural Log for P(C)
      pr0 =  math.log(prob_not_spam) 
      pr1 =  math.log(prob_spam)
     
      for column in spam_test:
           # Not counting "spam_label" while doing Predictions!
           if (column!="spam_label"):
               #print(row[column])
               pr0 += math.log(normpdf(row[column],class0_mean[column],class0_variance[column]))
               #print(pr0)
               pr1 += math.log(normpdf(row[column],class1_mean[column],class1_variance[column]))
               #print(pr1)
    
      #print("P(X|C=0) = ",pr0)  
      #print("P(X|C=1) = ",pr1)
    
      # Label the example with the class achieving the maximum value for this expression. If there is a tie, give the example the label 1.
      if (pr0 > pr1):
           class_label = 0
      else:
           class_label = 1
      #print("class_label is : ",class_label)
      answer_list.append(class_label)
      #print(class_label)
      
      if (row["spam_label"] == zero_r_label):
        c_label += 1
      
      # Comparing results with actual predictions
      if  row["spam_label"] == class_label:
        result= "Match"
        correct_count = correct_count+1
      else:
        result="No match"
      sheet.write(i, 0,row["spam_label"] ) 
      sheet.write(i, 1,class_label) 
      sheet.write(i, 2,result) 
      i=i+1
         
workbook.save("output.xls")

# Predicted Class Labels
print("\nPredicted Class Labels:")
answer_list = np.array(answer_list)
print(answer_list)

print("\nNo. of Correct Predictions = ", correct_count)

# 5. Which classes were predicted for the first 5 examples in the test set?
#print(answer_list[0:5])


# 6. Which classes were predicted for the last 5 examples in the test set?
#print(answer_list[195:200])

# 7. What was the percentage error on the examples in the test file?
total_test_labels = spam_test['spam_label'].count()
print("\nNo. of Incorrect Predictions = ", total_test_labels - correct_count)
percentage_error = (1 - (correct_count/total_test_labels))*100
print("\nPrecentage Error = ",percentage_error)


# Using Zero-R Classifier Methodology

# 8. Performance Evaluation using Zero-R Classifier
print("\nzero_r_label = ",zero_r_label)
print("\nMaximized Class Correct Predictions = ",c_label)
zero_r_accuracy = c_label/total_test_labels
print ("\nZero-R Classifier Accuracy = ",zero_r_accuracy )

# The accuracy of Zero-R Classifier is ~59% which is low as compared to performance of Naive-Bayes Classifier.
