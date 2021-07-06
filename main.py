#!/usr/local/bin/python3

import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from decouple import config
import time
import sys

def set_chrome_options() -> None:

    """Sets chrome options for Selenium.

    Chrome options for headless browser is enabled.

    """

    chrome_options = Options()

    chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_prefs = {}

    chrome_options.experimental_options["prefs"] = chrome_prefs

    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    return chrome_options

try:
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=chrome_options) #options=chrome_options
except:
    sys.exit('Could not find chromedriver')


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
                                                     "//div[@class='calendar-body__cell']")))[first_date]
    date_1_text = date_1.text
    date_1.click()
    date_3 = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     "//div[@class='calendar__month-name']")))
    month_1_text = date_3[0].text
    month_2_text = date_3[1].text
    date_2 = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     "//div[@class='calendar-body__cell']")))[second_date]
    date_2_text = date_2.text
    date_2.click()


    if int(date_1_text) < int(date_2_text):
        print('The flight is from', date_1_text,'to', date_2_text, 'of', month_1_text)
    else:
        print('The flight is from', date_1_text, 'of', month_1_text, 'to', date_2_text, 'of', month_2_text)

def number_of_people(adults, teens, children, infants):
    # close the subscribe button
    # driver.find_element_by_xpath("//button[@class='subscriber-widget__close-button']").click()
    # reopen passenger selection
    passengers_button = driver.find_elements_by_xpath("//fsw-input-button[@class='flight-widget-controls__control flight-widget-controls__control--passengers ng-tns-c80-4']"
                                                      "[@_ngcontent-ryanair-homepage-c80='']"
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

    driver.find_element_by_xpath("//button[@class='flight-search-widget__start-search ng-tns-c81-3 ry-button--gradient-yellow']"
                                 "[@aria-label='Search']").click()

def process_data_first_page():
    # select_origin_or_destiny(type, country, city)
    buttons = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,
                                                     "//button[@class='cookie-popup-with-overlay__button']"
                                                     "[@data-ref='cookie.accept-all']"
                                                     )))
    buttons[0].click()
    select_origin_or_destiny('departure','Portugal','Porto')
    select_origin_or_destiny('destination','Poland','Krakow')
    select_dates(1, 1)
    # number_of_people(adults, teens, children, infants)
    number_of_people(1,0,0,0)
    click_checkbox_and_search()



def process_data_second_page():
    #driver.find_element_by_xpath("//div[@class='cookie-popup__close']").click()
    #actions = ActionChains(driver)
    element = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class, 'card-header')]")))
    for i in range(len(element)):
        #  until(EC.visibility_of_all_elements_located((By.XPATH,"//div[@class='card-header b2 ng-tns-c124-15']")))

        #actions.move_to_element(element[i]).perform()

        element[i].click()
  #      WebDriverWait(driver, 20). \
  #          until(EC.visibility_of_all_elements_located((By.XPATH,
   #                                                      "//span[@class='fare-card__button-text ng-star-inserted']"
    #                                                     )))[0].click()
    #cost = driver.find_element_by_xpath("//span[@class='price-value h2 text-700 price-value--selected']").text
    cost = driver.find_element_by_xpath("//ry-price[contains(@class,'price')]").text
    print('Total cost is '+ cost)
    imp = input('Do you wish to proceed? (Y or N)')
    if imp == 'N':
        driver.quit()
        sys.exit("Exit requested by user")

    driver.find_element_by_xpath("//button[contains(@class,'fare-card__button')]").click()

    WebDriverWait(driver, 20). \
        until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@class,'ry-button--full login-touchpoint__login-button')]"))).click()

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
    time.sleep(1) #wait for login prompt to close

def personal_information_data():
    TITLE = config('TITLE')
    NAME = config('NAME')
    SURNAME = config('SURNAME')
    WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,"//button[@class='dropdown__toggle b2']")))[0].click()
    titles = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH,"//button[@class='dropdown-item__link dropdown-item__link--highlighted']")))
    for title in titles:
        if title.text == TITLE:
            title.click()
    name_box = driver.find_element_by_xpath("//input[@id='formState.passengers.ADT-0.name']")
    name_box.click()
    actions = ActionChains(driver)
    actions.move_to_element(name_box).send_keys(NAME).perform()
    surname_box = driver.find_element_by_xpath("//input[@id='formState.passengers.ADT-0.surname']")
    surname_box.click()
    actions = ActionChains(driver) ## Necessary, resets the keys currently within the driver
    actions.move_to_element(surname_box).send_keys(SURNAME).perform()
    driver.find_element_by_xpath("//button[contains(@class,'continue-flow__button')]").click()

def scroll_shim(passed_in_driver, object):
    x = object.location['x']
    y = object.location['y']
    print(x)
    print(y)
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)

def choose_seat():
    seat_options = WebDriverWait(driver, 20). \
        until(EC.visibility_of_all_elements_located((By.XPATH, "//button[@class='seats-v2-navigation__button h4 ng-tns-c149-1']")))

    for seat in seat_options:
        if seat.text == "Option 2: Random seat allocation":
            seat.click()

    element = driver.find_element_by_xpath( "//button[@class='random-allocation-info__actions__button b2 ry-button--gradient-yellow']")
    if 'firefox' in driver.capabilities['browserName']:
        scroll_shim(driver, element)
    actions = ActionChains(driver)
    actions.move_to_element(element)

    actions.perform()
    element.click()

def main():
    get_driver()
    process_data_first_page()
    process_data_second_page()
    login()
    personal_information_data()
    choose_seat()

    input()
    driver.quit()

if __name__ == "__main__":
    main()


