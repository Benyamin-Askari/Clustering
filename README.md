# Time Series Clustering Analysis

This project was originally for the Data Science module to test wether clustering analysis is feasible for time series data from wearable sensors, using techniques like K-means and DBSCAN after dimensionality reduction with PCA.

## Features

- Data preprocessing and feature extraction
- Window-based feature computation
  - RMS time series
  - Signal Vector Magnitude (SVM) for accelerometer and gyroscope data
  - Delta SVM calculations
  - Mean sample voltage
- Dimensionality reduction using PCA (90% variance retention)


## Requirements

```python
pandas
numpy
matplotlib
seaborn
missingno
scikit-learn
```

## Data Processing Pipeline

1. Data loading and initial exploration
2. Window-based feature extraction (window size = 50)
3. Feature standardization using StandardScaler
4. PCA dimensionality reduction

## Visualizations

- Pairwise scatter plot matrix
- Feature histograms and boxplots
- Correlation heatmap
- Missing value analysis
- PCA scree plot
