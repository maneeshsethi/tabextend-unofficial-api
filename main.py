from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from typing import List
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.keys import Keys

from time import sleep
from dotenv import dotenv_values

from pydantic import BaseModel

config = dotenv_values('.env')
username = config.get('USERNAME')
password = config.get('PASSWORD')


from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class Item(BaseModel):
    position: str
    name: str
    group_name: str
    
    def __str__(self):
        return f'{self.position} - {self.name} (Group: {self.group_name})'
    
    def __repr__(self):
        return self.__str__()
    
class Group(BaseModel):
    position: str
    name: str
    items: List[Item]
    
    def __str__(self):
        return f'{self.position} - {self.name}'
    
    def __repr__(self):
        return self.__str__()
   
    def list_items (self):
        return '\n'.join(map(str, self.items))
    
    
    def __init__(self, position: str, name: str):
        self.position = position
        self.name = name
        self.items = []
    
class Category(BaseModel):
    position: str
    name: str
    
    def __str__(self):
        return f'{self.position} - {self.name}'
    
    def __repr__(self):
        return self.__str__()
        
    def __init__(self, position: str, name: str):
        self.position = position
        self.name = name

options = Options()
options.headless = True
options.add_extension('./tabextend.crx')
options.add_argument("--window-size=1920,1200")


DRIVER_PATH = './chromedriver'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
#driver.get('https://www.tabextend.com/auth/signout')
driver.get('chrome-extension://ffikidnnejmibopbgbelephlpigeniph/index.html');



def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_id(id):
    try:
        driver.find_element(By.ID, id)
    except NoSuchElementException:
        return False
    return True

@app.get('/login')
def login(username=username, password=password):
        while not check_exists_by_xpath("//p[contains(.,'Log in')]"):
            sleep(3)
            #return 'Already logged in'
        
        try:
            login= driver.find_element(By.XPATH, "//p[contains(.,'Log in')] ").click()
            email = driver.find_element(By.XPATH, '//input[@type="email"]').send_keys(username)
            passw = driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(password)
            button = driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            #TODO check if login was successful
            return "Login Successful"
        except:
            #TODO handle bad username/pass
            return "Bad username/password"
  

@app.get('/get_groupname/{group_id}')
def get_groupname(group_id:str):
    x = 1
    xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[{group_id}]/div/div[1]/div/div[2]/div/span'
    if (check_exists_by_xpath(xpath)):
        return str(driver.find_element(By.XPATH, xpath).get_attribute('innerHTML'))
    else:
        return None

@app.get('/get_all_groupnames')
def get_all_groupnames(category:str= None):
    x = 1
    groupnames = []
    xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[{x}]/div/div[1]/div/div[2]/div/span'
    while (check_exists_by_xpath(xpath)):
        groupnames.append(get_groupname(x))
        x += 1
        xpath = f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[{x}]/div/div[1]/div/div[2]/div/span'
    return groupnames
        
    
@app.get('/get_all_items/{group_id}')
def get_all_items_from_group(group_id: str):
    items = []
    x=1
    try:
        while (True):
            xpath='/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[' + str(group_id)+ ']/div/div[2]/div/div[' + str(x)+ ']/div/div/div/div/textarea'
            v=driver.find_element(By.XPATH, xpath).get_attribute('innerHTML')
            group_name=get_groupname(group_id)
            i = Item( position=str(x), name=v, group_name=group_name)
            items.append(i)
            x+=1
    except NoSuchElementException:
        print (items)
        return items
@app.get('/get_all_items')
def get_all_items():
    all_items = {}
    group_position = 1
    xpath='/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[' + str(group_position)+ ']/div/div[2]/div/div[1]/div/div/div/div/textarea'

    while (check_exists_by_xpath(xpath)):
        items = []
        items.append(get_all_items_from_group(group_position))
        group_name=get_groupname(group_position)
        all_items[group_name]= items
        
        group_position += 1
        xpath='/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[' + str(group_position)+ ']/div/div[2]/div/div[1]/div/div/div/div/textarea'

    return all_items


@app.get('/is_logged_in')
def is_logged_in():
    if (check_exists_by_xpath("//p[contains(.,'Log in')]")):
        return False
    return True

    
login()
sleep(4)
# email = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[2]/section/div/form/div[1]/input').send_keys(username)
# #passw = driver.find_element(By.XPATH, '/html/body/div[1]/section[1]/div[1]/form/div[2]/div/div/input').send_keys(password)
# #button = driver.find_element(By.XPATH, '/html/body/div[1]/section[1]/div[1]/form/div[3]/p/button').click()
#  passw = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[2]/section/div/form/div[2]/input').send_keys(password)
#  button = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[2]/section/div/form/button').click()

# sleep(5)

# # my_mits_element=driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]')
# # my_mits_copybutton = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div/div[3]/button')
# # caleb_tasks_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[2]')
# # caleb_tasks_copybutton = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/div/div[3]/button')
# try:

#     my_mits = get_all_items_from_group(1)
#     caleb_tasks = get_all_items_from_group(2)


#     print(my_mits)
#     print(caleb_tasks)

#     print ("one more try")
#     all_items = get_all_items()
#     print(all_items)
    

#     print(get_all_groupnames())
    
#     print( get_groupname(1))

#     print( get_groupname(2))
# except:
#     pass


# print("Groups:")
# print(get_all_groupnames())
# print(get_all_items_from_group(1))

# print("")
# print("All Items:")
# print(get_all_items())

# driver.save_screenshot('screenshot.png')
