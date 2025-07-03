# 🛡️ AI-Driven Antivirus Project

An intelligent antivirus desktop application that uses machine learning to detect malicious files based on file-level characteristics such as entropy, size, and type.

---

## 📌 Features

- 🔍 Scans files in a selected folder
- 🧠 Uses a trained **SVM model** for malware classification
- 🧪 Detects known test files (like the **EICAR test file**)
- 📊 Shows scanning progress and infected files in a user-friendly GUI
- ✅ Simple to use and lightweight, with `.exe` packaging support

---

## 🧠 Machine Learning Details

- Model: **SVM (Support Vector Machine)** with RBF kernel
- Features:
  - File Size
  - File Entropy (measures randomness)
  - Encoded File Type (e.g., .exe, .txt, .jpg → numeric value)
- Trained using simulated file hash data from:
  - `virus_hashes.txt`
  - `legit_hashes.txt`

Model saved as: `svm_model.pkl`

---

## 🖥️ How to Run the Project

### 🔧 Requirements:
- Python 3.x
- `scikit-learn`, `numpy`, `Pillow`, `joblib`, `tkinter`

### ▶️ Steps:
1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
