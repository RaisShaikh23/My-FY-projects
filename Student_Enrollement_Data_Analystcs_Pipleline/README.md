# 🚀 Student Enrollment Data Engineering & Analytics Pipeline

End-to-End Data Cleaning, Feature Engineering, Outlier Detection, Machine Learning & Association Mining using SQL + Python

## 📌 Project Summary

- Real-world datasets are messy.
- This project simulates a production-level student enrollment dataset containing:
- Duplicate records
- Missing values
- Invalid ages (78*, 4, blank)
- Mixed currency symbols (₹, £, ?, $)
- Inconsistent gender formats (M 25, F 24)
- Multiple date formats (08-01-2023, 01-Jul-21)
- Typographical errors in course names (Web Developmet)
- NULL course values
- Extreme outliers

# # # 🎯 Objective
- Build a complete analytics pipeline:
- Raw Data → SQL Cleaning → Python Preprocessing → 
- Outlier Removal → Visualization → 
- Machine Learning → Association Rule Mining

# # 🏗 Architecture Overview
           ┌──────────────┐
           │ Raw CSV Data │
           └──────┬───────┘
                  │
                  ▼
        ┌──────────────────┐
        │   MySQL Cleaning │
        └──────┬───────────┘
               │
               ▼
        ┌──────────────────┐
        │ Python Cleaning  │
        │  (Pandas + Numpy)│
        └──────┬───────────┘
               │
               ▼
     ┌────────────────────────┐
     │ Outlier Detection (IQR)│
     └──────┬─────────────────┘
            │
            ▼
     ┌────────────────────────────┐
     │ Visualization (Matplotlib) │
     └──────┬─────────────────────┘
            │
            ▼
    ┌───────────────────────┐
    │ Linear Regression ML  │
    └──────┬────────────────┘
           │
           ▼
    ┌───────────────────────┐
    │ Apriori Pattern Mining│
    └───────────────────────┘

###  🛠 Tech Stack
Layer            Technology
Database	     MySQL
Language	     Python
Data Processing	 Pandas, NumPy
Visualization	 Matplotlib
Machine Learning Scikit-learn
Pattern Mining	 mlxtend (Apriori)

# # Outlier Detection (IQR Method)
- Used statistical Interquartile Range:
-  IQR = Q3 − Q1
- Upper Bound = Q3 + 1.5 × IQR
- Outliers removed before ML training to avoid skewed predictions.

## 🤖 Machine Learning: Linear Regression
- Objective:
- Predict student payment based on age.
- model = LinearRegression()
- model.fit(arr_age , arr_salary)

## 🛒 Association Rule Mining (Apriori)

- Used transaction-based transformation:
- freq_sub = apriori(df , min_support=0.1 , use_colnames=True)
- Objective:
- Identify most frequently enrolled courses per date.

#  Student-Enrollment-Analytics/
│
├── raw_data/
│   ├── C1.csv
│   └── additional_data.csv
│
├── cleaned_data/
│   └── Final_data.csv
│
├── sql/
│   └── cleaning_queries.sql
│
├── python/
│   └── analysis_pipeline.py
│
└── README.md

# Future Enhancements
- Add model evaluation metrics
- Build interactive dashboard (Streamlit)
