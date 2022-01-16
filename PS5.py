#!/usr/bin/env python3

import yaml

from dataclasses import dataclass
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Loading private information from yaml
data = yaml.safe_load(open("secrets.yaml"))

# Webdriver settings
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# Short path
clickable = EC.element_to_be_clickable
find = driver.find_element_by_xpath
located = EC.presence_of_element_located

# Xpath location
xpath = {
    "account": "//*[@id=\"loginAcc\"]",
    "add_product": "//*[@id=\"ButtonContainer\"]/button",
    "credit_card": "//*[@id=\"payment_creditcard\"]/dd/ul/li[1]/a",
    "cvc": "//*[@id=\"multi_CVV2Num\"]",
    "login": "//*[@id=\"btnLogin\"]",
    "password": "//*[@id=\"loginPwd\"]",
    "shopping_car": "//*[@id=\"24hrCartContainer\"]",
    "submit": "//*[@id=\"btnSubmit\"]",
}


@dataclass
class PcHome:
    account: str = data["account"]
    cvc: int = data["cvc"]
    password: int = data["password"]
    status: bool = True
    url: str = data["url"]

    def connect(self):
        # Connect to PcHome website
        driver.get(self.url)
        print("Connect successful")

    def check_status(self):
        # Check if product is available for purchase
        status = find(xpath["add_product"]).text
        if status == "加入購物車":
            wait.until(located((By.XPATH, xpath["add_product"]))).click()
            print("Add product to shopping car")
            # Click the shopping car
            shopping_car = wait.until(clickable((By.XPATH, xpath["shopping_car"])))
            driver.execute_script("arguments[0].click()", shopping_car)
        else:
            print("Not for sale or sold out")
            driver.close()
        return self.status

    def login(self):
        # Login PChome account
        wait.until(located((By.XPATH, xpath["account"]))).send_keys(self.account)
        wait.until(located((By.XPATH, xpath["password"]))).send_keys(self.password)
        wait.until(clickable((By.XPATH, xpath["login"]))).click()
        print("Login successful")

    def purchase(self):
        # Select credit card as payment
        credit_card = wait.until(clickable((By.XPATH, xpath["credit_card"])))
        driver.execute_script("arguments[0].click()", credit_card)

        # Fill in credit card security code
        wait.until(clickable((By.XPATH, xpath["cvc"]))).send_keys(self.cvc)

        # Submit purchase
        wait.until(clickable((By.XPATH, xpath["submit"])))
        driver.execute_script("arguments[0].click()", find(xpath["submit"]))
        print("Order successful")


pc = PcHome()
if __name__ == "__main__":
    try:
        # TODO: Should separate these function call.
        pc.connect()
        pc.check_status()
        pc.login()
        pc.purchase()
    except exceptions.TimeoutException as e:
        print(e.msg)
    except exceptions.UnexpectedAlertPresentException as e:
        print(e.alert_text)
    except exceptions.InvalidSessionIdException as e:
        print(e.msg)
