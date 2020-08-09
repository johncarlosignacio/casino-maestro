#!/usr/bin/python

import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(.3)
    apply_style(original_style)

def read_from_file(file):
 places = []
 # open file and read the content in a list
 with open(file, 'r') as filehandle:
  for line in filehandle:
   # remove linebreak which is the last character of the string
   currentPlace = line[:-1]
   # add item to the list
   places.append(currentPlace)
  return(places)

def append_to_file(list, file):
 # Open a file with access mode 'a'
 file_object = open(file, 'a')
 # Append 'hello' at the end of file
 for item in list:
  # print(item)
  file_object.write(item+'\n')
 # Close the file
 file_object.close()

def clear_contents_of_file(fName):
    with open(fName, "w"):
        pass

def close_village_news_window(driver, iframe, zero_elem):
    print("Trying to close the village news...")
    try:
        driver.switch_to.frame(iframe)
    except:
        print("Warning: already switched to iframe")
    x = 484
    y = 150
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(zero_elem, x, y).click().perform()

def click_invite_window(driver, iframe, zero_elem):
    print("Trying to open invite window...")
    try:
        driver.switch_to.frame(iframe)
    except:
        print("Warning: already switched to iframe")
    x = 328
    y = 444
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(zero_elem, x, y).click().perform()


file_with_friends_to_add = '/Users/carli/friends_to_invite'
file_of_recent_friends = '/Users/carli/recent_friends'

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\carli\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
options.add_argument('--profile-directory=Profile 2')
driver = webdriver.Chrome(executable_path='/Users/carli/chromedriver.exe',chrome_options=options)

driver.get("https://apps.friendsbook.com/casino-maestro/")

time.sleep(20)

iframe = driver.find_elements_by_xpath('//iframe')[0]
driver.switch_to.frame(iframe)
cm = driver.find_element_by_xpath('.//canvas')
invite_button = driver.find_elements_by_xpath('.//a[@title="Invite"]')[0]
invite_button.click()

zero_elem = cm
x_body_offset = zero_elem.location["x"]
y_body_offset = zero_elem.location["y"]
print("Body coordinates: {}, {}".format(x_body_offset, y_body_offset))

x = 328
y = 444

def add_friends(driver, iframe, zero_elem, file, output):
    invite_button = driver.find_elements_by_xpath('.//a[@title="Invite"]')[0]
    invite_button.click()
    names = read_from_file(file)
    if(len(names)>0):
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(zero_elem, x, y).click().perform()
        time.sleep(2)
        driver.switch_to.default_content()
        i=0
        while i < len(names):        
            print("Inviting " + names[i], end="... ")
            try:
                key_in_name(driver, names[i])
                i+=1
            except:
                print("Failed to open invite window. Trying again in 5 seconds...")
                time.sleep(2)
                close_village_news_window(driver, iframe, zero_elem)
                time.sleep(3)
                click_invite_window(driver, iframe, zero_elem)
                driver.switch_to.default_content()
        append_to_file(names, output)
        clear_contents_of_file(file)
        done_button = driver.find_elements_by_xpath('.//button[@name="__CONFIRM__"]')[0]
        done_button.click()
        driver.switch_to.frame(iframe)
    else:
        print("We have invited everyone to CM!")

def key_in_name(driver, name):
    search_bar = driver.find_elements_by_xpath('.//input[@placeholder="Search more friends..."]')[0]
    search_bar.send_keys(Keys.CONTROL + "a"+ Keys.DELETE)
    search_bar.send_keys(name)
    time.sleep(1)
    try:
        send_request(driver)
    except:
        print("FAILED!")

def send_request(driver):
    send = driver.find_elements_by_xpath('.//button[contains(.,"Send")]')[0]
    send.click()
    print("Success!")

while(True):
    add_friends(driver, iframe, zero_elem, file_with_friends_to_add, file_of_recent_friends)
    time.sleep(20)