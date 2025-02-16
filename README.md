# Automated_Product_Matching
This script automates product matching by extracting details from e-commerce search results using Selenium. Given an input CSV file containing model numbers and search URLs

## Description
This project automates product matching by extracting details from e-commerce search results using Selenium. Given an input CSV file containing model numbers and search URLs, the script:

- Searches for the product on an e-commerce website.
- Extracts the first product's title, price, and URL.
- Counts the number of search results.
- Matches the retrieved product title with the expected model name and calculates a similarity score.
- Saves the results in an updated CSV file.

This automation is useful for e-commerce analytics, price monitoring, and product matching.

## Features
- Automated web scraping using Selenium
- Data extraction from e-commerce search results
- Product matching using text similarity
- CSV-based input and output for easy processing

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Google Chrome
- Chrome WebDriver
- Required Python libraries:
  ```sh
  pip install selenium pandas
  ```

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/automated-ecommerce-matching.git
   cd automated-ecommerce-matching
   ```
2. Place your `chromedriver.exe` in the project directory.
3. Add your input CSV file (`input_data.csv`) in the same directory.

## Usage
Run the script using:
```sh
python script.py
```

## Input File Format
The input CSV should contain the following columns:
- `model_number.value`
- `item_name.value`
- `base_search_url`
- `Title_path`
- `price_path`
- `Results_path`
- `1st Product Link`

## Output
An updated CSV file is generated with:
- Search Result URL
- First Product URL
- First Product Title
- First Product Price
- Model match status (Yes/No)
- Match percentage with expected model name
- Number of search results

## Disclaimer
This project is created for **educational purposes only**. Ensure compliance with e-commerce website policies when using web scraping techniques.

## License
MIT License

