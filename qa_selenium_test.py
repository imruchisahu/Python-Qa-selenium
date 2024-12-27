import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Configurable constants
URL = "https://www.lambdatest.com/selenium-playground/table-sort-search-demo"
SEARCH_TERM = "New York"
EXPECTED_RESULTS = 5
TOTAL_ENTRIES = 24

@pytest.fixture(scope="module")
def setup_browser():
    """Setup the WebDriver and return the browser instance."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Uncomment the next line to use Firefox instead of Chrome
    # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_validate_search_functionality(setup_browser):
    """Test the search functionality of the table."""
    driver = setup_browser

    # Navigate to the target URL
    driver.get(URL)

    # Locate the search input box and perform the search
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']"))
    )
    search_box.clear()
    search_box.send_keys(SEARCH_TERM)

    # Validate search results
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#example tbody tr"))
    )

    # Exclude rows without actual content (empty rows due to incorrect matches)
    visible_rows = [row for row in rows if row.is_displayed()]
    print(f"Total rows found: {len(rows)}")
    print(f"Visible rows: {len(visible_rows)}")

    # Try to assert the visible rows count and handle AssertionError
    try:
        # Assert the number of visible rows matches the expected results
        assert len(visible_rows) == EXPECTED_RESULTS, (
            f"Expected {EXPECTED_RESULTS} rows, but found {len(visible_rows)}"
        )
    except AssertionError as e:
        print(f"Assertion Error: {str(e)}")
        # You can also log this error to a file, or take a screenshot if needed
        driver.save_screenshot("search_test_error.png")
        raise  # Re-raise the error if you want the test to fail after logging

    # Validate the total entries text
    total_entries_text = driver.find_element(By.ID, "example_info").text
    expected_text_fragment = f"(filtered from {TOTAL_ENTRIES} total entries)"
    try:
        assert expected_text_fragment in total_entries_text, (
            f"Expected '{expected_text_fragment}' in total entries text, but got '{total_entries_text}'"
        )
    except AssertionError as e:
        print(f"Assertion Error: {str(e)}")
        # You can take additional action if necessary, such as capturing the screen
        driver.save_screenshot("total_entries_error.png")
        raise # Re-raise the error if you want the test to fail after logging

# README content
README_CONTENT = """
# Selenium Search Functionality Test

This script tests the search functionality on the LambdaTest Selenium Playground's Table Sort/Search Demo.

## Prerequisites
1. **Environment Requirements:**
   - Python 3.8 or newer installed.
   - Google Chrome or Mozilla Firefox browser installed.

2. **Dependencies:**
   Install the required Python packages by running:

   ''' 
   pip install -r requirements.txt
   '''
   
   The `requirements.txt` file should include:
   '''
   selenium
   pytest
   webdriver-manager
   '''

3. **WebDriver Setup:**
   - Chrome: Ensure `chromedriver` is installed via `webdriver-manager`.
   - Firefox: Install `geckodriver` via `webdriver-manager` (if using Firefox).
 

## Approach

1.**Test Objective:**
   - Validate the search functionality by entering a search term (`New York`) in the search box and ensuring 
   that the results match expectations.

2. **Setup**: The script initializes a Chrome browser instance using `webdriver_manager`.
3. **Test Execution**:
   - Navigates to the specified URL.
   - Locates the search box and inputs the term "New York."
   - Validates the displayed search results match the expected number (5 entries out of 24 total).
4. **Validation**:
   - Asserts the number of visible rows after filtering.
   - Confirms the total number of rows before filtering.

5.**Test Framework:**
   - The test script uses `pytest` for test case structuring and Selenium WebDriver for browser automation.
6.**Teardown**: Closes the browser once the test completes.



## How to Run the Test

1. Clone this repository or copy the script files to your local machine.
2. Open a terminal and navigate to the folder containing the test script.
3. Run the test using the following command:

   '''bash
   pytest qa_selenium_test.py
   '''

4. View the test results in the terminal output.


## Additional Notes

- The test script is compatible with the latest stable Selenium version.
- To switch between Chrome and Firefox:
  - Uncomment the respective driver initialization line in the `setup_browser` fixture.
- Ensure a stable internet connection, as the test requires accessing a live website.


#### Code Quality
The script adheres to PEP8 standards, uses robust assertion statements, and employs a modular structure for easy maintenance and scalability.
""" 

if __name__ == "__main__":
    with open("README.md", "w") as readme_file:
        readme_file.write(README_CONTENT)
    print("README.md created successfully.")
    pytest.main(["-v", "qa_selenium_test.py"])

