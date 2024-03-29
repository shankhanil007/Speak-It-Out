from django.shortcuts import render, HttpResponse, redirect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
from home.models import Meet, Message, Buffer

# assign email id and password
mail_address = ''
password = ''


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
	time.sleep(5)
	driver.implicitly_wait(2000)
	driver.find_element_by_css_selector(
		'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
	

def AskToJoin(driver):
	# Ask to Join meet
	time.sleep(5)
	driver.implicitly_wait(2000)
	driver.find_element_by_css_selector(
		'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
	# Ask to join and join now buttons have same xpaths






#------------------------------------------------------------------------------------------------

def home(request): 
    return render(request, "home.html")

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('dashboard')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('dashboard')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        login(request, myuser)
        messages.success(request, "Account successfully created")
        return redirect('dashboard')

    else:
        return HttpResponse("404 - Not found")


def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect('dashboard')

    return HttpResponse("404- Not found")
    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('dashboard')

def dashboard(request): 
    return render(request, "dashboard.html")

def meet(request): 

    if request.method=="POST":
        code=request.POST['code']
        meet_obj = Meet.objects.filter(code = code).first()

        if meet_obj:
            if meet_obj.status :
                context={'code':code}
                return render(request, "postMessage.html", context)

            messages.error(request, "The meeting code is not active")
            return render(request, "home.html")
        messages.error(request, "The meeting code is not active")
        return render(request, "home.html")


def meetMessage(request,slug):
    context={'code':slug}
    return render(request, "meetMessage.html", context)

def postMessage(request,slug): 

    if request.method == "POST":
        content = request.POST.get('content')
        meet= Meet.objects.get(code=slug)
        message=Message(content=content, meet=meet, code=slug)
        message.save()
        context={'code':slug}

    return render(request, "postMessage.html", context)

def meetActivate(request): 

    if request.method == "POST":
        meetCode = request.POST.get('meetCode')
        meet = Meet(code=meetCode, status=True)
        meet.save()
        return redirect(f"/{meetCode}/newMessages")


def enter(request, slug): 

    code = slug

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

    # go to google meet
    driver.get('https://meet.google.com/'+code)

    turnOffMicCam(driver)

    # AskToJoin()
    joinNow(driver)

    # Message('Hello, This is a test message',driver)
    # time.sleep(2)
    # Message('Hello, This is a test message',driver)

    
    messages = Message.objects.filter(code = slug)
    context={'code':slug, 'messages': messages}
    return render(request, "newMessages.html", context)


def newMessages(request, slug): 
    messages = Message.objects.filter(code = slug)
    context={'code':slug, 'messages': messages}
    return render(request, "newMessages.html", context)


def bufferMessages(request, slug): 
    messages = Buffer.objects.filter(code = slug)
    context={'code':slug, 'messages': messages}
    return render(request, "bufferMessages.html", context)

def deleteMessage(request, slug, id): 
    message = Message.objects.get(sno = id)
    message.delete()
    messages = Message.objects.filter(code = slug)
    context={'code':slug, 'messages': messages}
    return render(request, "newMessages.html", context)

def buffer(request, slug, id): 
    message = Message.objects.get(sno = id)
    buffer = Buffer(content=message.content, meet=message.meet, code=slug)
    buffer.save()
    message.delete()
    messages = Message.objects.filter(code = slug)
    context={'code':slug, 'messages': messages}
    return render(request, "newMessages.html", context)



def sendMessage(request, slug, id, source):

    if source == "buffer":
        message = Buffer.objects.get(sno = id)

        # finding the text box to type message in text box.
        x_path = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[4]/div[1]/div[1]/div[2]/textarea'
        driver.find_element_by_xpath(x_path).send_keys(message.content)
        driver.implicitly_wait(10)

        # getting the message button in google meet.
        xpath_btn = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[4]/div[2]/span'
        driver.find_element_by_xpath(xpath_btn).click()
        driver.implicitly_wait(10)

        message.delete()
        messages = Buffer.objects.filter(code = slug)
        context={'code':slug, 'messages': messages}
        return render(request, "bufferMessages.html", context)

    else:
        message = Message.objects.get(sno = id)

        # finding the text box to type message in text box.
        x_path = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[4]/div[1]/div[1]/div[2]/textarea'
        driver.find_element_by_xpath(x_path).send_keys(message.content)
        driver.implicitly_wait(10)

        # getting the message button in google meet.
        xpath_btn = '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[4]/div/div[2]/div[2]/div[2]/span[2]/div/div[4]/div[2]/span'
        driver.find_element_by_xpath(xpath_btn).click()
        driver.implicitly_wait(10)

        message.delete()
        messages = Message.objects.filter(code = slug)
        context={'code':slug, 'messages': messages}
        return render(request, "newMessages.html", context)
