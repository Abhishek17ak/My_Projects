# Quick Start Guide

This guide will help you quickly get started with the Customer Segmentation project.

## Setup Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Abhishek17ak/Advanced_Customer_Segmentation_Analysis.git
   cd Advanced_Customer_Segmentation_Analysis
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   # Using venv
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Analysis

### Option 1: Standalone Python Files

For basic RFM analysis and K-means clustering:
```bash
python customer_segmentation.py
```

For advanced techniques (Dynamic Segmentation and Hierarchical Clustering):
```bash
python advanced_segmentation.py
```

### Option 2: Using Jupyter Notebook

1. Start Jupyter:
   ```bash
   jupyter notebook
   ```

2. Create a new notebook

3. Import the code:
   ```python
   # Run this in a Jupyter notebook cell
   %load customer_segmentation_notebook.py
   ```
   
   Alternatively, you can copy sections from `customer_segmentation_notebook.py` into notebook cells.

## Example Workflow

1. **Data Exploration**:
   ```python
   # Load the dataset
   df = pd.read_excel('data/Online Retail.xlsx')
   
   # Display the first few rows
   print(df.head())
   
   # Check for missing values
   print(df.isnull().sum())
   ```

2. **Data Cleaning**:
   ```python
   # Remove rows with missing CustomerID
   df_cleaned = df.dropna(subset=['CustomerID'])
   
   # Convert CustomerID to integer type
   df_cleaned['CustomerID'] = df_cleaned['CustomerID'].astype(int)
   
   # Convert InvoiceDate to datetime
   df_cleaned['InvoiceDate'] = pd.to_datetime(df_cleaned['InvoiceDate'])
   
   # Calculate TotalPrice
   df_cleaned['TotalPrice'] = df_cleaned['Quantity'] * df_cleaned['UnitPrice']
   
   # Remove negative quantities and prices
   df_cleaned = df_cleaned[(df_cleaned['Quantity'] > 0) & (df_cleaned['UnitPrice'] > 0)]
   ```

3. **RFM Analysis**:
   ```python
   # Calculate Recency, Frequency, and Monetary values
   reference_date = df_cleaned['InvoiceDate'].max() + dt.timedelta(days=1)
   
   # Group by CustomerID and calculate RFM metrics
   rfm = df_cleaned.groupby('CustomerID').agg({
       'InvoiceDate': lambda x: (reference_date - x.max()).days,  # Recency
       'InvoiceNo': 'nunique',  # Frequency
       'TotalPrice': 'sum'  # Monetary
   })
   
   # Rename columns
   rfm.columns = ['Recency', 'Frequency', 'Monetary']
   ```

4. **K-means Clustering**:
   ```python
   # Scale the RFM data
   scaler = StandardScaler()
   rfm_scaled = scaler.fit_transform(rfm)
   
   # Apply K-Means
   kmeans = KMeans(n_clusters=4, random_state=42)
   rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
   
   # Calculate average RFM values for each cluster
   cluster_avg = rfm.groupby('Cluster').mean().reset_index()
   print("\nCluster Profiles:")
   print(cluster_avg)
   ```

5. **Dynamic Segmentation**:
   ```python
   from advanced_segmentation import create_dynamic_segments, simulate_dynamic_segmentation, analyze_dynamic_segments
   
   # Simulate dynamic segmentation over time
   segment_history = simulate_dynamic_segmentation(rfm)
   
   # Analyze segment transitions
   analyze_dynamic_segments(segment_history)
   ```

6. **Hierarchical Clustering**:
   ```python
   from advanced_segmentation import perform_hierarchical_clustering, visualize_hierarchical_clusters
   
   # Perform hierarchical clustering
   rfm_with_clusters, cluster_profiles = perform_hierarchical_clustering(rfm)
   
   # Visualize clusters
   visualize_hierarchical_clusters(rfm_with_clusters)
   ```

## Next Steps

1. Explore the output visualizations to understand customer segments
2. Refine segmentation parameters based on your specific business needs
3. Develop targeted marketing strategies for each customer segment
4. Check the main README.md for more detailed information about the project

## Troubleshooting

- **Missing dependencies**: Make sure you've installed all required packages using `pip install -r requirements.txt`
- **File not found errors**: Ensure paths are correct for your local environment
- **Memory errors**: For large datasets, consider downsampling or using a machine with more RAM 
