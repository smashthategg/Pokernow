from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

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

# get_cards(driver) # WORKS

# close_log(driver) # WORKS



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
        EC.element_to_be_clickable((By.ID, "uid_8"))
    )
    # time.sleep(1)

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
        EC.element_to_be_clickable((By.XPATH, go_to_game_xpath))
    )
    time.sleep(5)
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
def read_full_log(driver):
    # click log button
    try:
        log_xpath = (
            "//button[contains(@class, 'button-1') and " +
            "contains(@class, 'show-log-button') and " +
            "contains(@class, 'small-button') and " +
            "contains(@class, 'dark-gray')]"
        )
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, log_xpath))
        )
        log_button = driver.find_element(By.XPATH, log_xpath)
        # print("Found log button")
        log_button.click()
    except ElementClickInterceptedException:
        print("Could not click log button")
        return None

    # read log
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'modal-body')]"))
    )
    time.sleep(1)
    log = driver.find_element(By.XPATH, "//div[contains(@class, 'modal-body')]")
    print("Found log")

    text = log.text

    # close log
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'modal-button-close'))
    )
    close_button = driver.find_element(By.CLASS_NAME, 'modal-button-close')
    close_button.click()
    print("Closed log")

    return text

def read_log(driver):
    # click log button
    try:
        log_xpath = (
            "//button[contains(@class, 'button-1') and " +
            "contains(@class, 'show-log-button') and " +
            "contains(@class, 'small-button') and " +
            "contains(@class, 'dark-gray')]"
        )
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, log_xpath))
        )
        log_button = driver.find_element(By.XPATH, log_xpath)
        log_button.click()
    except ElementClickInterceptedException:
        print("Could not click log button")
        return None

    # wait for the log modal to be visible
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'modal-body')]"))
    )
    time.sleep(2)  # give an extra second for the text to fully load
    log_modal = driver.find_element(By.XPATH, "//div[contains(@class, 'modal-body')]")
    
    # read log content
    text = log_modal.text
    hand_marker = "-- starting hand #"
    index = text.find(hand_marker, 1)  # start searching from index 1 to skip the first occurrence

    if index != -1:
        text = text[:index]  # cut the text up to the next hand marker
    else:
        print("No additional starting hand marker found.")

    # close log modal
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'modal-button-close'))
    )
    close_button = driver.find_element(By.CLASS_NAME, 'modal-button-close')
    close_button.click()
    
    return text


def check_turn0(driver):
    try:
        # Define the CSS selector for the "Your Turn" element
        your_turn_selector = "p.action-signal.suspended"

        # Wait for the element to be visible on the page
        element = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, your_turn_selector))
        )

        # Check the text of the element to confirm it's the "Your Turn" signal
        if element.text == "Your Turn":
            return True
        else:
            print("Element found, but text does not match.")
            return False

    except:
        return False


def check_turn(driver):
    try:
        # Define the button selector
        button_selector = 'button.button-1.with-tip.time-bank.suspended-action'
        
        # Wait for the button to be visible on the page
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, button_selector)))
        
        # If the button is visible, it's your turn
        return True
    except:
        # If the button is not found or not visible within the timeout, it's not your turn
        if check_turn0(driver):
            return True
        return False


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



def all_in(driver):
    # Define the CSS selector and the specific text we're looking for
    button_css_selector = "button.button-1.default-bet-button"
    button_text = "All In"

    try:
        # Wait for the button to be present and ensure it's the right one by text
        all_in_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_css_selector))
        )

        # Find all elements that match the class and then filter by text
        buttons = driver.find_elements(By.CSS_SELECTOR, button_css_selector)
        for button in buttons:
            if button.text == button_text:
                button.click()
                print("Clicked 'All In' button.")
                return True
        print("No 'All In' button found with the specified text.")
        return False

    except TimeoutException:
        print("Timeout waiting for 'All In' button.")
        return False


# ----------------- RAISE FUNCTION -------------------

def raise_func(driver, amount):

    # Wait for the button to be clickable
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button-1.with-tip.raise.green"))
    )
    # find and click raise button
    raise_button = driver.find_element(By.CSS_SELECTOR, "button.button-1.with-tip.raise.green")
    print("Found raise button")
    raise_button.click()
    print("Clicked raise button")

    # Wait for input to be interactable
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text'].value[pattern='[0-9]*'][inputmode='numeric']"))
    )
    # find and enter amount
    raise_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'].value[pattern='[0-9]*'][inputmode='numeric']")
    print("Found raise input")
    # time.sleep(1)

    # raise_input.clear()
    raise_input.send_keys(str(int(amount)) + Keys.ENTER)
    print("Sent raise amount")

    if (check_turn(driver)):
        all_in(driver)



