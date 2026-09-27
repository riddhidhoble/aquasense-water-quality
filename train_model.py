import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# --------------------------------------------------
# 1. Load Dataset
# --------------------------------------------------

base_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(
    base_path,
    "datasets",
    "Water Quality Dataset from Water Sources in Kenya",
    "water_quality_dataset1.csv"
)

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Dataset Shape:", df.shape)


# --------------------------------------------------
# 2. Select Input Features and Target
# --------------------------------------------------

X = df[[
    "pH",
    "TDS_ppm",
    "Turbidity_NTU",
    "Temperature_C"
]]

y = df["Label"]


# --------------------------------------------------
# 3. Convert Safe/Unsafe into Numbers
# --------------------------------------------------

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

print("\nClasses:")
print(label_encoder.classes_)


# --------------------------------------------------
# 4. Split Dataset into Training and Testing Data
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# --------------------------------------------------
# 5. Create Random Forest Model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)


# --------------------------------------------------
# 6. Train the Model
# --------------------------------------------------

model.fit(X_train, y_train)

print("\nModel training completed!")


# --------------------------------------------------
# 7. Make Predictions
# --------------------------------------------------

y_pred = model.predict(X_test)


# --------------------------------------------------
# 8. Evaluate the Model
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print(f"{accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
# --------------------------------------------------
# 9. Feature Importance
# --------------------------------------------------

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")
print(feature_importance)
# --------------------------------------------------
# 10. 5-Fold Cross-Validation
# --------------------------------------------------

cv_scores = cross_val_score(
    model,
    X_train,
    y_train,
    cv=5,
    scoring="accuracy"
)

print("\n5-Fold Cross-Validation Accuracy:")
print(cv_scores)

print(f"Mean CV Accuracy: {cv_scores.mean() * 100:.2f}%")
print(f"Standard Deviation: {cv_scores.std() * 100:.2f}%")
# --------------------------------------------------
# 11. Test Model with a New Water Sample
# --------------------------------------------------

new_sample = pd.DataFrame({
    "pH": [7.2],
    "TDS_ppm": [150],
    "Turbidity_NTU": [1.5],
    "Temperature_C": [24.0]
})

prediction = model.predict(new_sample)

predicted_label = label_encoder.inverse_transform(prediction)

print("\nNew Water Sample:")
print(new_sample)

print("\nPredicted Water Quality:")
print(predicted_label[0])
# --------------------------------------------------
# 12. Save Trained Model
# --------------------------------------------------

model_path = os.path.join(
    base_path,
    "models",
    "water_quality_model.pkl"
)

encoder_path = os.path.join(
    base_path,
    "models",
    "label_encoder.pkl"
)

joblib.dump(model, model_path)
joblib.dump(label_encoder, encoder_path)

print("\nModel saved successfully!")
print("Model path:", model_path)

print("\nLabel encoder saved successfully!")
print("Encoder path:", encoder_path)