# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from selenium.webdriver import ActionChains
import pytesseract
import os


# 打开浏览器
def openbrowser():
    global browser

    # https://passport.baidu.com/v2/?login
    url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"
    # 打开谷歌浏览器
    # Firefox()
    # Chrome()
    browser = webdriver.Chrome()
    # 输入网址
    browser.get(url)
    # 打开浏览器时间
    # print("等待10秒打开浏览器...")
    # time.sleep(10)

    # 找到id="TANGRAM__PSP_3__userName"的对话框
    # 清空输入框
    browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
    browser.find_element_by_id("TANGRAM__PSP_3__password").clear()
    
    # 读取账号密码并登入
    account = []
    try:
        fileaccount = open("../baidu/account.txt", encoding='UTF-8')
        accounts = fileaccount.readlines()
        for acc in accounts:
            account.append(acc.strip())
        fileaccount.close()
    except Exception as err:
        print(err)
        input("请正确在account.txt里面写入账号密码")
        exit()
    username = account[0]
    password = account[1]
    browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(username)
    time.sleep(1)
    browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(password)
    
    print("请手动输入验证码")
    select = input("是否已经输入正确的验证码(y/n)：")
    while 1:
        if select == "y" or select == "Y":
           print("即将登陆")
           break
    time.sleep(1)
    # 点击登陆登陆
    # id="TANGRAM__PSP_3__submit"
    browser.find_element_by_id("TANGRAM__PSP_3__submit").click()
    print("准备打开新的窗口...")


