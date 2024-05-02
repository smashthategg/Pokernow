from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chromedriver_path = r"C:\Users\uclam\Downloads\python_workspaces\pokernow\Pokernow\poker_bot_project\pokernow_actions\chromedriver.exe"
discord_user = ""
discord_pass = ""



service = Service(executable_path = chromedriver_path)
driver = webdriver.Chrome(service=service)


driver.get("https://network.pokernow.club/sng_tournaments")
print(driver.title)

# discord button
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'button-1') and contains(@class, 'big') and contains(@class, 'blue')]"))
)
link = driver.find_element(By.XPATH, "//button[contains(@class, 'button-1') and contains(@class, 'big') and contains(@class, 'blue')]")
link.click()

# discord login
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "uid_8"))
)

input_user = driver.find_element(By.ID, "uid_8")
input_user.clear()
input_user.send_keys(discord_user)

input_pass = driver.find_element(By.ID, "uid_10")
input_pass.clear()
input_pass.send_keys(discord_pass + Keys.ENTER)

time.sleep(5)
driver.quit()


'''
BUTTON ELEMENT DETAILS:

discord button: <button type="button" class="button-1 big blue">Join with your Discord</button>

discord login: <input class="inputDefault__22335 input_f27786 inputField__9fd91" id="uid_8" name="email" 
        type="text" placeholder="" aria-label="Email or Phone Number" required="" autocomplete="off" 
        autocapitalize="none" autocorrect="off" maxlength="999" spellcheck="false" 
        aria-labelledby=":r0:" value="">

discord password: "uid_10"

go to existing room: 
            <a href="https://network.pokernow.club/sng_tournaments/fcea2f82c75d6f128c3a3e9c187920d9/table"
            target="_blank" class="button-1 big green">Click here to go to the Room</a>

checkbox to notify when game is ready: <input type="checkbox" readonly="">

skip voicecall: <button type="button" class="button-1 middle-gray">Skip Video/Voice for Now</button>

call: <button class="button-1 call with-tip call green " type="button">Call 45</button>

raise: <button class="button-1 with-tip raise green" type="button">Raise</button>

raise_input: <input type="text" class="value" pattern="[0-9]*" inputmode="numeric" value="120">

check: <button class="button-1 with-tip check green " type="button">Check</button>

fold: <button class="button-1 with-tip fold red " type="button">Fold</button>

log: <button class="button-1 show-log-button small-button dark-gray" type="button">Log</button>

ledger (not useful): <button class="button-1 green-2 small-button highlighted ledger-button" type="button">Ledger</button>

close ledger/log: <button class="modal-button-close" type="button">Close</button>

end game view: <div class="alert-1-buttons"><button type="button" class="button-1 middle-gray">Ok</button><button 
        type="button" class="button-1 middle-gray">Go to Tournaments</button></div>

end game button (go to tournaments): <button type="button" class="button-1 middle-gray">Go to Tournaments</button>
'''


