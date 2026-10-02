import pytest
from selenium import webdriver

# @pytest.mark.selenium
def test_github():
    driver = webdriver.Chrome()
    url = "https://github.com/"
    driver.get(url)

    assert "GitHub" in driver.title
    assert driver.current_url == url