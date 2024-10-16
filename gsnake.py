import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Specify the path to your chromedriver executable
chrome_service = Service('/opt/homebrew/bin/chromedriver')

# Start a new Chrome browser session
driver = webdriver.Chrome(service=chrome_service)

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
    except Exception as e:
        print(f"Error simulating mouse click at X: {x}, Y: {y}: {e}")

# Function to play the snake game by controlling the arrow keys
def play_game(driver, game_area):
    try:
        # Click the dialog play button (coordinates need to be adapted)
        click_at_position(driver, 596, 712)
        while True:
            # Simulate snake movements
            game_area.send_keys(Keys.ARROW_RIGHT)
            time.sleep(.5)
            game_area.send_keys(Keys.ARROW_DOWN)
            time.sleep(.5)
            game_area.send_keys(Keys.ARROW_LEFT)
            time.sleep(.5)
            game_area.send_keys(Keys.ARROW_UP)
            time.sleep(.5)
    except KeyboardInterrupt:
        print("Game interaction stopped.")

# Function to log mouse position every second
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

# Function to track the mouse position periodically
def track_mouse_position(driver, duration=30):
    # Inject JavaScript to track mouse movement
    driver.execute_script("""
        document.addEventListener('mousemove', function(event) {
            window.mouseX = event.clientX;
            window.mouseY = event.clientY;
        });
    """)

    # Log the mouse position every second for the specified duration
    print("Tracking mouse position. Move your mouse across the page to log coordinates.")
    for _ in range(duration):
        log_mouse_position(driver)
        time.sleep(1)

# Main workflow
if __name__ == "__main__":
    try:
        # Open the game
        open_snake_game(driver)

        # Click the initial play button (Coordinates will depend on where the button is on the screen)
        click_at_position(driver, 297, 495)

        # Locate the game area (usually the body or canvas element)
        game_area = driver.find_element(By.TAG_NAME, 'body')
        game_area.click()

        # Start playing the game
        play_game(driver, game_area)

        # Optionally, track mouse position (unrelated to game, but included per request)
        track_mouse_position(driver)

    finally:
        # Close the browser after interaction
        driver.quit()
