# 💼 **Job Salary Predictor using DistilRoBERTa**

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Transformers](https://img.shields.io/badge/Transformers-4.30%2B-FFD21E?style=for-the-badge&logo=huggingface&logoColor=white)
![DistilRoBERTa](https://img.shields.io/badge/DistilRoBERTa-82M_Params-4B8BBE?style=for-the-badge&logo=huggingface&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-3776AB?style=for-the-badge&logo=seaborn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![CUDA](https://img.shields.io/badge/CUDA-GPU_Accelerated-76B900?style=for-the-badge&logo=nvidia&logoColor=white)

</div>

---

## 🎯 **Project Overview**

A **Job Salary Prediction System** that leverages **DistilRoBERTa** (a faster variant of RoBERTa) to predict salary ranges from job postings. The model analyzes job titles, company information, locations, descriptions, skills, and experience requirements to estimate accurate salary categories with **81.13% accuracy**.

### 🚀 **Key Features**

| Feature | Description |
|---------|-------------|
| **🧠 Transformer Model** | Uses DistilRoBERTa (82M params) for deep text understanding |
| **⚡ 8-10x Faster Training** | Optimized with FP16, batch size 32, 2 epochs |
| **📊 7 Salary Categories** | From 50-65k to 200k+ |
| **🔍 Rich Text Features** | Combines title, company, location, skills, experience |
| **📈 81.13% Accuracy** | Excellent performance on salary prediction |
| **🚀 GPU Acceleration** | Tesla T4 GPU training in just ~15 minutes |
| **💾 Model Export** | Full model saved and ready for deployment |

---

## 📊 **Model Performance Summary**

| Metric | Value | Description |
|--------|-------|-------------|
| **Accuracy** | **81.13%** | Overall correct predictions |
| **F1 Macro** | 0.7514 | Average F1 across all classes |
| **F1 Weighted** | 0.8056 | F1 weighted by class support |
| **Precision** | 0.8445 | Quality of predictions |
| **Recall** | 0.8113 | Coverage of predictions |
| **R² Score** | 0.9529 | Variance explained in salary prediction |
| **MAE** | $4,867.66 | Mean absolute error in salary |
| **Training Time** | 2.74 minutes | Fast training on GPU |
| **Model Size** | 82M parameters | DistilRoBERTa (2x faster than RoBERTa) |

---

## 🏆 **Model Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    🏆 BEST MODEL: DistilRoBERTa               │
├─────────────────────────────────────────────────────────────────┤
│  • Model Size:         82M parameters                         │
│  • Architecture:       6-layer Transformer (DistilRoBERTa)   │
│  • Vocabulary Size:    50,265                                 │
│  • Max Sequence:       128 tokens (optimized for speed)      │
│  • Training Epochs:    2 (fast convergence)                  │
│  • Batch Size:         32 (4x speed improvement)             │
│  • Learning Rate:      3e-5                                  │
│  • Optimization:       FP16 mixed precision                  │
│  • Accuracy:           81.13%                                │
├─────────────────────────────────────────────────────────────────┤
│  Why DistilRoBERTa: 2x faster than RoBERTa with minimal     │
│  accuracy loss. Optimized for production deployment with     │
│  82M parameters vs RoBERTa's 124M.                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 **End-to-End Pipeline**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           📊 DATA PIPELINE                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  📰 Job Dataset ──▶ 🔍 Feature Engineering ──▶ 📊 EDA & Visualization          │
│  (4,345 jobs)        (Skills, Industry,           (Salary distribution,        │
│                       Experience, Education)       Skills count, Remote vs On-site)
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🤖 FEATURE ENGINEERING                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   📝 Text Features ──▶ 🔗 Rich Text Creation ──▶ 🏷️ Salary Categories         │
│   (Title, Company,        (Combined features        (7 categories:             │
│    Location, Skills,       for transformer)          50-65k to 200k+)          │
│    Description, etc.)                                                          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🧠 DISTILROBERTA TRAINING                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ⚡ Data Split (80/20) ──▶ 🔄 Tokenization ──▶ 🚀 Training (2 epochs)        │
│   3,476/869 samples          (max_length=128)       (FP16, batch=32)           │
│                                                                                 │
│   ⬇                                                                             │
│   📊 Evaluation ──▶ 🎯 81.13% Accuracy ──▶ 💾 Model Export                    │
│   (Precision, Recall, F1)                                                      │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🚀 DEPLOYMENT                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   💾 Saved: DistilRoBERTa model, Tokenizer, Label Encoder                     │
│   📊 Generated: Confusion Matrix, Prediction Results, Metrics                  │
│   🎯 Prediction Function: `predict_salary(title, description, company, location)`│
│   📦 Package: ZIP archive ready for deployment                                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 **Feature Engineering**

### **Features Extracted from Job Postings**

| Feature | Description | Method |
|---------|-------------|--------|
| **Skills** | Technical skills extracted | Keyword matching from description |
| **Skills Count** | Number of skills identified | Count extracted skills |
| **Industry** | Industry classification | Keyword matching (Tech, Finance, Healthcare, etc.) |
| **Years Experience** | Required experience | Regex pattern extraction |
| **Education** | Required education level | Keyword matching (PhD, Master, Bachelor, etc.) |
| **Is Remote** | Remote work indicator | Location text analysis |
| **Description Length** | Length of job description | Character count |
| **Company Popularity** | Company frequency | Group by company |

### **Rich Text Creation**
Combines all features into a single text input for the transformer:
```
Title: Senior Machine Learning Engineer | Company: Google | Location: Remote | 
Industry: tech | Experience: 5 years | Education: master | Skills: python, tensorflow, aws | 
Remote: Yes | Description: We are looking for a Senior ML Engineer...
```

---

## 📊 **Performance Analysis**

### **Confusion Matrix**

<div align="center">
  <img src="confusion_matrix.png" alt="Confusion Matrix" width="600"/>
</div>

### **Per-Class Performance**

| Salary Category | Precision | Recall | F1-Score | Support |
|-----------------|-----------|--------|----------|---------|
| **100-120k** | 1.000 | 1.000 | 1.000 | 167 |
| **120-150k** | 0.522 | 1.000 | 0.686 | 71 |
| **150-200k** | 1.000 | 0.689 | 0.816 | 209 |
| **200k+** | 1.000 | 1.000 | 1.000 | 143 |
| **50-65k** | 0.717 | 1.000 | 0.835 | 104 |
| **65-80k** | 0.542 | 0.537 | 0.540 | 108 |
| **80-100k** | 0.667 | 0.269 | 0.383 | 67 |

### **Key Insights**

| Observation | Insight |
|-------------|---------|
| **100-120k & 200k+ perfect** | Model excels at high and medium-high categories |
| **80-100k lower performance** | Limited samples (67) and overlapping features |
| **120-150k recall 100%** | Model captures all instances but with lower precision |
| **81% overall accuracy** | Strong performance for salary prediction task |

---

## ⚡ **Speed Optimizations**

| Optimization | Before | After | Improvement |
|--------------|--------|-------|-------------|
| **Model** | RoBERTa (124M) | DistilRoBERTa (82M) | 2x faster |
| **Batch Size** | 8 | 32 | 4x faster |
| **Epochs** | 3 | 2 | 33% faster |
| **Max Length** | 256 | 128 | 2x faster |
| **FP16** | Off | On | 2x faster |
| **Total Speed** | - | - | **~8-10x faster** |

**Training Time:** ~2.74 minutes on Tesla T4 GPU 🚀

---

## 🛠️ **Tech Stack**

### **Core Libraries**

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.10+ |
| **Deep Learning** | PyTorch 2.0+, Transformers 4.30+ |
| **Transformer** | DistilRoBERTa (82M params) |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **ML Tools** | Scikit-Learn 1.3+ |
| **GPU Acceleration** | CUDA, FP16 mixed precision |

### **Key Dependencies**

```bash
pip install -q transformers torch sentence-transformers datasets accelerate
pip install -q pandas numpy matplotlib seaborn scikit-learn
```

---

## 📁 **Project Structure**

```
job_salary_predictor/
├── 📄 README.md                                    # Project documentation
├── 📄 Job_Salary_Predictor.ipynb                   # Main notebook
├── 📊 data_distribution.png                        # EDA visualizations
├── 📊 confusion_matrix.png                         # Confusion matrix
├── 📊 prediction_results.png                       # Prediction results
├── 📦 distilroberta_model.zip                      # Complete model package (291MB)
├── 📁 distilroberta_job_model/                    # Trained model files
│   ├── model.safetensors                           # Model weights (82M params)
│   ├── config.json                                 # Model configuration
│   ├── tokenizer.json                              # Tokenizer files
│   └── tokenizer_config.json                       # Tokenizer config
├── 📄 label_encoder.pkl                            # Label encoder
├── 📄 model_metadata.json                          # Model metadata
├── 📄 metrics.json                                 # Performance metrics
└── 📄 predict_salary.py                           # Prediction function
```

---

## 🎯 **Getting Started**

### **1. Clone the Repository**
```bash
git clone https://github.com/BROWNBOY047/LMXG-1.4-_-Muhammad_Umer/Job_Salary_Predictor_using_RoBERTa.git
cd LMXG-1.4-_-Muhammad_Umer
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Open in Google Colab**
- Upload the notebook (`Job_Salary_Predictor.ipynb`)
- Upload your job dataset (CSV format)
- Run cells top to bottom

### **4. Dataset Format**

| Column | Type | Description |
|--------|------|-------------|
| `title` | String | **Required** — Job title |
| `company` | String | **Required** — Company name |
| `location` | String | **Required** — Job location |
| `description` | String | **Required** — Job description |
| `salary_min` | Float | **Required** — Minimum salary (for labels) |
| `salary_max` | Float | Optional — Maximum salary |
| `url` | String | Optional — Job URL |
| `source` | String | Optional — Data source |
| `posted_date` | Date | Optional — Posting date |
| `job_id` | String | Optional — Unique ID |
| `experience_level` | String | Optional — Experience level |
| `skills` | List | Optional — Skills list |

### **5. Expected Outputs**
- ✅ **Trained DistilRoBERTa model** (81.13% accuracy)
- ✅ **Salary prediction function** for new jobs
- ✅ **Model evaluation metrics** and visualizations
- ✅ **Complete model package** (ZIP archive)
- ✅ **Deployment-ready prediction script**

---

## 💻 **Usage Example**

### **Predict Salary for New Jobs**

```python
from predict_salary import predict_salary

# Example job
title = "Senior Machine Learning Engineer"
company = "Google"
location = "Remote"
description = "We are looking for a Senior ML Engineer with 5+ years experience in Python, PyTorch, TensorFlow, and AWS. Strong background in deep learning and NLP."

# Predict salary
salary, category, confidence = predict_salary(title, description, company, location)

print(f"Predicted Salary: ${salary:,}")
print(f"Category: {category}")
print(f"Confidence: {confidence*100:.2f}%")
```

**Output:**
```
Predicted Salary: $175,000
Category: 150-200k
Confidence: 68.24%
```

---

## 📈 **Training Process**

### **1. Data Preparation**
- Load job dataset (4,345 jobs)
- Clean and preprocess text data
- Extract features (skills, industry, experience, education)
- Create salary categories (7 classes)

### **2. Feature Engineering**
- Extract skills using keyword matching
- Classify industry from description
- Extract years of experience via regex
- Determine education level required
- Create rich text features

### **3. Model Training**
- Split data: 80% train / 20% test
- Tokenize with DistilRoBERTa tokenizer (max_length=128)
- Train with FP16 precision, batch size 32
- 2 epochs, learning rate 3e-5
- Monitor accuracy and F1 metrics

### **4. Evaluation**
- Calculate accuracy, precision, recall, F1
- Generate confusion matrix
- Plot actual vs predicted salaries
- Analyze per-class performance

---

## 🎯 **Real-World Applications**

| Domain | Application |
|--------|-------------|
| **Job Portals** | Automated salary estimation for job postings |
| **HR Tech** | Salary benchmarking and compensation analysis |
| **Recruitment** | Salary transparency for job seekers |
| **Market Research** | Labor market salary trend analysis |
| **Career Planning** | Salary prediction for career path planning |

---

## 📈 **Future Improvements**

| Enhancement | Description |
|-------------|-------------|
| **Fine-Tuning** | More epochs with early stopping |
| **Data Augmentation** | Add more job postings for better generalization |
| **Multi-Lingual Support** | Support non-English job descriptions |
| **Ensemble Models** | Combine with XGBoost/ensemble methods |
| **Explainable AI** | SHAP/LIME for feature importance |
| **Web API** | Deploy as REST API endpoint |
| **Real-Time Prediction** | Streamlit/Gradio web interface |
| **Active Learning** | Human feedback loop for improvement |

---

## 🤝 **Contributing**

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch
3. **Commit** your changes
4. **Push** to your branch
5. **Open** a Pull Request

---

## 📄 **License**

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🎓 **Citation**

If you use this work in your research, please cite:

```bibtex
@misc{job-salary-predictor-2026,
  author = {Muhammad Umer},
  title = {Job Salary Predictor using DistilRoBERTa},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/BROWNBOY047/LMXG-1.4-_-Muhammad_Umer/Job_Salary_Predictor_using_RoBERTa}}
}
```

---

<div align="center">

## 🌟 **Star Us on GitHub!**

If you found this project useful, please give it a ⭐ star! 

[![GitHub stars](https://img.shields.io/github/stars/BROWNBOY047/LMXG-1.4-_-Muhammad_Umer?style=social)](https://github.com/BROWNBOY047/LMXG-1.4-_-Muhammad_Umer)

---

</div>

---

## 📧 **Contact & Support**

| Platform | Link |
|----------|------|
| 📧 Email | [iamumer34@gmail.com](mailto:iamumer34@gmail.com) |
| 🔗 GitHub | [BROWNBOY047](https://github.com/BROWNBOY047) |


---

<div align="center">

**Made with ❤️ by Muhammad Umer**

</div>
