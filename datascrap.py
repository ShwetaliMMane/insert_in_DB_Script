# ------Scrap Data on Website----------

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_ingredients(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)  

    # Scroll to the bottom of the page to ensure all elements load
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Retrieve ingredients list
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'woosg-title'))
        )
        ingredients = driver.find_elements(By.CLASS_NAME, 'woosg-title')  

        if ingredients:
            # Print all ingredients
            print("Ingredient list:")
            for ingredient in ingredients:
                print(ingredient.text)
            
            # Print the first ingredient specifically
            print("\nFirst ingredient:", ingredients[0].text.split ('\n'))
        else:
            print("No ingredients found.")

    except Exception as e:
        print("Ingredient list not found or took too long to load:", e)

    driver.quit()

url = 'https://anyfeast.in/recipe/appam/'  
scrape_ingredients(url)
