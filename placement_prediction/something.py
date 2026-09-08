import mysql.connector
import pandas as pd
import numpy as np


def datam():

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Rais.s0230',
            database='placement'
        )
        print("Connection successful")

        try:

            data = pd.read_sql_query(
                "SELECT * FROM INFO",
                conn
            )

            print("Data Fetch Successful")

            conn.close()

            return data

        except:

            print("Failed to fetch data")

            conn.close()

            return None

    except:

        print("Connection Error")

        return None


def model():

    data = datam()

    if data is None:
        return None, None

    x = data.iloc[:, :2]

    y = data.iloc[:, -1]


    from sklearn.model_selection import train_test_split

    X_train, x_test, Y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.1
    )


    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)

    x_test = scaler.transform(x_test)


    from sklearn.linear_model import LogisticRegression

    clf = LogisticRegression()

    clf.fit(X_train, Y_train)


    return scaler, clf


# Initial model training
scaler, clf = model()


def result(cgpa, iq):

    if clf is None or scaler is None:

        return "Model is Not Available"

    xa = np.array([cgpa, iq]).reshape(1, -1)

    xa = scaler.transform(xa)

    pre = clf.predict(xa)

    if pre[0] == 1:

        return "Placement--Yes"

    else:

        return "Placement--No"


def retrain_model():

    global clf, scaler

    new_scaler, new_clf = model()

    if new_scaler is None or new_clf is None:

        return False

    clf = new_clf

    scaler = new_scaler

    return True