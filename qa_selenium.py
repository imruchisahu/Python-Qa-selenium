import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest_html import extras

# Configurable constants
URL = "https://www.lambdatest.com/selenium-playground/table-sort-search-demo"
SEARCH_TERM = "New York"
EXPECTED_RESULTS = 5
TOTAL_ENTRIES = 24

@pytest.fixture(scope="module")
def setup_browser():
    """Setup the WebDriver and return the browser instance."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and attach screenshots."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("setup_browser")
        if driver:
            # Create the screenshots directory if it doesn't exist
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            # Save the screenshot
            screenshot_path = os.path.join(screenshots_dir, f"{item.name}.png")
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved at: {screenshot_path}")

            # Attach the screenshot link to the HTML report
            if hasattr(report, "extra"):
                screenshot_link = f"<a href='{screenshots_dir}' target='_blank'>Screenshot</a>"
                report.extra = report.extra or []
                report.extra.append(extras.html(screenshot_link))

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
    visible_rows = [row for row in rows if row.is_displayed()]
    assert len(visible_rows) == EXPECTED_RESULTS, (
        f"Expected {EXPECTED_RESULTS} rows, but found {len(visible_rows)}"
    )

    # Validate the total entries text
    total_entries_text = driver.find_element(By.ID, "example_info").text
    expected_text_fragment = f"(filtered from {TOTAL_ENTRIES} total entries)"
    assert expected_text_fragment in total_entries_text, (
        f"Expected '{expected_text_fragment}' in total entries text, but got '{total_entries_text}'"
    )

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
    

#pytest qa_selenium.py --html=report.html --self-contained-html
#open html report "open -a "Google Chrome" report.html"

