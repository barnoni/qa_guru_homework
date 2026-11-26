from selenium.webdriver.common.by import By
from seleniumpagefactory.Pagefactory import PageFactory

# pip install selenium-page-factory

class TextBoxPage(PageFactory):
    URL = "https://qa-guru.github.io/one-page-form/text-box.html" # Частный случай
    
    def __init__(self, driver):
        self.driver = driver
        self.locators = {
            "full_name_input": ('ID', "userName"),
            "email_input": ('ID', "userEmail"),
            "current_address_input": ('ID', "currentAddress"),
            "permanent_address_input": ('ID', "permanentAddress"),
            "submit_button": ('ID', "submit"),
            "output_box": ('ID', "output"),
            "output_name": ('ID', "name"),
            "output_email": ('ID', "email"),
            "output_current_address": ('CSS', "#output #currentAddress"),
            "output_permanent_address": ('CSS', "#output #permanentAddress")
        }

    def open(self):
        self.driver.get(self.URL)
        return self

    def fill_form(self, name=None, email=None, cur_addr=None, perm_addr=None):
        if name is not None:
            self.full_name_input.clear()
            self.full_name_input.send_keys(name)
        if email is not None:
            self.email_input.clear()
            self.email_input.send_keys(email)
        if cur_addr is not None:
            self.current_address_input.clear()
            self.current_address_input.send_keys(cur_addr)
        if perm_addr is not None:
            self.permanent_address_input.clear()
            self.permanent_address_input.send_keys(perm_addr)
        return self
        
    def submit(self):
        # Прокрутка до кнопки и клик через JS, если перекрыта футером
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.submit_button)
        self.submit_button.click()
        return self

    def get_output_data(self):
        # Возвращает текст из блока вывода, если он появился
        # PageFactory ждёт видимости, но output может быть скрыт при ошибке email.
        if not self.driver.find_element(By.ID, "output").is_displayed():
            return None
        
        # Парсинг строк (удаляем префиксы вроде 'Name:')
        name        = self.output_name.text.removeprefix("Name:").strip()
        email       = self.output_email.text.removeprefix("Email:").strip()
        cur_addr    = self.output_current_address.text.removeprefix("Current Address :").strip()
        perm_addr   = self.output_permanent_address.text.removeprefix("Permananet Address :").strip()
        
        return {"name": name, "email": email, "cur_addr": cur_addr, "perm_addr": perm_addr}

    def is_email_error_present(self):
        # Проверяем наличие класса ошибки у поля Email
        field_class = self.email_input.get_attribute("class") or ""
        return ("field-error" in field_class or "error" in field_class
                or bool(self.driver.find_elements(By.CSS_SELECTOR, "#userEmail:invalid")))

