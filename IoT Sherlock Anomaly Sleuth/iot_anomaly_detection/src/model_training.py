from pyspark.ml.classification import RandomForestClassifier, GBTClassifier, LinearSVC
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

def train_and_evaluate_models(df):
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    models = {
        "Random Forest": RandomForestClassifier(labelCol="is_malicious", featuresCol="features", seed=42),
        "Gradient Boosting": GBTClassifier(labelCol="is_malicious", featuresCol="features", seed=42),
        "SVM": LinearSVC(labelCol="is_malicious", featuresCol="features")
    }

    results = {}

    for name, model in models.items():
        fitted_model = model.fit(train_df)
        predictions = fitted_model.transform(test_df)
        evaluator = MulticlassClassificationEvaluator(labelCol="is_malicious", predictionCol="prediction")
        
        results[name] = {
            "Accuracy": evaluator.evaluate(predictions, {evaluator.metricName: "accuracy"}),
            "Precision": evaluator.evaluate(predictions, {evaluator.metricName: "weightedPrecision"}),
            "Recall": evaluator.evaluate(predictions, {evaluator.metricName: "weightedRecall"}),
            "F1-score": evaluator.evaluate(predictions, {evaluator.metricName: "f1"})
        }

    for model, metrics in results.items():
        print(f"\n{model} Results:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")

    return models["Random Forest"]

def tune_random_forest(df):
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    rf = RandomForestClassifier(labelCol="is_malicious", featuresCol="features")

    paramGrid = ParamGridBuilder() \
        .addGrid(rf.numTrees, [100, 200, 300]) \
        .addGrid(rf.maxDepth, [10, 20, 30]) \
        .addGrid(rf.minInstancesPerNode, [1, 2, 4]) \
        .build()

    crossval = CrossValidator(estimator=rf,
                              estimatorParamMaps=paramGrid,
                              evaluator=MulticlassClassificationEvaluator(labelCol="is_malicious", metricName="accuracy"),
                              numFolds=3)

    cvModel = crossval.fit(train_df)
    best_rf = cvModel.bestModel

    print("Best parameters:")
    print(f"numTrees: {best_rf.getNumTrees}")
    print(f"maxDepth: {best_rf.getMaxDepth}")
    print(f"minInstancesPerNode: {best_rf.getMinInstancesPerNode}")
    print(f"Best cross-validation score: {cvModel.avgMetrics[0]:.4f}")

    return best_rf
