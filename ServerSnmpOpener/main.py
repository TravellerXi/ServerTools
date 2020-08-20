#/usr/bin/env python3
#coding:utf-8
#Template used for IBM IMM, lenovol IMM, HP and DELL
# It can open snmp port automatically. It would be useful if you are using zabbix.
#Selenium EVN is required.

# Here we define snmp information. I have given 4 snmp-bindin IPs: ServerA/B/C/D.
# The default password has been used in this sample. Please replace it if you are not using the default password.
# Mutiple process.

ServerA=''
ServerB=''
ServerC=''
ServerD=''
Community='public'
IBMUsername='USERDID'
IBMPassword='PASSW0RD'
HPUsername='USERID'
HPPassword='PASSW0RD'
ContactPerson='System Admin'
ContactLocation='Shanghai'



from selenium import webdriver
import time
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def startProcess(ip):
    browser = webdriver.Chrome()
    browser.get('http://'+ip)
    sourceCode = browser.page_source
    if sourceCode.find('Hewlett') > -1:
        try:
            while 1:
                try:
                    browser.switch_to.frame('appFrame')
                    WebDriverWait(browser, 1200).until(
                        (EC.element_to_be_clickable((By.ID, 'login-form__submit')))
                    )
                    break
                except:
                    try:
                        WebDriverWait(browser, 1200).until(
                            (EC.element_to_be_clickable((By.ID, 'login-form__submit')))
                        )
                        break
                    except:
                        time.sleep(1)

            browser.find_element_by_xpath("//input[@id='username']").send_keys(HPUsername)
            browser.find_element_by_xpath("//input[@id='password']").send_keys(HPPassword)
            browser.find_element_by_id('login-form__submit').click()
            WebDriverWait(browser, 1200).until(
                (EC.visibility_of_element_located((By.ID, 'tabset_manage')))
            )
            browser.maximize_window()
            # waitByID('tabset_manage')
            browser.find_element_by_id('tabset_manage').click()

            browser.switch_to.frame('iframeContent')
            browser.find_element_by_id('sysloc').clear()
            browser.find_element_by_id('sysloc').send_keys(ContactLocation)
            browser.find_element_by_id('syscon').clear()
            browser.find_element_by_id('syscon').send_keys(ContactPerson)
            browser.find_element_by_id('readcom0').send_keys(Community)
            browser.find_element_by_id('settingsButton').click()
            WebDriverWait(browser, 1200).until(
                (EC.visibility_of_element_located((By.XPATH,
                                                   '/html/body/div[3]/div[1]/div[1]/form/section[1]/div[1]/div/div/div/div[2]/div[1]/div/span')))
            )

            successIps.append(ip)
            successType.append('HP')
            print('HP' + ip + '执行成功')
            browser.quit()
        except:
            failedIps.append(ip)
            print('HP' + ip + '需要手动执行')


    elif sourceCode.find('ibm') > -1:
        try:
            browser.get('https://' + ip + '/designs/imm/index.php')
            try:

                WebDriverWait(browser, 1200).until_not(
                    (EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[1]/span[1]")))
                )

                browser.maximize_window()

                # element.click()
            except:
                print('error')
            # waitUtil('https://' + ip + '/designs/imm/index.php', "/html/body/div[4]/div[1]/span[1]")
            browser.find_element_by_xpath("//input[@id='user']").send_keys(IBMUsername)
            browser.find_element_by_xpath("//input[@id='password']").send_keys(IBMPassword)
            browser.find_element_by_xpath(
                "/html/body/div[2]/table/tbody/tr[3]/td/table/tbody/tr[3]/td/div[1]/span/span/span/span[3]").click()

            WebDriverWait(browser, 1200).until(
                (EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/table[1]/tbody/tr/td/div[2]/div/div/div/table/tbody/tr[1]/td/h1")))
            )
            browser.maximize_window()

            # waitutilJumpTO("/html/body/table[1]/tbody/tr/td/div[2]/div/div/div/table/tbody/tr[1]/td/h1")
            # browser.get('https://10.187.11.202/designs/imm/index-console.php#21')
            browser.find_element_by_xpath('/html/body/table[1]/tbody/tr/td/div[1]/div/div[2]/div[6]').click()
            browser.find_element_by_id('dijit_MenuItem_21').click()

            WebDriverWait(browser, 1200).until(
                (EC.visibility_of_element_located((By.ID, 'networkPropertyNotebook_tablist_page36')))
            )
            browser.maximize_window()
            # waitByID('networkPropertyNotebook_tablist_page36')

            browser.find_element_by_id('networkPropertyNotebook_tablist_page36').click()

            WebDriverWait(browser, 1200).until(
                (EC.visibility_of_element_located((By.ID, 'contactlbl')))
            )
            browser.maximize_window()
            # waitByID('contactlbl')

            if not (browser.find_element_by_id('chkEnableSnmpv1').is_selected()):
                browser.find_element_by_id('chkEnableSnmpv1').click()
            # checkBoxBeforeDo('chkEnableSnmpv1')

            browser.find_element_by_xpath("//input[@id='contactPerson']").clear()
            browser.find_element_by_xpath("//input[@id='contactPerson']").send_keys(ContactPerson)
            browser.find_element_by_xpath("//input[@id='locationId']").clear()
            browser.find_element_by_xpath("//input[@id='locationId']").send_keys(ContactLocation)
            browser.find_element_by_id('CTRLButton2').click()

            if not (browser.find_element_by_id('communityenableComm1').is_selected()):
                browser.find_element_by_id('communityenableComm1').click()
            # checkBoxBeforeDo('communityenableComm1')
            # browser.find_element_by_id('communityenableComm1').click()
            browser.find_element_by_id('communityName1').clear()
            browser.find_element_by_id('communityName1').send_keys('public')

            browser.find_element_by_xpath("//input[@id='communty1Host1']").clear()
            browser.find_element_by_xpath("//input[@id='communty1Host1']").send_keys(ServerA)
            browser.find_element_by_xpath("//input[@id='communty2Host1']").clear()
            browser.find_element_by_xpath("//input[@id='communty2Host1']").send_keys(ServerB)
            browser.find_element_by_xpath("//input[@id='communty3Host1']").clear()
            browser.find_element_by_xpath("//input[@id='communty3Host1']").send_keys(ServerC)

            if not (browser.find_element_by_id('communityenableComm2').is_selected()):
                browser.find_element_by_id('communityenableComm2').click()

            browser.find_element_by_id('communityName2').clear()
            browser.find_element_by_id('communityName2').send_keys(Community)

            browser.find_element_by_xpath("//input[@id='communty1Host2']").clear()
            browser.find_element_by_xpath("//input[@id='communty1Host2']").send_keys(ServerD)
            time.sleep(1)
            browser.find_element_by_id('networkPropertiesInit_apply_label').click()
            WebDriverWait(browser, 1200).until_not(
                (EC.visibility_of_element_located((By.ID, 'consoleProgressText')))
            )
            successIps.append(ip)
            print('IBM' + ip + '执行成功')
            successType.append('IBM')
            browser.quit()
        except:
            failedIps.append(ip)
            print('IBM' + ip + '需要手动执行\n')

    elif sourceCode.find('idrac') > -1:
        print('DELL'+ip+'不需要执行')
        successIps.append(ip)
        successType.append('DELL')
        browser.quit()
    else:
        print(ip+'需要手动执行')
        failedIps.append(ip)
if __name__=='__main__':
    print('请输入管理口IP，以英文逗号分隔，输入完毕按回车\n')
    ips=input()
    arrIps=ips.split(',')
    successIps=[],successType=[],failedIps=[],threads = []
    for i in arrIps:
        t=threading.Thread(target=startProcess,args=(i,))
        threads.append(t)
    for i in threads:
        i.start()
    for i in threads:
        i.join()

    print('\n成功完成的IP列表：>>>')
    for i in successIps:
        a = 0
        print(i,successType[a])
        a=a+1
    print('\n')
    print('\n需要手动执行的IP列表:>>>>')
    for i in failedIps:
        print(i)
    print('\n\n任务完毕')
