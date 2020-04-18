import argparse
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected

MSG_XPATH = "//*[@id=\"menu\"]/a[8]"


def login(driver, username, password):
    driver.get('http://www.shinobi.fr/')
    time.sleep(1)

    user_field = driver.find_element_by_id("login")
    user_field.send_keys(username)

    pass_field = driver.find_element_by_name('pass')
    pass_field.send_keys(password)
    time.sleep(1)  # let user see inputs

    submit_btn = driver.find_element_by_xpath("//*[@id=\"blocConnexion\"]/form/input[3]")
    submit_btn.click()

    # wait 5 seconds max, to confirm login
    WebDriverWait(driver, 5).until(expected.visibility_of_element_located((By.XPATH, MSG_XPATH)))
    print("Login successful")
    time.sleep(1)


def logout(driver):
    logout_btn = driver.find_element_by_link_text("Déconnexion")
    logout_btn.click()
    time.sleep(1)


def go_to_messages(driver):
    driver.find_element_by_xpath(MSG_XPATH).click()
    time.sleep(1)


def go_next_page(driver):
    next_btn = driver.find_element_by_link_text("»")
    next_btn.click()


def delete_unread(driver):
    # delete all unread msgs on current page
    while True:
        try:
            unread = driver.find_element_by_class_name("nonlu")
        except NoSuchElementException:
            # no more unread msg
            return
        else:
            delete_btn = unread.find_element_by_css_selector("img[src='http://images.shinobi.fr/design/suppr.gif']")
            delete_btn.click()
            time.sleep(0.1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Delete unread messages on shinobi.fr")
    parser.add_argument("username", type=str, help="Username")
    parser.add_argument("password", type=str, help="Password")
    parser.add_argument("max", type=int, help="How many pages to go through (default 10)", default=10)
    args = parser.parse_args()

    # Use driver in the current directory
    webdriver = webdriver.Chrome('chromedriver.exe')

    login(webdriver, args.username, args.password)
    go_to_messages(webdriver)
    page = 1

    while page <= args.max:
        print(f"Deleting unread messages on page {page}")
        delete_unread(webdriver)
        go_next_page(webdriver)
        time.sleep(1)
        page += 1

    print("Done.")
    logout(webdriver)
    webdriver.quit()
