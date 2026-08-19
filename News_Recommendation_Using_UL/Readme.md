# 📰 **News Category Prediction using Unsupervised Learning**

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557C?style=for-the-badge&logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-3776AB?style=for-the-badge&logo=seaborn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![TF-IDF](https://img.shields.io/badge/TF--IDF-Feature_Extraction-4B8BBE?style=for-the-badge)
![K-Means](https://img.shields.io/badge/K--Means-Clustering-FF6F00?style=for-the-badge&logo=scikit-learn&logoColor=white)

</div>

---

## 🎯 **Project Overview**

An **unsupervised machine learning system** that automatically discovers hidden topics and categories in news headlines using **TF-IDF vectorization**, **dimensionality reduction**, and **K-Means clustering**. This project enables intelligent news categorization without requiring labeled training data.

### 🚀 **Key Features**

| Feature | Description |
|---------|-------------|
| **🧠 Semantic Understanding** | Converts news titles into numerical vectors using TF-IDF |
| **📊 Dimensionality Reduction** | Reduces 8,455 features to 100 using SVD for efficient clustering |
| **🎯 10 Topic Clusters** | Automatically discovers 10 distinct news categories |
| **🔍 Topic Discovery** | Unsupervised K-Means clustering for content organization |
| **📈 Deployment Ready** | Trained model can predict categories for new news titles |
| **⚡ Real-Time Prediction** | Deployable pipeline for instant news categorization |

---

## 📊 **Model Performance Summary**

| Metric | Value | Description |
|--------|-------|-------------|
| **Number of Clusters** | 10 | Optimal clusters determined by Silhouette Score |
| **Silhouette Score** | 0.0697 | Measures cluster cohesion and separation |
| **Davies-Bouldin Index** | 1.4695 | Lower values indicate better clustering |
| **Calinski-Harabasz Score** | 41.19 | Measures between-cluster dispersion |
| **TF-IDF Features** | 8,455 | Original feature space |
| **SVD Features** | 100 | Reduced feature space (98.8% reduction) |
| **Total News Titles** | 4,564 | After data cleaning and preprocessing |

---

## 🏆 **Best Clustering Configuration**

```
┌─────────────────────────────────────────────────────────────────┐
│                     🏆 BEST MODEL: K-Means (K=10)              │
├─────────────────────────────────────────────────────────────────┤
│  • Silhouette Score:     0.0697                                │
│  • Davies-Bouldin Index: 1.4695                                │
│  • Calinski-Harabasz:    41.19                                 │
│  • Features:             100 (SVD)                             │
│  • Total Titles:         4,564                                 │
├─────────────────────────────────────────────────────────────────┤
│  Why K=10: The silhouette score peaks at K=10, indicating     │
│  optimal separation between news topics. Higher K values      │
│  lead to overfitting and lower cluster quality.               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 **End-to-End Pipeline**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           📊 DATA PIPELINE                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  📰 News Dataset ──▶ 🔍 Data Cleaning ──▶ ✂️ Title Extraction                 │
│  (5,000 articles)      (Remove duplicates)      (Keep only 'Title' column)     │
│                           │                                                      │
│                           ▼                                                      │
│                    🧹 Text Cleaning ──▶ 📊 EDA & Visualization                 │
│                    (Lowercase, remove           (Title length distribution)    │
│                     punctuation, URLs)                                          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🔬 FEATURE ENGINEERING                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   📝 TF-IDF Vectorization ──▶ 📉 SVD Reduction ──▶ 📏 Feature Scaling         │
│   (8,455 features)              (100 components)        (StandardScaler)       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🎯 CLUSTERING & EVALUATION                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   🔍 K-Means Model Search (K=2 to 10) ──▶ 📊 Model Evaluation                 │
│                                              (Silhouette, DB, CH scores)      │
│                                                                                 │
│   ⬇                                                                             │
│   🏆 Best K=10 ──▶ 🔬 Final K-Means ──▶ 📈 Cluster Profiling                 │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🚀 DEPLOYMENT                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   💾 Save Models: TF-IDF, SVD, Scaler, K-Means                                │
│   📊 Generate Reports: Cluster Profiles, Evaluation Metrics                    │
│   🎯 Prediction Function: `predict_news_cluster(title)`                        │
│   📦 Package Project: ZIP archive of all artifacts                            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 **10 Discovered News Topics**

| Cluster | Size | Percentage | Top Terms | Representative Titles |
|:-------:|-----:|-----------:|-----------|----------------------|
| 0 | 4,285 | 93.89% | 2025, says, ai, new, china, announces, earnings, trump | General news & financial markets |
| 1 | 38 | 0.83% | data talk, talk, data, ends, index | Stock market indices & data talk |
| 2 | 31 | 0.68% | center, data center, data, ai, nvidia | Data centers & AI infrastructure |
| 3 | 18 | 0.39% | faruqi, behalf investors, claims behalf | Shareholder investigations |
| 4 | 24 | 0.53% | private placement, placement, private | Private placements & offerings |
| 5 | 15 | 0.33% | supreme court, supreme, court, voting | Supreme Court & voting rights |
| 6 | 23 | 0.50% | asset value, net asset, value, asset | Net asset value announcements |
| 7 | 42 | 0.92% | dow, dow jones, jones, data centers | Dow Jones & market headlines |
| 8 | 69 | 1.51% | ceo, ceo says, says, wajax, process | CEO announcements & succession |
| 9 | 19 | 0.42% | pro, m5, apple, chip, m5 chip | Apple products & M5 chip |

---

## 🛠️ **Tech Stack**

### **Core Libraries**

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.10+ |
| **ML Framework** | Scikit-Learn 1.3+ |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Feature Extraction** | TF-IDF Vectorizer |
| **Dimensionality Reduction** | TruncatedSVD |
| **Clustering** | K-Means |
| **Model Persistence** | Joblib |

### **Key Dependencies**

```bash
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
joblib>=1.2.0
```

---

## 📊 **Key Insights**

### **What Makes a Good News Clustering System?**

| Factor | Impact | Explanation |
|--------|--------|-------------|
| **TF-IDF Features** | ⬆️⬆️⬆️ | Captures important terms in each title |
| **SVD Dimensionality Reduction** | ⬆️⬆️ | Reduces noise while preserving key patterns |
| **Optimal K Selection** | ⬆️⬆️ | K=10 balances granularity & cluster quality |
| **Text Cleaning** | ⬆️⬆️ | Removes noise, improves clustering quality |
| **Feature Scaling** | ⬆️ | Standardizes features for better clustering |

### **Performance Cliff Notes**

| Observation | Insight |
|-------------|---------|
| **Majority in Cluster 0 (94%)** | Most news titles are general/financial content |
| **Small specialized clusters (0.3-1.5%)** | Specific niche topics form tight clusters |
| **K=10 optimal** | Silhouette score peaks at K=10 |
| **SVD reduces features by 98.8%** | Efficient without losing cluster quality |

---

## 📁 **Project Structure**

```
news_clustering_outputs/
├── 📄 news_clustered.csv                            # Final clustered dataset
├── 📄 evaluation_summary.csv                        # Model evaluation metrics
├── 📄 cluster_profiles.csv                          # Detailed cluster profiles
├── 🧠 tfidf_vectorizer.pkl                         # TF-IDF vectorizer
├── 🧠 svd.pkl                                      # SVD transformer
├── 🧠 scaler.pkl                                   # Feature scaler
├── 🧠 kmeans_model.pkl                             # Trained K-Means model
├── 🧠 cluster_names.pkl                            # Human-readable cluster names
└── 📦 news_clustering_project.zip                  # Complete project package
```

---

## 🎯 **Getting Started**

### **1. Clone the Repository**
```bash
git clone https://github.com/BROWNBOY047/news-clustering-unsupervised.git
cd news-clustering-unsupervised
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Open in Google Colab**
- Upload the notebook (`News_Category_Prediction_Unsupervised_Learning.ipynb`)
- Upload your news dataset (CSV format with a `Title` column)
- Run cells top to bottom

### **4. Dataset Format**

| Column | Type | Description |
|--------|------|-------------|
| `URL` | String | Article URL (optional) |
| `Title` | String | **Required** — Article headline |
| `Category` | String | **Required** — News category (optional) |
| `Group Leader` | String | Optional |

### **5. Expected Outputs**
- ✅ **10 automatically discovered news clusters**
- ✅ **Cluster profiles with top terms and examples**
- ✅ **Model evaluation metrics**
- ✅ **Trained models ready for deployment**
- ✅ **Prediction function for new titles**

---

## 📊 **Visualization Gallery**

### **2D Cluster Visualization**

<div align="center">
  <img src="2d_cluster_visualization.png" alt="2D Cluster Visualization" width="800"/>
</div>

### **Cluster Size Distribution**

<div align="center">
  <img src="cluster_distribution.png" alt="Cluster Size Distribution" width="600"/>
</div>

### **Model Evaluation Dashboard**

<div align="center">
  <img src="model_evaluation.png" alt="Model Evaluation Dashboard" width="800"/>
</div>

---

## 🧠 **How It Works: Deep Dive**

### **1. Data Preprocessing**
- **Cleaning**: Lowercasing, removing punctuation, URLs, HTML tags
- **Tokenization**: Split titles into meaningful tokens
- **Duplicates**: Remove exact duplicate titles

### **2. Feature Engineering**
- **TF-IDF Vectorization**: 
  - 8,455 features from 4,564 documents
  - n-gram range: (1,2) for unigrams + bigrams
  - Min DF: 2, Max DF: 95%
  - L2 normalization + sublinear TF scaling
- **SVD Dimensionality Reduction**:
  - Reduces 8,455 → 100 features
  - Preserves 16.71% of variance
  - Accelerates clustering and reduces noise
- **Feature Scaling**:
  - StandardScaler (zero mean, unit variance)
  - Ensures equal contribution from all features

### **3. Clustering**
- **Algorithm**: K-Means with K-means++ initialization
- **Model Search**: K=2 to 10 evaluated
- **Best K**: 10 (based on Silhouette Score)
- **Convergence**: 500 max iterations, 20 random inits

### **4. Evaluation Metrics**
- **Silhouette Score**: Measures how similar objects are to their own cluster vs. other clusters (higher = better)
- **Davies-Bouldin Index**: Average similarity between clusters (lower = better)
- **Calinski-Harabasz Score**: Ratio of between-cluster to within-cluster dispersion (higher = better)

---

## 🎯 **Real-World Applications**

| Domain | Application |
|--------|-------------|
| **News Aggregators** | Automatic news categorization (Google News, Flipboard) |
| **Content Platforms** | Topic discovery and content organization |
| **Market Research** | Trend identification and analysis |
| **Social Media** | Content categorization (Twitter, Reddit) |
| **Information Retrieval** | News search and recommendation systems |

---

## 📈 **Future Improvements**

| Enhancement | Description |
|-------------|-------------|
| **Deep Learning Embeddings** | Use BERT/Sentence-BERT for semantic understanding |
| **Hierarchical Clustering** | Discover nested topic structures |
| **Topic Modeling** | LDA or NMF for topic interpretation |
| **Dynamic Clustering** | Incremental/online learning for streaming data |
| **Hybrid Approaches** | Combine supervised + unsupervised learning |
| **Multi-lingual Support** | Support news in multiple languages |

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
@misc{news-clustering-unsupervised-2026,
  author = {Muhammad Umer},
  title = {News Category Prediction using Unsupervised Learning},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{[https://github.com/yourusername/news-clustering-unsupervised](https://github.com/BROWNBOY047/LMXG-1.4-_-Muhammad_Umer/edit/main/News_Recommendation_Using_UL)}}
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

**Made with ❤️ by Muhammad Umer**

</div>
