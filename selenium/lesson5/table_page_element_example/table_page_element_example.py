from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumpagefactory.Pagefactory import PageFactory


class TableElement(PageFactory):
    """Page Element: все действия выполняются внутри своей таблицы."""

    def __init__(self, driver, locator):
        self.driver = driver
        # PageFactory находит корневой элемент при обращении к self.root.
        self.locators = {"root": locator}

    @property
    def element(self):
        return self.root

    def get_headers(self) -> list[str]:
        return [header.text for header in self.element.find_elements(By.CSS_SELECTOR, "thead th")]

    def get_row_data(self, row_index: int) -> list[str]:
        """Возвращает ячейки строки; индексы начинаются с 0."""
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        return [cell.text for cell in rows[row_index].find_elements(By.TAG_NAME, "td")]

    def get_cell_value(self, row_index: int, column_index: int) -> str:
        return self.get_row_data(row_index)[column_index]

    def sort_by_column(self, column_index: int):
        self.element.find_elements(By.CSS_SELECTOR, "thead th")[column_index].click()


class TablesPage:
    URL = "https://the-internet.herokuapp.com/tables"

    def __init__(self, driver):
        self.driver = driver
        # Одинаковый компонент работает с двумя независимыми таблицами.
        self.table1 = TableElement(driver, ("ID", "table1"))
        self.table2 = TableElement(driver, ("ID", "table2"))

    def open(self):
        self.driver.get(self.URL)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    try:
        page = TablesPage(driver)
        page.open()
        for table in (page.table1, page.table2):
            print("Заголовки таблицы:", table.get_headers())
            print("Первая строка данных:", table.get_row_data(0))
            assert "Last Name" in table.get_headers()
            assert table.get_cell_value(0, 0) == "Smith"
            assert table.get_cell_value(2, 3) == "$100.00"
        print("Обе таблицы успешно проверены!")
    finally:
        driver.quit()
