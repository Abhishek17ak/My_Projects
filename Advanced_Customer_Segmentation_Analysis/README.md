# Advanced Customer Segmentation Analysis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0%2B-orange)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/pandas-1.3%2B-brightgreen)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/numpy-1.20%2B-yellow)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/matplotlib-3.5%2B-red)](https://matplotlib.org/)
[![SciPy](https://img.shields.io/badge/scipy-1.7%2B-9cf)](https://scipy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Overview

This project implements advanced customer segmentation techniques using machine learning and data analysis to identify distinct customer groups based on their purchasing behavior. By leveraging RFM (Recency, Frequency, Monetary) analysis and multiple clustering approaches, the project provides actionable insights for targeted marketing strategies.

The analysis combines traditional K-means clustering with more sophisticated techniques like Hierarchical Clustering and Dynamic Segmentation to create a comprehensive customer segmentation framework that can adapt to changing customer behaviors over time.

## Key Features

- **RFM Analysis**: Segments customers based on Recency, Frequency, and Monetary value metrics
- **K-means Clustering**: Identifies optimal customer segments using the Elbow Method and Silhouette Score
- **Dynamic Segmentation**: Tracks how customers move between segments over time
- **Hierarchical Clustering**: Discovers natural customer groupings through dendrogram analysis
- **Interactive Visualizations**: 2D, 3D, and radar chart visualizations of customer segments
- **Segment Comparison**: Analyzes overlap between different segmentation approaches
- **Marketing Recommendations**: Provides actionable insights for each customer segment

## Dataset

The project uses the [Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/Online+Retail) from the UCI Machine Learning Repository, which contains transactions for a UK-based online retailer between 2010-2011. The dataset includes:

- Customer ID
- Invoice information
- Product details
- Quantity and price
- Country information
- Purchase timestamps

## Project Structure

```
customer_seg/
├── data/
│   └── Online Retail.xlsx
├── customer_segmentation_notebook.ipynb  
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation and Usage

1. Clone the repository:
```bash
git clone https://github.com/yourusername/customer_seg.git
cd customer_seg
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the analysis:
   - Open Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
   - Navigate to and open `customer_segmentation_notebook.py`
   - Run all cells to perform the complete analysis

## Analysis Components

### 1. Data Loading and Cleaning
- Loads the Online Retail dataset
- Handles missing values and data type conversions
- Removes canceled orders and invalid entries
- Calculates derived metrics

### 2. RFM Analysis
- Calculates Recency, Frequency, and Monetary metrics
- Visualizes distributions of RFM values
- Identifies key customer characteristics

### 3. K-means Clustering
- Determines optimal number of clusters using Elbow Method
- Applies K-means clustering to RFM data
- Evaluates clustering quality using Silhouette Score
- Visualizes cluster characteristics

### 4. Dynamic Segmentation
- Creates time-based customer segments
- Tracks segment transitions over time
- Visualizes segment evolution
- Identifies at-risk customers

### 5. Hierarchical Clustering
- Performs hierarchical clustering on RFM data
- Visualizes cluster relationships with dendrograms
- Determines optimal cluster number
- Provides 3D visualization of segments

### 6. Segment Comparison
- Compares different segmentation approaches
- Analyzes segment overlap
- Provides comprehensive insights

## Results and Insights

The analysis identifies several distinct customer segments:

1. **High-Value Loyal Customers**: Recent purchasers with high frequency and monetary value
2. **Regular Customers**: Consistent purchasers with moderate monetary value
3. **At-Risk Customers**: Previously active customers showing declining engagement
4. **New Customers**: Recent first-time or infrequent purchasers
5. **Dormant Customers**: Inactive customers who haven't purchased in a long time

Each segment requires different marketing strategies, which are detailed in the analysis.

## Future Improvements

- Implement real-time segmentation with streaming data
- Add predictive modeling to forecast segment transitions
- Integrate customer demographic data for enhanced segmentation
- Develop an interactive dashboard for exploring segments
- Implement A/B testing framework for segment-based marketing strategies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Dataset provided by the UCI Machine Learning Repository
- Inspired by best practices in customer segmentation from industry leaders
- Analysis techniques adapted from recent research in customer analytics 
