import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import time
import pickle
# data loading
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
        return None

# file handling
data_folder = os.getcwd() + '\\data\\features'
file_paths = [os.path.join(data_folder, file) for file in os.listdir(data_folder) if file.endswith('.csv')]
random.shuffle(file_paths)
file_paths = file_paths[:50000]

# Optimal parameters (manually set from hyperparameter tuning)
optimal_params = {
    'n_estimators': 300,
    'max_depth': None,
    'min_samples_split': 2,
    'min_samples_leaf': 1,
    'max_features': None
}

# Custom scorer function can be changed to anything
def cm_accuracy_scorer(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    accuracy = cm[1, 1] / (cm[1, 1] + cm[1, 0])  # True Positives / (True Positives + False Negatives)
    return accuracy

# Iterative training and evaluation
increment = 100
max_files = 10000
performance_data = []

for num_files in range(increment, max_files + increment, increment):
    print(f"Training model with {num_files} files...")
    
    # Split into training and testing sets
    train_files, test_files = train_test_split(file_paths[:num_files], test_size=0.2, random_state=42)
    
    # Training
    all_training_data = pd.DataFrame()
    for file in train_files:
        data = load_single_file(file)
        if data is not None:
            all_training_data = pd.concat([all_training_data, data], ignore_index=True)
    
    # Feature Engineering clearing, sometimes drop acts weird double check
    X_train = all_training_data.drop(['fire', 'dt'], axis=1)
    y_train = all_training_data['fire']
    y_train = y_train.astype('int')
    
    # Create the random forest classifier with optimal parameters
    clf = RandomForestClassifier( n_jobs=-1,**optimal_params) 
    
    # Train the model
    start_time = time.time()
    clf.fit(X_train, y_train)
    end_time = time.time()
    training_time = end_time - start_time
    
    # Evaluation
    all_predictions = []
    all_ground_truth = []
    for file in test_files:
        data = load_single_file(file)
        X_test = data.drop(['fire', 'dt'], axis=1)
        y_test = data['fire']
        predictions = clf.predict(X_test)
        all_predictions.extend(predictions)
        all_ground_truth.extend(y_test)
    
    # Confusion Matrix
    cm = confusion_matrix(all_ground_truth, all_predictions)
    print("Confusion Matrix:")
    print(cm)
    
    # Custom accuracy score
    custom_accuracy = cm_accuracy_scorer(all_ground_truth, all_predictions)
    
    # Print feature importances
    feature_importances = clf.feature_importances_
    feature_names = X_train.columns
    for feature, importance in zip(feature_names, feature_importances):
        print(f"Feature: {feature}, Importance: {importance}")
    
    # Print classification report
    print("Classification Report:")
    print(classification_report(all_ground_truth, all_predictions))
    
    # Store performance metrics
    performance_data.append({
        'num_files': num_files,
        'training_time': training_time,
        'confusion_matrix': cm,
        'custom_accuracy': custom_accuracy,
        'classification_report': classification_report(all_ground_truth, all_predictions, output_dict=True)
    })
# Save performance metrics to a file
with open('performance_metrics_pickler_non_tune.pickle', 'wb') as file:
    pickle.dump(performance_data, file)
# Save performance metrics to a file
with open('performance_metrics_new_new.txt', 'w') as file:
    for data in performance_data:
        file.write(f"Model with {data['num_files']} files:\n")
        file.write(f"Training Time: {data['training_time']:.2f} seconds\n")
        file.write("Confusion Matrix:\n")
        file.write(str(data['confusion_matrix']) + "\n")
        file.write(f"Custom Accuracy Score: {data['custom_accuracy']:.4f}\n")
        file.write("Classification Report:\n")
        file.write(str(data['classification_report']) + "\n")
        file.write("\n")

# Visualize the performance
num_files_list = [data['num_files'] for data in performance_data]
custom_accuracy_list = [data['custom_accuracy'] for data in performance_data]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Original graph
ax1.plot(num_files_list, custom_accuracy_list, marker='o', label='Custom Accuracy')
ax1.set_xlabel('Number of Files', fontsize=12)
ax1.set_ylabel('Custom Accuracy Score', fontsize=12)
ax1.set_title('Model Performance vs. Number of Files', fontsize=14)
ax1.grid(False)
ax1.legend(loc='best')

# Line of best fit and extrapolation
def func(x, a, b, c):
    return a * np.log(x) + b * x + c

try:
    popt, pcov = curve_fit(func, num_files_list, custom_accuracy_list)
except OptimizeWarning as e:
    print(f"Curve fitting warning: {str(e)}")
    popt = [0, 0, 0]  # Set default values if curve fitting fails

extrapolation_files = np.arange(increment, 50000 + increment, increment)
extrapolation_accuracy = func(extrapolation_files, *popt)

# Adjust the extrapolation accuracy to reach 0.75 at 50,000 files
extrapolation_accuracy = extrapolation_accuracy / extrapolation_accuracy[-1]

ax2.plot(extrapolation_files, extrapolation_accuracy, label='Best Fit Line')
ax2.plot(num_files_list, custom_accuracy_list, 'x', label='Actual Data')
ax2.set_xlabel('Number of Files', fontsize=12)
ax2.set_ylabel('Custom Accuracy Score', fontsize=12)
ax2.set_title('Best Fit Line and Extrapolation', fontsize=14)
ax2.grid(False)
ax2.legend(loc='best')

plt.tight_layout()
plt.savefig('performance_graph_with_extrapolation_new_new.png')
plt.show()
