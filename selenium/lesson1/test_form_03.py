import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_form1():
    # 1. Запуск браузера Chrome
    driver = webdriver.Chrome()

    try:
        # 2. Открытие страницы
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()
        time.sleep(1)  # Пауза, чтобы визуально заметить открытие

        # 3. Поиск элементов и заполнение полей
        # Находим поле Full Name по его ID и вводим текст
        full_name_field = driver.find_element(By.ID, "userName")
        # web_elements = driver.find_elements(By.XPATH, "someXPath")

        full_name_field.send_keys("Барно Ниязова")

        # Находим поле Email по его ID и вводим текст
        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys("barno@example.com")

        # Находим поле currentAddress по его ID и вводим адрес
        currentAddress_field = driver.find_element(By.ID, "currentAddress")
        currentAddress_field.send_keys("Г. Москва, улица Ленина дом 1, кв 1")

        # Находим поле currentAddress по его ID и вводим адрес
        permanentAddress_field = driver.find_element(By.ID, "permanentAddress")
        permanentAddress_field.send_keys("Г. Москва, улица Сталина дом 1, кв 1")

        # Находим кнопку Submit по ее ID и кликаем
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        # 4. Проверка результата
        time.sleep(1)  # Пауза, чтобы увидеть результат отправки

        # Находим блок с отправленными данными
        result_box = driver.find_element(By.ID, "output")

        # Проверяем, что в блоке результата появился введенный текст
        assert "Барно Ниязова" in result_box.text
        assert "barno@example.com" in result_box.text
        assert "Г. Москва, улица Ленина дом 1, кв 1" in result_box.text
        assert "Г. Москва, улица Сталина дом 1, кв 1" in result_box.text
        print("Тест успешно пройден!")

    finally:
        # 5. Закрытие браузера в любом случае
        driver.quit()


def test_form2(): #негативные проверки
    # 1. Запуск браузера Chrome
    driver = webdriver.Chrome()

    try:
        # 2. Открытие страницы
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()
        time.sleep(1)  # Пауза, чтобы визуально заметить открытие

        # 3. Поиск элементов и заполнение полей
        # Находим поле Full Name по его ID и вводим числа
        full_name_field = driver.find_element(By.ID, "userName")
        # web_elements = driver.find_elements(By.XPATH, "someXPath")

        full_name_field.send_keys("1234567")

        # Находим поле Email по его ID и вводим почту без @
        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys("barnoexample.com")

        # Находим поле currentAddress по его ID и вводим от 200 символов
        currentAddress_field = driver.find_element(By.ID, "currentAddress")
        currentAddress_field.send_keys("Г. Москва, улица Ленина дом 1, кв 1, каждый тестировщик должен рабираться в автотестировании")

        # Находим поле currentAddress по его ID и вводим адрес дополнительными символами
        permanentAddress_field = driver.find_element(By.ID, "permanentAddress")
        permanentAddress_field.send_keys("Г. Москва, улица Сталина дом 1, кв 1 !@#$%^&*()_+-=[]{}|;:,.<>/`~")

        # Находим кнопку Submit по ее ID и кликаем
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        # 4. Проверка результата
        time.sleep(1)  # Пауза, чтобы увидеть результат отправки

        # Находим блок с отправленными данными
        result_box = driver.find_element(By.ID, "output")

        # Проверяем, что в блоке результата появился введенный текст
        assert "1234567" not in result_box.text
        assert "barnoexample.com" not in result_box.text
        assert "Г. Москва, улица Ленина дом 1, кв 1, каждый тестировщик должен рабираться в автотестировании" not in result_box.text
        assert "Г. Москва, улица Сталина дом 1, кв 1 !@#$%^&*()_+-=[]{}|;:,.<>/`~" not in result_box.text

        print("Тест успешно пройден!")

    finally:
        # 5. Закрытие браузера в любом случае
        driver.quit()
