#!/usr/bin/env python3

import yaml

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Loading private information from yaml
data = yaml.safe_load(open("secrets.yaml"))

# Webdriver settings
driver = webdriver.Firefox()
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
    "credit_card": "/html/body/div[1]/div[2]/div/div/div[2]/dl[1]/dd/ul/li[1]/a",
    "cvc": "//*[@id=\"multi_CVV2Num\"]",
    "login": "//*[@id=\"btnLogin\"]",
    "password": "//*[@id=\"loginPwd\"]",
    "shopping_car": "//*[@id=\"24hrCartContainer\"]",
    "submit": "//*[@id=\"btnSubmit\"]",
}


def order():
    # Set website address
    driver.get(data["url"])

    # Add product to shopping car
    wait.until(located((By.XPATH, xpath["add_product"]))).click()

    # Click the shopping car
    wait.until(clickable((By.XPATH, xpath["shopping_car"])))
    driver.execute_script("arguments[0].click()", find(xpath["shopping_car"]))

    # Login PChome account
    wait.until(located((By.XPATH, xpath["account"]))).send_keys(data["account"])
    wait.until(located((By.XPATH, xpath["password"]))).send_keys(data["password"])
    wait.until(located((By.XPATH, xpath["login"]))).click()
    print("Login successful")

    # Purchase product with credit card
    wait.until(clickable((By.XPATH, xpath["credit_card"])))
    driver.execute_script("arguments[0].click()", find(xpath["credit_card"]))

    #  Credit card security code
    wait.until(clickable((By.XPATH, xpath["cvc"])))
    find(xpath["cvc"]).send_keys(data["cvc"])

    # Submit purchase
    wait.until(clickable((By.XPATH, xpath["submit"])))
    driver.execute_script("arguments[0].click()", find(xpath["submit"]))
    print("Order successful")


if __name__ == "__main__":
    try:
        order()
    except TimeoutException:
        print("Website is timed out")
    except UnexpectedAlertPresentException:
        print("Product is sold out/not for sale yet")
