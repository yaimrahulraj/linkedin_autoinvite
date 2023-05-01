#!/usr/bin/env python
# coding: utf-8

# In[1]:


# connect python with webbrowser-chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui as pag
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains


# In[2]:


#User Input
username = "enter-your mail-id"
password = "enter-your-password"
keywords = ["talent acquisition"]
message = """Hi,

I hope you're doing well. I'm excited to explore new opportunities and believe my skills and experience would make me a valuable asset to your team. Please let me know if you have any potential opportunities available.

Thanks,
Your-name"""
# Number of requests you want to send
num_req = 100


# In[3]:


#tracker for number of people
pplCounter = 0


# In[4]:


def login(driver, wait, username, password):
    try:
        print("logging in to linkedin!")
        # Getting the login element and Sending the keys for username	
        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="session_key"]'))).send_keys(username)
        #//*[@id="session_key"]
        #//*[@id="session_password"]

        # Getting the password element and Sending the keys for password
        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="session_password"]'))).send_keys(password)
        # Getting the tag for submit button					
        #//*[@id="main-content"]/section[1]/div/div/form[1]/div[2]/button
        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="main-content"]/section[1]/div/div/form[1]/div[2]/button'))).click()
        print("Successfully logged in!")
    except:
        print("linkedin login failed!")
    


# In[5]:


def login1(driver, wait, username, password): 
    wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="email-or-phone"]'))).send_keys(username)
    wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="password"]'))).send_keys(password)


# In[6]:


def goto_network(driver, wait):
	driver.find_element_by_id("mynetwork-tab-icon").click()


# In[7]:


#Connecting with people
def send_requests(driver, wait,keyword):
    try:
        print("Inviting in Progress!!")
        for i in range(1, 11):
            try:
                connect_str = f'/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[{i}]/div/div/div[3]/div/button'
                all_buttons = driver.find_elements_by_tag_name("button")
                connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]
                for btn in connect_buttons:
                    driver.execute_script("arguments[0].click();", btn)
                    add_note = driver.find_element_by_xpath("//button[@aria-label='Add a note']")
                    driver.execute_script("arguments[0].click();", add_note)
                    wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="custom-message"]'))).send_keys(message)
                    send = driver.find_element_by_xpath("//button[@aria-label='Send now']")
                    driver.execute_script("arguments[0].click();", send)
                pplCounter +=1
            except:
                pass
        print(f"Completed Inviting people from {keyword}")
    except:
        print("Inviting people failed!")


# In[8]:


##Filter by the keywords and parse the html using bs4
def nav_page(driver, wait, num_req):
    for i in keywords:
        for j in range(1,num_req+1):
            driver.get("https://www.linkedin.com/search/results/people/?keywords="+i+"&page="+str(j))
            send_requests(driver, wait, i)


# In[9]:


def main():
    try:
        print("Starting the Bot!")
        # url of LinkedIn
        url = "http://linkedin.com/"
        # url of LinkedIn network page
        network_url = "https://www.linkedin.com/mynetwork/"
        # path to browser web driver
        chrome_options = Options()
        chrome_driver = ChromeDriverManager()
        chrome_options.add_argument('--ignore-certificate-errors')
        prefs = {"disable-transitions": True}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_driver.install(), options=chrome_options)
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])
        wait = WebDriverWait(driver, 10)    
        driver.get(url)
        login(driver,wait, username, password)
        try:
            ele = driver.find_element_by_xpath('//*[@id="email-or-phone"]')
            if(ele.is_displayed()):
                login1(driver,wait, username, password)
        except:
            pass
        nav_page(driver, wait, num_req)
        print(f"Congrats, you have connected with {pplCounter}, across {len(keywords)} keywords!")
    except Exception as e:
        print(f"Exception {e}, Occurred!", "\n", "Please try again!!")
    
    


# In[10]:


# Driver's code
if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