# ----------------- CHECK FUNCTION -------------------

def check(driver):
    check_css_selector = "button.button-1.with-tip.check.green"
    try:
        # Wait for the Check button to be clickable
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, check_css_selector))
        )
        # Find the Check button and click it
        check_button = driver.find_element(By.CSS_SELECTOR, check_css_selector)
        check_button.click()
        print("Clicked Check button")
        return True
    except TimeoutException:
        print("Check button not available.")
        return False


# ----------------- FOLD FUNCTION -------------------

def fold(driver):
    fold_css_selector = "button.button-1.with-tip.fold.red"
    try:
        # Wait for the Fold button to be clickable
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, fold_css_selector))
        )
        # Find the Fold button and click it
        fold_button = driver.find_element(By.CSS_SELECTOR, fold_css_selector)
        fold_button.click()
        print("Clicked Fold button")
        return True
    except TimeoutException:
        print("Fold button not available.")
        return False

# ----------------- CHECK OR FOLD FUNCTION -------------------

def check_fold(driver):
    # First try to check
    if not check(driver):  # If checking is not successful
        # Try to fold if checking was not possible
        if not fold(driver):  # If folding is also not successful
            print("Neither Check nor Fold was possible.")



# ----------------- GET CARDS FUNCTION -------------------

def get_cards(driver):
    # Find the container that holds the relevant cards
    card_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.table-player-cards"))
    )

    # Within this container, find all card elements that contain both value and suit
    card_elements = card_container.find_elements(By.CSS_SELECTOR, ".card-container")
    
    cards_list = []  # Initialize a list to store card values and suits
    suit_map = {'d': 'diamonds', 'h': 'hearts', 's': 'spades', 'c': 'clubs'}  # Mapping of suit symbols to words
    
    # Extract values and suits for each card
    for card in card_elements:
        try:
            # Check for the presence of value and suit elements within each card
            value = WebDriverWait(card, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".value"))
            ).text

            # Convert '10' to 'T'
            if value == '10':
                value = 'T'
            
            # Get all suit elements and filter out the ones with non-empty text
            suit_elements = WebDriverWait(card, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".suit"))
            )
            suit_symbol = next((el.text for el in suit_elements if el.text), 'unknown')
            suit = suit_map.get(suit_symbol, 'unknown')

            cards_list.extend([value, suit])
        except TimeoutException:
            print("Timed out waiting for card details to load.")
        except NoSuchElementException:
            print("One of the elements (value or suit) was not found for a card.")
    
    return cards_list


    



def read_pot(driver):
    try:
        # First, try to find and read the number from the first specified element
        add_on_value = driver.find_element(By.CSS_SELECTOR, ".add-on-container .chips-value .normal-value").text
        if add_on_value:
            return int(add_on_value)
    except NoSuchElementException:
        print("Add-on value not found.")
    # If the first element is not found, try the second element
    try:
        main_value = driver.find_element(By.CSS_SELECTOR, ".main-value .chips-value .normal-value").text
        return int(main_value)
    except NoSuchElementException:
        # If neither element is found, handle the error (you could return None or raise an exception)
        print("Neither element was found.")
        return None
    




if __name__ == "__main__":
   
    # chromedriver_path = r"C:\Users\jzlin\OneDrive\Documents\Pokernow\poker_bot_project\pokernow_actions\chromedriver.exe"
    chromedriver_path = r"C:\Users\uclam\Downloads\python_workspaces\pokernow\Pokernow\poker_bot_project\pokernow_actions\chromedriver.exe"
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)

    # crib_go_to_game(driver, "pokertest0915@gmail.com", "Pokernowbot")
    # driver.get(r'https://www.pokernow.club/games/pglZNexZmWZd2POyDldrW0qBl')

    discord_login(driver, "pokertest0915@gmail.com", "Pokernowbot")
    time.sleep(5)
    driver.get(r'https://www.pokernow.club/games/pgloE9xqVVmpKmM-BiKK5Fkg-')


    # register_for_game(driver) # remove if already a game in progress

    # go_to_game2(driver)

    # time.sleep(10)
    # driver.get(r"https://www.pokernow.club/games/pgl2DU_IERjgn3gojbVHVo387")
    # time.sleep(1)
    
    #log = read_log(driver)
    # print(log)
    # call(driver)
    # raise_func(driver, "500")
    # check(driver)
    # fold(driver)

    # print(get_cards(driver))
    print(check_turn(driver))
    time.sleep(10)


'''
<button class="button-1 default-bet-button" type="button">All In</button>
'''