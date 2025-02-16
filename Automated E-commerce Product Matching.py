#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import re
from difflib import SequenceMatcher

# Set up Chrome WebDriver
service = Service(executable_path="chromedriver.exe")  # Provide the correct path to your driver
driver = webdriver.Chrome(service=service)

# Function to clean text by removing special characters
def clean_text(text):
    return re.sub(r'[^A-Za-z0-9 ]+', '', text).lower().strip()

# Function to calculate match percentage
def calculate_match_percentage(text1, text2):
    text1_clean = clean_text(text1)
    text2_clean = clean_text(text2)
    return round(SequenceMatcher(None, text1_clean, text2_clean).ratio() * 100, 2)

# Function to extract product details
def extract_product_details(driver, title_path, price_path):
    product_title = "Title not available"
    product_price = "Price not available"
    
    try:
        # Extract Product Title
        try:
            title_element = driver.find_element(By.XPATH, title_path)
            product_title = title_element.text.strip()
        except:
            pass
        
        # Extract Price
        try:
            price_element = driver.find_element(By.XPATH, price_path)
            product_price = price_element.text.strip()
        except:
            pass
    except Exception as e:
        print(f"Error occurred while extracting product details: {e}")
    
    return product_title, product_price

# Function to process each row and extract details
def process_model_and_get_details(row):
    model_number = row['model_number.value']
    item_name = row['item_name.value']
    base_search_url = row['base_search_url']
    title_path = row['Title_path']
    price_path = row['price_path']
    results_path = row['Results_path']  # XPath to count search results
    search_url = f"{base_search_url}{model_number}"
    
    driver.get(search_url)
    time.sleep(3)

    result = {
        'Search Result Url': search_url,
        '1st Product URL': None,
        '1st Product Title': None,
        '1st Product Price': None,
        'Match with model number yes/no': "No",
        'Match % of item name vs product title': 0.0,
        'Number_of_results': 0  
    }
    
    try:
        # Get the number of search results
        try:
            results_element = driver.find_element(By.XPATH, results_path)
            result_text = results_element.text
            match = re.search(r'\d+', result_text)  
            if match:
                result['Number_of_results'] = int(match.group())
        except:
            print(f"No search results found for model: {model_number}")
        
        # Get the first product URL
        try:
            product_url_element = driver.find_element(By.XPATH, row['1st Product Link'])
            product_url = product_url_element.get_attribute("href")
            result['1st Product URL'] = product_url
        except:
            print(f"No product URL found for model: {model_number}")
            return result
        
        # Visit product page
        driver.get(product_url)
        time.sleep(3)
        
        # Extract product details
        product_title, product_price = extract_product_details(driver, title_path, price_path)
        result['1st Product Title'] = product_title
        result['1st Product Price'] = product_price

        # Check model number match
        if model_number in product_title:
            result['Match with model number yes/no'] = "Yes"
        
        # Calculate match percentage
        result['Match % of item name vs product title'] = calculate_match_percentage(item_name, product_title)
    
    except Exception as e:
        print(f"Error occurred for model number {model_number}: {e}")
    
    return result

# Load the input CSV file
input_file = "input_data.csv"  # Provide the input file path
output_file = input_file.replace(".csv", "_updated.csv")
df = pd.read_csv(input_file)

# Ensure the new column is added
if 'Number_of_results' not in df.columns:
    df['Number_of_results'] = 0

# Iterate through each row
for index, row in df.iterrows():
    print(f"Processing row {index + 1} with model number: {row['model_number.value']}")
    details = process_model_and_get_details(row)
    
    # Update DataFrame with extracted details
    df.at[index, 'Search Result Url'] = details['Search Result Url']
    df.at[index, '1st Product URL'] = details['1st Product URL']
    df.at[index, '1st Product Title'] = details['1st Product Title']
    df.at[index, '1st Product Price'] = details['1st Product Price']
    df.at[index, 'Match with model number yes/no'] = details['Match with model number yes/no']
    df.at[index, 'Match % of item name vs product title'] = details['Match % of item name vs product title']
    df.at[index, 'Number_of_results'] = details['Number_of_results']  

# Save updated CSV file
df.to_csv(output_file, index=False)
print(f"Updated file saved at: {output_file}")

# Quit WebDriver
driver.quit()


