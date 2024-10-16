import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Chrome driver
def init_driver(chrome_service_path='/opt/homebrew/bin/chromedriver'):
    chrome_service = Service(chrome_service_path)
    return webdriver.Chrome(service=chrome_service)

# Function to open the Google Snake game
def open_snake_game(driver):
    driver.get("https://www.google.com/search?q=snake")
    time.sleep(2)  # Let the page load

# Function to simulate mouse click at given X and Y coordinates
def click_at_position(driver, x, y):
    try:
        driver.execute_script(f"""
            var element = document.elementFromPoint({x}, {y});
            if (element) {{
                var event = new MouseEvent('click', {{
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': {x},
                    'clientY': {y}
                }});
                element.dispatchEvent(event);
            }} else {{
                console.log('No element found at the given coordinates');
            }}
        """)
        print(f"Mouse click simulated at X: {x}, Y: {y}")
        return True
    except Exception as e:
        print(f"Error simulating mouse click at X: {x}, Y: {y}: {e}")
        return False

# Function to find the "Play" button within a specific coordinate range
def find_and_click_dialog_play_button_within_range(driver, x_min, y_min, x_max, y_max):
    try:
        # Find all potential 'Play' buttons based on text or aria-label
        buttons = driver.find_elements(By.XPATH, "//div[contains(text(), 'Play') or @aria-label='Play']")

        for button in buttons:
            location = button.location
            x = location['x']
            y = location['y']
            
            # Check if the button is within the provided coordinate range
            if x_min <= x <= x_max and y_min <= y <= y_max:
                print(f"'Play' button found within range at X={x}, Y={y}")

                # Simulate a click on this button
                click_at_position(driver, x + 10, y + 10)
                return True

        print("No 'Play' button found within the specified coordinate range.")
        return False

    except Exception as e:
        print(f"Error finding or clicking the dialog 'Play' button within the range: {e}")
        return False
    
def log_mouse_position(driver):
    try:
        x = driver.execute_script("return window.mouseX;")
        y = driver.execute_script("return window.mouseY;")
        
        if x is not None and y is not None:
            print(f"Mouse position - X: {x}, Y: {y}")
        else:
            print("Mouse is not moving yet.")
    except Exception as e:
        print(f"Error fetching mouse position: {e}")

# Function to track mouse position
# def track_mouse_position(driver, duration=30):
#     # Inject JavaScript to track mouse movement
#     driver.execute_script("""
#         document.addEventListener('mousemove', function(event) {
#             window.mouseX = event.clientX;
#             window.mouseY = event.clientY;
#         });
#     """)

#     # Log the mouse position every second for the specified duration
#     print("Tracking mouse position. Move your mouse across the page to log coordinates.")
#     for _ in range(duration):
#         log_mouse_position(driver)
#         time.sleep(1)


def play_game(game_area):
    while True:
        game_area.send_keys(Keys.ARROW_RIGHT)
        time.sleep(.5)
        game_area.send_keys(Keys.ARROW_DOWN)
        time.sleep(.5)
        game_area.send_keys(Keys.ARROW_LEFT)
        time.sleep(.5)
        game_area.send_keys(Keys.ARROW_UP)
        time.sleep(.5)




# Main function to run the full workflow
def main():
    driver = init_driver()
    
    try:
        # Open the game
        open_snake_game(driver)

        # Click the initial play button (coordinates may need to be adapted)
        if click_at_position(driver, 261, 492):
            print("Initial 'Play' button clicked. Waiting for dialog 'Play' button...")
            time.sleep(2)

            # Find and click the dialog "Play" button within the specified coordinates
            x_min = 276
            y_min = 262
            x_max = 928
            y_max = 900

            if find_and_click_dialog_play_button_within_range(driver, x_min, y_min, x_max, y_max):
                print("Dialog 'Play' button clicked. Starting the game...")

                # Locate the game area (usually the body or canvas element)
                game_area = driver.find_element(By.TAG_NAME, 'body')
                game_area.click()

                # Start playing the game (this can be extended with actual gameplay logic)
                play_game(game_area)
            else:
                print("Failed to find or click dialog 'Play' button within the range.")
        else:
            print("Initial 'Play' button not clicked. Cannot proceed.")

    finally:
        # Close the browser after interaction
        driver.quit()

if __name__ == "__main__":
    main()
