import pandas as pd
data = pd.read_json("C:/Users/Afroz/Desktop/ML_journey/train.json")

import numpy as np

# ingredients is a list per row, join into a string
data['ingredients_text'] = data["ingredients"].apply(lambda x: ' '.join(i.lower().replace(' ','_') for i in x))

# print(data['ingredients_text'])

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
x = vectorizer.fit_transform(data['ingredients_text'])
y = data['cuisine']


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=42)

#clf = LogisticRegression(max_iter=1000, C=3, solver='lbfgs') #--1 accuracy-:78.0515  # or solver='saga' for multinomial + L1 

#clf = LogisticRegression(max_iter=1000, C=3, solver='liblinear') #--2 # ERROR:--'liblinear' solver does not support multiclass classification (n_classes >= 3).

clf = LogisticRegression(max_iter=1000, C=3, solver='saga') #--3 accuracy-:78.1018

#clf = LogisticRegression(max_iter=2000, C=3, solver='newton-cg') #--4 accuracy:-78.10182


clf.fit(X_train, y_train)

# print(clf.score(X_test, y_test))

# pred = clf.predict(X_test)
# from sklearn.metrics import accuracy_score
# score = accuracy_score(y_test,pred)
# print(score*100)

def devi(ingredients):
    ingred = [' '.join(i.lower().replace(' ','_') for i in ingredients)]

    value = vectorizer.transform(ingred)
    prediction = clf.predict(value)
    return prediction[0]

r2 = ['tortillas', 'black beans', 'cilantro', 'lime', 'jalapeno', 'avocado']

r3 = ['parmesan cheese', 'basil', 'olive oil', 'garlic', 'spaghetti', 'tomatoes']

r4 = ['garam masala', 'turmeric', 'cumin', 'coriander', 'ghee', 'basmati rice']

r5 = ['fish sauce', 'lemongrass', 'thai basil', 'coconut milk', 'lime leaves']

r6 = ['feta cheese', 'kalamata olives', 'cucumber', 'oregano', 'olive oil']

f7 = ['tortillas','garlic','cumin','thai basil','kalamata olives']

print(devi(f7))
