from PIL import Image, ImageDraw
from selenium import webdriver
import os
import sys
import time 

class ScreenAnalysis:

    CHROME_URL = 'https://www.hvg.hu/'
    FIREFOX_URL = 'https://www.hvg.hu/'
    ChromeDriver = None
    FirefoxDriver = None

    def __init__(self):
        startall = time.time()
        os.makedirs('./screenshots', exist_ok=True)
        self.set_up()
        startcap = time.time()
        self.capture_screens() # Comment for manual use
        print ('Capture - ', time.time()- startcap)
        startan = time.time()
        self.analyze()
        print ('Analyze - ', time.time()- startan)
        self.clean_up()
        print ('All - ', time.time()- startall)

    def set_up(self):
        # Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('headless') # Headless option
        options.add_argument("start-maximized");
        self.ChromeDriver = webdriver.Chrome(options=options)
        # Firefox
        options = webdriver.FirefoxOptions()
        options.headless = True # Headless option
        self.FirefoxDriver = webdriver.Firefox(options=options)
        self.FirefoxDriver.maximize_window()

    def clean_up(self):
        self.ChromeDriver.close()
        self.FirefoxDriver.close()

    def capture_screens(self):
        self.screenshot(self.CHROME_URL, 'screenshot_chrome.png', 'chrome')
        self.screenshot(self.FIREFOX_URL, 'screenshot_firefox.png', 'firefox')

    def screenshot(self, url, file_name, driver_type):
        path = os.path.join('./', 'screenshots', file_name)
        if (driver_type == 'chrome'):
            print("Capturing", url, "screenshot as", file_name, "with chrome...")
            self.ChromeDriver.get(url)
            height = self.ChromeDriver.execute_script("return document.body.scrollHeight")
            self.ChromeDriver.set_window_size(1920,height+100)
            self.ChromeDriver.save_screenshot(path)
            print("Done.")
        elif (driver_type == 'firefox'):
            print("Capturing", url, "screenshot as", file_name, "with firefox ...")
            self.FirefoxDriver.get(url)
            height = self.FirefoxDriver.execute_script("return document.body.scrollHeight")
            self.FirefoxDriver.set_window_size(1920,height+100)
            self.FirefoxDriver.save_screenshot(path)
            print("Done.")
        
        
    def analyze(self):
        print("Analyzing screenshots...")
        screenshot_chrome = Image.open("screenshots/screenshot_chrome.png")
        screenshot_firefox = Image.open("screenshots/screenshot_firefox.png")
        columns = 120
        rows = 160
        screen_width, screen_height = screenshot_chrome.size

        block_width = ((screen_width - 1) // columns) + 1 # this is just a division ceiling
        block_height = ((screen_height - 1) // rows) + 1

        for y in range(0, screen_height, block_height+1):
            for x in range(0, screen_width, block_width+1):
                region_staging = self.process_region(screenshot_chrome, x, y, block_width, block_height)
                region_production = self.process_region(screenshot_firefox, x, y, block_width, block_height)

                if region_staging is not None and region_production is not None and region_production != region_staging:
                    draw = ImageDraw.Draw(screenshot_chrome)
                    draw.rectangle((x, y, x+block_width, y+block_height), outline = "red")

        screenshot_chrome.save("screenshots/result.png")
        print("Result screenshot saved!")

    def process_region(self, image, x, y, width, height):
        region_total = 0

        # This can be used as the sensitivity factor, the larger it is the less sensitive the comparison
        factor = 100

        for coordinateY in range(y, y+height):
            for coordinateX in range(x, x+width):
                try:
                    pixel = image.getpixel((coordinateX, coordinateY))
                    region_total += sum(pixel)/4
                except:
                    return

        return region_total/factor

ScreenAnalysis()