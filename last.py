total = 1
c = 1
while True:
    try:
        # Extract and save post content for the current page

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
            total+=1
            print(f"Moved to page {total}")
        else:
            # Check if the last link has the 'pgR' class
            if "pgR" in page_links[-1].get_attribute("class"):
                # Click the 'pgR' link to move to the next set of pagination links
                page_links[-1].click()
                time.sleep(5)
                c = 1  # Reset the counter for the next set of pagination links
                print(f"Moved to next set of pagination links")
            else:
                print("No more pages to navigate")
                break
    except:
        print("No more pages to navigate exept")
        break
