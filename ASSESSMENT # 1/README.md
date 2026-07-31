# 🎯 **Assessment #1 Overview**

---

This project extracts the latest 10 articles from three major news sources and saves them in CSV format:

1. **Bloomberg** 
2. **Reuters** 
3. **CBS News**  

---

## 🚀 **Project Files**

| File Name | Description | Output File |
|-----------|-------------|-------------|
| `bloomberg_scraper.py` | Bloomberg News Scraper | `bloomberg_latest_news_Data.csv` |
| `reuters_scraper.py` | Reuters News Scraper | `reuters_latest_news_Data.csv` |
| `cbs_scraper.py` | CBS News Scraper | `CBC_latest_news_Data.csv` |

---

## 📊 **Data Extracted**

| Field | Description |
|-------|-------------|
| **Title** | News headline |
| **URL** | Full article link |
| **Published Date** | Date of publication |
| **Published Time** | Time of publication |
| **Summary** | Article summary |
| **Full Content** | Complete article text |
| **Image URL** | Main article image |
| **Source Feed** | How article was found |
| **Scraped At** | When the article was scraped |

---

## 🛠️ **Technologies Used**

| Library | Purpose |
|---------|---------|
| **requests** | HTTP requests |
| **BeautifulSoup4** | HTML/XML parsing |
| **Selenium** | Browser automation |
| **pandas** | CSV export |
| **webdriver-manager** | ChromeDriver management |

---

## 🔧 **Scraping Methods Used**

| Method | Description | Used For |
|--------|-------------|----------|
| **Google News RSS** | Most reliable, bypasses blocking | Bloomberg, Reuters |
| **Direct RSS** | Official RSS feeds | Bloomberg, Reuters |
| **Web Scraping** | BeautifulSoup parsing | Bloomberg, Reuters, CBS |
| **Selenium** | Browser automation | CBS News |
| **JSON API** | Hidden API endpoints | Bloomberg |
| **Sitemap** | Sitemap parsing | Reuters |

---

## 🏃 **How to Run**

### 🔹 **Run Bloomberg Scraper**
```bash
python Bloomberg_latest_news_Scraper.py
# Choose: 1 for Quick, 2 for Full Content
```

### 🔹 **Run Reuters Scraper**
```bash
python Reuters_latest_news_Scraper.py
# Choose: 1 for Quick, 2 for Full Content
```

### 🔹 **Run CBS Scraper**
```bash
python CBS_latest_news_Scraper.py
# Automatically scrapes and saves data
```

---

## 📦 **Installation**

```bash
pip install requests beautifulsoup4 pandas selenium webdriver-manager
```

---

## 📊 **Sample Output**

### 🔹 **Bloomberg CSV**
```
id,title,published_date,published_time,summary,full_content,image_url,link,source_feed,scraped_at
1,Fed Signals Rate Cut,2025-07-31,14:30:22,Federal Reserve officials...,Full article...,https://...,https://...,Google News RSS,2025-07-31 15:30:00
```

### 🔹 **Reuters CSV**
```
id,title,published_date,published_time,summary,full_content,image_url,link,source_feed,scraped_at
1,AI Model Distillation,2025-07-31,06:09:44,A technique that...,Full article...,https://...,https://...,Google News RSS,2025-07-31 15:30:00
```

### 🔹 **CBS CSV**
```
News URL,Title,Publish Date (New York),First Paragraph
https://www.cbsnews.com/news/...,CBS News Headline 1,2025-07-31 14:30:22,First paragraph content...
```

---

## 🔄 **Scraping Flow**

```
1. Google News RSS (Primary - Most Reliable)
         ↓ (If fails)
2. Direct RSS (Secondary)
         ↓ (If fails)  
3. Web Scraping (Fallback)
         ↓ (If fails)
4. Sitemap/API (Last Resort)
```

---

## 🐞 **Troubleshooting**

| Issue | Solution |
|-------|----------|
| No articles found | Increase `TARGET` or `TIMEOUT` |
| SSL Error | Add `verify=False` to requests |
| ChromeDriver Error | Update Chrome browser |
| Rate Limiting | Add `time.sleep()` between requests |

---

## 💡 **Key Features**

✅ Multiple scraping methods with auto-fallback  
✅ Full content extraction  
✅ Image extraction  
✅ Duplicate removal  
✅ Error handling with retry logic  
✅ CSV output format  

---

## 📁 **File Structure**

```
project/
│
├── Bloomberg_latest_news_Scraper.py
├── Reuters_latest_news_Scraper.py
├── CBS_latest_news_Scraper.py
│
├── bloomberg_latest_news_Data.csv
├── reuters_latest_news_Data.csv
├── CBC_latest_news_Data.csv
│
└── requirements.txt
```


## 📝 **Conclusion**

This project provides a reliable news scraping solution that:
✅ Extracts latest 10 articles from 3 major sources
✅ Uses 6 different scraping methods
✅ Handles errors gracefully
✅ Saves data in CSV format

---


**🌟 Happy Scraping! 🌟**
