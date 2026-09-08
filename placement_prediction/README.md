# 🎓 Placement Prediction Dashboard

A machine learning-based **Student Placement Prediction Dashboard** built using **Python, Streamlit, MySQL, Pandas, NumPy, and Scikit-learn**.

The application uses **Logistic Regression** to predict whether a student is likely to get placed based on two input parameters:

* 🎓 CGPA
* 🧠 IQ

The project also provides a dashboard to view student placement data and allows the machine learning model to be **retrained whenever new data is added**.

---

## 📌 Project Overview

The project consists of two main components:

1. **Machine Learning Backend**

   * Connects to a MySQL database.
   * Retrieves student placement data.
   * Trains a Logistic Regression model.
   * Standardizes CGPA and IQ using `StandardScaler`.
   * Provides placement predictions.
   * Allows the model to be retrained.

2. **Streamlit Dashboard**

   * Displays the student dataset.
   * Shows basic dataset statistics.
   * Displays placement distribution.
   * Accepts CGPA and IQ as user inputs.
   * Predicts Placement Yes/No.
   * Provides a Retrain Model button.
   * Prevents repeated model retraining for 60 seconds.

---

## 🗂️ Project Structure

```text
Placement_Project/
│
├── app.py
├── something.py
└── requirements.txt
```

### `app.py`

Contains the Streamlit dashboard and user interface.

### `something.py`

Contains the machine learning model and database functions.

Main functions:

```python
datam()
model()
result(cgpa, iq)
retrain_model()
```

### `requirements.txt`

Contains the Python packages required to run the project.

---

## 🛠️ Technologies Used

| Technology          | Purpose                     |
| ------------------- | --------------------------- |
| Python              | Programming language        |
| Streamlit           | Dashboard and web interface |
| MySQL               | Student placement database  |
| Pandas              | Data manipulation           |
| NumPy               | Numerical operations        |
| Scikit-learn        | Machine learning            |
| Logistic Regression | Placement classification    |
| StandardScaler      | Feature scaling             |

---

## 🗄️ Database

The project uses a MySQL database named:

```text
placement
```

The application reads student information from the table:

```text
INFO
```

The database connection is configured in `something.py`.

The first two columns of the `INFO` table are used as model features, while the last column is used as the target variable.

Conceptually:

```text
CGPA ────────┐
             ├──> Logistic Regression ──> Placement
IQ ──────────┘
```

---

## 🤖 Machine Learning Model

The project uses **Logistic Regression** for binary classification.

### Features

The model uses:

```text
CGPA
IQ
```

### Target

The target represents placement status:

```text
1 → Placement Yes
0 → Placement No
```

Before training, the input features are standardized using:

```python
StandardScaler()
```

The model is trained using:

```python
LogisticRegression()
```

---

## 🔄 Model Training Process

The machine learning workflow is:

```text
MySQL Database
       ↓
Load Student Data
       ↓
Select CGPA & IQ
       ↓
Train/Test Split
       ↓
StandardScaler
       ↓
Logistic Regression
       ↓
Trained Model
       ↓
Placement Prediction
```

---

## 🎯 Placement Prediction

Users can enter:

```text
CGPA
IQ
```

For example:

```text
CGPA = 8.5
IQ   = 120
```

The dashboard sends these values to:

```python
result(cgpa, iq)
```

The model then returns:

```text
Placement--Yes
```

or

```text
Placement--No
```

The Streamlit dashboard displays the result in a user-friendly format.

---

## 🔄 Retrain Model

The dashboard includes a **Retrain Model** button.

When clicked:

```text
New Data in MySQL
        ↓
Fetch Updated Dataset
        ↓
Train New Model
        ↓
Replace Existing Model
```

This allows the model to learn from newly added student records.

### 60-Second Retraining Restriction

To prevent repeated unnecessary training, the dashboard disables the **Retrain Model** button for **60 seconds** after a successful retraining.

The dashboard displays a countdown indicating when retraining will be available again.

---

## 📊 Dashboard Features

### Dashboard

Provides an overview of the dataset, including:

* Total number of students
* Average CGPA
* Average IQ
* Number of students with Placement Yes
* Placement distribution chart

### Dataset

Displays the complete student placement dataset in a Streamlit dataframe.

### Prediction

Allows users to enter:

* CGPA
* IQ

and receive a placement prediction.

### Model Controls

Provides:

* Retrain Model button
* Retraining status
* 60-second cooldown

---

## ⚙️ Installation

### 1. Clone or download the project

Place the project in a folder named:

```text
Placement_Project
```

---

### 2. Open the terminal

Navigate to the project folder:

```bash
cd Desktop\Placement_Project
```

---

### 3. Install dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## 🗃️ MySQL Configuration

Make sure MySQL Server is running.

Create/use the database:

```sql
CREATE DATABASE placement;
```

The application expects the student data table:

```text
INFO
```

Make sure the database connection details in `something.py` match your local MySQL configuration.

Example:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="placement"
)
```

> **Security Note:** Do not commit your real MySQL password to GitHub. For a public project, use environment variables instead.

---

## ▶️ Running the Application

From inside the `Placement_Project` folder, run:

```bash
streamlit run app.py
```

Streamlit will start the application and provide a local web address.

Open the displayed address in your browser.

---

## 📋 Example Workflow

### Step 1 — Start the application

```bash
streamlit run app.py
```

### Step 2 — Open Dashboard

View:

```text
Total Students
Average CGPA
Average IQ
Placement Distribution
```

### Step 3 — Check Dataset

Navigate to:

```text
📋 Dataset
```

to view the student records.

### Step 4 — Predict Placement

Navigate to:

```text
🎯 Prediction
```

Enter:

```text
CGPA = 8.5
IQ = 120
```

Click:

```text
🔍 Predict Placement
```

The application will display the predicted placement result.

### Step 5 — Retrain

If new student data has been added to MySQL, click:

```text
🔄 Retrain Model
```

The model will be trained again using the updated database.

---

## 📦 Requirements

The `requirements.txt` file should contain:

```text
streamlit
pandas
numpy
scikit-learn
mysql-connector-python
```

---

## 🔐 Security

For development, database credentials may be stored locally.

For production or GitHub:

* Do not expose database passwords.
* Use environment variables.
* Do not commit `.env` files.
* Add sensitive files to `.gitignore`.

Example:

```text
.env
__pycache__/
*.pyc
```

---

## 🚀 Future Improvements

Possible improvements include:

* 📈 Model accuracy display
* 📊 Confusion matrix
* 📉 ROC-AUC curve
* 📌 Prediction probability
* 📥 Download prediction results
* 🔍 Student search/filtering
* 📊 CGPA vs IQ visualization
* 👨‍🎓 Individual student profiles
* 🔐 User authentication
* ☁️ Deployment to Streamlit Community Cloud
* 🔒 Secure database configuration using environment variables

---

## 👨‍💻 Project

**Project Name:** Placement Prediction Dashboard

**Machine Learning Algorithm:** Logistic Regression

**Input Features:** CGPA, IQ

**Output:** Placement Yes / Placement No

**Interface:** Streamlit

**Database:** MySQL

---

## 📄 License

This project is intended for educational and learning purposes.
