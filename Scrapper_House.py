from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


# Create webdriver
driver = webdriver.Chrome()
driver.get("https://www.hepsiemlak.com/istanbul-satilik")

# Wait for the page to load
time.sleep(5)

# Dismiss the cookie
def dismiss_cookie_policy():
    try:
        cookie_policy = driver.find_element(By.XPATH, '//*[@class="cookie-policy"]')
        close_button = cookie_policy.find_element(By.XPATH, './/button')
        close_button.click()
        print("Cookie policy closed.")
    except:
        pass  # No cookie popup, continue

def random_sleep():
    time.sleep(random.uniform(3, 8))

# Scrape listings
def get_article_urls(target_count=250):
    data = []
    page_num = 0

    while len(data) < target_count:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//article'))
            )
        except:
            print("Articles not found, or timed out.")
            break

        # Get all articles
        articles = driver.find_elements(By.XPATH, '//article')

        for article in articles:
            if len(data) >= target_count:
                break  # Stop when have enough data

            # Extract listing URL
            try:
                link_element = article.find_element(By.XPATH, './/a[@href]')
                listing_url = link_element.get_attribute("href")
            except:
                continue  # Skip if no link

            # Open listing in a new tab
            random_sleep()
            driver.execute_script("window.open(arguments[0]);", listing_url)
            driver.switch_to.window(driver.window_handles[1])  # Switch to new tab
            time.sleep(2)  # Wait for it to load

            try:
                price = driver.find_element(By.CSS_SELECTOR,
                                            '#__layout > div > div > section.wrapper.detail-page.detail-page-wrapper > div:nth-child(3) > div.det-content.cont-block.left > div.cont-inner > div.realty-wrap > div.detail-info-wrap > div.detail-modal-price-wrap > div.detail-price-wrap > p').text.split()[
                    0]
            except:
                price = 'N/A'

            try:
                neighborhood = driver.find_element(By.CSS_SELECTOR,
                                                   '#__layout > div > div > section.wrapper.detail-page.detail-page-wrapper > div:nth-child(3) > div.det-content.cont-block.left > div.cont-inner > div.realty-wrap > div.detail-info-wrap > ul > li:nth-child(2)').text.strip()
            except:
                neighborhood = 'N/A'

            try:
                building_type = driver.find_element(By.CSS_SELECTOR,
                                                    '#__layout > div > div > section.wrapper.detail-page.detail-page-wrapper > div:nth-child(3) > div.det-content.cont-block.left > div.cont-inner > div.realty-wrap > div.detail-info-wrap > div.det-adv-info > div > ul > li:nth-child(4) > div:nth-child(2) > span').text.strip()
            except:
                building_type = 'N/A'

            try:
                room_count = driver.find_element(By.CSS_SELECTOR,
                                                 '#__layout > div > div > section.wrapper.detail-page.detail-page-wrapper > div:nth-child(3) > div.det-content.cont-block.left > div.cont-inner > div.realty-wrap > div.detail-info-wrap > div.det-adv-info > div > ul > li:nth-child(6) > div:nth-child(2) > span').text.strip()
            except:
                room_count = 'N/A'

            try:
                toilet_count = driver.find_element(By.CSS_SELECTOR,
                                                   '#__layout > div > div > section.wrapper.detail-page.detail-page-wrapper > div:nth-child(3) > div.det-content.cont-block.left > div.cont-inner > div.realty-wrap > div.detail-info-wrap > div.det-adv-info > div > ul > li:nth-child(7) > div:nth-child(2) > span').text.strip()
            except:
                toilet_count = 'N/A'

            try:
                size = driver.find_element(By.CSS_SELECTOR,
                                           '#__layout > div > div > section.wrapper.detail-page.detail-page-wrapper > div:nth-child(3) > div.det-content.cont-block.left > div.cont-inner > div.realty-wrap > div.detail-info-wrap > div.det-adv-info > div > ul > li:nth-child(8) > span:nth-child(3)').text
            except:
                size = 'N/A'

            try:
                building_age = driver.find_element(By.CSS_SELECTOR,
                                                   '#__layout > div > div > section.wrapper.detail-page.detail-page-wrapper > div:nth-child(3) > div.det-content.cont-block.left > div.cont-inner > div.realty-wrap > div.detail-info-wrap > div.det-adv-info > div > ul > li:nth-child(11) > div:nth-child(2) > span').text.split()[
                    0]
            except:
                building_age = 'N/A'

            try:
                heating_type = driver.find_element(By.CSS_SELECTOR,
                                                   '#__layout > div > div > section.wrapper.detail-page.detail-page-wrapper > div:nth-child(3) > div.det-content.cont-block.left > div.cont-inner > div.realty-wrap > div.detail-info-wrap > div.det-adv-info > div > ul > li:nth-child(12) > div:nth-child(2) > span').text.strip()
            except:
                heating_type = 'N/A'

            # For floor
            try:
                floor = driver.find_element(By.CSS_SELECTOR,
                                            '#__layout > div > div > section.wrapper.detail-page.detail-page-wrapper > div:nth-child(3) > div.det-content.cont-block.left > div.cont-inner > div.realty-wrap > div.detail-info-wrap > div.det-adv-info > div > ul > li:nth-child(10) > div:nth-child(2) > span').text.strip()
            except:
                floor = 'N/A'



            # Store data
            article_data = {
                'price': price,
                'room_count': room_count,
                'toilet_count': toilet_count,
                'size': size,
                'heating_type': heating_type,
                'building_age': building_age,
                'building_type': building_type,
                'neighborhood': neighborhood,
                'floor': floor
            }
            data.append(article_data)

            # Close tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        # Go to next page
        if len(data) < target_count:
            dismiss_cookie_policy()
            try:
                random_sleep()
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Sonraki Sayfa")]'))
                )
                driver.execute_script("arguments[0].click();", next_page_button)
                time.sleep(5)
            except:
                break

    return data

# Start scraping
article_data = get_article_urls()

# Print preview
print(f"Scraped {len(article_data)} articles.")
for item in article_data[:5]:
    print(item)

# Close driver
driver.quit()

import pandas as pd
df = pd.DataFrame(article_data)
df.to_csv("scraped_data3.csv", index=False)
print("Data saved to scraped_data2.csv")