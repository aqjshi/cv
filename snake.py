import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
def play_game():
    while True:
        # Send the arrow keys to control the snake
        
        game_area.send_keys(Keys.ARROW_RIGHT)
        time.sleep(2)
        game_area.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        game_area.send_keys(Keys.ARROW_LEFT)
        time.sleep(2)
        game_area.send_keys(Keys.ARROW_UP)
        time.sleep(2)
        # You can add more complex movements here based on game logic or continue the loop


# Specify the path to your chromedriver executable
chrome_service = Service('/opt/homebrew/bin/chromedriver')

# Start a new Chrome browser session
driver = webdriver.Chrome(service=chrome_service)

# Open the Patorjk Snake game
driver.get("http://patorjk.com/games/snake/")

# Give the page some time to load
time.sleep(3)

# Optionally, you can click the play button to start the game
try:
    play_button = driver.find_element(By.XPATH, '//button[contains(text(),"Play Game")]')
    play_button.click()
    time.sleep(2)  # Give it some time to start
except Exception as e:
    print(f"Could not start the game automatically: {e}")

# Control the snake by sending arrow key presses
try:
    # Focus on the game area
    game_area = driver.find_element(By.ID, 'game-area')
    game_area.click()  # Make sure the game area is focused

    play_game()



    # You can add more complex movements here based on game logic or continue the loop
except Exception as e:
    print(f"Error interacting with the game: {e}")

# Keep the browser open for a while before quitting
time.sleep(10)

# Close the browser session
driver.quit()
