from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class Calendar:
    def __init__(self, driver):
        self.driver = driver

    CALENDAR_INPUT = (By.ID, "dateOfBirthInput")
    YEAR_SELECT = (By.CSS_SELECTOR, ".react-datepicker__year-select")
    MONTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__month-select")

    def select_date(self, date):
        year, month, day = date
        self.driver.find_element(*self.CALENDAR_INPUT).click()
        Select(self.driver.find_element(*self.YEAR_SELECT)).select_by_value(year)
        Select(self.driver.find_element(*self.MONTH_SELECT)).select_by_value(month)
        day_class = f".react-datepicker__day--{int(day):03d}"
        self.driver.find_element(
            By.CSS_SELECTOR,
            day_class + ":not(.react-datepicker__day--outside-month)",
        ).click()

