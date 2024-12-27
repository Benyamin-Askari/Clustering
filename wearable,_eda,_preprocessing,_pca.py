# -*- coding: utf-8 -*-
"""Wearable, EDA, Preprocessing, PCA

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Dq1K9CtKSpUsb2XbNQrGiUk4osd64bjG
"""

!pip install pandas numpy matplotlib seaborn missingno

import pandas as pd

# load the dataset
data = pd.read_csv('filtered_data.csv')

## Overview of the dataset
print("Dataset Shape:", data.shape)
data.info()
print(data.describe(include='all'))

## Display the first few rows
print(data.head())

## Pairwise scatter plot matrix
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(15, 15))
sns.pairplot(data.drop(columns=['Subject ID', 'Activity_Label']).dropna(), diag_kind='kde', plot_kws={'alpha': 0.5})
plt.suptitle('Pairwise Scatter Plot Matrix', y=1.02)
plt.show()

# Columns to exclude from plotting
exclude_cols = ['Subject ID', 'Activity_Label']

# Select numerical columns excluding the specified columns
import numpy as np

numerical_cols = data.select_dtypes(include=['number']).columns.tolist()
numerical_cols = [col for col in numerical_cols if col not in exclude_cols]

# Set the style for seaborn
sns.set(style="whitegrid")

# Plot Histograms
sns.set(style="whitegrid")

