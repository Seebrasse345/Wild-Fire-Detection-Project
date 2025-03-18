#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_data(file_path):
    """
    Load data from CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        DataFrame: Loaded data or None if error
    """
    try:
        logger.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return None

def create_output_dir():
    """
    Create output directory for visualizations.
    
    Returns:
        str: Path to output directory
    """
    output_dir = os.path.join(os.getcwd(), 'visualizations')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{output_dir}_{timestamp}"
    
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")
        return output_dir
    except Exception as e:
        logger.error(f"Error creating output directory: {str(e)}")
        # Fall back to current directory
        return os.getcwd()

def visualize_fire_events_by_day(df, output_dir):
    """
    Visualize fire events by day of the week.
    
    Args:
        df (DataFrame): Input data
        output_dir (str): Output directory for saving visualization
        
    Returns:
        str: Path to saved visualization
    """
    try:
        # Filter for fire events only 
        df_fire_events = df[df['fire'] == 1]
        
        # Count fire events by day of the week
        day_of_week_fire_counts = df_fire_events.groupby('day_of_week')['fire'].count()
        
        # Create a bar plot
        plt.figure(figsize=(10, 6))
        ax = day_of_week_fire_counts.plot.bar(color='firebrick')
        
        # Add labels and title
        plt.xlabel('Day of Week', fontsize=12)
        plt.ylabel('Fire Event Count', fontsize=12)
        plt.title('Distribution of Fire Events by Day of Week', fontsize=14)
        
        # Customize x-axis labels
        plt.xticks(range(7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], fontsize=10)
        
        # Add data labels on bars
        for i, v in enumerate(day_of_week_fire_counts):
            ax.text(i, v + 5, str(v), ha='center', fontsize=10)
        
        plt.tight_layout()
        
        # Save figure
        output_path = os.path.join(output_dir, 'fire_events_by_day.png')
        plt.savefig(output_path, dpi=300)
        plt.close()
        
        logger.info(f"Created visualization: fire events by day of week, saved to {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error creating day of week visualization: {str(e)}")
        return None

def visualize_fire_events_by_hour(df, output_dir):
    """
    Visualize fire events by hour of the day.
    
    Args:
        df (DataFrame): Input data
        output_dir (str): Output directory for saving visualization
        
    Returns:
        str: Path to saved visualization
    """
    try:
        # Filter for fire events only 
        df_fire_events = df[df['fire'] == 1]
        
        # Count fire events by hour of the day
        hour_fire_counts = df_fire_events.groupby('hour_of_day')['fire'].count()
        
        # Create a line plot
        plt.figure(figsize=(12, 6))
        
        # Plot line with markers
        plt.plot(hour_fire_counts.index, hour_fire_counts.values, 
                marker='o', linestyle='-', color='darkorange', 
                linewidth=2, markersize=8)
        
        # Fill area under the line
        plt.fill_between(hour_fire_counts.index, hour_fire_counts.values, 
                        alpha=0.2, color='darkorange')
        
        # Add labels and title
        plt.xlabel('Hour of Day', fontsize=12)
        plt.ylabel('Fire Event Count', fontsize=12)
        plt.title('Distribution of Fire Events by Hour of Day', fontsize=14)
        
        # Customize x-axis
        plt.xticks(range(0, 24, 2), fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Save figure
        output_path = os.path.join(output_dir, 'fire_events_by_hour.png')
        plt.savefig(output_path, dpi=300)
        plt.close()
        
        logger.info(f"Created visualization: fire events by hour of day, saved to {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error creating hour of day visualization: {str(e)}")
        return None

def visualize_weather_correlation(df, output_dir):
    """
    Visualize correlation between weather variables and fire events.
    
    Args:
        df (DataFrame): Input data
        output_dir (str): Output directory for saving visualization
        
    Returns:
        str: Path to saved visualization
    """
    try:
        # Select relevant columns
        weather_cols = ['temperature', 'humidity', 'wind_speed', 'rain', 'clouds', 'fire']
        weather_cols = [col for col in weather_cols if col in df.columns]
        
        if len(weather_cols) < 2:
            logger.warning("Insufficient weather columns for correlation analysis")
            return None
        
        # Create correlation matrix
        corr_matrix = df[weather_cols].corr()
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        
        sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmax=.3, center=0,
                   square=True, linewidths=.5, annot=True, fmt='.2f',
                   cbar_kws={"shrink": .5})
        
        plt.title('Correlation Between Weather Variables and Fire Events', fontsize=14)
        plt.tight_layout()
        
        # Save figure
        output_path = os.path.join(output_dir, 'weather_correlation.png')
        plt.savefig(output_path, dpi=300)
        plt.close()
        
        logger.info(f"Created visualization: weather correlation matrix, saved to {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error creating correlation visualization: {str(e)}")
        return None

