import pytest
from text_box_page_pf import TextBoxPage


# 1. Создание виртуального окружения
#python -m venv venv

# 1.5 Если не отработал пункт 2 под Windows
# PowerShell: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 2. Активация (Для Windows)
#venv\Scripts\activate
# 2. Активация (Для macOS/Linux)
#source venv/bin/activate

# 3. Установка зависимостей
#pip install -r requirements.txt

# 4. Запуск всех тестов
#pytest -v test_text_box.py

# 4. Запуск конкретного параметризованного метода (TestSuite)
#pytest -v test_text_box.py::test_empty_form_submission

# 4. Запуск конкретного тест-кейса из параметризованного набора
#pytest test_text_box.py::test_positive_form_submission[John Doe-john@example.com-123 Elm St-456 Oak St] -v

# --- 1. Позитивные сценарии (Валидные данные) ---
@pytest.mark.parametrize("name, email, cur_addr, perm_addr", [
    ("John Doe", "john@example.com", "123 Elm St", "456 Oak St"),                      # Стандартный кейс
    ("Иван Иванов", "ivan@mail.ru", "ул. Ленина, д. 1", "ул. Пушкина, д. 2"),          # Кириллица
    ("A", "a@b.cc", "B", "C"),                                                         # Минимальная длина строк
    ("Name-With Dash", "dash@email.co.uk", "Addr 1/2", "Addr 3 & 4"),                  # Спецсимволы в полях
    ("   John   ", "spaces@test.com", "  Street 1  ", "  Street 2  "),                 # Строки с пробелами
])
def test_positive_form_submission(driver, name, email, cur_addr, perm_addr):

    page = TextBoxPage(driver)
    output = page.open().fill_form(name, email, cur_addr, perm_addr).submit().get_output_data()
    assert output is not None, "Блок с результатами не отобразился"
    assert output["name"] == name.strip()
    assert output["email"] == email.strip()
    assert output["cur_addr"] == cur_addr.strip()
    assert output["perm_addr"] == perm_addr.strip()


# --- 2. Частичное заполнение обязательных/необязательных полей ---
@pytest.mark.parametrize("name, email, cur_addr, perm_addr", [
    ("Only Name", "", "", ""),
    ("", "only@email.com", "", ""),
    ("", "", "Only Current Address", ""),
    ("", "", "", "Only Permanent Address"),
    ("Name & Email", "name_email@test.com", "", ""),
])
def test_partial_form_submission(driver, name, email, cur_addr, perm_addr):
    page = TextBoxPage(driver)
    page.open()
    page.fill_form(name, email, cur_addr, perm_addr)
    page.submit()
    output = page.get_output_data()

    assert output is not None, "Форма должна отправляться при частичном заполнении"
    assert output == {"name": name, "email": email, "cur_addr": cur_addr, "perm_addr": perm_addr}


# --- 3. Негативные сценарии (Невалидный Email) ---
@pytest.mark.parametrize("invalid_email", [
    "plainaddress",          # Нет собаки и домена
    "@no-local-part.com",    # Нет имени пользователя
    "john@@example.com",     # Две собаки
    "john@example..com",     # Две точки подряд
])
def test_invalid_email_validation(driver, invalid_email):
    page = TextBoxPage(driver)
    page.open()
    page.fill_form(name="Test", email=invalid_email)
    page.submit()

    # Проверяем и отсутствие результата, и ошибку встроенной валидации.
    output = page.get_output_data()

    assert output is None, f"Email '{invalid_email}' не должен быть принят системой"
    assert page.is_email_error_present()


@pytest.mark.parametrize("email", ["john.doe@com", "john@missing-dot"])
def test_email_without_dot(driver, email):
    page = TextBoxPage(driver).open()
    page.fill_form(name="Test", email=email)
    page.submit()
    assert not page.is_email_error_present()
    assert page.get_output_data() == {
        "name": "Test", "email": email, "cur_addr": "", "perm_addr": ""
    }


# --- 4. Граничные значения и нагрузка на длину полей (Длинные строки) ---
@pytest.mark.parametrize("field_type, long_string", [
    ("name", "A" * 1000),                             # Экстремально длинное имя
    ("email", f"{'b' * 64}@example.com"),             # Максимальная длина локальной части email
    ("cur_addr", "Current " * 200),                   # Длинный адрес (проверка на переполнение)
    ("perm_addr", "Permanent " * 200)                 # Длинный адрес
])
def test_long_input_fields(driver, field_type, long_string):
    page = TextBoxPage(driver).open()

    page.fill_form(**{field_type: long_string})

    page.submit()
    output = page.get_output_data()

    assert output is not None, f"Форма не справилась с длинной строкой в поле {field_type}"
    expected = {"name": "", "email": "", "cur_addr": "", "perm_addr": ""}
    expected[field_type] = long_string.strip()
    assert output == expected


# --- 5. Отображение HTML и спецсимволов как обычного текста ---
@pytest.mark.parametrize("security_payload", [
    pytest.param("<script>alert('xss')</script>", marks=pytest.mark.xfail(
        strict=True, raises=AssertionError, reason="Ошибка страницы: ввод вставляется через innerHTML"
    )),
    "1' OR '1'='1",                                  # Базовая SQL-инъекция
    ":):):):))))::;)",                               # Текстовые смайлики
    pytest.param("<div>HTML injection</div>", marks=pytest.mark.xfail(
        strict=True, raises=AssertionError, reason="Ошибка страницы: ввод вставляется через innerHTML"
    ))
])
def test_security_and_special_inputs(driver, security_payload):
    page = TextBoxPage(driver).open()
    # Заполняем все поля потенциально опасным контентом
    page.fill_form(name=security_payload, cur_addr=security_payload, perm_addr=security_payload)
    page.submit()
    output = page.get_output_data()

    assert output is not None, "Форма упала при вводе спецсимволов/инъекций"
    # Текст должен отобразиться строго как строка, а не выполниться кодом
    assert output == {
        "name": security_payload, "email": "",
        "cur_addr": security_payload, "perm_addr": security_payload
    }


# --- 6. Пустая форма ---
def test_empty_form_submission(driver):
    page = TextBoxPage(driver).open()
    page.submit()
    output = page.get_output_data()


    # На этой странице все поля необязательные, пустая форма отправляется.
    assert output == {"name": "", "email": "", "cur_addr": "", "perm_addr": ""}
