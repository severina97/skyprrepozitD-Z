import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_zip_validation():
    driver = webdriver.Edge(service=EdgeService("C:/WebDriver/msedgedriver.exe"))
    wait = WebDriverWait(driver, 20)

    try:
        # Открываем страницу
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

        # Заполняем все поля кроме ZIP
        fields_data = {
            "first-name": "Иван",
            "last-name": "Петров",
            "address": "Ленина, 55-3",
            "e-mail": "test@skypro.com",
            "phone": "+7985899998787",
            "city": "Москва",
            "country": "Россия",
            "job-position": "QA",
            "company": "SkyPro",
        }

        for name, value in fields_data.items():
            elem = wait.until(EC.presence_of_element_located((By.NAME, name)))
            elem.clear()
            elem.send_keys(value)

        # Сабмит формы (ZIP пустой)
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type=submit]")))
        submit.click()

        # Ждём появления красного блока с ошибкой для ZIP
        zip_alert = wait.until(EC.presence_of_element_located((By.ID, "zip-code")))

        # Проверяем, что это именно блок с классом alert-danger
        assert "alert-danger" in zip_alert.get_attribute("class"), "ZIP не подсвечен красным!"
    finally:
        driver.quit()