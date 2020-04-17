## Info

This script takes two screenshots with the help of Selenium automation framework, one with the chrome driver, one with the firefox driver and compares them. The results will be printed as an image with red squares to show different areas.

## Usage

- It is recommended to activate venv and then install the requirements.

- The script also requires the used browser engines to be installed and added to PATH. <br>
(If you use chocolatey -> https://chocolatey.org/packages/selenium-all-drivers)

- Change url constants to compare screenshots of the pages you would like to check out.

- To compare custom pictures just put screenshots with the correct name into the 'screenshots' folder and comment the 'capture_screens' function.

## How it works

Comparation is done by calculating average brightness per square and it draws the squares which are different.

## [Based on](https://blog.rinatussenov.com/automating-manual-visual-regression-tests-with-python-and-selenium-be66be950196)