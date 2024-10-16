# Predicting NFL Pass Plays Before the Ball Drops

## NFL Big Data Bowl 2025 Submission

This project is a submission for the NFL Big Data Bowl 2025, focusing on leveraging pre-snap data to predict pass plays in NFL games.

### Project Overview

In the fast-paced world of NFL football, the ability to predict an opponent's play before the snap can be a game-changer. This project dives deep into the pre-snap data provided by the NFL's Next Gen Stats, aiming to uncover patterns and insights that can predict whether a play will be a pass or a run.

### Key Features

- **Data Analysis**: Comprehensive analysis of NFL tracking data, including player positions, formations, and game situations.
- **Machine Learning**: Implementation of a Random Forest model to predict pass plays with 79% accuracy.
- **Feature Engineering**: Creation of novel features from pre-snap data to enhance predictive power.
- **Visualization**: Insightful visualizations of feature importances and model performance.

### Methodology

1. **Data Preprocessing**: Cleaned and merged various datasets including game, play, player, and tracking data.
2. **Feature Engineering**: Created new features such as time remaining and score differential.
3. **Model Development**: Trained a Random Forest classifier on pre-snap features.
4. **Evaluation**: Assessed model performance using accuracy, precision, recall, and F1-score metrics.

### Key Findings

- Offensive formation is the most crucial factor in predicting pass plays.
- Time remaining and game situation (down, distance, score) significantly influence play-calling.
- Certain pre-snap movements and alignments are strong indicators of pass plays.

### Future Work

- Explore more advanced machine learning techniques like deep learning for improved accuracy.
- Incorporate player-specific statistics for more nuanced predictions.
- Develop a real-time prediction system for in-game use.

### Tools Used

- Python
- Pandas for data manipulation
- Scikit-learn for machine learning
- Matplotlib and Seaborn for data visualization

### Acknowledgments

Special thanks to the NFL and Kaggle for providing the data and hosting this competition. This project was completed as part of the NFL Big Data Bowl 2025.