'''
Graveyard:
    # click to notify when game is ready
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox'][readonly]"))
    )
    checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox'][readonly]")
    checkbox.click()

    # click to go to room
    WebDriverWait(driver, 300)



# ----------------- GO TO GAME FUNCTION -------------------
    
def go_to_game(driver):
    go_to_game_xpath = "//a[contains(text() , 'Click here to go to the Room')]"
    # go_to_game_xpath = "//a[contains(@class, 'button-1') and contains(@class, 'big') and contains(@class, 'green')]"
    
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, go_to_game_xpath))
    )
    link = driver.find_element(By.XPATH, go_to_game_xpath)
    link.click()


# ----------------- GO TO EXISTING GAME FUNCTION -------------------
    
def go_to_existing_game(driver):
    existing_game_xpath = "//a[contains(@class, 'button-1') and contains(@class, 'big') and contains(@class, 'green')]"
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, existing_game_xpath))
    )
    link = driver.find_element(By.XPATH, existing_game_xpath)
    driver.execute_script("arguments[0].click();", link) # og javascript click

# ----------------- GET GAME LINK FUNCTION -------------------
 
def get_game_link(driver):
    # locate the area with the game link
    try:
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.ID, "main-sng-tournament-app-container"))
        )
        time.sleep()
        container = driver.find_element(By.ID, "main-sng-tournament-app-container")
        print("container located\n")
        # print(container.text)
        container_html = container.get_attribute("outerHTML")
        print("\nHTML source of the container:\n", container_html)

    except:
        print("Could not find container")


    pattern = r'https://network\.pokernow\.club/sng_tournaments/.*/table'

    # Use re.search() to find the first occurrence of the link
    match = re.search(pattern, container_html)

    # Check if a match was found
    if match:
        game_link = match.group()
        print(f"Found game link: {game_link}")
        return game_link
    else:
        print("No link found matching the pattern.")
        return None
    
    # For auto enabling notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "profile.default_content_setting_values.notifications": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)


    # Create a new instance of the Chrome driver
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)


driver.get("https://www.google.com")

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.NAME, "q"))
)

input_element = driver.find_element(By.NAME, "q")
input_element.clear()
input_element.send_keys("poop" + Keys.ENTER)

link = driver.find_element(By.LINK_TEXT, "Images")
link.click()

time.sleep(5)
driver.quit()
'''

#w1 learn
#w2 program
#w3 integrate


'''
Found log
12:57
-- ending hand #6 --
12:57
luc2 collected 20 from pot
12:57
Uncalled bet of 10 returned to luc2
12:57
luc1 folds
12:57
luc2 posts a big blind of 20
12:57
luc1 posts a small blind of 10
12:57
Player stacks: #1 luc1 (970) | #2 luc2 (1030)
12:57
-- starting hand #6 (id: fisdtpueve27) (No Limit Texas Hold'em) (dealer: luc1) --     
12:56
-- ending hand #5 --
12:56
luc1 collected 20 from pot
12:56
Uncalled bet of 10 returned to luc1
12:56
luc2 folds
12:56
luc1 posts a big blind of 20
12:56
luc2 posts a small blind of 10
12:56
Player stacks: #1 luc1 (960) | #2 luc2 (1040)
12:56
-- starting hand #5 (id: onlqnbidryow) (No Limit Texas Hold'em) (dealer: luc2) --     
12:56
-- ending hand #4 --
12:56
luc2 collected 20 from pot
12:56
Uncalled bet of 10 returned to luc2
12:56
luc1 folds
12:56
luc2 posts a big blind of 20
12:56
luc1 posts a small blind of 10
12:56
Player stacks: #1 luc1 (970) | #2 luc2 (1030)
12:56
-- starting hand #4 (id: we3qhagujazj) (No Limit Texas Hold'em) (dealer: luc1) --     
12:56
-- ending hand #3 --
12:56
luc1 collected 20 from pot
12:56
Uncalled bet of 10 returned to luc1
12:56
luc2 folds
12:55
luc1 posts a big blind of 20
12:55
luc2 posts a small blind of 10
12:55
Player stacks: #1 luc1 (960) | #2 luc2 (1040)
12:55
-- starting hand #3 (id: hvsqmmxaoe6z) (No Limit Texas Hold'em) (dealer: luc2) --     
12:55
-- ending hand #2 --
12:55
luc2 collected 160 from pot
12:55
Uncalled bet of 80 returned to luc2
12:55
luc1 folds
12:55
luc2 raises to 120
12:55
luc1 bets 40
12:55
luc2 checks
12:55
Flop: [Q♣, 7♠, 8♣]
12:55
luc1 calls 40
12:55
luc2 raises to 40
12:55
luc1 calls 20
12:55
luc2 posts a big blind of 20
12:55
luc1 posts a small blind of 10
12:55
Player stacks: #1 luc1 (1040) | #2 luc2 (960)
12:55
-- starting hand #2 (id: 7vuwhjcxxsj1) (No Limit Texas Hold'em) (dealer: luc1) --     
12:55

'''