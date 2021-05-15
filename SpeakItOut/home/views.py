from django.shortcuts import render, HttpResponse, redirect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


# assign email id and password
mail_address = 'tatusharma321@gmail.com'
password = 'malowali'


def Glogin(mail_address, password,driver):
	# Login Page
	driver.get(
		'https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ')

	# input Gmail
	driver.find_element_by_id("identifierId").send_keys(mail_address)
	driver.find_element_by_id("identifierNext").click()
	driver.implicitly_wait(10)

	# input Password
	driver.find_element_by_xpath(
		'//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
	driver.implicitly_wait(10)
	driver.find_element_by_id("passwordNext").click()
	driver.implicitly_wait(10)

	# go to google home page
	driver.get('https://google.com/')
	driver.implicitly_wait(100)


def turnOffMicCam(driver):
	# # turn off Microphone
	# time.sleep(2)
	# driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[1]/div/div/div').click()
	# driver.implicitly_wait(3000)

	# # turn off camera
	# time.sleep(1)
	# driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[2]/div/div').click()
	# driver.implicitly_wait(3000)

	diss_btn = driver.find_element_by_xpath("/html/body/div/div[3]/div/div[2]/div[3]/div/span/span")
	diss_btn.click()


def joinNow(driver):
	# Join meet
	print(1)
	time.sleep(5)
	driver.implicitly_wait(2000)
	driver.find_element_by_css_selector(
		'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
	print(1)
	

def AskToJoin(driver):
	# Ask to Join meet
	time.sleep(5)
	driver.implicitly_wait(2000)
	driver.find_element_by_css_selector(
		'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
	# Ask to join and join now buttons have same xpaths


def Message(message, driver):
	# finding the text box to type message in text box.
	x_path = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[4]/div[1]/div[1]/div[2]/textarea'
	driver.find_element_by_xpath(x_path).send_keys(message)
	driver.implicitly_wait(10)

	# getting the message button in google meet.
	xpath_btn = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[4]/div[2]/span'
	driver.find_element_by_xpath(xpath_btn).click()
	driver.implicitly_wait(10)


def home(request): 
    return render(request, "home.html")

def enter(request): 

    if request.method == "POST":
        code = request.POST.get('code')

        # create chrome instamce
        opt = Options()
        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_argument('--start-maximized')
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1
        })
        global driver 
        driver = webdriver.Chrome('C:/Selenium Drivers/chromedriver.exe')

        # login to Google account
        Glogin(mail_address, password, driver)
        print('Login')

        # go to google meet
        driver.get('https://meet.google.com/'+code)

        turnOffMicCam(driver)
        print('Turned of MicCAM')

        # AskToJoin()
        joinNow(driver)

        Message('Hello, This is a test message',driver)
        time.sleep(2)
        Message('Hello, This is a test message',driver)
        
        print("done")
        
        return render(request, "home.html")



def postMessage(request): 

    if request.method == "POST":
        msg = request.POST.get('msg')
        Message(msg,driver)
        return render(request, "home.html")

def dashboard(request): 
    return render(request, "dashboard.html")

def meet(request): 
    return render(request, "meet.html")