def visualize_fire_probability(df, output_dir):
    """
    Visualize fire probability by temperature and humidity.
    
    Args:
        df (DataFrame): Input data
        output_dir (str): Output directory for saving visualization
        
    Returns:
        str: Path to saved visualization
    """
    try:
        # Check if necessary columns exist
        if not all(col in df.columns for col in ['temperature', 'humidity', 'fire']):
            logger.warning("Missing required columns for fire probability visualization")
            return None
        
        # Create temperature and humidity bins
        df['temp_bin'] = pd.cut(df['temperature'], bins=10)
        df['humidity_bin'] = pd.cut(df['humidity'], bins=10)
        
        # Calculate fire probability by temperature bin
        temp_prob = df.groupby('temp_bin')['fire'].mean() * 100
        
        # Calculate fire probability by humidity bin
        humidity_prob = df.groupby('humidity_bin')['fire'].mean() * 100
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot temperature probability
        temp_prob.plot(kind='bar', ax=ax1, color='red')
        ax1.set_title('Fire Probability by Temperature', fontsize=14)
        ax1.set_xlabel('Temperature (°C)', fontsize=12)
        ax1.set_ylabel('Fire Probability (%)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Plot humidity probability
        humidity_prob.plot(kind='bar', ax=ax2, color='blue')
        ax2.set_title('Fire Probability by Humidity', fontsize=14)
        ax2.set_xlabel('Humidity (%)', fontsize=12)
        ax2.set_ylabel('Fire Probability (%)', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Save figure
        output_path = os.path.join(output_dir, 'fire_probability.png')
        plt.savefig(output_path, dpi=300)
        plt.close()
        
        logger.info(f"Created visualization: fire probability, saved to {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error creating fire probability visualization: {str(e)}")
        return None

def create_summary_report(df, output_dir):
    """
    Create a summary report of fire events.
    
    Args:
        df (DataFrame): Input data
        output_dir (str): Output directory for saving report
        
    Returns:
        str: Path to saved report
    """
    try:
        # Count fire events
        fire_events = df['fire'].sum()
        total_events = len(df)
        fire_percentage = (fire_events / total_events) * 100
        
        # Calculate basic statistics
        avg_temp_fire = df[df['fire'] == 1]['temperature'].mean()
        avg_humidity_fire = df[df['fire'] == 1]['humidity'].mean()
        avg_wind_fire = df[df['fire'] == 1]['wind_speed'].mean() if 'wind_speed' in df.columns else 'N/A'
        
        # Create report content
        report_content = f"""Fire Event Analysis Summary
---------------------------
Total Fire Events: {fire_events}
Total Non-Fire Events: {total_events - fire_events}
Proportion of Fire Events: {fire_percentage:.2f}%

Average Conditions During Fire Events:
- Temperature: {avg_temp_fire:.2f}°C
- Humidity: {avg_humidity_fire:.2f}%
- Wind Speed: {avg_wind_fire if isinstance(avg_wind_fire, str) else f"{avg_wind_fire:.2f} m/s"}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        # Save report
        output_path = os.path.join(output_dir, 'fire_analysis_summary.txt')
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        logger.info(f"Created summary report, saved to {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error creating summary report: {str(e)}")
        return None

def main():
    """Main function to execute the data visualization pipeline."""
    # Define input file path
    input_file = os.path.join(os.getcwd(), 'data_combined.csv')
    
    # Load data
    df = load_data(input_file)
    if df is None:
        logger.error("Failed to load data. Exiting.")
        return
    
    # Create output directory
    output_dir = create_output_dir()
    
    # Create visualizations
    visualize_fire_events_by_day(df, output_dir)
    visualize_fire_events_by_hour(df, output_dir)
    visualize_weather_correlation(df, output_dir)
    visualize_fire_probability(df, output_dir)
    
    # Create summary report
    create_summary_report(df, output_dir)
    
    logger.info(f"All visualizations created in {output_dir}")

if __name__ == "__main__":
    main()