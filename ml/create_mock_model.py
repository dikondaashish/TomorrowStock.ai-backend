import os
import joblib
import numpy as np
from xgboost import XGBClassifier

# Create directories
os.makedirs('models', exist_ok=True)

# Initialize a simple XGBoost model
model = XGBClassifier(n_estimators=10, max_depth=3, random_state=42)

# Train on random data
n_samples = 100
n_features = 10
X = np.random.randn(n_samples, n_features)
y = np.random.randint(0, 2, n_samples)
feature_names = [f'feature_{i}' for i in range(n_features)]

# Train the model
model.fit(X, y)

# Save the model
joblib.dump(model, 'models/xgb_model.pkl')
print('Mock model saved to models/xgb_model.pkl')

# Save feature names
with open('models/feature_names.txt', 'w') as f:
    f.write('\n'.join(feature_names))
print('Feature names saved to models/feature_names.txt')
