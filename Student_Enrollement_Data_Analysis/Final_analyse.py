import pandas as pd
import numpy as np
data = pd.read_csv("C1.csv")

# Filtering Data :----

# cleaning Name Column :
def name_col(data):
    data["FIRST_NAME"] = data["FIRST_NAME"].str.rstrip()
name_col(data)

# cleaning Gender Column :
def gender_col(data):
    data["GENDER"] = data["GENDER"].str.replace(r"[\d+]","",regex=True).str.rstrip()
gender_col(data)

# Cleaning Enrollment Date column :
dicti = {
    "1":"jan",
    "2":"feb",
    "3":"mar",
    "4":"apr",
    "5":"may",
    "6":"jun",
    "7":"july",
    "8":"aug",
    "9":"sep",
    "10":"oct",
    "11":"nov",
    "12":"dec"
}
def enroll_date_col(dicti, date):
    for i in range(len(data["ENROLLMENT_DATE"].index)):
        if date[i][3:6].isalpha()!=True:
            date[i] = f"{date[i][:2]}-{dicti[date[i][4:5]]}-{date[i][6:]}"
        elif len(date[i][7:])<=2:
            date[i] = f"{date[i][:2]}-{date[i][3:6]}-20{date[i][7:]}"

date = data["ENROLLMENT_DATE"]
enroll_date_col(dicti, date)

# Cleaning Total Payment Column :
def payment_col(data):
    data["TOTAL_PAYMENTS"] = (data["TOTAL_PAYMENTS"].astype(str).str.replace(r"[₹£?,]",'', regex=True).str.strip())
    data["TOTAL_PAYMENTS"] = data["TOTAL_PAYMENTS"].astype(float)
payment_col(data)

# Cleaning Age Column :
def age_col(data):
    data["AGE"] = data["AGE"].str.replace(r"[*]","",regex=True)
age_col(data)

# Data
# print(data)
# Final_data
dropped_data = (data.dropna()).reset_index(drop=True)

# Import Final Data To Csv File.
# dropped_data.to_csv("Final_data.csv" , index=False)

# Checking_outlier:----
def detect_out(data , col):
    l1 = [i for i in data[col].dropna()]
    q1 = np.percentile(l1,25)
    q3 = np.percentile(l1,75)
    iqr = q3 - q1
    upper_limit = q3 + (1.5 * iqr)
    return upper_limit

# Visualization 
import matplotlib.pyplot as mtplt
age = sorted(dropped_data["AGE"].values)
payment = dropped_data["TOTAL_PAYMENTS"].values
mtplt.scatter(age,payment ,linestyle = "--", marker="." , color = "black")
mtplt.xlabel("Age")
mtplt.ylabel("Payment")
#mtplt.show()

# Detecting Outliers :
new_data = pd.read_csv("Final_data.csv")
col = 'AGE'
outlier  = detect_out(new_data , col)

# Removing Outliers :
new_data1 = new_data[new_data["AGE"]<outlier]

# Predict Future value using sklearn :
# Simple Sklearn Model for Prediction of Salary in corresponding to Age.

from sklearn.linear_model import LinearRegression
import random as rm
arr_age = np.array([i for i in new_data1['AGE']]).reshape(-1 , 1)
arr_salary = np.array([int(i) for i in new_data1['TOTAL_PAYMENTS']])

# Building Model.
model = LinearRegression()
model.fit(arr_age , arr_salary)

# Testing Model.
# Providing Random Age Group Between 20 to 30 And Predict Salary.
for _ in range(10):
    age = np.array([[rm.randint(20,30)]])
    pred = model.predict(age)
    #print(f" Age :{age} , Salary :{pred[0]}")



import numpy as np
x = np.arange(len(new_data1["TOTAL_PAYMENTS"]))

import matplotlib.pyplot as mtplt
mtplt.bar(x , new_data1["TOTAL_PAYMENTS"] )
mtplt.xticks(x,new_data1["ENROLLMENT_DATE"].str[0:3])
# mtplt.show()


# Building Model to Identify Most Purchesed Course.
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori , association_rules


dicti = {}
for _, row in new_data1.iterrows():
    dicti.setdefault(row["ENROLLMENT_DATE"], []).append(row["COURSE"])

subjects = list(dicti.values())

te = TransactionEncoder()
te_array = te.fit(subjects).transform(subjects)

df = pd.DataFrame(te_array , columns=te.columns_)

freq_sub = apriori(df , min_support=0.1 , use_colnames=True)

print(freq_sub)