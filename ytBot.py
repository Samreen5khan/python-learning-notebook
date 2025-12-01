from selenium import webdriver
import time
from random import randrange

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  

from tkinter import *

#GUI Design

#initialting gui thread loop
root = Tk()

def TriggerBots():
        # print("Function triggered")
        # print(inputLinkValue.get())
       
        # Set up Chrome options
        options = Options() 

        #Refresh Time in seconds
        refresh_time = 20
        browser_list = []
        options = webdriver.ChromeOptions()

        #chrome Exe Path
        options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

        # Create a WebDriver instance
        for _ in range(3):
                driver = webdriver.Chrome()
                browser_list.append(driver)

        for browser in browser_list:
                # You change your youtube link here
                browser.get(inputLinkValue.get())

        while(True):
                browser_num = randrange(0, len(browser_list))
                browser_list[browser_num]
                print("browser number", browser_num, "refreshed")
                time.sleep(refresh_time)

        browser.close()
        


# height X width
root.geometry("550x350")

# min height and width
root.minsize(400,200)

# max height and width
root.maxsize(1200, 988)

#creating a heading
header = Label(root, text="Youtube Bot", font="comicsansms 13 bold", pady=25, padx=50).grid(row=0, column=5)

#creating read only label
inputLink = Label(root, text="Give your link in below text box", font="comicsansms 13", pady=5, padx=50).grid(row=2, column=5)
Label(root, text="No - single qoutes or double quotes", font="comicsansms 10 bold").grid(row=3,column=5)

#declaring variable type
inputLinkValue = StringVar()

#creating input text box/entry point
inputLinkEntry = Entry(root, textvariable=inputLinkValue, width=80).grid(row=4,column=5)

Label(root).grid(row=3, column=1)
Label(root).grid(row=3, column=2)
Label(root).grid(row=3, column=3)
Label(root).grid(row=3, column=4)
Label(root).grid(row=5, column=5)

#creating button and packing
Button(text="Submit", command=TriggerBots).grid(row=6, column=5)

# loop is started here
root.mainloop()







#chrome driver Exe Path
# browser_one  = Service(executable_path=r'https://developer.chrome.com/docs/chromedriver/downloads#current_releases', options=options)
# browser_two  = Service(executable_path=r'https://developer.chrome.com/docs/chromedriver/downloads#chromedriver_1140573590')
# browser_three  = Service(executable_path=r'https://developer.chrome.com/docs/chromedriver/downloads#chromedriver_1140573590')



#driver.get("https://www.youtube.com/")

#browser_list.append( browser_one )
#browser_list.append( browser_two )
#browser_list.append( browser_three )

#browser_list = [driver]



        #YT video link
#        browser_one.get("https://www.google.com")
#        browser_two.get("https://www.google.com")
#        browser_three.get("https://www.google.com")