plt.figure(figsize=(15, 10))
for idx, col in enumerate(numerical_cols):
    plt.subplot(len(numerical_cols)//3 + 1, 3, idx + 1)
    sns.histplot(data[col].dropna(), kde=True, bins=30, color='skyblue')
    plt.title(f'Histogram of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Plot Boxplots
plt.figure(figsize=(15, 10))
for idx, col in enumerate(numerical_cols):
    plt.subplot(len(numerical_cols)//3 + 1, 3, idx + 1)
    sns.boxplot(y=data[col], color='lightgreen')
    plt.title(f'Boxplot of {col}')
    plt.ylabel(col)
plt.tight_layout()
plt.show()

## Correlation heatmap
plt.figure(figsize=(18, 16))
corr_matrix = data.drop(columns=['Subject ID', 'Activity_Label'], errors='ignore').corr(method='spearman')
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, fmt='.2f')
plt.title('Correlation Matrix Heatmap', fontsize=18)
plt.xticks(fontsize=12, rotation=45, ha='right')
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

# Check for missing values
print("\nMissing Values:")
print(data.isnull().sum())

# Visualizing missing values using missingno
import missingno as msno

# Bar plot to visualize the count of non-missing data for each column
msno.bar(data, color='dodgerblue')
plt.title('Missing Values Bar Plot')
plt.show()

# Matrix plot to visualize the distribution of missing data
msno.matrix(data.drop(columns=['Subject ID', 'Activity_Label'], errors='ignore'), color=(0.3, 0.4, 0.7))
plt.title('Missing Values Matrix Plot')
plt.show()

# Heatmap to visualize correlations between missing values in different columns
plt.figure(figsize=(18, 16))
msno.heatmap(data.drop(columns=['Subject ID', 'Activity_Label'], errors='ignore'), cmap='viridis')
plt.title('Missing Values Correlation Heatmap')
plt.show()

# Plot the number of samples per each activity label
activity_counts = data['Activity_Label'].value_counts()
print("Number of samples per activity label:")
print(activity_counts)

plt.figure(figsize=(10, 6))
sns.countplot(x='Activity_Label', data=data, palette='viridis')
plt.title('Number of Samples per Activity Label')
plt.xlabel('Activity Label')
plt.ylabel('Number of Samples')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

import pandas as pd
import numpy as np
from collections import Counter

# Create a new dataset excluding the Subject ID column
data_clean = data.drop(columns=['Subject ID'])

# Function to compute window features
def compute_window_features(df, window_size=50):
    rms_time_series = []
    svm_accel_leg = []
    svm_gyro_leg = []
    svm_accel_hand = []
    svm_gyro_hand = []
    svm_accel_chest = []
    dsvm_accel_leg = []
    dsvm_gyro_leg = []
    dsvm_accel_hand = []
    dsvm_gyro_hand = []
    dsvm_accel_chest = []
    mean_sample_v = []
    labels = []

    num_windows = int(np.ceil(len(df) / window_size))

    prev_svm_accel_leg = 0
    prev_svm_gyro_leg = 0
    prev_svm_accel_hand = 0
    prev_svm_gyro_hand = 0
    prev_svm_accel_chest = 0

    for i in range(num_windows):
        start = i * window_size
        end = start + window_size
        window = df.iloc[start:end]

        # Compute RMS for time series (Timestamp)
        if 'Timestamp (microseconds)' in window.columns and not window['Timestamp (microseconds)'].empty:
            rms = np.sqrt(np.mean(np.square(window['Timestamp (microseconds)'])))
        else:
            rms = np.nan
        rms_time_series.append(rms)

        # Compute Signal Vector Magnitude (SVM) for accelerometer on leg
        leg_accel_cols = ['Accel X (g)_leg', 'Accel Y (g)_leg', 'Accel Z (g)_leg']
        if all(col in window.columns for col in leg_accel_cols) and not window[leg_accel_cols].empty:
            accel_svm_leg = np.sqrt(
                window['Accel X (g)_leg']**2 +
                window['Accel Y (g)_leg']**2 +
                window['Accel Z (g)_leg']**2
            )
            avg_accel_svm_leg = accel_svm_leg.mean()
        else:
            avg_accel_svm_leg = np.nan
        svm_accel_leg.append(avg_accel_svm_leg)
        dsvm_accel_leg.append(avg_accel_svm_leg - prev_svm_accel_leg)
        prev_svm_accel_leg = avg_accel_svm_leg

        # Compute Signal Vector Magnitude (SVM) for gyroscope on leg
        leg_gyro_cols = ['Gyro X (°/s)_leg', 'Gyro Y (°/s)_leg', 'Gyro Z (°/s)_leg']
        if all(col in window.columns for col in leg_gyro_cols) and not window[leg_gyro_cols].empty:
            gyro_svm_leg = np.sqrt(
                window['Gyro X (°/s)_leg']**2 +
                window['Gyro Y (°/s)_leg']**2 +
                window['Gyro Z (°/s)_leg']**2
            )
            avg_gyro_svm_leg = gyro_svm_leg.mean()
        else:
            avg_gyro_svm_leg = np.nan
        svm_gyro_leg.append(avg_gyro_svm_leg)
        dsvm_gyro_leg.append(avg_gyro_svm_leg - prev_svm_gyro_leg)
        prev_svm_gyro_leg = avg_gyro_svm_leg

        # Compute Signal Vector Magnitude (SVM) for accelerometer on hand
        hand_accel_cols = ['Accel X (g)_hand', 'Accel Y (g)_hand', 'Accel Z (g)_hand']
        if all(col in window.columns for col in hand_accel_cols) and not window[hand_accel_cols].empty:
            accel_svm_hand = np.sqrt(
                window['Accel X (g)_hand']**2 +
                window['Accel Y (g)_hand']**2 +
                window['Accel Z (g)_hand']**2
            )
            avg_accel_svm_hand = accel_svm_hand.mean()
        else:
            avg_accel_svm_hand = np.nan
        svm_accel_hand.append(avg_accel_svm_hand)
        dsvm_accel_hand.append(avg_accel_svm_hand - prev_svm_accel_hand)
        prev_svm_accel_hand = avg_accel_svm_hand

        # Compute Signal Vector Magnitude (SVM) for gyroscope on hand
        hand_gyro_cols = ['Gyro X (°/s)_hand', 'Gyro Y (°/s)_hand', 'Gyro Z (°/s)_hand']
        if all(col in window.columns for col in hand_gyro_cols) and not window[hand_gyro_cols].empty:
            gyro_svm_hand = np.sqrt(
                window['Gyro X (°/s)_hand']**2 +
                window['Gyro Y (°/s)_hand']**2 +
                window['Gyro Z (°/s)_hand']**2
            )
            avg_gyro_svm_hand = gyro_svm_hand.mean()
        else:
            avg_gyro_svm_hand = np.nan
        svm_gyro_hand.append(avg_gyro_svm_hand)
        dsvm_gyro_hand.append(avg_gyro_svm_hand - prev_svm_gyro_hand)
        prev_svm_gyro_hand = avg_gyro_svm_hand

        # Compute Signal Vector Magnitude (SVM) for accelerometer on chest
        chest_accel_cols = ['Accel X (g)_chest', 'Accel Y (g)_chest', 'Accel Z (g)_chest']
        if all(col in window.columns for col in chest_accel_cols) and not window[chest_accel_cols].empty:
            accel_svm_chest = np.sqrt(
                window['Accel X (g)_chest']**2 +
                window['Accel Y (g)_chest']**2 +
                window['Accel Z (g)_chest']**2
            )
            avg_accel_svm_chest = accel_svm_chest.mean()
        else:
            avg_accel_svm_chest = np.nan
        svm_accel_chest.append(avg_accel_svm_chest)
        dsvm_accel_chest.append(avg_accel_svm_chest - prev_svm_accel_chest)
        prev_svm_accel_chest = avg_accel_svm_chest

        # Compute mean for Sample (V) column
        if 'Sample (V)' in window.columns and not window['Sample (V)'].empty:
            mean_v = window['Sample (V)'].mean()
        else:
            mean_v = np.nan
        mean_sample_v.append(mean_v)

        # Assign the most frequent label in the window
        if 'Activity_Label' in window.columns and not window['Activity_Label'].empty:
            most_common_label = Counter(window['Activity_Label']).most_common(1)[0][0]
        else:
            most_common_label = np.nan
        labels.append(most_common_label)

    # Create a new DataFrame with the computed features
    features_df = pd.DataFrame({
        'rms_time_series': rms_time_series,
        'svm_accel_leg': svm_accel_leg,
        'svm_gyro_leg': svm_gyro_leg,
        'svm_accel_hand': svm_accel_hand,
        'svm_gyro_hand': svm_gyro_hand,
        'svm_accel_chest': svm_accel_chest,
        'dsvm_accel_leg': dsvm_accel_leg,
        'dsvm_gyro_leg': dsvm_gyro_leg,
        'dsvm_accel_hand': dsvm_accel_hand,
        'dsvm_gyro_hand': dsvm_gyro_hand,
        'dsvm_accel_chest': dsvm_accel_chest,
        'mean_sample_v': mean_sample_v,
        'label': labels
    })

    return features_df

# Compute the windowed features
windowed_features = compute_window_features(data_clean, window_size=50)

# Display the first few rows of the computed features
print(windowed_features.head())

# Export the windowed features to a CSV file
windowed_features.to_csv('windowed_features.csv', index=False)

# Standardize the data using StandardScaler
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
features_to_scale = windowed_features.drop(columns=['label'])
scaled_features = scaler.fit_transform(features_to_scale)
scaled_data = pd.DataFrame(scaled_features, columns=features_to_scale.columns)
scaled_data['label'] = windowed_features['label'].values

# Display the first few rows of the scaled data
print(scaled_data.head())

# Apply PCA on the scaled data
from sklearn.decomposition import PCA

scaled_columns = scaled_data.drop(columns=['label'])
pca = PCA()
pca.fit(scaled_columns)
cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
n_components = np.argmax(cumulative_variance >= 0.90) + 1
pca = PCA(n_components=n_components)
reduced_features = pca.fit_transform(scaled_columns)
print(f'PCA completed with {n_components} components.')

# Plotting the scree plot for PCA
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o', linestyle='--')
plt.axhline(y=0.90, color='r', linestyle='-')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('Scree Plot')
plt.grid()
plt.show()