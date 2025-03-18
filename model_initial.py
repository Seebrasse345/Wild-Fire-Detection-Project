import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# import numpy as np

# Select features and target

# ------ Data Loading and Preprocessing ------
def load_single_file(file_path):
    try:
        df = pd.read_csv(file_path, sep=',')
        df.dropna()

        columns_to_keep = ['clouds', 'wind_speed', 'hour_of_day', 'fire', 'rain', 'dt', 'day_of_week', 'humidity', 'temperature']
        columns_to_keep = [col for col in columns_to_keep if col in df.columns]
        df = df[columns_to_keep]

        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None  # return None if file not found


# ------ File Handling ------
data_folder = os.getcwd() + '\\data\\features'
file_paths = [os.path.join(data_folder, file) for file in os.listdir(data_folder) if file.endswith('.csv')]

# Split into training and testing sets
train_files, test_files = train_test_split(file_paths, test_size=0.2, random_state=42)
# ------ Training ------
all_training_data = pd.DataFrame()

for file in train_files:
    data = load_single_file(file)
    if data is not None:  # only concatenate if data is not None
        all_training_data = pd.concat([all_training_data, data], ignore_index=True)
# Feature Engineering
X_train = all_training_data.drop(['fire', 'dt'], axis=1)  
y_train = all_training_data['fire']
y_train = y_train.astype('int')

# Select features and target
# Model Creation and Training

clf = RandomForestClassifier(random_state=42) 
clf.fit(X_train, y_train)
all_predictions = []
all_ground_truth = []
directory = 'test_files'
empty_files = []

# Total number of files
total_files = 0


for file in test_files:
    data = load_single_file(file)
    
    
    X_test  = data.drop(['fire', 'dt'], axis=1)
    
    
    y_test = data['fire']

    predictions = clf.predict(X_test)
    all_predictions.extend(predictions)
    all_ground_truth.extend(y_test)


from sklearn.metrics import confusion_matrix

# Confusion Matrix
cm = confusion_matrix(all_ground_truth, all_predictions)
print("Confusion Matrix:")
print(cm)

# Other Evaluation Metrics
tn, fp, fn, tp = cm.ravel()
print("True Negatives:", tn)
print("False Positives:", fp)
print("False Negatives:", fn)
print("True Positives:", tp)
print("Accuracy:", accuracy_score(all_ground_truth, all_predictions))
print("Precision:", precision_score(all_ground_truth, all_predictions))
print("Recall:", recall_score(all_ground_truth, all_predictions))
print("F1-Score:", f1_score(all_ground_truth, all_predictions))
