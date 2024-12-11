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
# Switch to the iframe
iframe = driver.find_element(By.XPATH, '//*[@id="cafe_main"]')  # Adjust the XPath as needed

driver.switch_to.frame(iframe)



try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'listSizeSelectDiv'))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="listSizeSelectDiv"]/ul/li[7]/a'))
    ).click()
except Exception as e:
    print(f"Error clicking '50개씩' link: {e}")
time.sleep(5)

forum_number = 6
posts = driver.find_elements(By.CSS_SELECTOR, '#main-area > div:nth-child(4) > table > tbody > tr')
# print(posts)
for post in posts:
    time.sleep(5)
    post_date = post.find_element(By.CLASS_NAME, 'td_date').text.strip().replace(".", "")  # Extract post date
    post_folder = f"Forum{forum_number}/{post_date}"
    os.makedirs(post_folder, exist_ok=True)

    # Click the article to open the detailed view
    article_link = post.find_element(By.CLASS_NAME, 'article')
    if article_link:
        article_link.click()
        time.sleep(5)

        # Switch to the iframe containing the article content
        # article_iframe = driver.find_element(By.XPATH, "//iframe[@id='cafe_main']")
        # driver.switch_to.frame(article_iframe)

        # Extract text content
        text_content_div = driver.find_element(By.CLASS_NAME, 'se-module-text')
        if text_content_div:
            text_content = text_content_div.text.strip()
            with open(f"{post_folder}/{post_date} text.txt", 'w', encoding='utf-8') as txt_file:
                txt_file.write(text_content)
        else:
            print("Text not found")

        # Extract image if exists
        image_div = driver.find_element(By.CLASS_NAME, 'se-module-image')
        if image_div:
            image_tag = image_div.find_element(By.CLASS_NAME, 'se-image-resource')
            if image_tag:
                image_url = image_tag.get_attribute('src')
                image_data = requests.get(image_url).content
                with open(f"{post_folder}/{post_date} image.jpg", 'wb') as img_file:
                    img_file.write(image_data)

        # Switch back to the main iframe
        driver.switch_to.default_content()
        driver.switch_to.frame(iframe)

        # Go back to the main page
        driver.back()
        time.sleep(5)
