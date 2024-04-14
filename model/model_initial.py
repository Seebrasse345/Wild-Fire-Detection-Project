import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix
import random
import matplotlib.pyplot as plt

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
print(len(file_paths))
file_paths = file_paths[:10000]
random.shuffle(file_paths)
print(len(file_paths))

# Split into training and testing sets
train_files, test_files = train_test_split(file_paths, test_size=0.2, random_state=42)

# training
all_training_data = pd.DataFrame()
for file in train_files:
    data = load_single_file(file)
    if data is not None:
        all_training_data = pd.concat([all_training_data, data], ignore_index=True)

# Feature Engineering
X_train = all_training_data.drop(['fire', 'dt'], axis=1)
y_train = all_training_data['fire']
y_train = y_train.astype('int')

# Define the parameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 5, 10],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2', None]
}

# Create the random forest classifier
clf = RandomForestClassifier(random_state=42)

# Perform grid search
grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Get the best hyperparameters and best score
best_params = grid_search.best_params_
best_score = grid_search.best_score_
print("Best Hyperparameters:", best_params)
print("Best Accuracy Score:", best_score)

# Evaluate the model with the best hyperparameters
best_model = grid_search.best_estimator_

all_predictions = []
all_ground_truth = []
for file in test_files:
    data = load_single_file(file)
    X_test = data.drop(['fire', 'dt'], axis=1)
    y_test = data['fire']
    predictions = best_model.predict(X_test)
    all_predictions.extend(predictions)
    all_ground_truth.extend(y_test)

# Confusion Matrix
cm = confusion_matrix(all_ground_truth, all_predictions)
print("Confusion Matrix:")
print(cm)

# Extract accuracy from the confusion matrix
accuracy = (cm[0, 0] + cm[1, 1]) / cm.sum()

# Visualize the results
param_names = ['n_estimators', 'max_depth', 'min_samples_split', 'min_samples_leaf', 'max_features']
param_values = [param_grid[param] for param in param_names]
accuracy_scores = []

fig, axs = plt.subplots(len(param_names), 1, figsize=(8, 12), sharex=True, sharey=True)
fig.suptitle('Hyperparameter Tuning Results')

for i, param in enumerate(param_names):
    accuracy_scores = []
    for params in grid_search.cv_results_['params']:
        if params[param] == param_values[i][0]:
            accuracy_scores.append(grid_search.cv_results_['mean_test_score'][grid_search.cv_results_['params'].index(params)])
    
    axs[i].plot(param_values[i], accuracy_scores, marker='o')
    axs[i].set_xlabel(param)
    axs[i].set_ylabel('Accuracy')
    axs[i].set_title(f'{param} vs. Accuracy')
    axs[i].legend([param], loc='best')
    
    plt.savefig(f'{param}_tuning_results.png')

plt.tight_layout()
plt.savefig('combined_hyperparameter_tuning_results.png')
plt.show()