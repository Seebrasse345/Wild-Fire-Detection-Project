import os
import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_backup(directory):
    """
    Create a backup of the data directory.
    
    Args:
        directory (str): Path to the directory to backup
        
    Returns:
        str: Path to the backup directory
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{directory}_backup_{timestamp}"
    
    try:
        # Create backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        # Copy files to backup directory
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                backup_path = os.path.join(backup_dir, filename)
                
                # Read and write to create a copy
                df = pd.read_csv(file_path)
                df.to_csv(backup_path, index=False)
                
        logger.info(f"Created backup directory: {backup_dir}")
        return backup_dir
    except Exception as e:
        logger.error(f"Failed to create backup: {str(e)}")
        return None

def analyze_data_quality(directory):
    """
    Analyze data quality issues in CSV files.
    
    Args:
        directory (str): Path to directory containing CSV files
        
    Returns:
        dict: Dictionary of data quality metrics
    """
    total_files = 0
    empty_files = 0
    files_with_missing_values = 0
    total_missing_values = 0
    file_info = []
    
    try:
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                total_files += 1
                
                try:
                    df = pd.read_csv(file_path)
                    missing_values = df.isnull().sum().sum()
                    
                    file_info.append({
                        'filename': filename,
                        'rows': len(df),
                        'columns': len(df.columns),
                        'missing_values': missing_values,
                        'empty': len(df) == 0
                    })
                    
                    if df.empty:
                        empty_files += 1
                    
                    if missing_values > 0:
                        files_with_missing_values += 1
                        total_missing_values += missing_values
                        
                except Exception as e:
                    logger.error(f"Error reading file {filename}: {str(e)}")
                    
        # Calculate summary statistics
        empty_percentage = (empty_files / total_files * 100) if total_files > 0 else 0
        
        results = {
            'total_files': total_files,
            'empty_files': empty_files,
            'empty_percentage': empty_percentage,
            'files_with_missing_values': files_with_missing_values,
            'total_missing_values': total_missing_values,
            'file_info': file_info
        }
        
        logger.info(f"Data quality analysis complete. Found {empty_files} empty files out of {total_files} ({empty_percentage:.2f}%)")
        logger.info(f"Files with missing values: {files_with_missing_values}")
        logger.info(f"Total missing values: {total_missing_values}")
        
        return results
    
    except Exception as e:
        logger.error(f"Failed to analyze data quality: {str(e)}")
        return None

def clean_empty_files(directory, dry_run=False):
    """
    Remove empty CSV files from the directory.
    
    Args:
        directory (str): Path to directory containing CSV files
        dry_run (bool): If True, only report what would be deleted without deleting
        
    Returns:
        list: List of deleted file paths
    """
    deleted_files = []
    
    try:
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                
                try:
                    df = pd.read_csv(file_path)
                    
                    if df.empty:
                        if dry_run:
                            logger.info(f"Would delete empty file: {filename}")
                        else:
                            os.remove(file_path)
                            logger.info(f"Deleted empty file: {filename}")
                        deleted_files.append(file_path)
                        
                except Exception as e:
                    logger.error(f"Error processing file {filename}: {str(e)}")
        
        logger.info(f"{'Dry run: ' if dry_run else ''}Cleaned {len(deleted_files)} empty files")
        return deleted_files
    
    except Exception as e:
        logger.error(f"Failed to clean empty files: {str(e)}")
        return []

def clean_missing_values(directory, strategy='drop_rows'):
    """
    Clean missing values in CSV files.
    
    Args:
        directory (str): Path to directory containing CSV files
        strategy (str): Strategy for handling missing values ('drop_rows', 'drop_columns', 'fill_mean')
        
    Returns:
        int: Number of files processed
    """
    processed_files = 0
    
    try:
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                
                try:
                    df = pd.read_csv(file_path)
                    
                    if df.isnull().sum().sum() > 0:
                        original_shape = df.shape
                        
                        if strategy == 'drop_rows':
                            df = df.dropna()
                        elif strategy == 'drop_columns':
                            df = df.dropna(axis=1)
                        elif strategy == 'fill_mean':
                            df = df.fillna(df.mean())
                        else:
                            logger.error(f"Unknown strategy: {strategy}")
                            continue
                        
                        # Save cleaned file
                        df.to_csv(file_path, index=False)
                        processed_files += 1
                        
                        logger.info(f"Cleaned file {filename}: {original_shape} -> {df.shape}")
                        
                except Exception as e:
                    logger.error(f"Error cleaning file {filename}: {str(e)}")
        
        logger.info(f"Cleaned missing values in {processed_files} files using strategy '{strategy}'")
        return processed_files
    
    except Exception as e:
        logger.error(f"Failed to clean missing values: {str(e)}")
        return 0

def main():
    """Main function to execute the data cleaning pipeline."""
    # Define the directory path
    directory = os.path.join(os.getcwd(), 'data', 'features')
    
    if not os.path.exists(directory):
        logger.error(f"Directory does not exist: {directory}")
        return
    
    # Create a backup before cleaning
    backup_dir = create_backup(directory)
    if not backup_dir:
        confirmation = input("Failed to create backup. Continue anyway? (yes/no): ")
        if confirmation.lower() != 'yes':
            logger.info("Operation cancelled by user")
            return
    
    # Analyze data quality
    quality_results = analyze_data_quality(directory)
    if not quality_results:
        logger.error("Failed to analyze data quality")
        return
    
    # Prompt user for confirmation to delete empty files
    if quality_results['empty_files'] > 0:
        confirmation = input(f"There are {quality_results['empty_files']} empty files out of {quality_results['total_files']} total files ({quality_results['empty_percentage']:.2f}%). Delete them? (yes/no): ")
        
        if confirmation.lower() == 'yes':
            deleted_files = clean_empty_files(directory)
            logger.info(f"Deleted {len(deleted_files)} empty files")
        else:
            logger.info("No files were deleted")
    else:
        logger.info("No empty files found")
    
    # Prompt user for confirmation to clean missing values
    if quality_results['files_with_missing_values'] > 0:
        print("Choose a strategy for handling missing values:")
        print("1. Drop rows with missing values")
        print("2. Drop columns with missing values")
        print("3. Fill missing values with mean")
        print("4. Skip cleaning missing values")
        
        choice = input("Enter your choice (1-4): ")
        
        strategies = {
            '1': 'drop_rows',
            '2': 'drop_columns',
            '3': 'fill_mean'
        }
        
        if choice in strategies:
            processed_files = clean_missing_values(directory, strategy=strategies[choice])
            logger.info(f"Cleaned missing values in {processed_files} files")
        else:
            logger.info("Skipped cleaning missing values")
    else:
        logger.info("No files with missing values found")
    
    logger.info("Data cleaning completed")

if __name__ == "__main__":
    main()