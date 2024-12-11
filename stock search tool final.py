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

# Navigate to the forum page
driver.get("https://cafe.naver.com/stockseeker")
time.sleep(5)  # Wait for the page to load

# Click the 6th forum
driver.find_element(By.ID, "menuLink4").click()
time.sleep(5)

# Switch to the main iframe
try:
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cafe_main"))
    )
    driver.switch_to.frame(iframe)
except Exception as e:
    print(f"Error switching to iframe: {e}")
    driver.quit()

# Change the number of posts displayed per page to 50
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

# Function to extract and save post content
def extract_and_save_content(driver, forum_number):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    posts = soup.select('#main-area > div:nth-child(4) > table > tbody > tr')
    
    for post in posts:
        post_date = post.find('td', class_='td_date').text.strip().replace(".", "")  # Extract post date
        post_folder = f"Forum{forum_number}/{post_date}"
        os.makedirs(post_folder, exist_ok=True)

        # Click the article to open the detailed view
        article_link = post.find('a', class_='article')
        if article_link:
            article_url = article_link['href']
            driver.get(f"https://cafe.naver.com{article_url}")
            time.sleep(5)

            # Switch to the iframe containing the article content
            try:
                article_iframe = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "cafe_main"))
                )
                driver.switch_to.frame(article_iframe)
            except Exception as e:
                print(f"Error switching to article iframe: {e}")
                continue

            # Extract text and image from the detailed view
            detailed_soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract text content
            text_content_div = detailed_soup.find('div', class_="se-module se-module-text")
            if text_content_div:
                text_content = text_content_div.get_text(separator='\n').strip()
                with open(f"{post_folder}/{post_date} text.txt", 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text_content)
            else:
                print("Text not found")

            # Extract image if exists
            image_div = detailed_soup.find('div', class_='se-module se-module-image')
            if image_div:
                image_tag = image_div.find('img', class_='se-image-resource')
                if image_tag:
                    image_url = image_tag['src']
                    image_data = requests.get(image_url).content
                    with open(f"{post_folder}/{post_date} image.jpg", 'wb') as img_file:
                        img_file.write(image_data)

        break
        # Return to the main forum page and reinitialize the iframe
    try:
        driver.get("https://cafe.naver.com/stockseeker")
        time.sleep(5)
        driver.find_element(By.ID, "menuLink4").click()
        time.sleep(5)
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cafe_main"))
        )
        driver.switch_to.frame(iframe)
    except Exception as e:
        print(f"Error returning to the forum page: {e}")
# Main function to handle pagination
def main():
    c = 1
    total = 1
    
    while True:
        try:
            # Extract and save post content for the current page
            extract_and_save_content(driver, forum_number)

            # Locate the pagination div
            pagination_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "prev-next"))
            )

            # Find all page links
            page_links = pagination_div.find_elements(By.TAG_NAME, "a")

            # Check if the current page is the last one in the current pagination window
            if c < len(page_links) and not ("pgR" in page_links[c].get_attribute("class")):
                # Click the next page link
                next_page_link = page_links[c]
                next_page_link.click()
                time.sleep(5)
                c += 1
                total += 1
                print(f"Moved to page {total}")
            else:
                # Check if the last link has the 'pgR' class
                if "pgR" in page_links[-1].get_attribute("class"):
                    # Click the 'pgR' link to move to the next set of pagination links
                    page_links[-1].click()
                    time.sleep(5)
                    c = 1  # Reset the counter for the next set of pagination links
                    print("Moved to next set of pagination links")
                else:
                    print("No more pages to navigate")
                    break
        except Exception as e:
            print("No more pages to navigate, exception:", e)
            break

    driver.quit()

if __name__ == "__main__":
    main()
