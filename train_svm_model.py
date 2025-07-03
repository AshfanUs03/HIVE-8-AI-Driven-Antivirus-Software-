import os
import random
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from joblib import dump

def simulate_features_from_hash(hash_val, label_type):
    hash_int = int(hash_val[:8], 16)
    random.seed(hash_int)

    size = random.randint(1000, 10000000) 
    entropy = random.uniform(3.0, 8.0)

    if label_type == 1:
        file_type = random.choice([1, 2])  
    else:
        file_type = random.choice([1, 2, 3, 4, 5, 6])  

    return [size, entropy, file_type]

def load_hashes(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

virus_hashes = load_hashes("virus_hashes.txt")
legit_hashes = load_hashes("legit_hashes.txt")

print(f"Virus hashes loaded: {len(virus_hashes)}")
print(f"Legit hashes loaded: {len(legit_hashes)}")

features = []
labels = []

for hash_val in virus_hashes:
    features.append(simulate_features_from_hash(hash_val, label_type=1))
    labels.append(1)

for hash_val in legit_hashes:
    features.append(simulate_features_from_hash(hash_val, label_type=0))
    labels.append(0)

X = np.array(features)
y = np.array(labels)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = svm.SVC(kernel="rbf", C=1.0, gamma='scale')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\nModel Evaluation:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

try:
    dump(model, "svm_model.pkl")
    print("\n✅ Model saved as 'svm_model.pkl'")
except Exception as e:
    print(f"Error saving model: {e}")
