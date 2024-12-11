import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Selenium WebDriver
def initialize_driver():
    driver = webdriver.Chrome()  # Ensure you have the correct ChromeDriver installed
    driver.get("https://cafe.naver.com/stockseeker")
    time.sleep(5)  # Wait for the page to load
    return driver

# Navigate to the specific forum and switch to the iframe
def navigate_to_forum(driver, forum_id="menuLink4"):
    try:
        driver.find_element(By.ID, forum_id).click()
        time.sleep(5)  # Allow page to load
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cafe_main"))
        )
        driver.switch_to.frame(iframe)
    except Exception as e:
        print(f"Error navigating to forum or switching to iframe: {e}")
        driver.quit()
        raise

# Set the number of posts displayed per page to 50
def set_posts_per_page(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'listSizeSelectDiv'))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="listSizeSelectDiv"]/ul/li[7]/a'))
        ).click()
        time.sleep(5)
    except Exception as e:
        print(f"Error setting posts per page: {e}")

# Extract and save post content
def extract_and_save_content(driver, forum_number, forum_id):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    posts = soup.select('#main-area > div:nth-child(4) > table > tbody > tr')
    
    for post in posts:
        post_date = post.find('td', class_='td_date').text.strip().replace(".", "")  # Extract post date
        post_folder = f"Forum{forum_number}/{post_date}"
        os.makedirs(post_folder, exist_ok=True)

        article_link = post.find('a', class_='article')
        if article_link:
            article_url = article_link['href']
            driver.get(f"https://cafe.naver.com{article_url}")
            time.sleep(5)

            try:
                article_iframe = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "cafe_main"))
                )
                driver.switch_to.frame(article_iframe)
            except Exception as e:
                print(f"Error switching to article iframe: {e}")
                continue

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
        
    return_to_forum(driver, forum_id)  # Pass the forum_id dynamically



# Return to the main forum page and reinitialize iframe for a specific forum
def return_to_forum(driver, forum_id):
    try:
        driver.get("https://cafe.naver.com/stockseeker")
        time.sleep(5)  # Allow the main page to load
        navigate_to_forum(driver, forum_id)  # Navigate back to the specific forum
        set_posts_per_page(driver)  # Reset posts per page
    except Exception as e:
        print(f"Error returning to the forum page for {forum_id}: {e}")
        raise

# Handle pagination logic
def handle_pagination(driver, forum_number, forum_id):
    c = 1
    total = 1

    while True:
        try:
            extract_and_save_content(driver, forum_number, forum_id)

            pagination_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "prev-next"))
            )
            page_links = pagination_div.find_elements(By.TAG_NAME, "a")

            if c < len(page_links) and not ("pgR" in page_links[c].get_attribute("class")):
                next_page_link = page_links[c]
                next_page_link.click()
                time.sleep(5)
                c += 1
                total += 1
                print(f"Moved to page {total}")
            else:
                if "pgR" in page_links[-1].get_attribute("class"):
                    page_links[-1].click()
                    time.sleep(5)
                    c = 1
                    print("Moved to next set of pagination links")
                else:
                    print("No more pages to navigate")
                    break
        except Exception as e:
            print(f"No more pages to navigate, exception: {e}")
            break

# Main function
def main():
    forums = [
        {"forum_number": 4, "forum_id": "menuLink8"},
        {"forum_number": 6, "forum_id": "menuLink4"},
    ]
    
    driver = initialize_driver()

    try:
        for forum in forums:
            print(f"Processing forum {forum['forum_number']}...")
            navigate_to_forum(driver, forum['forum_id'])
            set_posts_per_page(driver)
            handle_pagination(driver, forum['forum_number'], forum['forum_id'])
            print(f"Finished processing forum {forum['forum_number']}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

