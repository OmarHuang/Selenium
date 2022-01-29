#!/usr/bin/env python3
"""This for PChome product."""
import yaml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Loading private information from yaml
with open("secrets.yaml", encoding="utf-8") as file:
    data = yaml.safe_load(file)

# Webdriver settings
options = webdriver.ChromeOptions()
options.add_argument(data["profile"])

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(100)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

"""Xpath location."""
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


class PChome:
    """PChome class."""
    account = data["account"]
    cvc = data["cvc"]
    max_retry = 10
    password = data["password"]
    retry = 1
    url = data["url"]

    def login(self):
        """Login in to your PChome account."""
        driver.get("https://ecvip.pchome.com.tw/login/v3/login.htm")
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath["account"])))
        driver.find_element_by_xpath(xpath["account"]).send_keys(self.account)
        driver.find_element_by_xpath(xpath["password"]).send_keys(self.password)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath["login"]))).click()
        print("Login successful")
        self.get(self.url)

    def get(self, url):
        """Get to PChome product page that you want to buy."""
        driver.get(url)
        print("Connect successful")
        self.check_status()

    def check_status(self):
        """Check if product is available for purchase."""
        while self.retry <= self.max_retry:
            status = driver.find_element_by_xpath(xpath["add_product"]).text
            if status == "加入購物車":
                self.add_product()
            elif self.retry >= self.max_retry:
                print("Product is not for sale or sold out")
                driver.close()
            else:
                driver.refresh()
                self.retry += 1

    def add_product(self):
        """Add product to shopping car."""
        wait.until(EC.presence_of_element_located((By.XPATH, xpath["add_product"]))).click()
        print("Add product to shopping car")
        shopping_car = wait.until(EC.element_to_be_clickable((By.XPATH, xpath["shopping_car"])))
        driver.execute_script("arguments[0].click()", shopping_car)
        self.purchase()

    def purchase(self):
        """Select credit card and purchase it."""
        credit_card = wait.until(EC.element_to_be_clickable((By.XPATH, xpath["credit_card"])))
        driver.execute_script("arguments[0].click()", credit_card)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath["cvc"]))).send_keys(self.cvc)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath["submit"])))
        driver.execute_script("arguments[0].click()", driver.find_element_by_xpath(xpath["submit"]))
        print("Order successful")
