from selenium import webdriver


def test_selenium():
    driver = webdriver.Chrome()
    url = "https://www.selenium.dev/"
    driver.get(url)

    assert "Selenium" in driver.title
    assert driver.current_url == url
