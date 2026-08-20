
# 📰 **News Summary Generator - BART Text Summarization**

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![BART](https://img.shields.io/badge/BART-Large-FFD21E?style=for-the-badge&logo=huggingface&logoColor=white)
![Transformers](https://img.shields.io/badge/Transformers-4.30%2B-FFD21E?style=for-the-badge&logo=huggingface&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Text_Summarization-FFD21E?style=for-the-badge&logo=huggingface&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![CUDA](https://img.shields.io/badge/CUDA-GPU_Accelerated-76B900?style=for-the-badge&logo=nvidia&logoColor=white)

</div>

---

## 🎯 **Project Overview**

A **News Summary Generator** that leverages **BART (Bidirectional and Auto-Regressive Transformer)** to automatically generate concise summaries of news articles. The system processes 1,214+ news articles from multiple sources and produces human-quality summaries using state-of-the-art text-to-text generation.

### 🚀 **Key Features**

| Feature | Description |
|---------|-------------|
| **🧠 BART Large Model** | Uses `facebook/bart-large-cnn` for high-quality summarization |
| **📰 Multi-Source Data** | Merges 3 datasets (2,072 articles) with deduplication |
| **⚡ GPU Accelerated** | Optimized batch processing with CUDA support |
| **🔍 Data Cleaning** | Aggressive deduplication and content cleaning |
| **📈 1,214 Articles** | Successfully summarized with high quality |
| **💾 CSV Export** | Ready-to-use dataset with summaries |
| **🚀 16+ Minutes** | Efficient processing at 1.21 articles/second |

---

## 📊 **Dataset Overview**

### **Data Sources & Merging**

| File | Original Rows | After Dedup | Source Count |
|------|---------------|-------------|--------------|
| **news_dataset.csv** | 571 | 566 | 52 sources |
| **news_dataset_3000.csv** | 640 | 414 | 54 sources |
| **news_dataset_extra.csv** | 861 | 235 | 52 sources |
| **Total Merged** | **2,072** | **1,215** | **58 sources** |

### **Deduplication Results**

```
Total rows before dedup: 2,072
Exact duplicates removed: 857
Final clean articles: 1,215
Articles with < 30 words removed: 1
Final summarized: 1,214
```

### **Source Distribution (Top 10)**

| Source | Articles | Source | Articles |
|--------|----------|--------|----------|
| **Independent** | 50 | **Wired** | 50 |
| **CNBC** | 49 | **Guardian_World** | 45 |
| **FoxNews** | 44 | **BBC_Business** | 43 |
| **Google_News** | 36 | **BBC_World** | 33 |
| **CNN_World** | 30 | **CNN_US** | 29 |

---

## 🏆 **Model Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    🏆 MODEL: BART Large                       │
├─────────────────────────────────────────────────────────────────┤
│  • Model:              facebook/bart-large-cnn               │
│  • Parameters:         1.6 Billion                           │
│  • Architecture:       Transformer (BART)                   │
│  • Task:               Text-to-Text Summarization           │
│  • Max Input Tokens:   1,024                                │
│  • Max Output Tokens:  60                                   │
│  • Min Output Tokens:  15                                   │
│  • Beam Search:        4 beams (quality optimization)       │
│  • Length Penalty:     2.0                                  │
│  • Processing Speed:   1.21 articles/second                │
│  • Total Time:         16:45 minutes                       │
├─────────────────────────────────────────────────────────────────┤
│  Why BART: State-of-the-art text generation with excellent   │
│  summarization capabilities. Fine-tuned on CNN/DailyMail    │
│  dataset for optimal news summarization.                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 **End-to-End Pipeline**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           📊 DATA PIPELINE                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  📁 Multiple Datasets ──▶ 🔄 Merge & Dedup ──▶ 📋 Column Standardization      │
│  (3 CSV files)            (2,072 → 1,215 rows)    (Title, Content, Source)    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🔬 DATA CLEANING                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   🧹 Exact Deduplication ──▶ 📏 Length Filter ──▶ 🧼 Content Cleaning          │
│   (title+content)           (< 30 words removed)  (Remove boilerplate)         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🤖 TEXT SUMMARIZATION                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   📝 Text Input ──▶ 🔄 Tokenization ──▶ 🧠 BART Model ──▶ 📝 Summary Output   │
│   (Full article)     (max 1,024 tokens)   (1.6B params)    (15-60 tokens)      │
│                                                                                 │
│   ⬇                                                                             │
│   💾 Batch Processing ──▶ 📊 Quality Check ──▶ 📈 Export                      │
│   (1,214 articles)        (0 failures)        (CSV format)                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🚀 DEPLOYMENT                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   💾 Saved: news_summaries_final.csv (6.5 MB)                                 │
│   📊 Columns: Title, Content, Generated_Summary, Source                       │
│   🎯 Ready: Summarization pipeline for new articles                           │
│   📦 Format: CSV for easy integration                                          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 **Sample Summaries**

### **Example 1: Technology & Business**

**Original Title:**
*"Silicon Valley Bank collapse renews calls to address disparities impacting entrepreneurs of color"*

**Generated Summary:**
> *Venture capitalist Arlan Hamilton stepped in to help some founders of color who panicked about losing access to payroll funds.*

**Key Entities Extracted:** Arlan Hamilton, Silicon Valley Bank

---

### **Example 2: Environment & Energy**

**Original Title:**
*"Big-box stores could help slash emissions and save millions by putting solar panels on roofs. Why aren't more of them doing it?"*

**Generated Summary:**
> *As the US attempts to wean itself off its heavy reliance on fossil fuels and shift to cleaner energy sources, many experts are eyeing a promising solution.*

---

### **Example 3: Entertainment & Culture**

**Original Title:**
*"Look of the Week: Blackpink headline Coachella in Korean hanboks"*

**Generated Summary:**
> *Blackpink became the first Asian act to ever headline Coachella. The group paid homage to their Korean heritage by wearing hanboks.*

---

### **Example 4: Business & Finance**

**Original Title:**
*"Michael Jordan's 1998 NBA Finals sneakers sell for a record $2.2 million"*

**Generated Summary:**
> *The game-winning sneakers sold for $2.2 million at Sotheby's in New York on Tuesday. The previous record was $1.47 million, set in 2021 by a pair of Nike Air Ships.*

---

### **Example 5: Media & Entertainment**

**Original Title:**
*"How Playboy cut ties with Hugh Hefner to create a new identity"*

**Generated Summary:**
> *Hugh Hefner launched Playboy Magazine 70 years ago. The company is now trying to create a new identity.*

---

## 🛠️ **Tech Stack**

### **Core Libraries**

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.10+ |
| **Deep Learning** | PyTorch 2.0+, Transformers 4.30+ |
| **Summarization** | BART Large (1.6B parameters) |
| **Data Processing** | Pandas, NumPy |
| **Utilities** | TQDM, Re (regex) |
| **GPU Acceleration** | CUDA, Tesla T4 |

### **Key Dependencies**

```bash
pip install transformers datasets evaluate rouge_score sentencepiece accelerate
```

---

## 📁 **Project Structure**

```
News_Summary_Generator/
├── 📄 README.md                                    # Project documentation
├── 📄 News_Summary_Generator.ipynb                 # Main notebook
├── 📊 news_summaries_final.csv                    # Final dataset with summaries (6.5 MB)
├── 📁 input_data/                                 # Original datasets
│   ├── news_dataset.csv                           # 571 articles
│   ├── news_dataset_3000.csv                      # 640 articles
│   └── news_dataset_extra.csv                     # 861 articles
└── 📄 model/                                      # BART model (optional)
    └── facebook/bart-large-cnn                    # Pre-trained model
```

---

## 🎯 **Getting Started**

### **1. Install Dependencies**
```bash
pip install transformers datasets evaluate rouge_score sentencepiece accelerate
```

### **2. Open in Google Colab**
- Upload the notebook (`News_Summary_Generator.ipynb`)
- Upload your news dataset files (CSV format)
- Run cells top to bottom

### **3. Dataset Format**

| Column | Type | Description |
|--------|------|-------------|
| `title` | String | **Required** — Article headline |
| `content` | String | **Required** — Full article text |
| `source` | String | **Required** — News source identifier |
| `link` | String | Optional — Article URL |
| `word_count` | Integer | Optional — Article word count |

### **4. Expected Outputs**
- ✅ **Merged and deduplicated dataset**
- ✅ **Generated summaries for all articles**
- ✅ **CSV file ready for download**
- ✅ **0% failure rate (all articles summarized)**

---

## 📈 **Processing Statistics**

### **Performance Metrics**

| Metric | Value |
|--------|-------|
| **Total Articles** | 1,214 |
| **Total Processing Time** | 16:45 minutes |
| **Average Time per Article** | 0.83 seconds |
| **Processing Speed** | 1.21 articles/second |
| **GPU Utilization** | Tesla T4 |
| **Batch Size** | 1 (sequential processing) |
| **Beam Search** | 4 beams |
| **Max Input Length** | 1,024 tokens |
| **Max Output Length** | 60 tokens |
| **Min Output Length** | 15 tokens |
| **Failure Rate** | 0% |

### **Data Quality Checks**

| Check | Result |
|-------|--------|
| **Missing Values** | 0 after cleaning |
| **Duplicate Removal** | 857 exact duplicates removed |
| **Short Articles (< 30 words)** | 1 removed |
| **Empty Summaries** | 0 (all successful) |
| **Source Count** | 58 unique sources |

---

## 🔬 **How It Works**

### **1. Data Loading & Merging**
- Loads 3 separate CSV files
- Standardizes column names
- Merges into single dataset

### **2. Deduplication**
- Identifies exact duplicates based on `title` + `content`
- Keeps first occurrence only
- Validates duplicate groups

### **3. Data Cleaning**
- Removes articles with < 30 words
- Removes common scraped boilerplate
- Cleans navigation menus and share buttons

### **4. Summarization**
- Uses `facebook/bart-large-cnn` model
- Tokenizes with max length of 1,024 tokens
- Generates summaries with beam search (4 beams)
- Output length: 15-60 tokens

### **5. Export**
- Creates final CSV with all columns
- Includes generated summaries
- Ready for download

---

## 📊 **Sample Summaries by Category**

| Category | Example Summary |
|----------|-----------------|
| **Technology** | *"Venture capitalist Arlan Hamilton stepped in to help some founders of color who panicked about losing access to payroll funds."* |
| **Business** | *"The game-winning sneakers sold for $2.2 million at Sotheby's in New York on Tuesday."* |
| **Environment** | *"As the US attempts to wean itself off its heavy reliance on fossil fuels and shift to cleaner energy sources, many experts are eyeing a promising solution."* |
| **Entertainment** | *"Blackpink became the first Asian act to ever headline Coachella. The group paid homage to their Korean heritage by wearing hanboks."* |

---

## 🎯 **Real-World Applications**

| Domain | Application |
|--------|-------------|
| **News Aggregators** | Automated article summaries for users |
| **Content Curation** | Quick scanning of multiple articles |
| **Market Research** | Summarized news monitoring |
| **Social Media** | Shareable summaries for social platforms |
| **Education** | Teaching summarization techniques |
| **Media Monitoring** | Daily news digest generation |

---

## 📈 **Future Improvements**

| Enhancement | Description |
|-------------|-------------|
| **Fine-Tuning** | Fine-tune BART on domain-specific data |
| **Abstractive Summarization** | More creative summary generation |
| **Multi-Document Summarization** | Summarize multiple articles simultaneously |
| **Topic-Specific Models** | Specialized models for different categories |
| **Web Interface** | Streamlit/Gradio for easy access |
| **Real-Time Processing** | API endpoint for on-demand summarization |
| **Evaluation Metrics** | ROUGE, BLEU scores for quality assessment |

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
@misc{news-summary-generator-2026,
  author = {Muhammad Umer},
  title = {News Summary Generator - BART Text Summarization},
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
