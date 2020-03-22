# coding = utf-8

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

#driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

class unblocker_class():
    def __init__(self,url,password):
        self.url = url
        self.password = password
    def unblocker(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('window-size=1200x600')
        user_ag="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        chrome_options.add_argument('user-agent=%s'%user_ag)
        driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",options=chrome_options)
        driver.get(self.url)
        #print(driver.page_source)

        try:
            driver.find_element_by_css_selector("#content>iforgot>div>iforgot-body>sa>idms-flow>div>section>div>web-reset-options>div.content-body>div:nth-child(2)>div>button").click()
        except Exception as e:
            res = {}
            res['err_no'] = '1'
            res['err_msg'] = '{0}'.format(e) #url invalid
            #print(type(res['err_msg']))
            return res
        else:
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "idms-error-wrapper")))
            except Exception as e:
                res = {}
                res['err_no'] = '2'
                res['err_msg'] = '{0}'.format(e) #clear ip is needed
                return res
            else:
                area=driver.find_elements_by_tag_name("idms-error-wrapper")[0].get_attribute('error-input-id').split('-')
                #area=element[0].get_attribute('error-input-id').split('-')
                #print(area)
                id=str('input-'+area[-2]+'-'+area[-1])
                #print(id)
                area2=driver.find_element_by_id(id)
                ActionChains(driver).move_to_element(area2).click(area2).perform()
                driver.find_element_by_id(id).send_keys(self.password)
                driver.find_element_by_css_selector("#action").click()
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "unlock-success")))
                except Exception as e :
                    #print(repr(e))
                    res = {}
                    res['err_no'] = '3'
                    res['err_msg'] = '{0}'.format(e) #wrong pasword
                    return res
                else:
                    #print('Apple ID unblocked!')
                    return True
        finally:
            driver.quit()


#unblocker_class("https://iforgot.apple.com/verify/email?key=001264-00-a9b4db47953323b6cfa0fb743cfed070cdd61aa7fd6953d46336c9329f0b1c53LTOW&language=CN-ZH","Shadowsocket9").unblocker()