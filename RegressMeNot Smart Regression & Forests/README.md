# RegressMeNot: Smart Regression & Forests

"RegressMeNot: Smart Regression & Forests" is an R package developed as part of a project submission for the Statistical Learning course at Stony Brook University for the MS in Data Science program. This package provides a comprehensive suite of tools for conducting various types of regression analyses and random forest methods. It simplifies the process of model fitting and tuning by automating the selection of critical parameters like lambda and alpha and supports advanced techniques such as bagging to enhance prediction accuracy and model robustness.

## Project Overview

This package was created to offer data scientists and statisticians a robust toolset for predictive modeling. It includes functionalities for logistic regression, linear regression, lasso, ridge, and elastic net methods, along with an implementation of random forest that incorporates optional bagging. Whether you're conducting academic research or working on industry data science projects, "RegressMeNot" provides the necessary tools to produce high-quality predictive models efficiently.

## Features

- **Regression Methods:** Supports logistic, linear, lasso, ridge, and elastic net regression.
- **Random Forest:** Offers an implementation with optional bagging for enhanced prediction accuracy and stability.
- **Automatic Parameter Tuning:** Utilizes cross-validation to automatically detect optimal values for lambda and alpha.
- **Documentation and Vignettes:** Includes comprehensive guides and practical examples to facilitate understanding and application.
- **Top k Predictors:** Features functionality to identify and return the top k predictors for focused model refinement.
- **Bagging Option:** Employs bagging techniques to improve model accuracy and generalization.

## Installation

Install "RegressMeNot" directly from GitHub using the `devtools` package:

```r
# Install using devtools
devtools::install_github("your_github_username/RegressMeNot")
```
## Tools and Frameworks Used

The development of this package incorporated the following tools and frameworks:

- **R Markdown:** For creating dynamic documentation and vignettes.
- **Roxygen2:** Used to generate Rd files from annotations in the R scripts, facilitating documentation maintenance.
- **RStudio:** The primary development environment, enhancing code writing, testing, and package management.
- **glmnet:** For fitting generalized linear and elastic-net regularized models.
- **randomForest:** For constructing random forest models.
- **cv.glmnet:** For cross-validation of glmnet models to optimize parameters.

## Conclusion

"RegressMeNot: Smart Regression & Forests" is crafted to streamline statistical modeling processes and enhance predictive analytics capabilities. Reflecting the rigorous academic standards of the MS in Data Science program at Stony Brook University, it incorporates cutting-edge statistical learning techniques. This package is not only a robust tool for researchers and analysts but also serves as a testament to the practical application of statistical theory in solving real-world problems.
