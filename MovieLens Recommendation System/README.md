# 🎬 MovieLens Recommendation System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-1.3.5-yellow)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20.3-orange)](https://numpy.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0.2-red)](https://scikit-learn.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-green)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A comprehensive movie recommendation system built using collaborative filtering techniques on the MovieLens dataset. This project implements both item-based and SVD-based recommendation methods to provide personalized movie suggestions to users.



## 🌟 Features

- **Multiple recommendation algorithms**:
  - Item-based collaborative filtering
  - SVD-based matrix factorization
- **Interactive recommendation interface**
- **Comprehensive data analysis and visualizations**
- **Model evaluation with RMSE metrics**
- **User and movie similarity analysis**

## 📊 Dataset

This project uses the MovieLens 100K dataset, which contains 100,000+ ratings from 600+ users on 9,000+ movies. The dataset includes:

- `ratings.csv`: User ratings (userId, movieId, rating, timestamp)
- `movies.csv`: Movie information (movieId, title, genres)
- `tags.csv`: User-generated tags for movies
- `links.csv`: Links to movie information on IMDB and TMDB

The dataset was collected by the GroupLens Research Project at the University of Minnesota and is widely used for recommendation system research.

## 🚀 Implementation

### Collaborative Filtering Approaches

1. **Item-Based Collaborative Filtering**
   - Computes similarity between items (movies)
   - Uses cosine similarity metric
   - Recommends movies similar to the ones the user has already liked

2. **SVD-Based Collaborative Filtering**
   - Uses matrix factorization to identify latent factors
   - Decomposes the user-item matrix to discover hidden patterns
   - Projects users and items into the same latent space for comparison

### Evaluation

The recommendation models are evaluated using:
- Root Mean Squared Error (RMSE)
- Train-test split validation (80/20)
- Comparison of predicted vs. actual ratings

## 📊 Exploratory Data Analysis

The project includes extensive exploratory data analysis:

- Rating distribution analysis
- Movie genre distribution
- User activity patterns
- Rating trends over time
- Sparsity analysis of the user-item matrix

## 🛠️ Technology Stack

- **Python**: Core programming language
- **Pandas & NumPy**: Data manipulation and numerical operations
- **scikit-learn**: For matrix factorization and model evaluation
- **Matplotlib & Seaborn**: Data visualization
- **Jupyter Notebook**: Interactive development and presentation

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Required packages: pandas, numpy, matplotlib, seaborn, scikit-learn, scipy

### Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
```

2. Install the required packages
```bash
pip install -r requirements.txt
```

3. Open the Jupyter notebook
```bash
jupyter notebook
```

4. Run the cells in the notebook to:
   - Load and explore the dataset
   - Create the recommendation models
   - Generate personalized recommendations

## 📚 Usage Examples

### Get Movie Recommendations

```python
# Get similar movies
movie_id = 1  # Toy Story
similar_movies = get_similar_movies(movie_id)
print(similar_movies[['title', 'genres', 'similarity']])
```

### Get User-Based Recommendations

```python
# Get recommendations for a user
user_id = 42
recommendations = get_movie_recommendations(user_id)
print(recommendations[['title', 'genres', 'score']])
```

### Get SVD-Based Recommendations

```python
# Get SVD-based recommendations
user_id = 42
svd_recommendations = get_svd_recommendations(user_id)
print(svd_recommendations[['title', 'genres', 'predicted_rating']])
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [GroupLens Research](https://grouplens.org/) for providing the MovieLens dataset
- [Scikit-learn](https://scikit-learn.org/) for machine learning tools
- Everyone who has contributed to the project

---
