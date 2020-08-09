#!/usr/bin/python

import time
from selenium import webdriver

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

file_with_friends_to_invite = '/Users/carli/friends_to_invite'
file_of_recent_friends = '/Users/carli/recent_friends'

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\carli\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
options.add_argument('--profile-directory=Profile 1')
driver = webdriver.Chrome(executable_path='/Users/carli/chromedriver.exe',chrome_options=options)

driver.get("https://www.friendsbook.com/carlignacio/friends_recent")

def write_to_file(list, file):
 with open(file,'w') as filehandle:
  for listitem in list:
   filehandle.write('%s\n' % listitem)

def getRecentFriends():
 driver.get("https://www.friendsbook.com/carlignacio/friends_recent")
 
 friends = driver.find_elements_by_xpath('//li[@class="_698"]')
 links = driver.find_element_by_xpath('.//a')
 
 recent_friends = []
 
 for friend in friends:
  a = friend.find_element_by_xpath('.//div[@class="fsl fwb fcb"]')
  b = a.find_element_by_xpath('.//a')
  name = b.get_attribute('text')
  try:
   #print(name)
   recent_friends.append(name)
  except:
   print("Failed to get name")
 return(recent_friends)

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

#write_to_file(recent_friends,'/Users/carli/recent_friends')
def append_to_file(list, file):
 # Open a file with access mode 'a'
 file_object = open(file, 'a')
 # Append 'hello' at the end of file
 for item in list:
  print(item)
  file_object.write(item+'\n')
 # Close the file
 file_object.close()

def run():
 temp1 = getRecentFriends()
 my = read_from_file(file_of_recent_friends)
 s = set(my)
 temp3 = [x for x in temp1 if x not in s]
 append_to_file(temp3,file_with_friends_to_invite)

while True:
 run()
 print('-------')
 time.sleep(60)