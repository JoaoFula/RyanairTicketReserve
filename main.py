#!/usr/local/bin/python3

import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from decouple import config


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

    if from_or_to == 'departure':
        # Find all origin cities within the origin country
        from_airports = WebDriverWait(driver, 20). \
            until(EC.visibility_of_all_elements_located((By.XPATH,
                                                         "//span[@class='b2 airport-item']"

                                                         )), message='Something is wrong with the request or'
                                                                     'cannot fly from '+ city)

    from_airports = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     "//span[@class='b2 airport-item']",

                                                     )), message='Something is wrong with the request or'
                                                                     'cannot fly to '+ city)

    # Locate origin city from the airport list and click the origin city button
    for airports in from_airports:
        if airports.text == city:
            airports.click()
            break

def select_dates(first_date, second_date):
    choose_date_buttons = driver.find_elements_by_xpath("//div[@class='input-button__input ng-star-inserted']")
    choose_date_buttons[0].click()

    #wrappers = driver.find_elements_by_xpath("//calender[@class = '']")

    date_1 = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     ("//div[@class='calendar-body__cell']"
                                                     "[@_ngcontent-ryanair-homepage-c85='']"
                                                     "[@tabindex='0']")

                                                     )))[first_date]
    date_1_text = date_1.text
    date_1.click()
    date_3 = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     ("//div[@class='calendar__month-name']"
                                                      "[@_ngcontent-ryanair-homepage-c84='']"
                                                      ))))
    month_1_text = date_3[0].text
    month_2_text = date_3[1].text
    date_2 = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     ("//div[@class='calendar-body__cell']"
                                                      "[@_ngcontent-ryanair-homepage-c85='']"
                                                      "[@tabindex='0']")

                                                     )))[second_date]
    date_2_text = date_2.text
    date_2.click()


    if int(date_1_text) < int(date_2_text):
        print('The flight is from', date_1_text,'to', date_2_text, 'of', month_1_text)
    else:
        print('The flight is from', date_1_text, 'of', month_1_text, 'to', date_2_text, 'of', month_2_text)

def number_of_people(adults, teens, children, infants):
    # close the subscribe button
    driver.find_element_by_xpath("//button[@class='subscriber-widget__close-button']").click()
    # reopen passenger selection
    passengers_button = driver.find_elements_by_xpath("//fsw-input-button[@class='flight-widget-controls__control flight-widget-controls__control--passengers']"
                                                      "[@_ngcontent-ryanair-homepage-c29='']"
                                                      "[@container='body']"
                                                      "[@uniqueid='passengers']")
    passengers_button[0].click()




    buttons = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     "//div[@class='counter__button-wrapper--enabled']"
                                                     )))

    for i in range(adults-1):
        buttons[0].click()
    for i in range(teens):
        buttons[1].click()
    for i in range(children):
        buttons[2].click()
    for i in range(infants):
        buttons[3].click()

    driver.find_element_by_xpath("//button[@class='passengers__confirm-button ry-button--anchor-blue ry-button--anchor']"
                                  "[@aria-label='Done']").click()

def click_checkbox_and_search():
    driver.find_element_by_xpath("//ry-checkbox"
                                 "[@data-ref='terms-of-use__terms-checkbox']").click()

    driver.find_element_by_xpath("//button[@class='flight-search-widget__start-search ry-button--gradient-yellow ng-trigger ng-trigger-collapseExpandCta']"
                                 "[@aria-label='Search']").click()

def process_data_first_page():
    # select_origin_or_destiny(type, country, city)
    select_origin_or_destiny('departure','Portugal','Porto')
    select_origin_or_destiny('destination','Poland','Krakow')
    select_dates(1, 1)
    # number_of_people(adults, teens, children, infants)
    number_of_people(1,0,0,0)
    click_checkbox_and_search()

def process_data_second_page():
    driver.find_element_by_xpath("//div[@class='cookie-popup__close']").click()
    actions = ActionChains(driver)

    for i in range(2):
        element = WebDriverWait(driver, 20). \
            until(EC.visibility_of_all_elements_located((By.XPATH,"//div[@class='card-header b2']")))

        actions.move_to_element(element[i]).perform()

        element[i].click()
        WebDriverWait(driver, 20). \
            until(EC.visibility_of_all_elements_located((By.XPATH,
                                                         "//span[@class='fare-card__button-text ng-star-inserted']"
                                                         )))[0].click()
    #cost = driver.find_element_by_xpath("//span[@class='price-value h2 text-700 price-value--selected']").text
    cost = driver.find_element_by_xpath("//ry-price[@class='ng-tns-c19-1 price ng-star-inserted']").text
    print('Total cost is '+ cost)
    input('Do you wish to proceed?')

    driver.find_element_by_xpath("//button[@class='ry-button--full login-touchpoint__login-button ry-button--gradient-blue ry-button--medium']").click()

def login():
    EMAIL = config('EMAIL')
    PASSWORD = config('PASSWORD')
    text_boxes = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,"//input[@name='email']")))


    text_boxes[0].click()
    actions = ActionChains(driver)
    actions.move_to_element(text_boxes[0]).send_keys(EMAIL).perform()
    text_box = driver.find_element_by_xpath("//input[@name='password']")
    text_box.click()
    actions = ActionChains(driver)
    actions.move_to_element(text_box).send_keys(PASSWORD).perform()
    driver.find_element_by_xpath("//button[@class='auth-submit__button ry-button--full ry-button--flat-yellow']").click()


def main():
    get_driver()
    process_data_first_page()
    process_data_second_page()
    login()

    input()
    driver.quit()

if __name__ == "__main__":
    main()


