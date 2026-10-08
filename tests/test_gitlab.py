from selenium import webdriver


def test_github():
    driver = webdriver.Chrome()
    url = "https://github.com/"
    driver.get(url)

    assert "GitHub" in driver.title
    assert driver.current_url == url
