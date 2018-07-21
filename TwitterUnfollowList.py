import os.path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


### This method waits for al elements on the page to load
def WaitForLoad(driver):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located
        )
    finally:
        time.sleep(.5)

### This method does the setup by handling the twitter login
def Setup():
    #the following two lines asks the user for username and password and keeps it for later use
    username = input("Enter Username: ")
    password = input("Enter password: ")


    directory = os.path.dirname(os.path.abspath(__file__))  # gets the path of where this file is saved
    location_of_driver = (os.path.join(directory,'chromedriver'))  # appends 'chromedriver' to the current file path - make sure chrome driver is in same directory as this file

    # print(locationOfDriver) #this line may be commented out to make sure its correctly reaching the location of the chromedriver

    driver = webdriver.Chrome(location_of_driver) #gets the chromedriver

    driver.get("https://twitter.com/login")  #navigates the driver to the twitter login page
    WaitForLoad(driver)

    login_list = driver.find_elements_by_name("session[username_or_email]")  # finds the elements on the page that have a matching name

    login_box = login_list[1]  # looking through the HTML, you can see that the second instance of "session[username_or_email]" corresponds to the actual login box
    login_box.send_keys(username, Keys.ARROW_DOWN)  # sending the username to the login box, and the down arrow key to indicate its finished

    password_list = driver.find_elements_by_name("session[password]")  # finds all elements relating to password
    password_box = password_list[1]  # second element mentioned on the page corresponds to the password box

    password_box.send_keys(password, Keys.ARROW_DOWN)  # send the password to the appropriate box

    password_box.send_keys(Keys.TAB, Keys.ENTER)  # navigating and 'clicking' the log in button

    return driver, username


### Returns the list of people you follow
def GetFollowingList(driver, username):
    driver.get("https://twitter.com/" + str(username)) #navigates to the twitter page that was logged into

    num_following = int((driver.find_element_by_xpath('//*[@id="page-container"]/div[3]/div/div[2]/div[2]/div/div[2]/div/div/ul/li[2]/a/span[3]')).text) #extracts how many people you follow

    driver.get("https://twitter.com/" + str(username) + "/following") #navigates the driver to the page of following profiles

    time.sleep(1)

    times_to_scroll = int(num_following/10) #scroll down 1/10 of the number of people you follow

    ## This block of code below scrolls down the indicated number, hopefully loading everyone you follow
    times_scrolled = 0
    while times_scrolled < times_to_scroll:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(.25)
        times_scrolled += 1


    following_found = driver.find_elements_by_class_name('ProfileCard-screenname') #this is a list people you follow

    ## This block of code below makes sure that the number of followers found on the page are equal to the number extracted from the profile page
    ## if not, the page scrolls some more
    extra_scrolls = 0
    while len(following_found) != num_following:
        extra_scrolls+=1
        for _ in range(100):
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.5)
        following_found = driver.find_elements_by_class_name('ProfileCard-screenname')
    print("Extra Scrolls: " + str(extra_scrolls)) #this line prints out how many times the program had loop through the extra scrolling
    # NOTE: if the 'extra scrolls' is too high, try to raise the times_to_scroll variable by dividing by a smaller number

    return(following_found)


### This method takes the list of following profiles and extracts whether or not they follow you. If not, their handle is printed to a file.
def print_to_file(following_list):
    file = open('People_to_unfollow.txt', 'w')
    for following in following_list:
        text_array = following.text.split()
        if len(text_array) < 2:
            twitter_handle = following.text.replace("@", "")
            file.write(twitter_handle + "\n")
    file.close()
    driver.quit()



start = time.time() #starts a timer to see how long it will take
driver, username = Setup() #sets driver, username to the results of the Setup method, which returns the driver and username to be used in another method
following = GetFollowingList(driver, username) #returns the list of people you follow
print_to_file(following) #takes that list that is returned from the GetFollowingList method and prints people who don't follow you back to a file
print("Total time taken: " + str(time.time() - start)) #prints total time
