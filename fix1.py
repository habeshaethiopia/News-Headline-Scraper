import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Selenium WebDriver
driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed
driver.get("https://cafe.naver.com/stockseeker")

# Click the 6th forum
driver.find_element(By.ID, "menuLink4").click()
time.sleep(5)

# Switch to the main iframe
def switch_to_main_iframe():
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cafe_main"))
    )
    driver.switch_to.frame(iframe)

switch_to_main_iframe()

# Parse posts using BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
posts = soup.select('#main-area > div:nth-child(4) > table > tbody > tr')

forum_number = 6

for post in posts:
    try:
        # Extract post date
        post_date = post.find('td', class_='td_date').text.strip().replace(".", "")
        post_folder = f"Forum{forum_number}/{post_date}"
        os.makedirs(post_folder, exist_ok=True)

        # Find article link and navigate
        article_link = post.find('a', class_='article')
        if article_link:
            article_url = article_link['href']
            driver.get(f"https://cafe.naver.com{article_url}")
            time.sleep(5)

            # Switch to the article iframe
            try:
                article_iframe = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "cafe_main"))
                )
                driver.switch_to.frame(article_iframe)
            except Exception as e:
                print(f"Error switching to article iframe: {e}")
                continue

            # Extract article content with BeautifulSoup
            detailed_soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract text content
            text_content_div = detailed_soup.find('div', class_="se-module se-module-text")
            if text_content_div:
                text_content = text_content_div.get_text(separator='\n').strip()
                with open(f"{post_folder}/{post_date} text.txt", 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text_content)
            else:
                print("Text not found.")

            # Extract image content
            image_div = detailed_soup.find('div', class_='se-module se-module-image')
            if image_div:
                image_tag = image_div.find('img', class_='se-image-resource')
                if image_tag:
                    image_url = image_tag['src']
                    image_data = requests.get(image_url).content
                    with open(f"{post_folder}/{post_date} image.jpg", 'wb') as img_file:
                        img_file.write(image_data)

            # Return to the main page
            driver.get("https://cafe.naver.com/stockseeker")
            time.sleep(5)

            # Re-navigate to the 6th forum
            driver.find_element(By.ID, "menuLink4").click()
            time.sleep(5)

            # Reattach to the iframe
            switch_to_main_iframe()

    except Exception as e:
        print(f"Error processing post: {e}")
        continue
