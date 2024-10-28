import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import shutil


DATA_FNAME = r"./build/data.pickle"
data_file = open(DATA_FNAME, 'rb')
data_dict = pickle.load(data_file)
data_file.close()

#print(data_dict.keys(), data_dict)

data, labels = data_dict['data'], data_dict['labels']

train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.05, shuffle=True, stratify=labels)

model = RandomForestClassifier(n_estimators=300, max_features="log2")
model.fit(train_data, train_labels)

test_labels_predicted = model.predict(test_data)

score = accuracy_score(test_labels, test_labels_predicted)*100
print(score, "% sample classified correctly")


MODEL_FNAME = r"./build/model.pickle"
MODEL_FNAME_BAK = r"./build/model_bak.pickle" # create a backup of previous data file if it exists
if os.path.exists(MODEL_FNAME): shutil.move(MODEL_FNAME, MODEL_FNAME_BAK)

model_file = open(MODEL_FNAME, 'wb')
pickle.dump({'model': model}, model_file)
model_file.close()
