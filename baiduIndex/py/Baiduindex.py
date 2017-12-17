# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

# 参考 https://github.com/TTyb/Baiduindex

# 百度指数的抓取
# 截图教程：http://www.myexception.cn/web/2040513.html
#
# 登陆百度地址：https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F
# 百度指数地址：http://index.baidu.com

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
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

    '''
    select = input("请观察浏览器网站是否已经登陆(y/n)：")
    
    while 1:
        if select == "y" or select == "Y":
            print("登陆成功！")
            print("准备打开新的窗口...")
            # time.sleep(1)
            # browser.quit()
            break

        elif select == "n" or select == "N":
            selectno = input("账号密码错误请按0，验证码出现请按1...")
            # 账号密码错误则重新输入
            if selectno == "0":

                # 找到id="TANGRAM__PSP_3__userName"的对话框
                # 清空输入框
                browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
                browser.find_element_by_id("TANGRAM__PSP_3__password").clear()

                # 输入账号密码
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

                browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
                browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])
                # 点击登陆sign in
                # id="TANGRAM__PSP_3__submit"
                browser.find_element_by_id("TANGRAM__PSP_3__submit").click()

            elif selectno == "1":
                # 验证码的id为id="ap_captcha_guess"的对话框
                input("请在浏览器中输入验证码并登陆...")
                select = input("请观察浏览器网站是否已经登陆(y/n)：")

        else:
            print("请输入“y”或者“n”！")
            select = input("请观察浏览器网站是否已经登陆(y/n)：")
    '''

