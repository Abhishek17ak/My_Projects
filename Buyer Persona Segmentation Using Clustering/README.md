# Buyer Persona Segmentation Using Clustering

## Overview
This project analyzes customer data from a direct marketing campaign to design actionable buyer personas using advanced feature engineering, K-Means, and DBSCAN clustering algorithms. Data cleaning, feature transformation, and unsupervised learning techniques reveal key consumer segments for targeted marketing strategies and campaign planning.

## Dataset
- Source: `marketing_campaign.csv` on Kaggle
- Contains demographics, spending, purchase habits, family structure, and engagement data from 2,213 anonymized customers.

## Methodology

### Data Cleaning & Preprocessing:
- Removed rows with missing income/outlier ages
- Engineered features:
  - Age
  - Family_Size
  - Total_Spending
  - Avg_Transaction_Value
  - Tenure metrics
  - Encoded demographics
- Feature Scaling: Used z-score standardization for clustering

### Clustering Algorithms:
- K-Means (optimal K selected via elbow and silhouette scores)
- DBSCAN (density-based, with epsilon chosen by k-NN method)

### Evaluation:
- Silhouette and Davies-Bouldin metrics for cluster cohesion and separation
- Cluster profiles to inform marketing segments

## Results

### K-Means Segmentation:
Three distinct personas:
- High-income loyal spenders
- Value-oriented families
- Younger moderate buyers

### DBSCAN Discovery:
- Similar core groups
- Additional outlier/noise segment for edge-case customers

### Cluster Quality:
- Moderate silhouette scores (~0.14–0.25), typical for complex human data

### Outputs:
- Customer segment assignments exported for direct CRM/marketing use (`customer_segments.csv`)

## How to Run

1. Clone the repo and download the dataset from Kaggle.

2. Install requirements:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

3. Place `marketing_campaign.csv` in the root folder.

4. Run the analysis notebook (`.ipynb`) or script step-by-step.

5. Outputs include visuals, segment profiles, and a CSV of cluster assignments.

## Project Structure
- `buyer_persona.ipynb` – step-by-step notebook
- `customer_segments.csv` – segment assignments (for targeting)
- Plots/visuals PNGs for reporting

## Results Summary
This clustering workflow cleanly segments customers into actionable groups for targeted marketing, with interpretable insights and portfolios-ready visuals. Outlier groups can be flagged for special campaigns or further research.

## License
This project and code are released under the MIT License. Please check dataset license/citation requirements before public or commercial use.

## Acknowledgments
- Data Source: Kaggle – Customer Personality Analysis
- Clustering code inspired by scikit-learn documentation
