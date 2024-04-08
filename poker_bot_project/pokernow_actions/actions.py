from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException

import re
import time

# ----------------- FUNCTION LIBRARY -------------------

# discord_login(driver, user, pass) # WORKS

# register_for_game(driver) # WORKS 

# go_to_game2(driver) # WORKS

# crib_go_to_game(driver) # WORKS

# read_log # WORKS

# check_turn 

# call(driver) # WORKS

# raise(driver, amount) # WORKS

# check(driver) # WORKS

# fold(driver) # WORKS


#----------------- NOTES -------------------
# using x_path for most identifications - reliable, but not fast
# how to integrate with poker playing logic?
# need an extra click to authorize discord and go to game room when ready
# check / fold - bot can just sit there and do nothing



# ----------------- DISCORD LOGIN FUNCTION ---------------------

def discord_login(driver, discord_user, discord_pass):

    driver.get("https://network.pokernow.club/sng_tournaments")
    
    discord_button_xpath = "//button[contains(@class, 'button-1') and contains(@class, 'big') and contains(@class, 'blue')]"

    # discord button
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
        (By.XPATH, discord_button_xpath))
    )
    link = driver.find_element(
        By.XPATH, discord_button_xpath)
    link.click()

    # discord login
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "uid_8"))
    )
    time.sleep(1)

    input_user = driver.find_element(By.ID, "uid_8")
    input_user.clear()
    input_user.send_keys(discord_user)

    input_pass = driver.find_element(By.ID, "uid_10")
    input_pass.clear()
    input_pass.send_keys(discord_pass + Keys.ENTER)



# ----------------- REGISTER FOR GAME FUNCTION -------------------

def register_for_game(driver):
    join_queue_xpath = "//button[contains(@class, 'button-1') and contains(@class, 'big') and contains(@class, 'blue')]"
    
    # register for game
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, join_queue_xpath))
        )
        link = driver.find_element(By.XPATH, join_queue_xpath)
        link.click()
    except:
        print("Could not find join queue button") 
    
    
    # handle alert
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present(),
                                        "Waiting for alert after registration")
        alert = driver.switch_to.alert
        alert.accept()
        print("Alert accepted")
    except:
        print("No alert appeared after registration")



# ----------------- GO TO GAME FUNCTION -------------------
def go_to_game2(driver):
    go_to_game_xpath = "//a[contains(@class, 'button-1') and contains(@class, 'big') and contains(@class, 'green')]"
    
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, go_to_game_xpath))
    )
    time.sleep(1)
    link = driver.find_element(By.XPATH, go_to_game_xpath)
    link.click()
    print("Clicked on go to game link")
    time.sleep(10)


# ----------------- CRIB GO TO GAME FUNCTION -------------------

def crib_go_to_game(driver, user, password):
    discord_login(driver, user, password)
    register_for_game(driver)
    print("waiting 10 seconds")
    time.sleep(9)
    go_to_game2(driver)



# ----------------- READ LOG FUNCTION -------------------
def read_log(driver):
    # click log button
    log_xpath = (
        "//button[contains(@class, 'button-1') and " +
        "contains(@class, 'show-log-button') and " +
        "contains(@class, 'small-button') and " +
        "contains(@class, 'dark-gray')]"
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, log_xpath))
    )
    log_button = driver.find_element(By.XPATH, log_xpath)
    print("Found log button")
    log_button.click()

    # read log
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'modal-body')]"))
    )
    time.sleep(1)
    log = driver.find_element(By.XPATH, "//div[contains(@class, 'modal-body')]")
    print("Found log")

    return log.text



# ----------------- CALL FUNCTION -------------------
    
def call(driver):
    call_xpath = "//button[contains(@class, 'button-1') and contains(@class, 'call') and contains(@class, 'green')]"

    # Wait for the button to be clickable
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, call_xpath))
    )

    # Find the button and click it
    call_button = driver.find_element(By.XPATH, call_xpath)
    print("Found call button")
    call_button.click()
    print("Clicked call button")


# ----------------- RAISE FUNCTION -------------------

def raise_func(driver, amount):

    # Wait for the button to be clickable
    WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button-1.with-tip.raise.green"))
    )
    # find and click raise button
    raise_button = driver.find_element(By.CSS_SELECTOR, "button.button-1.with-tip.raise.green")
    print("Found raise button")
    raise_button.click()
    print("Clicked raise button")

    # Wait for input to be interactable
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text'].value[pattern='[0-9]*'][inputmode='numeric']"))
    )
    # find and enter amount
    raise_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'].value[pattern='[0-9]*'][inputmode='numeric']")
    print("Found raise input")
    time.sleep(1)
    # raise_input.clear()
    raise_input.send_keys(amount + Keys.ENTER)
    print("Sent raise amount")


# ----------------- CHECK FUNCTION -------------------
def check(driver):
    check_css_selector = "button.button-1.with-tip.check.green"

    # Wait for the Check button to be clickable
    WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, check_css_selector))
    )

    # Find the Check button and click it
    check_button = driver.find_element(By.CSS_SELECTOR, check_css_selector)
    check_button.click()
    print("Clicked Check button")



# ----------------- FOLD FUNCTION -------------------
def fold(driver):
    fold_css_selector = "button.button-1.with-tip.fold.red"

    # Wait for the Fold button to be clickable
    WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, fold_css_selector))
    )

    # Find the Fold button and click it
    fold_button = driver.find_element(By.CSS_SELECTOR, fold_css_selector)
    fold_button.click()
    print("Clicked Fold button")


if __name__ == "__main__":
   
    # chromedriver_path = r"C:\Users\jzlin\OneDrive\Documents\Pokernow\poker_bot_project\pokernow_actions\chromedriver.exe"
    chromedriver_path = r"C:\Users\uclam\Downloads\python_workspaces\pokernow\Pokernow\poker_bot_project\pokernow_actions\chromedriver.exe"
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)

    # crib_go_to_game(driver, "pokertest0915@gmail.com", "Pokernowbot")

    discord_login(driver, "pokertest0915@gmail.com", "Pokernowbot")

    # register_for_game(driver) # remove if already a game in progress

    # go_to_game2(driver)

    # driver.get(r"https://www.pokernow.club/games/pglB7XuZa4_E41m7NtpAENUC9")
    time.sleep(1)
    
    # log = read_log(driver)
    # print(log)
    # call(driver)
    # raise_func(driver, "500")
    # check(driver)
    # fold(driver)
    time.sleep(10)