def getDemandMap(keyword):
    openbrowser()
    time.sleep(2)

    
    # 这里开始进入百度指数
    # 要不这里就不要关闭了，新打开一个窗口
    # http://blog.csdn.net/DongGeGe214/article/details/52169761
    # 新开一个窗口，通过执行js来新开一个窗口
    js = 'window.open("http://index.baidu.com");'
    browser.execute_script(js)
    # 新窗口句柄切换，进入百度指数
    # 获得当前打开所有窗口的句柄handles
    # handles为一个数组
    handles = browser.window_handles
    # print(handles)
    # 切换到当前最新打开的窗口
    browser.switch_to_window(handles[-1])
    # 在新窗口里面输入网址百度指数
    # 清空输入框
    time.sleep(3)
    browser.find_element_by_id("schword").clear()
    # 写入需要搜索的百度指数
    browser.find_element_by_id("schword").send_keys(keyword)
    # 点击搜索
    # <input type="submit" value="" id="searchWords" onclick="searchDemoWords()">
    browser.find_element_by_id("searchWords").click()
    time.sleep(3)
    # 最大化窗口
    browser.maximize_window()
    time.sleep(2)

    #browser.find_element_by_id("compOtharea").click()
    #time.sleep(1)
    # //*[@id="auto_gsid_16"]/div/dl[2]/dd/a[1]
    #print(browser.find_element_by_xpath("//span[@class='selectA provA slided']//div//a[@href='#" + "928" + "']").text)
    #time.sleep(1)
    #browser.find_element_by_xpath("//span[@class='selectA provA slided']//div//a[@href='#" + "928" + "']").click()

    # 切换到需求图谱
    browser.find_element_by_class_name("demandIcon").click()
    time.sleep(2)

    file = open("../baidu/demandMap.txt", "w", encoding='UTF-8')
    file.write(keyword)
    file.write("：\n")

    # 切换时间 
    # 注意这里css使用svg写的，需要特殊的xpath写法和点击方式！
    
    # //*[@id="demand"]/svg/rect[1] -> //*[@id="demand"]/*[name()="svg"]/*[name()="rect"][1]
    # //*[@id="demand"]/svg/rect[4]
    # //*[@id="demand"]/svg/rect[7]
    # //*[@id="demand"]/svg/rect[10]
    # //*[@id="demand"]/svg/rect[13]
    # //*[@id="demand"]/svg/rect[16]
    # //*[@id="demand"]/svg/rect[154]
    #print(browser.find_element_by_xpath('//*[@id="auto_gsid_1"]/span[2]').text)
    #timeElement = browser.find_element_by_xpath('//*[@id="demand"]/*[name()="svg"]/*[name()="rect"][1]')
    #action = ActionChains(browser)
    #action.click(timeElement).perform()
    
    count = 1
    while count <= 154:
        timePath = '//*[@id="demand"]/*[name()="svg"]/*[name()="rect"][' + str(count) + ']'
        timeElement = browser.find_element_by_xpath(timePath)
        action = ActionChains(browser)
        action.click(timeElement).perform()
        time.sleep(2.5)
        timeText = browser.find_element_by_xpath('//*[@id="auto_gsid_1"]/span[2]').text
        print(timeText)
        file.write(timeText + "\n")

        # 模拟下拉操作
        target = browser.find_element_by_id("tablelist")
        browser.execute_script("arguments[0].scrollIntoView();", target)
        time.sleep(1)

        # 来源相关词和相关度
        # //*[@id="tablelist"]/div[1]/div/div[1]/table/tbody/tr[2]/td[2]/div/a
        # //*[@id="tablelist"]/div[1]/div/div[1]/table/tbody/tr[2]/td[3]/div/div
        # //*[@id="tablelist"]/div[1]/div/div[1]/table/tbody/tr[3]/td[2]/div/a
        # //*[@id="tablelist"]/div[1]/div/div[1]/table/tbody/tr[3]/td[3]/div/div
        print("来源相关词-相关度：")
        file.write("来源相关词-相关度："  + "\n")
        result = []
        for i in range(2,17):
            # 相关词
            textPath = "//*[@id='tablelist']/div[1]/div/div[1]/table/tbody/tr[" + str(i) + "]/td[2]"
            word = browser.find_element_by_xpath(textPath).text

            # 相关度
            percentPath = "//*[@id='tablelist']/div[1]/div/div[1]/table/tbody/tr[" + str(i) + "]/td[3]/div/div"
            percentLocation = browser.find_element_by_xpath(percentPath)
            browser.execute_script("alert(window.getComputedStyle(arguments[0],false).width);", percentLocation)
            alert = browser.switch_to_alert()
            time.sleep(0.8)
            test = alert.text
            alert.accept()
            temp = float(test.replace("px" , '')) / 162 * 100
            percent = str(float('%.2f' % temp))

            result.append(word + "-" + percent + "%")

        for i in result:
            print(i)
            file.write(i)
            file.write("\n")
        

        # 去向相关词和相关度
        # //*[@id="tablelist"]/div[1]/ul/li[2]
        # //*[@id="tablelist"]/div[1]/div/div[2]/table/tbody/tr[2]/td[2]/div/a
        # //*[@id="tablelist"]/div[1]/div/div[2]/table/tbody/tr[2]/td[3]/div/div
        # //*[@id="tablelist"]/div[1]/div/div[2]/table/tbody/tr[16]/td[2]/div/a
        # //*[@id="tablelist"]/div[1]/div/div[2]/table/tbody/tr[16]/td[3]/div/div
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="tablelist"]/div[1]/ul/li[2]').click()
        time.sleep(1)
        file.write("\n")
        print("去向相关词-相关度：")
        file.write("去向相关词-相关度：")
        file.write("\n")
        result = []
        for i in range(2,17):
            # 相关词
            textPath = "//*[@id='tablelist']/div[1]/div/div[2]/table/tbody/tr[" + str(i) + "]/td[2]"
            word = browser.find_element_by_xpath(textPath).text

            # 相关度
            percentPath = "//*[@id='tablelist']/div[1]/div/div[2]/table/tbody/tr[" + str(i) + "]/td[3]/div/div"
            percentLocation = browser.find_element_by_xpath(percentPath)
            browser.execute_script("alert(window.getComputedStyle(arguments[0],false).width);", percentLocation)
            alert = browser.switch_to_alert()
            time.sleep(0.8)
            test = alert.text
            alert.accept()
            temp = float(test.replace("px" , '')) / 162 * 100
            percent = str(float('%.2f' % temp))

            result.append(word + "-" + percent + "%")

        for i in result:
            print(i)
            file.write(i)
            file.write("\n")
        
        # 搜索指数
        # //*[@id="tablelist"]/div[2]/div/div[1]/table/tbody/tr[2]/td[2]/div/a
        # //*[@id="tablelist"]/div[2]/div/div[1]/table/tbody/tr[2]/td[3]
        # //*[@id="tablelist"]/div[2]/div/div[1]/table/tbody/tr[16]/td[2]/div/a
        # //*[@id="tablelist"]/div[2]/div/div[1]/table/tbody/tr[16]/td[3]
        time.sleep(2)
        print("查询词-搜索指数：")
        file.write("\n")
        file.write("查询词-搜索指数：")
        file.write("\n")
        result = []
        for i in range(2,17):
            # 查询词
            textPath = "//*[@id='tablelist']/div[2]/div/div[1]/table/tbody/tr[" + str(i) + "]/td[2]"
            word = browser.find_element_by_xpath(textPath).text

            # 搜索指数
            indexPath = "//*[@id='tablelist']/div[2]/div/div[1]/table/tbody/tr[" + str(i) + "]/td[3]"
            index = browser.find_element_by_xpath(indexPath).text
            result.append(word + "-" + index)

        for i in result:
            print(i)
            file.write(i)
            file.write("\n")


        # 上升最快
        # //*[@id="tablelist"]/div[2]/ul/li[2]
        # //*[@id="tablelist"]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/a
        # //*[@id="tablelist"]/div[2]/div/div[2]/table/tbody/tr[2]/td[3]
        # //*[@id="tablelist"]/div[2]/div/div[2]/table/tbody/tr[16]/td[2]/div/a
        # //*[@id="tablelist"]/div[2]/div/div[1]/table/tbody/tr[16]/td[3]
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="tablelist"]/div[2]/ul/li[2]').click()
        print("查询词-变化率：")
        file.write("\n")
        file.write("查询词-变化率：")
        file.write("\n")
        result = []
        for i in range(2,17):
            # 查询词
            textPath = "//*[@id='tablelist']/div[2]/div/div[2]/table/tbody/tr[" + str(i) + "]/td[2]"
            word = browser.find_element_by_xpath(textPath).text

            # 变化率
            indexPath = "//*[@id='tablelist']/div[2]/div/div[2]/table/tbody/tr[" + str(i) + "]/td[3]"
            index = browser.find_element_by_xpath(indexPath).text
            result.append(word + "-" + index)

        for i in result:
            print(i)
            file.write(i)
            file.write("\n")

        file.write("--------------------------------------------------\n")
        time.sleep(1)
        count += 3

    file.close()



    # 来源相关词和相关度
    # //*[@id="tablelist"]/div[1]/div/div[1]/table/tbody/tr[2]/td[2]/div/a
    # //*[@id="tablelist"]/div[1]/div/div[1]/table/tbody/tr[2]/td[3]/div/div
    # //*[@id="tablelist"]/div[1]/div/div[1]/table/tbody/tr[3]/td[2]/div/a
    # //*[@id="tablelist"]/div[1]/div/div[1]/table/tbody/tr[3]/td[3]/div/div
    '''
    print("来源相关词-相关度：")
    result = []
    for i in range(2,17):
        # 相关词
        textPath = "//*[@id='tablelist']/div[1]/div/div[1]/table/tbody/tr[" + str(i) + "]/td[2]"
        word = browser.find_element_by_xpath(textPath).text

        # 相关度
        percentPath = "//*[@id='tablelist']/div[1]/div/div[1]/table/tbody/tr[" + str(i) + "]/td[3]/div/div"
        percentLocation = browser.find_element_by_xpath(percentPath)
        browser.execute_script("alert(window.getComputedStyle(arguments[0],false).width);", percentLocation)
        alert = browser.switch_to_alert()
        time.sleep(0.8)
        test = alert.text
        alert.accept()
        temp = float(test.replace("px" , '')) / 162 * 100
        percent = str(float('%.2f' % temp))

        result.append(word + "-" + percent + "%")

    for i in result:
        print(i)
    '''

    
    # 去向相关词和相关度
    # //*[@id="tablelist"]/div[1]/ul/li[2]
    # //*[@id="tablelist"]/div[1]/div/div[2]/table/tbody/tr[2]/td[2]/div/a
    # //*[@id="tablelist"]/div[1]/div/div[2]/table/tbody/tr[2]/td[3]/div/div
    # //*[@id="tablelist"]/div[1]/div/div[2]/table/tbody/tr[16]/td[2]/div/a
    # //*[@id="tablelist"]/div[1]/div/div[2]/table/tbody/tr[16]/td[3]/div/div
    '''
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="tablelist"]/div[1]/ul/li[2]').click()
    time.sleep(1)
    print("去向相关词-相关度：")
    result = []
    for i in range(2,17):
        # 相关词
        textPath = "//*[@id='tablelist']/div[1]/div/div[2]/table/tbody/tr[" + str(i) + "]/td[2]"
        word = browser.find_element_by_xpath(textPath).text

        # 相关度
        percentPath = "//*[@id='tablelist']/div[1]/div/div[2]/table/tbody/tr[" + str(i) + "]/td[3]/div/div"
        percentLocation = browser.find_element_by_xpath(percentPath)
        browser.execute_script("alert(window.getComputedStyle(arguments[0],false).width);", percentLocation)
        alert = browser.switch_to_alert()
        time.sleep(0.8)
        test = alert.text
        alert.accept()
        temp = float(test.replace("px" , '')) / 162 * 100
        percent = str(float('%.2f' % temp))

        result.append(word + "-" + percent + "%")

    for i in result:
        print(i)
    '''

    # 搜索指数
    # //*[@id="tablelist"]/div[2]/div/div[1]/table/tbody/tr[2]/td[2]/div/a
    # //*[@id="tablelist"]/div[2]/div/div[1]/table/tbody/tr[2]/td[3]
    # //*[@id="tablelist"]/div[2]/div/div[1]/table/tbody/tr[16]/td[2]/div/a
    # //*[@id="tablelist"]/div[2]/div/div[1]/table/tbody/tr[16]/td[3]
    '''
    time.sleep(1)
    print("查询词-搜索指数：")
    result = []
    for i in range(2,17):
        # 查询词
        textPath = "//*[@id='tablelist']/div[2]/div/div[1]/table/tbody/tr[" + str(i) + "]/td[2]"
        word = browser.find_element_by_xpath(textPath).text

        # 搜索指数
        indexPath = "//*[@id='tablelist']/div[2]/div/div[1]/table/tbody/tr[" + str(i) + "]/td[3]"
        index = browser.find_element_by_xpath(indexPath).text
        result.append(word + "-" + index)

    for i in result:
        print(i)
    '''

    # 上升最快
    # //*[@id="tablelist"]/div[2]/ul/li[2]
    # //*[@id="tablelist"]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/a
    # //*[@id="tablelist"]/div[2]/div/div[2]/table/tbody/tr[2]/td[3]
    # //*[@id="tablelist"]/div[2]/div/div[2]/table/tbody/tr[16]/td[2]/div/a
    # //*[@id="tablelist"]/div[2]/div/div[1]/table/tbody/tr[16]/td[3]
    '''
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="tablelist"]/div[2]/ul/li[2]').click()
    print("查询词-变化率：")
    result = []
    for i in range(2,17):
        # 查询词
        textPath = "//*[@id='tablelist']/div[2]/div/div[2]/table/tbody/tr[" + str(i) + "]/td[2]"
        word = browser.find_element_by_xpath(textPath).text

        # 变化率
        indexPath = "//*[@id='tablelist']/div[2]/div/div[2]/table/tbody/tr[" + str(i) + "]/td[3]"
        index = browser.find_element_by_xpath(indexPath).text
        result.append(word + "-" + index)

    for i in result:
        print(i)
    '''

    #file = open("../baidu/index.txt", "w", encoding='UTF-8')
    #for item in index:
    #    file.write(str(item) + "\n")
    #file.close()
    



if __name__ == "__main__":
    keyword = input("请输入查询关键字：")
    getDemandMap(keyword)
