# 📰 **DEEPNEWS - Deep Learning News Title Classification**

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![LSTM](https://img.shields.io/badge/LSTM-Deep_Learning-FF6F00?style=for-the-badge&logo=pytorch&logoColor=white)
![GRU](https://img.shields.io/badge/GRU-RNN_Architecture-4B8BBE?style=for-the-badge&logo=pytorch&logoColor=white)
![BiLSTM](https://img.shields.io/badge/BiLSTM-Bidirectional-9C27B0?style=for-the-badge&logo=pytorch&logoColor=white)
![CNN](https://img.shields.io/badge/TextCNN-CNN_Architecture-E91E63?style=for-the-badge&logo=pytorch&logoColor=white)
![Attention](https://img.shields.io/badge/Attention-Mechanism-00BCD4?style=for-the-badge&logo=pytorch&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-3776AB?style=for-the-badge&logo=seaborn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

</div>

---

## 🎯 **Project Overview**

A **Deep Learning News Title Classification System** that compares five different neural network architectures for categorizing news headlines into 6 distinct categories. The project implements **LSTM, GRU, BiLSTM, TextCNN, and CNN-BiLSTM-Attention** models to identify the most effective architecture for text classification tasks.

### 🚀 **Key Features**

| Feature | Description |
|---------|-------------|
| **🧠 5 Deep Learning Models** | LSTM, GRU, BiLSTM, TextCNN, CNN-BiLSTM-Attention |
| **📊 6 News Categories** | Business, Markets, Politics, Technology, Health, Energy |
| **⚡ Balanced Training** | WeightedRandomSampler for class imbalance handling |
| **🔍 Text Preprocessing** | Custom tokenization with 8,056 vocabulary size |
| **📈 54.07% Test Accuracy** | Best model (TextCNN) performance |
| **🚀 GPU Training** | Optimized with CUDA support |
| **💾 Model Export** | Complete model package ready for deployment |

---

## 📊 **Model Performance Comparison**

| Rank | Model | Val Accuracy | Val Macro F1 | Test Accuracy | Test Macro F1 | Test Weighted F1 |
|:----:|-------|:------------:|:------------:|:-------------:|:-------------:|:----------------:|
| 🥇 | **TextCNN** | **54.00%** | **42.43%** | **54.07%** | **43.38%** | **53.00%** |
| 🥈 | CNN-BiLSTM-Attention | 49.86% | 40.40% | 50.07% | 38.70% | 48.78% |
| 🥉 | BiLSTM | 46.00% | 40.06% | 47.65% | 40.55% | 48.94% |
| 4 | GRU | 17.43% | 4.95% | 17.55% | 4.98% | 5.24% |
| 5 | LSTM | 8.71% | 2.67% | 8.84% | 2.71% | 1.44% |

---

## 🏆 **Winner: TextCNN**

```
┌─────────────────────────────────────────────────────────────────┐
│                     🏆 BEST MODEL: TextCNN                     │
├─────────────────────────────────────────────────────────────────┤
│  • Test Accuracy:      54.07%                                  │
│  • Test Macro F1:      43.38%                                  │
│  • Test Weighted F1:   53.00%                                  │
│  • Validation Accuracy: 54.00%                                 │
│  • Parameters:         923,526                                 │
├─────────────────────────────────────────────────────────────────┤
│  Why TextCNN Wins: Convolutional filters capture local text   │
│  patterns effectively. Simple architecture with strong        │
│  performance on short text classification tasks.              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 **End-to-End Pipeline**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           📊 DATA PIPELINE                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  📰 News Dataset ──▶ 🔍 Data Cleaning ──▶ 🏷️ Label Encoding                   │
│  (5,000 articles)      (Remove duplicates,       (6 categories:                │
│                         Clean titles)             Business, Energy, etc.)      │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🔬 TEXT PREPROCESSING                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   📝 Tokenization ──▶ 📚 Vocabulary Building ──▶ 🔢 Sequence Encoding          │
│   (Custom tokenizer)    (8,056 words)            (max_len=40, padding)         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🤖 MODEL TRAINING                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   🔀 Data Split (70/15/15) ──▶ ⚖️ Balanced Sampler ──▶ 🧠 Model Training      │
│   3,268/700/701 samples         (WeightedRandom)       (5 architectures)       │
│                                                                                 │
│   ⬇                                                                             │
│   📊 Evaluation ──▶ 🎯 Best Model (TextCNN) ──▶ 💾 Model Export               │
│   (Accuracy, F1, Confusion)                                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🚀 DEPLOYMENT                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   💾 Saved: Best Model (.pth), Vocabulary, Label Mapping                      │
│   📊 Generated: Confusion Matrix, Training Curves, Model Comparison           │
│   🎯 Prediction Function: Ready for deployment                                 │
│   📦 Package: ZIP archive with all model artifacts                            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 **Model Architectures**

### **1. LSTM (Long Short-Term Memory)**
- **Parameters**: 848,454
- **Architecture**: Single-layer LSTM with 96 hidden units
- **Pros**: Good for sequential data
- **Cons**: Underfitting on this dataset

### **2. GRU (Gated Recurrent Unit)**
- **Parameters**: 829,830
- **Architecture**: Single-layer GRU with 96 hidden units
- **Pros**: Faster than LSTM
- **Cons**: Underfitting on this dataset

### **3. BiLSTM (Bidirectional LSTM)**
- **Parameters**: 923,526
- **Architecture**: Bidirectional LSTM (96 hidden units each direction)
- **Pros**: Captures context from both directions
- **Cons**: Overfitting observed

### **4. TextCNN (Text Convolutional Neural Network)**
- **Parameters**: 923,526
- **Architecture**: CNN with 3 kernel sizes (3,4,5), 128 filters each
- **Pros**: Excellent for text classification
- **Cons**: Slight overfitting

### **5. CNN-BiLSTM-Attention**
- **Parameters**: 951,463
- **Architecture**: CNN + BiLSTM + Attention Mechanism
- **Pros**: Hybrid architecture captures local and global features
- **Cons**: Overfitting, higher complexity

---

## 📊 **Performance Analysis**

### **Confusion Matrix - Best Model (TextCNN)**

<div align="center">
  <img src="confusion_matrix.png" alt="Confusion Matrix" width="600"/>
</div>

### **Per-Class Performance (TextCNN)**

| Category | Precision | Recall | F1-Score | Support |
|----------|-----------|--------|----------|---------|
| **Business** | 0.4962 | 0.7386 | 0.5936 | 264 |
| **Energy** | 0.3333 | 0.2222 | 0.2667 | 18 |
| **Health** | 0.5000 | 0.2000 | 0.2857 | 20 |
| **Markets** | 0.6258 | 0.4766 | 0.5411 | 214 |
| **Politics** | 0.6543 | 0.4309 | 0.5196 | 123 |
| **Technology** | 0.4773 | 0.3387 | 0.3962 | 62 |

### **Key Insights**

| Observation | Insight |
|-------------|---------|
| **TextCNN outperforms RNNs** | CNNs better capture local text patterns |
| **Business & Markets best predicted** | Larger sample sizes (264, 214) help |
| **Energy & Health underperform** | Small sample sizes (18, 20) limit learning |
| **Overfitting in complex models** | BiLSTM, CNN-BiLSTM show train-val gap > 35% |
| **Simple models underfit** | LSTM, GRU achieve < 20% accuracy |

---

## 🛠️ **Tech Stack**

### **Core Libraries**

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.10+ |
| **Deep Learning** | PyTorch 2.0+ |
| **RNN Models** | LSTM, GRU, BiLSTM |
| **CNN Models** | TextCNN, CNN-BiLSTM-Attention |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **ML Tools** | Scikit-Learn 1.3+ |
| **GPU Acceleration** | CUDA |

### **Key Dependencies**

```bash
pip install -q transformers datasets accelerate
pip install -q pandas numpy matplotlib seaborn scikit-learn
```

---

## 📁 **Project Structure**

```
DeepNews_Best_Model/
├── 📄 best_model.pth                            # Trained TextCNN model (3.53 MB)
├── 📄 vocabulary.json                           # Vocabulary dictionary (8,056 words)
├── 📄 label_mapping.json                        # Category mapping (0-5)
├── 📄 model_comparison.csv                      # Model comparison results
├── 📊 confusion_matrix.png                      # Confusion matrix visualization
├── 📊 model_comparison.png                      # Model comparison bar chart
├── 📊 loss_curve.png                            # Training/Validation loss
├── 📊 accuracy_curve.png                        # Training/Validation accuracy
└── 📦 DeepNews_Best_Model.zip                  # Complete model package
```

---

## 🎯 **Getting Started**

### **1. Clone the Repository**
```bash
git clone https://github.com/BROWNBOY047/deepnews-classification.git
cd deepnews-classification
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Open in Google Colab**
- Upload the notebook (`News_Category_Prediction_Deep_Learning.ipynb`)
- Upload your news dataset (CSV format)
- Run cells top to bottom

### **4. Dataset Format**

| Column | Type | Description |
|--------|------|-------------|
| `URL` | String | Article URL (optional) |
| `Title` | String | **Required** — Article headline |
| `Category` | String | **Required** — News category |
| `Group Leader` | String | Optional |

### **5. Expected Outputs**
- ✅ **5 trained deep learning models**
- ✅ **Comprehensive model comparison**
- ✅ **Best model (TextCNN) saved and ready**
- ✅ **Model evaluation metrics and visualizations**
- ✅ **Complete model package (ZIP archive)**

---

## 📊 **Visualization Gallery**

### **Model Comparison**

<div align="center">
  <img src="model_comparison.png" alt="Model Comparison" width="800"/>
</div>

### **Training Curves - TextCNN (Best Model)**

<div align="center">
  <img src="loss_curve.png" alt="Loss Curve" width="800"/>
  <img src="accuracy_curve.png" alt="Accuracy Curve" width="800"/>
</div>

### **Category Distribution**

<div align="center">
  <img src="category_distribution.png" alt="Category Distribution" width="600"/>
</div>

---

## 🧠 **How It Works: Deep Dive**

### **1. Data Preprocessing**
- **Cleaning**: Remove missing values, duplicates, URLs, HTML tags
- **Normalization**: Lowercase, whitespace normalization
- **Category Encoding**: LabelEncoder for 6 categories

### **2. Text Preprocessing**
- **Tokenization**: Custom regex tokenizer (`[a-z0-9]+(?:'[a-z]+)?`)
- **Vocabulary**: Built from training data only
- **Encoding**: Convert tokens to integer IDs (max_len=40)
- **Padding**: Fixed-length sequences with <PAD> token

### **3. Model Training**
- **Balanced Sampling**: WeightedRandomSampler for class imbalance
- **Optimizer**: AdamW (lr=0.001, weight_decay=1e-4)
- **Scheduler**: ReduceLROnPlateau (patience=1, factor=0.5)
- **Gradient Clipping**: max_norm=1.0
- **Early Stopping**: patience=2 epochs
- **Loss**: CrossEntropyLoss

### **4. Evaluation Metrics**
- **Accuracy**: Overall correct predictions
- **Macro F1**: Unweighted average F1 across classes
- **Weighted F1**: F1 weighted by class support
- **Precision/Recall**: Per-class performance

---

## 🎯 **Real-World Applications**

| Domain | Application |
|--------|-------------|
| **News Aggregators** | Automatic news categorization |
| **Content Platforms** | Topic classification and organization |
| **Social Media** | Content filtering and recommendation |
| **Market Research** | Trend identification and analysis |
| **Information Retrieval** | News search and discovery |

---

## 📈 **Future Improvements**

| Enhancement | Description |
|-------------|-------------|
| **Pre-trained Embeddings** | Use GloVe/Word2Vec for better semantic understanding |
| **BERT/Transformers** | Fine-tune pre-trained language models |
| **Data Augmentation** | Back-translation, synonym replacement |
| **Ensemble Models** | Combine multiple architectures |
| **Hyperparameter Tuning** | Grid search / Bayesian optimization |
| **More Data** | Increase dataset size for better generalization |
| **Multi-label Classification** | Support multiple categories per article |

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
@misc{deepnews-2026,
  author = {Muhammad Umer},
  title = {DEEPNEWS - Deep Learning News Title Classification},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/BROWNBOY047/deepnews-classification}}
}
```

---

<div align="center">

## 🌟 **Star Us on GitHub!**

If you found this project useful, please give it a ⭐ star! 
---

</div>

---

## 📧 **Contact & Support**

| Platform | Link |
|----------|------|
| 📧 Email | iamumer34@gmail.com |


---

<div align="center">

**Made with ❤️ by Your Team**

</div>
