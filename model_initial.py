import pandas as pd
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import joblib

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ------ Data Loading and Preprocessing ------
def load_single_file(file_path):
    """
    Load a single CSV file and preprocess it.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        DataFrame: Preprocessed DataFrame or None if file not found
    """
    try:
        df = pd.read_csv(file_path, sep=',')
        # Drop rows with missing values
        df = df.dropna()

        # Select relevant columns
        columns_to_keep = ['clouds', 'wind_speed', 'hour_of_day', 'fire', 'rain', 'dt', 
                          'day_of_week', 'humidity', 'temperature']
        columns_to_keep = [col for col in columns_to_keep if col in df.columns]
        df = df[columns_to_keep]

        logger.info(f"Loaded file: {file_path}, Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error loading file {file_path}: {str(e)}")
        return None

def load_and_preprocess_data(data_folder, test_size=0.2, random_state=42):
    """
    Load all CSV files from a folder, preprocess them, and split into train/test sets.
    
    Args:
        data_folder (str): Path to folder containing CSV files
        test_size (float): Proportion of data to use for testing
        random_state (int): Random seed for reproducibility
        
    Returns:
        tuple: X_train, X_test, y_train, y_test, feature_names
    """
    # Get all CSV files in the data folder
    file_paths = [os.path.join(data_folder, file) for file in os.listdir(data_folder) 
                 if file.endswith('.csv')]
    
    if not file_paths:
        logger.error(f"No CSV files found in {data_folder}")
        return None, None, None, None, None
    
    logger.info(f"Found {len(file_paths)} CSV files in {data_folder}")
    
    # Split into training and testing sets at file level
    train_files, test_files = train_test_split(
        file_paths, test_size=test_size, random_state=random_state
    )
    
    # Load and combine training data
    all_training_data = pd.DataFrame()
    for file in train_files:
        data = load_single_file(file)
        if data is not None:
            all_training_data = pd.concat([all_training_data, data], ignore_index=True)
    
    # Load and combine testing data
    all_testing_data = pd.DataFrame()
    for file in test_files:
        data = load_single_file(file)
        if data is not None:
            all_testing_data = pd.concat([all_testing_data, data], ignore_index=True)
    
    if all_training_data.empty or all_testing_data.empty:
        logger.error("No valid data found after loading files")
        return None, None, None, None, None
    
    logger.info(f"Training data shape: {all_training_data.shape}")
    logger.info(f"Testing data shape: {all_testing_data.shape}")
    
    # Feature engineering
    X_train = all_training_data.drop(['fire', 'dt'], axis=1)
    y_train = all_training_data['fire'].astype('int')
    
    X_test = all_testing_data.drop(['fire', 'dt'], axis=1)
    y_test = all_testing_data['fire'].astype('int')
    
    feature_names = X_train.columns.tolist()
    
    return X_train, X_test, y_train, y_test, feature_names

def train_random_forest_model(X_train, y_train, cv=5, n_jobs=-1):
    """
    Train a Random Forest model with hyperparameter tuning.
    
    Args:
        X_train (DataFrame): Training features
        y_train (Series): Training target
        cv (int): Number of cross-validation folds
        n_jobs (int): Number of parallel jobs for GridSearchCV
        
    Returns:
        GridSearchCV: Trained model with best parameters
    """
    # Define the hyperparameter grid
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    }
    
    # Create the base model
    rf = RandomForestClassifier(random_state=42)
    
    # Set up GridSearchCV
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=cv,
        n_jobs=n_jobs,
        scoring='f1',
        verbose=1
    )
    
    # Fit the model
    logger.info("Starting hyperparameter tuning with GridSearchCV...")
    grid_search.fit(X_train, y_train)
    
    logger.info(f"Best parameters: {grid_search.best_params_}")
    logger.info(f"Best cross-validation score: {grid_search.best_score_:.4f}")
    
    return grid_search

def evaluate_model(model, X_test, y_test, feature_names):
    """
    Evaluate the model on the test set and visualize results.
    
    Args:
        model: Trained model
        X_test (DataFrame): Test features
        y_test (Series): Test target
        feature_names (list): Names of features
        
    Returns:
        dict: Dictionary of evaluation metrics
    """
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Create confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    # Print metrics
    logger.info("Model Evaluation Metrics:")
    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info(f"Precision: {precision:.4f}")
    logger.info(f"Recall: {recall:.4f}")
    logger.info(f"F1-Score: {f1:.4f}")
    logger.info("\nConfusion Matrix:")
    logger.info(f"True Negatives: {tn}")
    logger.info(f"False Positives: {fp}")
    logger.info(f"False Negatives: {fn}")
    logger.info(f"True Positives: {tp}")
    
    # Print classification report
    logger.info("\nClassification Report:")
    logger.info(classification_report(y_test, y_pred))
    
    # Visualize confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['No Fire', 'Fire'],
                yticklabels=['No Fire', 'Fire'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    
    # Plot feature importance
    if hasattr(model, 'best_estimator_'):
        feature_importance = model.best_estimator_.feature_importances_
    else:
        feature_importance = model.feature_importances_
        
    sorted_idx = feature_importance.argsort()
    plt.figure(figsize=(10, 8))
    plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx])
    plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
    plt.xlabel('Feature Importance')
    plt.title('Random Forest Feature Importance')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm,
        'y_pred': y_pred
    }

def save_model(model, filename='random_forest_model.joblib'):
    """
    Save the trained model to a file.
    
    Args:
        model: Trained model to save
        filename (str): Output filename
        
    Returns:
        str: Path to saved model
    """
    try:
        joblib.dump(model, filename)
        logger.info(f"Model saved to {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error saving model: {str(e)}")
        return None

def main():
    """Main function to execute the model training pipeline."""
    # Set the path to the data folder
    data_folder = os.path.join(os.getcwd(), 'data', 'features')
    
    # Load and preprocess data
    X_train, X_test, y_train, y_test, feature_names = load_and_preprocess_data(data_folder)
    
    if X_train is None:
        logger.error("Failed to load data. Exiting.")
        return
    
    # Train model with hyperparameter tuning
    model = train_random_forest_model(X_train, y_train)
    
    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test, feature_names)
    
    # Save model
    save_model(model)
    
    logger.info("Model training and evaluation complete.")
    return model, metrics

if __name__ == "__main__":
    main()
