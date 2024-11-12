# -*- coding: utf-8 -*-
"""ML_Ops_Major.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aV8H2pacO829kmxICcQ0Xy9keBbERWBS

###Question 1
"""

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class IrisDataProcessor:
    def __init__(self):
        # Loading Iris dataset
        self.data = load_iris()
        self.df = None
        self.scaler = StandardScaler()

    def prepare_data(self):
        # Converting to DataFrame
        self.df = pd.DataFrame(self.data.data, columns=self.data.feature_names)
        self.df['target'] = self.data.target

        # Feature scaling
        features = self.df[self.data.feature_names]
        scaled_features = self.scaler.fit_transform(features)
        self.df[self.data.feature_names] = scaled_features

        # Train-test split
        X = self.df[self.data.feature_names]
        y = self.df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def get_feature_stats(self):
        # Return basic statistical analysis
        return self.df.describe()

processor = IrisDataProcessor()
X_train, X_test, y_train, y_test = processor.prepare_data()
print(processor.get_feature_stats())

"""### Question 2"""

# !pip install mlflow

import mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import cross_val_score

class IrisExperiment:
    def __init__(self, data_processor):
        self.X_train, self.X_test, self.y_train, self.y_test = data_processor.prepare_data()

    def run_experiment(self):
        # Define models
        models = {
            "Logistic Regression": LogisticRegression(),
            "Random Forest": RandomForestClassifier()
        }

        # Track experiments
        for model_name, model in models.items():
            with mlflow.start_run(run_name=model_name):
                model.fit(self.X_train, self.y_train)
                predictions = model.predict(self.X_test)

                # Evaluate metrics
                accuracy = accuracy_score(self.y_test, predictions)
                precision = precision_score(self.y_test, predictions, average='weighted')
                recall = recall_score(self.y_test, predictions, average='weighted')

                # Log metrics
                mlflow.log_param("Model", model_name)
                mlflow.log_metric("Accuracy", accuracy)
                mlflow.log_metric("Precision", precision)
                mlflow.log_metric("Recall", recall)

                # Log model
                mlflow.sklearn.log_model(model, model_name)

    def log_results(self):
        print("Experiments logged to MLflow")

# Example usage:
experiment = IrisExperiment(processor)
experiment.run_experiment()

"""### Question 3"""

from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np

class IrisModelOptimizer:
    def __init__(self, experiment):
        self.model = LogisticRegression()
        self.X_train, self.X_test, self.y_train, self.y_test = experiment.X_train, experiment.X_test, experiment.y_train, experiment.y_test

    def quantize_model(self):
        # Fit and quantize model
        self.model.fit(self.X_train, self.y_train)
        joblib.dump(self.model, "logistic_regression_model.joblib")
        print("Model quantized and saved.")

    def run_tests(self):
        # Load model and run tests
        model = joblib.load("logistic_regression_model.joblib")
        assert model is not None, "Model not loaded correctly."
        assert len(np.unique(model.predict(self.X_test))) > 1, "Model predictions are invalid."
        print("All tests passed.")

# Example usage:
optimizer = IrisModelOptimizer(experiment)
optimizer.quantize_model()
optimizer.run_tests()

def main():
    processor = IrisDataProcessor()
    experiment = IrisExperiment(processor)
    experiment.run_experiment()
    optimizer = IrisModelOptimizer(experiment)
    optimizer.quantize_model()
    optimizer.run_tests()

if __name__ == "__main__":
    main()

