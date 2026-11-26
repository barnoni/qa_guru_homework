import os
import tempfile
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Из корня проекта: python -m unittest discover -s selenium/lesson3 -p simple_test_student_registration_form.py

class TestAutomationForm(unittest.TestCase):

    def setUp(self):
        # Инициализация WebDriver (в данном примере Chrome)
        #options = webdriver.ChromeOptions()
        #options.add_argument("--window-size=1920,1080")
        # Раскомментируйте строку ниже, если хотите запустить в фоновом режиме:
        # options.add_argument("--headless")
        #self.driver = webdriver.Chrome(options=options)

        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)  # Явное ожидание до 5 секунд
        self.url = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

        self.driver.get(self.url)

        # Закрываем промобаннер, чтобы он не перекрывал поля формы.
        close_banner = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#fixedban button"))
        )
        close_banner.click()
        self.wait.until(EC.invisibility_of_element_located((By.ID, "fixedban")))

        # Закрепленный футер перехватывает клики по нижним полям и Submit.
        self.driver.execute_script("document.querySelector('footer').style.display = 'none';")

    def test_fill_entire_form(self):
        driver = self.driver

        # 0. Проверяем заголовок и подзаголовок формы.
        form_title = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "main h1")))
        self.assertEqual(form_title.text, "Practice Form")

        form_sub_title = driver.find_element(By.CSS_SELECTOR, "main .subtitle")
        self.assertEqual(form_sub_title.text, "Student Registration Form")

        # 2. Текстовые поля: Имя и Фамилия
        first_name = self.wait.until(EC.element_to_be_clickable((By.ID, "firstName")))
        first_name.send_keys("Иван")

        last_name = driver.find_element(By.ID, "lastName")
        last_name.send_keys("Петров")

        # 3. Текстовое поле: Email
        email = driver.find_element(By.ID, "userEmail")
        email.send_keys("ivan.petrov@example.com")

        # 4. Радиокнопки (Gender): кликаем по подписи <label>, связанной с радиокнопкой
        gender_male_label = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='gender-radio-1']")))
        gender_male_label.click()

        # 5. Текстовое поле: Номер телефона (Mobile)
        mobile_number = driver.find_element(By.ID, "userNumber")
        mobile_number.send_keys("9991234567")

        # 6. Виджет календаря (Date of Birth)
        date_input = driver.find_element(By.ID, "dateOfBirthInput")
        date_input.click()

        # Ожидаем появление всплывающего окна календаря
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "react-datepicker__month-container")))

        # Выбираем месяц (декабрь) через выпадающий список внутри календаря
        month_select = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__month-select")))
        month_select.click()
        month_select.find_element(By.XPATH, "//option[@value='11']").click()  # 11 — это Декабрь

        # Выбираем год (1995)
        year_select = driver.find_element(By.CLASS_NAME, "react-datepicker__year-select")
        year_select.click()
        year_select.find_element(By.XPATH, "//option[@value='1995']").click()

        # Выбираем конкретный день месяца (например, 25-е число)
        # Используем специальный класс react-datepicker__day--025, исключая дни соседних месяцев (outside-month)
        day_element = driver.find_element(By.CSS_SELECTOR, ".react-datepicker__day--025:not(.react-datepicker__day--outside-month)")
        day_element.click()

        # 7. Поле автодополнения (Subjects)
        subjects_input = self.wait.until(EC.element_to_be_clickable((By.ID, "subjectsInput")))
        subjects_input.send_keys("Computer Science")
        subjects_input.send_keys(Keys.ENTER)

        # 8. Чекбоксы (Hobbies): кликаем по связанному <label>
        hobby_sports = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']"))
        )
        hobby_sports.click()

        hobby_music = driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-3']")
        hobby_music.click()

        # 9. Загрузка файла (Picture)
        # Создаем временный файл для теста, чтобы код оставался переносимым
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        temp_file_path = os.path.join(temp_dir.name, "test_image.jpg")
        with open(temp_file_path, "w") as f:
            f.write("fake image data")

        upload_input = driver.find_element(By.ID, "uploadPicture")
        upload_input.send_keys(temp_file_path)

        # 10. Текстовая область: Текущий адрес (Current Address)
        current_address = driver.find_element(By.ID, "currentAddress")
        current_address.send_keys("123456, г. Москва, ул. Ленина, д. 1")

        # 11. Выпадающий список (Dropdown): Выбор Штата (State)
        state_dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, "state")))
        state_dropdown.click()
        # Ждем появления пункта NCR и кликаем по нему.
        state_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='stateCity-wrapper']/div[. = 'NCR']")))
        state_option.click()

        # 12. Выпадающий список (Dropdown): Выбор Города (City)
        city_dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, "city")))
        city_dropdown.click()
        city_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='stateCity-wrapper']/div[. = 'Delhi']")))
        city_option.click()

        # 13. Отправка формы (Submit)
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        # 14. Проверка результатов (Expected Conditions для модального окна)
        # Проверяем, что появилось финальное окно с подтверждением
        modal_title = self.wait.until(
            EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg"))
        )
        self.assertEqual(modal_title.text, "Thanks for submitting the form")

        # Проверяем наличие валидных данных в таблице результатов
        result_table = driver.find_element(By.CLASS_NAME, "table-responsive")
        self.assertIn("Иван Петров", result_table.text)
        self.assertIn("ivan.petrov@example.com", result_table.text)
        self.assertIn("Male", result_table.text)
        self.assertIn("9991234567", result_table.text)
        self.assertIn("25 Dec 1995", result_table.text)
        self.assertIn("Computer Science", result_table.text)
        self.assertIn("Sports, Music", result_table.text)
        self.assertIn("test_image.jpg", result_table.text)
        self.assertIn("123456, г. Москва, ул. Ленина, д. 1", result_table.text)
        self.assertIn("NCR Delhi", result_table.text)

    def _fill_required_fields(self, first_name="Анна", last_name="Смирнова",
                              select_gender=True, mobile="0123456789"):
        self.driver.find_element(By.ID, "firstName").send_keys(first_name)
        self.driver.find_element(By.ID, "lastName").send_keys(last_name)
        if select_gender:
            self.driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-2']").click()
        self.driver.find_element(By.ID, "userNumber").send_keys(mobile)

    def _assert_submission_rejected(self):
        self.driver.find_element(By.ID, "submit").click()
        error = self.wait.until(EC.visibility_of_element_located((By.ID, "formError")))
        self.assertEqual(
            error.text,
            "Please fill required fields and enter a valid 10-digit mobile number.",
        )
        self.assertFalse(self.driver.find_element(By.ID, "resultModal").is_displayed())

    def test_submit_required_fields_only(self):
        self._fill_required_fields()
        self.driver.find_element(By.ID, "submit").click()

        modal = self.wait.until(EC.visibility_of_element_located((By.ID, "resultModal")))
        rows = modal.find_elements(By.CSS_SELECTOR, "#resultBody tr")
        actual = {}
        for row in rows:
            label, value = row.find_elements(By.TAG_NAME, "td")
            actual[label.text] = value.text

        self.assertEqual(actual, {
            "Student Name": "Анна Смирнова",
            "Student Email": "-",
            "Gender": "Female",
            "Mobile": "0123456789",
            "Date of Birth": "-",
            "Subjects": "-",
            "Hobbies": "-",
            "Picture": "-",
            "Address": "-",
            "State and City": "-",
        })

    def test_submit_without_first_name(self):
        self._fill_required_fields(first_name="")
        self._assert_submission_rejected()

    def test_submit_without_last_name(self):
        self._fill_required_fields(last_name="")
        self._assert_submission_rejected()

    def test_submit_without_gender(self):
        self._fill_required_fields(select_gender=False)
        self._assert_submission_rejected()

    def test_submit_without_mobile(self):
        self._fill_required_fields(mobile="")
        self._assert_submission_rejected()

    def test_submit_with_nine_digit_mobile(self):
        self._fill_required_fields(mobile="123456789")
        self._assert_submission_rejected()

    def test_submit_with_letter_in_mobile(self):
        self._fill_required_fields(mobile="12345a7890")
        self._assert_submission_rejected()

    def test_changing_state_resets_city(self):
        state = self.driver.find_element(By.ID, "state")
        city = self.driver.find_element(By.ID, "city")
        dropdown = self.driver.find_element(By.ID, "stateCity-wrapper")

        state.click()
        dropdown.find_element(By.XPATH, "./div[. = 'NCR']").click()
        city.click()
        dropdown.find_element(By.XPATH, "./div[. = 'Delhi']").click()
        self.assertEqual(city.text, "Delhi")

        state.click()
        dropdown.find_element(By.XPATH, "./div[. = 'Haryana']").click()
        self.assertEqual(city.text, "Select City")

        city.click()
        options = dropdown.find_elements(By.CLASS_NAME, "state-city-option")
        self.assertEqual([option.text for option in options], ["Karnal", "Panipat"])

if __name__ == "__main__":
    unittest.main()
