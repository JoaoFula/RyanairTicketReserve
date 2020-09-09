#!/usr/local/bin/python3

import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

try:
    driver=webdriver.Firefox()
except:
    path = input('geckodriver is not in your path, please type the path to the geckodriver executable: ')
    driver = webdriver.Firefox(executable_path=path)


def get_driver():
    url = "https://www.ryanair.com/gb/en"
    driver.get(url)
    return driver

def select_origin_or_destiny(from_or_to, country, city):
    # Locate departure text box
    from_text_box = driver.find_element_by_xpath("//input[@id='input-button__"+from_or_to+"']"
                                                 "[@class='input-button__input ng-star-inserted']")
    from_text_box.click()

    # Find all origin countries
    from_airports = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     "//span[@data-ref='country__name']"
                                                     )))
    # Locate origin country from the airport list and click the origin country button
    for airports in from_airports:
        if airports.text == country:
            airports.click()
            break

    # Find all origin cities within the origin country
    from_airports = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     "//span[@class='b2 airport-item']"
                                                     )))
    # Locate origin city from the airport list and click the origin city button
    for airports in from_airports:
        if airports.text == city:
            airports.click()
            break

def select_dates(first_date, second_date):
    choose_date_buttons = driver.find_elements_by_xpath("//div[@class='input-button__input ng-star-inserted']")
    choose_date_buttons[0].click()

    #wrappers = driver.find_elements_by_xpath("//calender[@class = '']")

    WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     ("//div[@class='calendar-body__cell']"
                                                     "[@_ngcontent-ryanair-homepage-c85='']"
                                                     "[@tabindex='0']")

                                                     )))[first_date].click()
    WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     ("//div[@class='calendar-body__cell']"
                                                      "[@_ngcontent-ryanair-homepage-c85='']"
                                                      "[@tabindex='0']")

                                                     )))[second_date].click()


    #print('The flight is from ', dates[first_date].text, 'to ', dates[second_date].text)


def process_data():
    select_origin_or_destiny('departure','Portugal','Porto')
    select_origin_or_destiny('destination','Poland','Krakow')
    select_dates(1, 2)

    input()
    driver.quit()


def main():
    get_driver()
    process_data()


if __name__ == "__main__":
    main()
