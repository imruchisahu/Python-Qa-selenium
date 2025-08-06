
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
