import pytest
from selenium import webdriver

from table_page_element_example import TablesPage


@pytest.fixture
def page():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    try:
        tables_page = TablesPage(driver)
        tables_page.open()
        yield tables_page
    finally:
        driver.quit()


def test_headers_in_both_tables(page):
    expected = ["Last Name", "First Name", "Email", "Due", "Web Site", "Action"]
    assert page.table1.get_headers() == expected
    assert page.table2.get_headers() == expected


def test_data_in_both_tables(page):
    expected = ["Smith", "John", "jsmith@gmail.com", "$50.00", "http://www.jsmith.com", "edit delete"]
    for table in (page.table1, page.table2):
        assert table.get_row_data(0) == expected
        assert table.get_cell_value(2, 3) == "$100.00"


def test_sorting_tables_is_independent(page):
    page.table1.sort_by_column(0)
    assert [page.table1.get_cell_value(i, 0) for i in range(4)] == [
        "Bach", "Conway", "Doe", "Smith"
    ]
    assert page.table2.get_cell_value(0, 0) == "Smith"

    page.table2.sort_by_column(3)
    assert [page.table2.get_cell_value(i, 3) for i in range(4)] == [
        "$50.00", "$50.00", "$51.00", "$100.00"
    ]
    assert page.table1.get_cell_value(0, 0) == "Bach"
