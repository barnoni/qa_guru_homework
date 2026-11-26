import os
import automation_practice_form_po

class AutomationPracticeFormTestSuite:
    def __init__(self):
        self.automation_practice_form = automation_practice_form_po.AutomationPracticeFormPO("https://qa-guru.github.io/one-page-form/automation-practice-form.html")

    def setup(self):
        self.automation_practice_form.setup()
        self.tmp_file_name = self._create_tmp_file()

    def _create_tmp_file(self):
        file_path = os.path.abspath('test_file.jpg')
        with open(file_path, 'w') as file:
            file.write("Test")
        return file_path
    
    def test_form_positive01(self):
        self.automation_practice_form.fill_in_form(self.tmp_file_name, "Dmitry","Bugaev", "bugaev@example.com", "Male","1234567890",("1988", "4", "22"),("Maths", "English"), ("Sports", "Music"), "г. Санкт-Петербург, ул. Невский проспект, д 101", "NCR",  "Noida")
        self.automation_practice_form.assert_form(self.tmp_file_name, "Dmitry","Bugaev", "bugaev@example.com", "Male","1234567890",("1988", "4", "22"),("Maths", "English"), ("Sports", "Music"), "г. Санкт-Петербург, ул. Невский проспект, д 101", "NCR",  "Noida")

    def test_form_positive02(self):
        self.automation_practice_form.fill_in_form(self.tmp_file_name, "Anna", "Ivanova", "anna.ivanova@example.com", "Female", "9876543210", ("1995", "11", "25"), ("Physics", "Chemistry"), ("Reading",), "г. Москва, ул. Тверская, д. 10", "Haryana", "Karnal")
        self.automation_practice_form.assert_form(self.tmp_file_name, "Anna", "Ivanova", "anna.ivanova@example.com", "Female", "9876543210", ("1995", "11", "25"), ("Physics", "Chemistry"), ("Reading",), "г. Москва, ул. Тверская, д. 10", "Haryana", "Karnal")

    def tear_down(self):
        if os.path.exists(self.tmp_file_name):
            os.remove(self.tmp_file_name)
        self.automation_practice_form.tear_down()


for test in (
    AutomationPracticeFormTestSuite.test_form_positive01,
    AutomationPracticeFormTestSuite.test_form_positive02,
):
    test_suite = AutomationPracticeFormTestSuite()
    try:
        test_suite.setup()
        test(test_suite)
        print(f"{test.__name__}: PASSED")
    finally:
        test_suite.tear_down()
