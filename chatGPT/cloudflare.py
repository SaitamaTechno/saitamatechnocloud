import pyautogui
import time
import pyperclip

time.sleep(3)

t=10
mt=30
bt=60
def first_js():
    run_js('''
    function getElementByXpath(path) {
      return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    }''')
def fill(msg):
    pyperclip.copy(msg)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(t)

def run_js(command):
    pyautogui.hotkey("ctrl", "shift", "j")
    time.sleep(t)
    fill(command)
    pyautogui.press("enter")
    pyautogui.hotkey("ctrl", "shift", "j")
    time.sleep(t)

def delete_domain(num):
    run_js('''
    var delete_domain=getElementByXpath("/html/body/div[1]/div[1]/main/div/form/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div/table/tbody/tr[{}]/td[6]/div[2]/button")
    delete_domain.click()
    '''.format(num+1))
    time.sleep(t)
    run_js('''
    var delete_hostname=getElementByXpath("/html/body/div[7]/div/div/div/div/div[2]/div/div/button[2]")
    delete_hostname.click()
    ''')
    time.sleep(bt)
def create_domain(subdomain, domain, service, IP, PORT):
    command1='''var add_hostname=getElementByXpath("/html/body/div[1]/div[1]/main/div/form/div/div[2]/div[2]/div[1]/div/a")
    add_hostname.click()'''
    run_js(command1)

    pyautogui.press("tab", presses=2)
    fill(subdomain)
    pyautogui.press("tab")
    fill(domain)
    pyautogui.press("tab", presses=4)
    fill("{}:{}".format(IP, PORT))

    if service=="HTTP":
        service=1
    elif service=="SSH":
        service=5
    run_js('''var service_type=getElementByXpath("/html/body/div[1]/div[1]/main/form/div/div[5]/div/div[4]/div[1]/div[1]/div/div[2]/div/button")
    service_type.click()

    var HTTP=getElementByXpath("/html/body/div[1]/div[1]/main/form/div/div[5]/div/div[4]/div[1]/div[1]/div/div[2]/div/ul/li[{}]")
    HTTP.click()

    var save_button=getElementByXpath("/html/body/div[1]/div[1]/main/form/div/div[5]/button")
    save_button.click()
    '''.format(service))
    time.sleep(bt)

def add_app(appname, subdomain, domain):
    run_js('''
    var add_app=getElementByXpath("/html/body/div[1]/div[1]/main/div/div[3]/div[2]/div/div/a")
    add_app.click()
    ''')
    run_js('''
    var self_hosted=getElementByXpath("/html/body/div[1]/div[1]/main/div/form/div/div[3]/div[3]/section/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[3]/button")
    self_hosted.click()
    ''')
    pyautogui.press("tab", presses=5)
    fill(appname)
    pyautogui.press("tab", presses=2)
    fill(subdomain)
    pyautogui.press("tab")
    fill(domain)
    pyautogui.press("tab")
    run_js('''
    var next_button=getElementByXpath("/html/body/div[1]/div[1]/main/div/form/div/div[3]/div[2]/div[2]/button[2]")
    next_button.click()
    ''')
    pyautogui.press("tab", presses=2)
    fill(appname)
    run_js('''
    var select_button=getElementByXpath("/html/body/div[1]/div[1]/main/div/form/div/div[3]/div[3]/section/div/div/div/div[2]/div[3]/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div/button")
    select_button.click()
    var everyone_button=getElementByXpath("/html/body/div[1]/div[1]/main/div/form/div/div[3]/div[3]/section/div/div/div/div[2]/div[3]/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div/ul/li[6]")
    everyone_button.click()
    var next_button=getElementByXpath("/html/body/div[1]/div[1]/main/div/form/div/div[3]/div[2]/div[2]/button[2]")
    next_button.click()
    ''')
    run_js('''
    var ssh0_button=getElementByXpath("/html/body/div[1]/div[1]/main/div/form/div/div[3]/div[3]/section/div/div/div/div[2]/div[4]/div/div[3]/div[2]/div[2]/div/div[2]/div/div/div/button")
    ssh0_button.click()
    var ssh1_button=getElementByXpath("/html/body/div[1]/div[1]/main/div/form/div/div[3]/div[3]/section/div/div/div/div[2]/div[4]/div/div[3]/div[2]/div[2]/div/div[2]/div/div/div/ul/li[2]")
    ssh1_button.click()
    var add_button=getElementByXpath("/html/body/div[1]/div[1]/main/div/form/div/div[3]/div[2]/div[2]/button[2]")
    add_button.click()''')
    time.sleep(mt)
def delete_app(appname):
    pyautogui.press("tab", presses=2)
    fill(appname)
    time.sleep(mt)
    run_js('''
    var delete_button=getElementByXpath("/html/body/div[1]/div[1]/main/div/div[5]/div[1]/div/div/div/table/tbody/tr[2]/td[6]/div/div/button")
    delete_button.click()
    ''')
    run_js('''
    var delete1_button=getElementByXpath("/html/body/div[5]/div/div/div/div/div[2]/div/div/button[2]")
    delete1_button.click()
    ''')
    time.sleep(mt)
    pyautogui.press("backspace", presses=len(appname))
def change_tab():
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(mt)
first_js()
#add_app("botname", "bot", "stcloud.site")
#delete_app("botname")

print(create_domain("enes", "stcloud.site", "HTTP", "192.168.1.144", 1010))
#print(create_domain("sshenes", "stcloud.site", "SSH", "192.168.1.144", 1011))
#delete_domain(3)

