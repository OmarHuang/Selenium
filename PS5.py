#!/usr/bin/env python3

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def order():
    # Webdriver settings
    driver = webdriver.Firefox()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    # Set website address
    driver.get("https://24h.pchome.com.tw/prod/DGBJG9-A900B51SM?fq=/S/DGBJG9")

    # Add product to shopping car
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[3]/div[2]/div/div[2]/ul["
                                                         "2]/li/button"))).click()
    # Redirect to shopping car
    driver.get("https://ecssl.pchome.com.tw/sys/cflow/fsindex/BigCar/BIGCAR/ItemList")

    # Login PChome account
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"loginAcc\"]"))).send_keys("username")
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"loginPwd\"]"))).send_keys("password")
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"btnLogin\"]"))).click()

    # Order product
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/dl[1]/dd/ul/li[1]/a")))\
        .click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"btnSubmit\"]"))).click()
    print("Order is success")

    # Close browser
    driver.close()


if __name__ == "__main__":
    try:
        order()
    except TimeoutException:
        print("Website is timed out")
    except UnexpectedAlertPresentException:
        print("Product is sold out/not for sale yet")
