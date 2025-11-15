from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    first_name = (By.ID, "first-name")
    last_name = (By.ID, "last-name")
    postal_code = (By.ID, "postal-code")
    continue_button = (By.ID, "continue")
    total_label = (By.CLASS_NAME, "summary_total_label")

    def fill_info(self, first_name: str, last_name: str, postal_code: str):

        first_name_input = self.wait.until(
            EC.visibility_of_element_located(self.first_name))
        first_name_input.clear()
        first_name_input.send_keys(first_name)

        last_name_input = self.wait.until(
            EC.visibility_of_element_located(self.last_name))
        last_name_input.clear()
        last_name_input.send_keys(last_name)

        postal_code_input = self.wait.until(
            EC.visibility_of_element_located(self.postal_code))
        postal_code_input.clear()
        postal_code_input.send_keys(postal_code)

        self.wait.until(EC.element_to_be_clickable(
            self.continue_button)).click()

    def get_total(self) -> str:
        total_text = self.wait.until(EC.presence_of_element_located(
            self.total_label)).text  # "Total: $58.29"
        return total_text.replace("Total: $", "")  # возвращаем только "58.29"
