# coding=utf-8
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
    # time.sleep(1)


def logout(driver):
    logout_btn = driver.find_element_by_link_text("Déconnexion")
    logout_btn.click()
    # time.sleep(1)


def go_to_messages(driver):
    driver.find_element_by_xpath(MSG_XPATH).click()
    # time.sleep(1)


def go_next_page(driver):
    next_btn = driver.find_element_by_link_text("»")
    next_btn.click()
    # time.sleep(0.1)


def go_to_page(driver, page: int):
    driver.get(f"http://www.shinobi.fr/index.php?page=menu-messagerie&pg={page}")


def delete_unread(driver):
    # delete the first unread found on the page
    try:
        unread = driver.find_element_by_class_name("nonlu")
        delete_btn = unread.find_element_by_css_selector("img[src='http://images.shinobi.fr/design/suppr.gif']")
        delete_btn.click()
        return True
    except NoSuchElementException:
        # no more unread msg
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Delete unread messages on shinobi.fr")
    parser.add_argument("username", type=str, help="Username")
    parser.add_argument("password", type=str, help="Password")
    parser.add_argument("max", type=int, help="How many pages to go through (default 10)", default=10)
    parser.add_argument("--start", type=int, dest="start", help="Specify a starting page")
    args = parser.parse_args()

    # Use driver in the current directory
    webdriver = webdriver.Chrome('chromedriver.exe')

    login(webdriver, args.username, args.password)
    go_to_messages(webdriver)

    if args.start:
        page = args.start
        go_to_page(webdriver, page)
    else:
        page = 1

    while page <= args.max:
        print(f"Deleting unread messages on page {page}")
        if delete_unread(webdriver):
            # deleted something, go back to the page
            go_to_page(webdriver, page)
        else:
            # found no unread, increment page
            page += 1
            go_to_page(webdriver, page)

    print("Done.")
    logout(webdriver)
    webdriver.quit()
