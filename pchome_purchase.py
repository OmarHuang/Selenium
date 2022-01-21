#!/usr/bin/env python3

import yaml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Loading private information from yaml
data = yaml.safe_load(open("secrets.yaml"))

# Webdriver settings
options = webdriver.ChromeOptions()
options.add_argument(data["profile"])

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(100)
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


class PcHome:
    account = data["account"]
    cvc = data["cvc"]
    max_retry = 10
    password = data["password"]
    retry = 1
    url = data["url"]

    def connect(self):
        # Connect to PcHome website
        driver.get(self.url)
        print("Connect successful")
        self.check_status()

    def check_status(self):
        # Check if product is available for purchase
        while self.retry <= self.max_retry:
            status = find(xpath["add_product"]).text
            if status == "加入購物車":
                self.add_product()
                break
            elif self.retry >= self.max_retry:
                print("Product is not for sale or sold out")
                driver.close()
            else:
                driver.refresh()
                self.retry += 1

    def add_product(self):
        # Add product to shopping car
        wait.until(located((By.XPATH, xpath["add_product"]))).click()
        print("Add product to shopping car")

        # Click the shopping car
        shopping_car = wait.until(clickable((By.XPATH, xpath["shopping_car"])))
        driver.execute_script("arguments[0].click()", shopping_car)
        self.check_login()

    def check_login(self):
        try:
            self.login()
        except Exception as login_exception:
            self.purchase()
            print(login_exception, "You are already logins")

    def login(self):
        wait.until(located((By.XPATH, xpath["account"]))).send_keys(self.account)
        wait.until(located((By.XPATH, xpath["password"]))).send_keys(self.password)
        wait.until(clickable((By.XPATH, xpath["login"]))).click()
        print("Login successful")
        self.purchase()

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
        pc.connect()
    except Exception as e:
        print(e)
