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


#def getInfomation(province, city, province2, city2, province3, city3):
def getInfomation(province, city, province2, city2, province3, city3):
    global browser
    url = "http://top.baidu.com/"
    # 打开谷歌浏览器
    # Firefox()
    # Chrome()
    browser = webdriver.Chrome()
    # 输入网址
    browser.get(url)
    time.sleep(3)

    # 最大化窗口
    browser.maximize_window()
    time.sleep(2)

    # 地域风向标
    browser.find_element_by_xpath("//*[@id='main-nav']/li[10]/a").click()
    time.sleep(2)

    # 热点
    browser.find_element_by_xpath("//*[@id='provinceSel']/div[3]/div[1]/ul/li[4]").click()
    time.sleep(2)

    # 民生热点
    browser.find_element_by_xpath("//*[@id='provinceSel']/div[3]/div[3]/div[4]/div[1]/ul/li[2]").click()
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

    file = open("../baidu/result.txt", "w", encoding='UTF-8')

    
    # 选择最左边的省份
    browser.find_element_by_xpath("//*[@id='provinceSel']/div[3]/div[2]/div[1]/div/div[1]/div").click()
    time.sleep(1)
    browser.find_element_by_xpath("//div[@id='shengPanel']//a[@val='" + provinceDict[province] + "']").click()
    time.sleep(1)
    # 选择最左边的城市
    browser.find_element_by_xpath("//*[@id='provinceSel']/div[3]/div[2]/div[1]/div/div[2]/div").click()
    time.sleep(1)
    browser.find_element_by_xpath("//div[@id='shiPanel']//a[@val='" + cityDict[city] + "']").click()
    time.sleep(3)

    file.write(province + "-" + city)
    file.write("\n")
    # 关键词
    count = 1
    while count <= 50:
        # 排名
        item = str(count) + " "
        # 关键词
        keyWordPath = "//*[@id='provinceSel']/div[3]/div[3]/div[4]/div[2]/div[2]/div[1]/div[2]/ul/li[" + str(count) + "]/div/a"
        item += browser.find_element_by_xpath(keyWordPath).text
        item += " "
        # 关注度
        focusPath = "//*[@id='provinceSel']/div[3]/div[3]/div[4]/div[2]/div[2]/div[1]/div[2]/ul/li[" + str(count) + "]/div/div/span"
        focus = browser.find_element_by_xpath(focusPath)
        browser.execute_script("alert(window.getComputedStyle(arguments[0],false).width);", focus)
        alert = browser.switch_to_alert()
        time.sleep(0.5)
        test = alert.text
        alert.accept()
        temp = float(test.replace("px" , '')) / 97 * 100
        percent = str(float('%.2f' % temp)) + "%"

        item += percent
        print(item)
        file.write(item)
        file.write("\n")
        count += 1


    file.write("\n")
    time.sleep(2)
    

    # 选择中间的的省份
    browser.find_element_by_xpath("//*[@id='provinceSel']/div[3]/div[2]/div[2]/div/div[1]/div").click()
    time.sleep(1)
    browser.find_element_by_xpath("//div[@id='shengPanel']//a[@val='" + provinceDict[province2] + "']").click()
    time.sleep(1)
    # 选择中间的的城市
    browser.find_element_by_xpath("//*[@id='provinceSel']/div[3]/div[2]/div[2]/div/div[2]/div").click()
    time.sleep(1)
    browser.find_element_by_xpath("//div[@id='shiPanel']//a[@val='" + cityDict[city2] + "']").click()
    time.sleep(3)

    file.write(province2 + "-" + city2)
    file.write("\n")
    # 关键词
    count = 1
    while count <= 50:
        # 排名
        item = str(count) + " "
        # 关键词
        keyWordPath = "//*[@id='provinceSel']/div[3]/div[3]/div[4]/div[2]/div[2]/div[2]/div[2]/ul/li[" + str(count) + "]/div/a"
        item += browser.find_element_by_xpath(keyWordPath).text
        item += " "
        # 关注度
        focusPath = "//*[@id='provinceSel']/div[3]/div[3]/div[4]/div[2]/div[2]/div[2]/div[2]/ul/li[" + str(count) + "]/div/div/span"
        focus = browser.find_element_by_xpath(focusPath)
        browser.execute_script("alert(window.getComputedStyle(arguments[0],false).width);", focus)
        alert = browser.switch_to_alert()
        time.sleep(0.5)
        test = alert.text
        alert.accept()
        temp = float(test.replace("px" , '')) / 97 * 100
        percent = str(float('%.2f' % temp)) + "%"

        item += percent
        print(item)
        file.write(item)
        file.write("\n")
        count += 1

    file.write("\n")
    time.sleep(2)
    
    # 选择最右边的省份
    browser.find_element_by_xpath("//*[@id='provinceSel']/div[3]/div[2]/div[3]/div/div[1]/div").click()
    time.sleep(1)
    browser.find_element_by_xpath("//div[@id='shengPanel']//a[@val='" + provinceDict[province3] + "']").click()
    time.sleep(1)
    # 选择最右边的城市
    browser.find_element_by_xpath("//*[@id='provinceSel']/div[3]/div[2]/div[3]/div/div[2]/div").click()
    time.sleep(1)
    browser.find_element_by_xpath("//div[@id='shiPanel']//a[@val='" + cityDict[city3] + "']").click()
    time.sleep(3)

    file.write(province3 + "-" + city3)
    file.write("\n")
    # 关键词
    count = 1
    while count <= 50:
        # 排名
        item = str(count) + " "
        # 关键词
        keyWordPath = "//*[@id='provinceSel']/div[3]/div[3]/div[4]/div[2]/div[2]/div[3]/div[2]/ul/li[" + str(count) + "]/div/a"
        item += browser.find_element_by_xpath(keyWordPath).text
        item += " "
        # 关注度
        focusPath = "//*[@id='provinceSel']/div[3]/div[3]/div[4]/div[2]/div[2]/div[3]/div[2]/ul/li[" + str(count) + "]/div/div/span"
        focus = browser.find_element_by_xpath(focusPath)
        browser.execute_script("alert(window.getComputedStyle(arguments[0],false).width);", focus)
        alert = browser.switch_to_alert()
        time.sleep(0.5)
        test = alert.text
        alert.accept()
        temp = float(test.replace("px" , '')) / 97 * 100
        percent = str(float('%.2f' % temp)) + "%"

        item += percent
        print(item)
        file.write(item)
        file.write("\n")
        count += 1


    

    file.close()


if __name__ == "__main__":
    province = input("请输入第一个省份：")
    city = input("请输入第一个城市：")
    province2 = input("请输入第二个省份：")
    city2 = input("请输入第二个城市：")
    province3 = input("请输入第三个省份：")
    city3 = input("请输入第三个城市：")
    getInfomation(province, city, province2, city2, province3, city3)
    #getInfomation(province, city, province2, city2)
