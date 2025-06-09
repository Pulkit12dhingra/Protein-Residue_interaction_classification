import numpy as np
import flaml
from flaml.automl import AutoML
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Assuming X_train and y_train are already defined
X_train = np.random.rand(2990, 4, 10, 1)  # Example data
y_train = np.random.randint(0, 2, size=(2990,))  # Binary labels

# Reshape input to 2D (flattening)
X_train = X_train.reshape(2990, -1)  # Shape (2990, 40)

# Split into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

print(X_train.shape, y_train.shape)
print(X_val.shape, y_val.shape)

# Initialize FLAML AutoML
automl = AutoML()

# Define settings
settings = {
    "time_budget": 300,  # Run for 300 seconds
    "task": "classification",
    "metric": "accuracy",
    "log_file_name": "flaml_classification.log",
    "estimator_list":["rf", "xgboost", "catboost"]
}



# Train model
automl.fit(X_train=X_train, y_train=y_train, **settings)

# Predict on validation data
y_pred = automl.predict(X_val)

# Evaluate model
accuracy = accuracy_score(y_val, y_pred)
print(f"Validation Accuracy: {accuracy:.4f}")

# Best model found
print("Best Model:", automl.best_estimator)
