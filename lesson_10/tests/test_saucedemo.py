import allure
import pytest
from selenium import webdriver

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.title("Проверка покупки товаров на saucedemo.com")
def test_saucedemo_checkout():
    with allure.step("Запуск Chrome в режиме инкогнито"):
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)

    with allure.step("Открытие сайта"):
        driver.get("https://www.saucedemo.com/")

    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_to_cart("Sauce Labs Backpack")
    inventory.add_to_cart("Sauce Labs Bolt T-Shirt")
    inventory.add_to_cart("Sauce Labs Onesie")
    inventory.go_to_cart()

    cart = CartPage(driver)
    cart.checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_info("Ivan", "Ivanov", "12345")

    with allure.step("Проверка итоговой суммы"):
        total = checkout.get_total()
        assert total == "58.29"

    driver.quit()