def getindex(keyword, province, city, length):
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
    time.sleep(5)
    browser.find_element_by_id("schword").clear()
    # 写入需要搜索的百度指数
    browser.find_element_by_id("schword").send_keys(keyword)
    # 点击搜索
    # <input type="submit" value="" id="searchWords" onclick="searchDemoWords()">
    browser.find_element_by_id("searchWords").click()
    time.sleep(5)
    # 最大化窗口
    browser.maximize_window()
    time.sleep(2)

    # 选择城市
    # 要根据网站上的省份-编号和城市-编号构造map读取
    provinceDict = {'安徽':'928', '澳门':'934', '北京':'911', '重庆':'904', '福建':'909', '广东':'913', '甘肃':'925', '广西':'912', '贵州':'902', 
    '河北':'920', '黑龙江':'921', '河南':'927', '湖南':'908', '湖北':'906', '海南':'930', '吉林':'922', '江苏':'916', '江西':'903', '辽宁':'907', 
    '内蒙古':'905', '宁夏':'919', '青海':'918', '上海':'910', '四川':'914', '山东':'901', '山西':'929', '陕西':'924', '天津':'923', '台湾':'931', 
    '西藏':'932', '香港':'933', '新疆':'926', '云南':'915', '浙江':'917'}
    
    cityDict = {'合肥':'189','滁州':'182','宿州':'179','安庆':'186','六安':'181','蚌埠':'187','亳州':'391','阜阳':'184','芜湖':'188','宣城':'176', 
    '巢湖':'177','铜陵':'173','淮南':'178','马鞍山':'185', '淮北':'183','黄山':'174','池州':'175','澳门':'664','北京':'514','上海':'57','天津':'164',
    '台湾':'0','重庆':'11','香港':'663','福州':'50','泉州':'55','厦门':'54','漳州':'56','宁德':'87','三明':'52','莆田':'51','南平':'253','龙岩':'53',
    '广州':'95','深圳':'94','佛山':'196','惠州':'199','汕头':'212','东莞':'133','茂名':'203','江门':'198','珠海':'200','湛江':'197','肇庆':'209',
    '揭阳':'205','中山':'207','韶关':'201','阳江':'202','云浮':'195','梅州':'211','清远':'208','潮州':'204','汕尾':'213','河源':'210','兰州':'166',
    '武威':'283','张掖':'285','嘉峪关':'286','天水':'308','平凉':'307','陇南':'344','庆阳':'281','定西':'282','酒泉':'284','白银':'309','金昌':'343'
    ,'临夏':'346','南宁':'90','柳州':'89','桂林':'91','百色':'131','河池':'119','梧州':'132','贵港':'93','玉林':'118','北海':'128','钦州':'129',
    '来宾':'506','贺州':'92','防城港':'130','贵阳':'2','遵义':'59','六盘水':'4','黔南':'3','毕节':'426','安顺':'424','铜仁':'422','黔东南':'61',
    '黔西南':'588','石家庄':'141','唐山':'261','保定':'259','沧州':'148','邯郸':'292','衡水':'143','秦皇岛':'146','廊坊':'147','邢台':'293','承德':'145',
    '张家口':'144','哈尔滨':'152','大庆':'153','绥化':'324','齐齐哈尔':'319','佳木斯':'320','牡丹江':'322','黑河':'300','鸡西':'323','伊春':'295',
    '鹤岗':'301','双鸭山':'359','七台河':'302','大兴安岭':'297','郑州':'168','洛阳':'378','南阳':'262','新乡':'263','信阳':'373','安阳':'370','平顶山':'266',
    '驻马店':'371','焦作':'265','三门峡':'381','周口':'375','许昌':'268','开封':'264','商丘':'376','濮阳':'380','漯河':'379','鹤壁':'374','长沙':'43',
    '株洲':'46','衡阳':'45','郴州':'49','常德':'68','岳阳':'44','永州':'269','邵阳':'405','怀化':'67','益阳':'48','湘潭':'47','娄底':'66','张家界':'226',
    '湘西':'65','武汉':'28','宜昌':'35','荆州':'31','襄樊':'32','十堰':'36','荆门':'34','黄冈':'33','孝感':'41','黄石':'30','咸宁':'40','恩施':'38','随州':'37',
    '鄂州':'39','仙桃':'42','潜江':'74','天门':'73','海口':'239','三亚':'243','儋州':'244','万宁':'241','五指山':'582','琼海':'242','东方':'456','长春':'154',
    '吉林':'270','延边':'525','四平':'155','白城':'410','通化':'407','松原':'194','白山':'408','辽源':'191','苏州':'126','南京':'125','无锡':'127','徐州':'161',
    '镇江':'169','盐城':'160','南通':'163','常州':'162','扬州':'158','泰州':'159','连云港':'156','宿迁':'172','淮安':'157','南昌':'5','赣州':'10','九江':'6',
    '上饶':'9','景德镇':'137','吉安':'115','鹰潭':'7','宜春':'256','抚州':'8','萍乡':'136','新余':'246','沈阳':'150','大连':'29','锦州':'217','鞍山':'215',
    '辽阳':'224','丹东':'219','营口':'221','本溪':'220','铁岭':'218','抚顺':'222','朝阳':'216','阜新':'223','葫芦岛':'225','盘锦':'151','呼和浩特':'20',
    '呼伦贝尔':'25','赤峰':'21','包头':'13','巴彦淖尔':'15','通辽':'22','鄂尔多斯':'14','乌海':'16','乌兰察布':'331','兴安盟':'333','锡林郭勒盟':'19',
    '阿拉善盟':'17','银川':'140','吴忠':'395','石嘴山':'472','固原':'396','中卫':'480','西宁':'139','海西':'608','玉树':'659','海东':'652','成都':'97',
    '绵阳':'98','乐山':'107','德阳':'106','泸州':'103','达州':'113','眉山':'291','自贡':'111','南充':'104','内江':'102','宜宾':'96','广安':'108','雅安':'114',
    '资阳':'109','广元':'99','遂宁':'100','攀枝花':'112','巴中':'101','甘孜':'417','凉山':'479','阿坝':'457','济南':'1','青岛':'77','潍坊':'80','烟台':'78',
    '临沂':'79','淄博':'81','泰安':'353','济宁':'352','聊城':'83','东营':'82','威海':'88','德州':'86','滨州':'76','莱芜':'356','枣庄':'85','菏泽':'84',
    '日照':'366','太原':'231','运城':'233','吕梁':'237','晋中':'230','临汾':'232','大同':'227','晋城':'234','长治':'228','忻州':'229','阳泉':'236','朔州':'235',
    '西安':'165','渭南':'275','咸阳':'277','宝鸡':'273','汉中':'276','榆林':'278','安康':'272','延安':'401','商洛':'274','铜川':'271','拉萨':'466','那曲':'655',
    '林芝':'656','日喀则':'516','乌鲁木齐':'467','石河子':'280','塔城':'563','克拉玛依':'317','阿克苏':'315','哈密':'312','巴音郭楞':'499','阿勒泰':'383',
    '昌吉':'311','伊犁哈萨克':'660','吐鲁番':'310','喀什':'384','博尔塔拉':'318','克孜勒苏柯尔克孜':'653','和田':'386','五家渠':'661','昆明':'117','红河':'337',
    '玉溪':'123','曲靖':'339','大理':'334','文山':'437','保山':'438','丽江':'342','昭通':'335','思茅':'662','临沧':'350','楚雄':'124','杭州':'138','温州':'149',
    '宁波':'289','金华':'135','台州':'287','嘉兴':'304','绍兴':'303','湖州':'305','丽水':'134','衢州':'288','舟山':'306'}


    browser.find_element_by_id("compOtharea").click()
    time.sleep(1)
    browser.find_element_by_xpath("//span[@class='selectA provA slided']//div//a[@href='#" + provinceDict[province] + "']").click()
    time.sleep(1)
    browser.find_element_by_xpath("//span[@class='selectA cityA slided']//div//a[@href='#" + cityDict[city] + "']").click()
    time.sleep(2)

    file = open("../baidu/index.txt", "w", encoding='UTF-8')

    
    # 记录开始时间
    print("开始时间：" + str(time.strftime("%H:%M:%S")))
    file.write("开始时间：" + str(time.strftime("%H:%M:%S")) + "\n")

    # 找到图表框
    xoyelement = browser.find_elements_by_css_selector("#trend rect")[2]
    num = 0


    

    # 储存数字的数组
    index = []
    try:
        y_0 = 25
        monthDict = {'1':'31', '2':'28', '3':'31', '4':'30', '5':'31', '6':'30', '7':'31', '8':'31', '9':'30','10':'31','11':'30','12':'31'}
        year = 2017
        day = 1
        month = 1
        startMonth = "0" + str(month)
        endMonth = "0" + str(month + 5)
        
        # 第一次选择搜索时间  2011.1-2011.6
        browser.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
        time.sleep(1)
        browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
        time.sleep(1)
        browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
        time.sleep(1)
        browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
        time.sleep(1)
        browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "01" + "']").click()
        time.sleep(1)

        browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
        time.sleep(1)
        browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
        time.sleep(1)
        browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
        time.sleep(1)
        browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "06" + "']").click()
        time.sleep(1)
        browser.find_element_by_xpath("//input[@value='确定']").click()
        time.sleep(5)

        # 整体趋势
        count = 0
        # 每次修改完区间，稍微一动一下鼠标，不然修改完的第一次可能没法查出来
        isMove = 0 
        for i in range(length):
            
            # 不同时间，不同间隔
            if month <= 6: # 前半年
                if year % 4 == 0:
                    size = 6.70718232
                else:
                    size = 6.744444444
            else:
                if year != 2017:
                    size = 6.633879781
                else:
                    size = 1214 / (153 + int(time.strftime("%d")) - 2 - 1) # 这里如果到2018年了还需要修改的

            # 坐标偏移量
            if count == 0:
                x_0 = 2
            else:
                x_0 = (count - 0.13) * size

            if count <= 8:
                y_0 = 30
            else:
                y_0 = 5

            if isMove == 0:
                ActionChains(browser).move_to_element_with_offset(xoyelement, 0.9*size, y_0).perform()
                time.sleep(1)
                isMove = 1
            ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
            time.sleep(1)
            # <div class="imgtxt" style="margin-left:-117px;"></div> 
            imgelement = browser.find_element_by_xpath('//div[@id="viewbox"]')
            time.sleep(1)
            # 找到图片坐标
            locations = imgelement.location
            #print(locations)
            # 找到图片大小
            #sizes = imgelement.size
            #print(sizes)

            temp = len(keyword)
            l = 0
            for c in keyword:
                if ord(c) > 127:
                    l += 1
                else:
                    l += 0.43
            l += 1
            if l > 8:
                l = 8
            rangle = (int(int(locations['x'])) + l * 10 + 34, int(int(locations['y'])) + 28, int(int(locations['x'])) + l * 10 + 38 + 75, int(int(locations['y'])) + 56)
            

            if month < 10:
                monthName = '0' + str(month)
            else:
                monthName = str(month)
            if day < 10:
                dayName = '0' + str(day)
            else:
                dayName = str(day)
            name = str(year) + monthName + dayName

            print(name + ":" + str(locations))
            # 截取当前浏览器
            #path = "../baidu/" + str(num)
            path = "../baidu/" + str(province) + '/' + str(city) + '/' + name
            browser.save_screenshot(str(path) + ".png")
            # 打开截图切割
            img = Image.open(str(path) + ".png")
            jpg = img.crop(rangle)
            jpg.save(str(path) + ".jpg")

            # 将图片放大一倍，增加识图准确率
            jpgzoom = Image.open(str(path) + ".jpg")
            (x, y) = jpgzoom.size
            x_s = 60 * 10
            y_s = 20 * 10
            out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
            out.save(path + 'zoom.jpg', 'png', quality=95)

            # 图像识别
            try:
                image = Image.open(str(path) + "zoom.jpg")
                code = pytesseract.image_to_string(image)

                if code:
                    # 去除一些奇奇怪怪的干扰
                    # pytesseract识别图片数字的准确率其实不是说特别高
                    code = code.replace("S", '5').replace("?", '7').replace(" ", "").replace(",", "").replace("E", "8").replace(".", "").replace("'", "").replace(u"‘", "")\
                    .replace("B", "8").replace("\"", "").replace("I", "1").replace("i", "").replace("-", "").replace("$", "8").replace(u"’", "").strip()
                    
                    result = str(province) + str(city) + '-' + name + '-' + code
                    index.append(result)

                else:
                    index.append(str(province) + str(city) + '-' + name + '-' + '0')
            except:
                index.append("")
            num = num + 1

            # 下面是日期修改
            if str(day) == monthDict.get(str(month)):
                if month != 12:
                    day = 0
                    month += 1
                    # 修改查询区间了
                    if month == 7:
                        browser.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
                        time.sleep(1)
                        #browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
                        #time.sleep(1)
                        #browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
                        #time.sleep(1)
                        browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
                        time.sleep(1)
                        browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "07" + "']").click()
                        time.sleep(1)

                        #browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
                        #time.sleep(1)
                        #browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
                        #time.sleep(1)
                        browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
                        time.sleep(1)
                        browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "12" + "']").click()
                        time.sleep(1)
                        browser.find_element_by_xpath("//input[@value='确定']").click()

                        time.sleep(5)

                        count = -1
                        isMove = 0
                else:
                    day = 0
                    month = 1
                    year += 1
                    if year % 4 == 0:
                        monthDict['2'] = '29'
                    else:
                        monthDict['2'] = '28'

                    # 重新加载网站
                    js = 'window.open("http://index.baidu.com");'
                    browser.execute_script(js)
                    handles = browser.window_handles
                    browser.switch_to_window(handles[-1])
                    time.sleep(5)
                    browser.find_element_by_id("schword").clear()
                    browser.find_element_by_id("schword").send_keys(keyword)
                    time.sleep(1)
                    browser.find_element_by_id("searchWords").click()
                    time.sleep(5)
                    
                    #browser.find_element_by_id("schword").clear()
                    #time.sleep(1)
                    #browser.find_element_by_id("schword").send_keys(keyword)
                    #browser.find_element_by_id("schsubmit").click()
                    #time.sleep(3)
                    browser.find_element_by_id("compOtharea").click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA provA slided']//div//a[@href='#" + provinceDict[province] + "']").click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA cityA slided']//div//a[@href='#" + cityDict[city] + "']").click()
                    time.sleep(2)
                    xoyelement = browser.find_elements_by_css_selector("#trend rect")[2]
                    time.sleep(5)

                    # 更新日期
                    browser.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
                    time.sleep(1)
                    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
                    time.sleep(1)
                    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "01" + "']").click()
                    time.sleep(1)

                    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
                    time.sleep(1)
                    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "06" + "']").click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//input[@value='确定']").click()

                    time.sleep(5)

                    count = -1
                    isMove = 0

            if year == 2017 and month == 12 and day == int(time.strftime("%d")) - 2:
                break

            day += 1
            count += 1
            
            ActionChains(browser).move_to_element_with_offset(xoyelement, 0, 0).perform()
            time.sleep(1)



        #  移动趋势 这里需要重新切换年份
        print("mobile")
        time.sleep(2)
        y_0 = 25
        year = 2011
        day = 1
        month = 1
        count = 0
        # 每次修改完区间，稍微一动一下鼠标，不然修改完的第一次可能没法查出来
        isMove = 0 

        # 重新加载网站
        js = 'window.open("http://index.baidu.com");'
        browser.execute_script(js)
        handles = browser.window_handles
        browser.switch_to_window(handles[-1])
        time.sleep(5)
        browser.find_element_by_id("schword").clear()
        browser.find_element_by_id("schword").send_keys(keyword)
        time.sleep(1)
        browser.find_element_by_id("searchWords").click()
        time.sleep(5)

        #browser.find_element_by_id("schword").clear()
        #time.sleep(1)
        #browser.find_element_by_id("schword").send_keys(keyword)
        #browser.find_element_by_id("schsubmit").click()
        #time.sleep(3)
        browser.find_element_by_id("compOtharea").click()
        time.sleep(1)
        browser.find_element_by_xpath("//span[@class='selectA provA slided']//div//a[@href='#" + provinceDict[province] + "']").click()
        time.sleep(1)
        browser.find_element_by_xpath("//span[@class='selectA cityA slided']//div//a[@href='#" + cityDict[city] + "']").click()
        time.sleep(2)
        xoyelement = browser.find_elements_by_css_selector("#trend rect")[2]
        time.sleep(5)

        # 选择移动趋势
        browser.find_element_by_class_name("icon-wise").click()
        time.sleep(1)

        # 第一次选择搜索时间  2011.1-2011.6
        browser.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
        time.sleep(1)
        browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
        time.sleep(1)
        browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
        time.sleep(1)
        browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
        time.sleep(1)
        browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "01" + "']").click()
        time.sleep(1)

        browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
        time.sleep(1)
        browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
        time.sleep(1)
        browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
        time.sleep(1)
        browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "06" + "']").click()
        time.sleep(1)
        browser.find_element_by_xpath("//input[@value='确定']").click()

        time.sleep(5)

        for i in range(length):
            # 不同时间，不同间隔
            if month <= 6: # 前半年
                if year % 4 == 0:
                    size = 6.70718232
                else:
                    size = 6.744444444
            else:
                if year != 2017:
                    size = 6.633879781
                else:
                    size = 1214 / (153 + int(time.strftime("%d")) - 2 - 1) # 这里如果到2018年了还需要修改的

            # 坐标偏移量
            if count == 0:
                x_0 = 2
            else:
                x_0 = (count - 0.13) * size

            if count <= 8:
                y_0 = 30
            else:
                y_0 = 5

            if isMove == 0:
                ActionChains(browser).move_to_element_with_offset(xoyelement, 0.9*size, y_0).perform()
                time.sleep(1)
                isMove = 1
            ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()

            time.sleep(1)
            # <div class="imgtxt" style="margin-left:-117px;"></div> 
            imgelement = browser.find_element_by_xpath('//div[@id="viewbox"]')
            time.sleep(1)
            # 找到图片坐标
            locations = imgelement.location
            #print(locations)
            # 找到图片大小
            #sizes = imgelement.size
            #print(sizes)

            l = len(keyword)
            if l > 8:
                l = 8
            rangle = (int(int(locations['x'])) + l * 10 + 34, int(int(locations['y'])) + 28, int(int(locations['x'])) + l * 10 + 38 + 75, int(int(locations['y'])) + 56)


            if month < 10:
                monthName = '0' + str(month)
            else:
                monthName = str(month)
            if day < 10:
                dayName = '0' + str(day)
            else:
                dayName = str(day)
            name = str(year) + monthName + dayName
            print(name + ":" + str(locations))

            # 截取当前浏览器
            #path = "../baidu/" + str(num)
            path = "../baidu/" + str(province) + '/' + str(city) + '/' + name + '-mobile'
            browser.save_screenshot(str(path) + ".png")
            # 打开截图切割
            img = Image.open(str(path) + ".png")
            jpg = img.crop(rangle)
            jpg.save(str(path) + ".jpg")

            # 将图片放大一倍，增加识图准确率
            jpgzoom = Image.open(str(path) + ".jpg")
            (x, y) = jpgzoom.size
            x_s = 60 * 10
            y_s = 20 * 10
            out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
            out.save(path + 'zoom.jpg', 'png', quality=95)

            # 图像识别
            try:
                image = Image.open(str(path) + "zoom.jpg")
                code = pytesseract.image_to_string(image)
                print(code)

                if code:
                    # 去除一些奇奇怪怪的干扰
                    # pytesseract识别图片数字的准确率其实不是说特别高
                    code = code.replace("S", '5').replace("?", '7').replace(" ", "").replace(",", "").replace("E", "8").replace(".", "").replace("'", "").replace(u"‘", "")\
                    .replace("B", "8").replace("\"", "").replace("I", "1").replace("i", "").replace("-", "").replace("$", "8").replace(u"’", "").strip()
                    print(code)
                    index[i] += str(code)
                    print(index[i])
                    #result = str(province) + str(city) + '-' + name + '-' + code
                    #index.append(result)


                else:
                    index[i] += '-0'
                    #result = str(province) + str(city) + '-' + name + '-0'
                    #index.append(result)
            except:
                index[i] += ''
            num = num + 1

            # 下面是日期修改
            if str(day) == monthDict.get(str(month)):
                if month != 12:
                    day = 0
                    month += 1
                    # 修改查询区间了
                    if month == 7:
                        browser.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
                        time.sleep(1)
                        #browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
                        #time.sleep(1)
                        #browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
                        #time.sleep(1)
                        browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
                        time.sleep(1)
                        browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "07" + "']").click()
                        time.sleep(1)

                        #browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
                        #time.sleep(1)
                        #browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
                        #time.sleep(1)
                        browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
                        time.sleep(1)
                        browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "12" + "']").click()
                        time.sleep(1)
                        browser.find_element_by_xpath("//input[@value='确定']").click()

                        time.sleep(5)

                        count = -1
                        isMove = 0
                else:
                    day = 0
                    month = 1
                    year += 1
                    if year % 4 == 0:
                        monthDict['2'] = '29'
                    else:
                        monthDict['2'] = '28'

                    # 重新加载网站
                    js = 'window.open("http://index.baidu.com");'
                    browser.execute_script(js)
                    handles = browser.window_handles
                    browser.switch_to_window(handles[-1])
                    time.sleep(5)
                    browser.find_element_by_id("schword").clear()
                    browser.find_element_by_id("schword").send_keys(keyword)
                    time.sleep(1)
                    browser.find_element_by_id("searchWords").click()
                    time.sleep(5)
                    
                    #browser.find_element_by_id("schword").clear()
                    #time.sleep(1)
                    #browser.find_element_by_id("schword").send_keys(keyword)
                    #browser.find_element_by_id("schsubmit").click()
                    #time.sleep(3)
                    browser.find_element_by_id("compOtharea").click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA provA slided']//div//a[@href='#" + provinceDict[province] + "']").click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA cityA slided']//div//a[@href='#" + cityDict[city] + "']").click()
                    time.sleep(2)
                    xoyelement = browser.find_elements_by_css_selector("#trend rect")[2]
                    time.sleep(5)


                    # 选择移动趋势
                    browser.find_element_by_class_name("icon-wise").click()
                    time.sleep(1)

                    # 更新日期
                    browser.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
                    time.sleep(1)
                    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
                    time.sleep(1)
                    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "01" + "']").click()
                    time.sleep(1)

                    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
                    time.sleep(1)
                    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + "06" + "']").click()
                    time.sleep(1)
                    browser.find_element_by_xpath("//input[@value='确定']").click()

                    time.sleep(5)

                    count = -1
                    isMove = 0

            if year == 2017 and month == 12 and day == int(time.strftime("%d")) - 2:
                break

            day += 1
            count += 1

            ActionChains(browser).move_to_element_with_offset(xoyelement, 0, 0).perform()
            time.sleep(1)
    except Exception as err:
        print(err)
        print(num)

    print(index)
    # 日期也是可以图像识别下来的
    # 只是要构造rangle就行，但是我就是懒
    print("完成时间：" + str(time.strftime("%H:%M:%S")))
    file.write("完成时间：" + str(time.strftime("%H:%M:%S")) + "\n")
    for item in index:
        file.write(str(item) + "\n")
    file.close()
    



if __name__ == "__main__":
    keyword = input("请输入查询关键字：")
    province = input("请输入省份：")
    city = input("请输入城市：")
    length = int(input("请输入查询天数："))
    getindex(keyword, province, city, length)
