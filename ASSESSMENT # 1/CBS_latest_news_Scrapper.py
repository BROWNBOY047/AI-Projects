import time
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# -----------------------------
# Start Chrome
# -----------------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open CBS News homepage
driver.get("https://www.cbsnews.com/")

# Wait for page to load
time.sleep(5)

# Parse homepage
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find first 10 news articles
articles = soup.find_all("a", class_="item__anchor")

news_data = []

for article in articles[:10]:

    # -----------------------------
    # URL
    # -----------------------------
    news_url = article.get("href")

    # -----------------------------
    # Title
    # -----------------------------
    title_tag = article.find("h4")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # -----------------------------
    # First Paragraph (Homepage Summary)
    # -----------------------------
    para_tag = article.find("p", class_="item__dek")
    first_paragraph = para_tag.get_text(strip=True) if para_tag else ""

    # -----------------------------
    # Open article page
    # -----------------------------
    publish_date = ""

    try:
        driver.get(news_url)

        time.sleep(3)

        article_soup = BeautifulSoup(driver.page_source, "html.parser")

        time_tag = article_soup.find("time")

        if time_tag:
            publish_date = time_tag.get_text(strip=True)
        else:
            publish_date = "Not Found"

    except:
        publish_date = "Error"

    # -----------------------------
    # Save Data
    # -----------------------------
    news_data.append({
        "News URL": news_url,
        "Title": title,
        "Publish Date (New York)": publish_date,
        "First Paragraph": first_paragraph
    })

# Close browser
driver.quit()

# Save CSV
df = pd.DataFrame(news_data)

df.to_csv("latest_news.csv", index=False, encoding="utf-8-sig")

print(df)

print("\nCSV file created successfully!")