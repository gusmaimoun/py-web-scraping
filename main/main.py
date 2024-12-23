import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service("C:/Users/gusta/OneDrive/Desktop/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://oxylabs.io/blog")

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "oxy-1g1amat")))

results = []
other_results = []

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

parent_elements1 = soup.find_all(class_="oxy-6v2bts e28lh853")
for a in parent_elements1:
    anchor = a.find("a", class_="oxy-1g1amat e28lh854")
    if anchor and anchor.text.strip():
        results.append(anchor.text.strip())

parent_elements2 = soup.find_all(class_="oxy-12xtph8 e28lh856")
for b in parent_elements2:
    paragraphs = b.find_all("p")
    if len(paragraphs) > 1:
        second_paragraph = paragraphs[1]
        if second_paragraph.text.strip():
            other_results.append(second_paragraph.text.strip())

max_length = max(len(results), len(other_results))
results.extend([None] * (max_length - len(results)))
other_results.extend([None] * (max_length - len(other_results)))

print("Anchor Results (Article Titles):", results)
print("Other Results (Second Paragraph):", other_results)

df = pd.DataFrame({"Names:": results, "Dates/Time:": other_results})
df.to_csv("names.csv", index=False, encoding="utf-8")

driver.quit()
