# 📰 **NewsNER - Named Entity Recognition Extractor**

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![BERT](https://img.shields.io/badge/BERT-Large-FFD21E?style=for-the-badge&logo=huggingface&logoColor=white)
![Transformers](https://img.shields.io/badge/Transformers-4.30%2B-FFD21E?style=for-the-badge&logo=huggingface&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Token_Classification-FFD21E?style=for-the-badge&logo=huggingface&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![CUDA](https://img.shields.io/badge/CUDA-GPU_Accelerated-76B900?style=for-the-badge&logo=nvidia&logoColor=white)

</div>

---

## 🎯 **Project Overview**

A **Named Entity Recognition (NER) Extractor** that processes news headlines to identify and extract **People, Organizations, and Dates** using a fine-tuned **BERT Large** model. The system processes 5,000+ news headlines, extracts entities, and stores them in a structured dictionary format for easy analysis and integration.

### 🚀 **Key Features**

| Feature | Description |
|---------|-------------|
| **🧠 BERT Large NER** | Uses `dbmdz/bert-large-cased-finetuned-conll03-english` model |
| **📊 3 Entity Types** | Extracts Names (PER), Organizations (ORG), and Dates (DATE) |
| **📰 5,000+ Headlines** | Processes large-scale news datasets efficiently |
| **🔍 Intelligent Filtering** | Aggressive cleaning removes false positives |
| **📈 3,540 Unique Entities** | Comprehensive entity coverage |
| **🚀 GPU Accelerated** | Optimized batch processing with CUDA |
| **💾 Multiple Formats** | CSV, JSON, and dictionary outputs |

---

## 📊 **Extraction Results Summary**

| Entity Type | Count | Coverage |
|-------------|-------|----------|
| **Names (PER)** | 268 | 29.7% of articles |
| **Organizations (ORG)** | 3,250 | 95.1% of articles |
| **Dates (DATE)** | 22 | 5.8% of articles |
| **Total Unique Entities** | **3,540** | 4,810 articles with entities |
| **Average Entities/Article** | **4.33** | - |
| **Max Entities in Article** | **18** | - |

---

## 🏆 **Model Performance**

```
┌─────────────────────────────────────────────────────────────────┐
│                    🏆 NER MODEL: BERT Large                   │
├─────────────────────────────────────────────────────────────────┤
│  • Model:              dbmdz/bert-large-cased-finetuned-conll03│
│  • Parameters:         1.3 Billion                            │
│  • Architecture:       Transformer (BERT Large)              │
│  • Entity Types:       PER (Names), ORG (Organizations),      │
│                        DATE (Dates)                           │
│  • Confidence Threshold: 0.65 (aggressive filtering)          │
│  • Processing Speed:   98.2 headlines/second                  │
│  • Total Time:         50.89 seconds                          │
├─────────────────────────────────────────────────────────────────┤
│  Why BERT Large: State-of-the-art NER performance with       │
│  robust entity recognition. Fine-tuned on CONLL03 dataset     │
│  for optimal accuracy on news text.                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 **End-to-End Pipeline**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           📊 DATA PIPELINE                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  📰 News Dataset ──▶ 🔍 Data Analysis ──▶ 📋 Column Selection                 │
│  (5,000 articles)      (Column inspection,      (Title, Category)              │
│                         null value check)                                       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🔬 NER EXTRACTION                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   📝 Batch Processing ──▶ 🤖 BERT Large NER ──▶ 🧹 Aggressive Cleaning        │
│   (32 headlines/batch)      (Entity recognition)    (Filter false positives)   │
│                                                                                 │
│   ⬇                                                                             │
│   📊 Entity Collection ──▶ 🗂️ Unique Entity Storage ──▶ 📈 Entity Statistics   │
│   (Names, Orgs, Dates)       (3,540 unique entities)    (Coverage analysis)    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           📦 DATA ENRICHMENT                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   🔗 Entity Mapping ──▶ 📊 Column Addition ──▶ 📝 Dictionary Format            │
│   (Entity per headline)    (Extracted_Names,       ({names: [],                │
│                            Extracted_Orgs,          organizations: [],          │
│                            Extracted_Dates)         dates: []})                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🚀 DEPLOYMENT                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   💾 Saved: CSV (with JSON strings), JSON (preserved dicts)                   │
│   📊 Master Dictionary: news_ner_clean_results.json                           │
│   🎯 Ready: Entity extraction pipeline for new data                           │
│   📦 Formats: Multiple output formats for different use cases                 │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 **Entity Extraction Process**

### **1. Entity Types Extracted**

| Entity Type | NER Tag | Description | Example |
|-------------|---------|-------------|---------|
| **Names** | PER | Person names | Alex Jones, Elon Musk |
| **Organizations** | ORG | Companies, institutions | Google, Microsoft, DOJ |
| **Dates** | DATE | Temporal expressions | October 2025, Q4 2025 |

### **2. Aggressive Cleaning Process**

```
Raw NER Output → Filtering Steps → Clean Entities

1. Remove subword tokens (##)
2. Filter short entities (< 3 chars)
3. Remove numeric patterns
4. Eliminate common false positives
5. Apply confidence threshold (0.65+)
6. Keep valid acronyms (NASA, IBM)
7. Sort and deduplicate
```

### **3. False Positive Filtering**

| Pattern | Example | Action |
|---------|---------|--------|
| **Single letters** | A, B, C | Removed |
| **Pure numbers** | 123, 456 | Removed |
| **Common words** | and, or, the | Removed |
| **Subword tokens** | ##er, ##ing | Removed |
| **Short acronyms** | AB, CD (not uppercase) | Removed |

---

## 🛠️ **Tech Stack**

### **Core Libraries**

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.10+ |
| **Deep Learning** | PyTorch 2.0+, Transformers 4.30+ |
| **NER Model** | BERT Large (1.3B parameters) |
| **Data Processing** | Pandas, NumPy |
| **Utilities** | TQDM, JSON, Re (regex) |
| **GPU Acceleration** | CUDA, Tesla T4 |

### **Key Dependencies**

```bash
pip install transformers datasets pandas tqdm openpyxl
```

---

## 📁 **Project Structure**

```
NewsNER_Extractor/
├── 📄 README.md                                        # Project documentation
├── 📄 News_NER_Extractor.ipynb                         # Main notebook
├── 📊 News_Classification_Dataset_With_Dict.csv        # Dataset with entities (1.4 MB)
├── 📊 News_Classification_Dataset_With_Dict.json       # Dataset with preserved dicts (2.3 MB)
├── 📄 news_ner_clean_results.json                      # Master entity dictionary (72 KB)
└── 📂 final_dict/                                      # Entity dictionary structure
    ├── names/                                          # 268 unique names
    ├── organizations/                                  # 3,250 unique organizations
    ├── dates/                                          # 22 unique dates
    └── metadata/                                       # Project metadata
```

---

## 🎯 **Getting Started**

### **1. Install Dependencies**
```bash
pip install transformers datasets pandas tqdm openpyxl
```

### **2. Open in Google Colab**
- Upload the notebook (`News_NER_Extractor.ipynb`)
- Upload your news dataset (CSV, JSON, or Excel format)
- Run cells top to bottom

### **3. Dataset Format**

| Column | Type | Description |
|--------|------|-------------|
| `URL` | String | Article URL (optional) |
| `Title` | String | **Required** — Article headline for NER |
| `Category` | String | **Required** — News category |
| `Group Leader` | String | Optional |

### **4. Expected Outputs**
- ✅ **Master entity dictionary** (names, organizations, dates)
- ✅ **Enhanced dataset** with entity columns
- ✅ **Multiple file formats** (CSV, JSON)
- ✅ **Entity statistics** and coverage analysis
- ✅ **Ready-to-use dictionary format**

---

## 📊 **Entity Distribution by Category**

| Category | Total Articles | With Names | With Orgs | With Dates |
|----------|---------------|------------|-----------|------------|
| **Business** | 1,896 | ~560 | ~1,800 | ~110 |
| **Markets** | 1,518 | ~450 | ~1,440 | ~85 |
| **Politics** | 862 | ~255 | ~820 | ~50 |
| **Technology** | 452 | ~135 | ~430 | ~25 |
| **Health** | 144 | ~42 | ~137 | ~8 |
| **Energy** | 127 | ~37 | ~121 | ~7 |

---

## 📊 **Sample Extracted Entities**

### **Names (Sample of 20 from 268)**
```
AR Rahman, Aaron Vandeford, Abbott, Abdulaziz bin Salman, 
Aditya Birla, Aidan O'Shea, Akcay, Aldar, Alex Jones, 
Alexis Ohanian, Ali, Ali Mirian, Allan Gray, Amaya Espinal, 
Anant Raj, Arnault, Artur Bergman, Arun Kaul, Awfis, Bang Si
```

### **Organizations (Sample of 20 from 3,250)**
```
1960s, 49ers Foundation, AAPL, AAR, ABK Biomedical, ABS, 
ABS - 201 Androgenetic Alopecia Program, ABT, ACA, ACCC, 
ACET, ACI Jet, ACRES Commercial Realty Corp, ADOCIA, AEC, 
AECI, AES, AFL - CIO, AFP
```

### **Dates (All 22)**
```
10/15/2025, April, August 2024, August 2025, December, 
February, January, January 2026, June, May 2022, November, 
OCTOBER, OCTOBER 2025, Oct, October, October 2023, 
October 2025, Q2 2026, Q3 2025, Q4 2025, September, 
September 2025
```

---

## 📈 **Output Format**

### **Master Entity Dictionary**
```json
{
  "names": ["Alex Jones", "Elon Musk", ...],
  "organizations": ["Google", "Microsoft", "DOJ", ...],
  "dates": ["October 2025", "Q4 2025", ...],
  "categories": ["Business", "Markets", ...],
  "metadata": {
    "total_articles": 5000,
    "model_used": "dbmdz/bert-large-cased-finetuned-conll03-english",
    "extraction_time": "50.89 seconds",
    "entity_counts": {
      "total_names": 268,
      "total_organizations": 3250,
      "total_dates": 22
    }
  }
}
```

### **Enhanced Dataset Structure**
```python
{
  'Title': 'Vietnam Airlines data leak exposes a crisis',
  'Category': 'Technology',
  'Entities': {
    'names': [],
    'organizations': ['Data', 'Vietnam Airlines'],
    'dates': []
  },
  'Entity_Count': 2
}
```

---

## 🎯 **Real-World Applications**

| Domain | Application |
|--------|-------------|
| **News Aggregators** | Entity extraction for content tagging |
| **Media Monitoring** | Person/org tracking across articles |
| **Market Intelligence** | Company and person mentions tracking |
| **Research** | Entity relationship analysis |
| **Knowledge Graphs** | Building entity databases |
| **Analytics** | Trend analysis by entity mentions |

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
@misc{newsner-extractor-2026,
  author = {Muhammad Umer},
  title = {NewsNER - Named Entity Recognition Extractor},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub Repository}
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
