from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Calendar:
    def __init__(self, driver, base_element):
        self.driver = driver
        self.input_field = base_element

    def select_date(self, day: str, month: str, year: str):
        wait = WebDriverWait(self.driver, 5)
        close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fixedban button")))
        close_button.click()
        wait.until(EC.invisibility_of_element_located((By.ID, "fixedban")))

        self.input_field.click()
        month_select = self.driver.find_element(By.CSS_SELECTOR, ".react-datepicker__month-select")
        Select(month_select).select_by_visible_text(month)
        year_select = self.driver.find_element(By.CSS_SELECTOR, ".react-datepicker__year-select")
        Select(year_select).select_by_visible_text(year)
        day_padded = day.zfill(3)  # Например, "15" превращается в "015".
        self.driver.find_element(
            By.CSS_SELECTOR,
            f".react-datepicker__day--{day_padded}:not(.react-datepicker__day--outside-month)",
        ).click()


class AutomationPracticeFormPage:
    def __init__(self, driver):
        driver.get("https://qa-guru.github.io/one-page-form/automation-practice-form.html")
        self.birthday_calendar = Calendar(driver, driver.find_element(By.ID, "dateOfBirthInput"))


class TestSuite:
    def __init__(self, driver):
        self.driver = driver

    def test_select_birthday_date(self):
        page = AutomationPracticeFormPage(self.driver)
        page.birthday_calendar.select_date(day="15", month="July", year="2000")
        assert page.birthday_calendar.input_field.get_attribute("value") == "15 Jul 2000"


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    try:
        ts = TestSuite(driver)
        ts.test_select_birthday_date()
        print("Дата выбрана верно: 15 Jul 2000")
    finally:
        driver.quit()
