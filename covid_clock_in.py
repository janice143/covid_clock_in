# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


# 网站打卡操作
def clock_in(uid, pwd):
    # 打开浏览器，进入百度搜索
    browser = webdriver.Chrome()
    browser.get('这里填你要打卡的网站地址')
    time.sleep(2)

    # 通过find_element_by_xpath来定位用户名和密码的输入框
    browser.find_element_by_xpath("//*[@id='form1']/div[3]/div[4]/input").send_keys(uid)
    browser.find_element_by_xpath("//*[@id='form1']/div[3]/div[5]/input").send_keys(pwd)

    # 点击登录
    browser.find_element_by_xpath("//*[@id='form1']/div[3]/div[7]/input").send_keys(Keys.ENTER)

    # 点击健康打卡
    click_btn = browser.find_element_by_xpath("//*[@id='apply-content']/div[2]/ul[1]/li[2]")
    ActionChains(browser).click(click_btn).perform()
    # time.sleep(2)

    # 点击填报
    click_btn2 = browser.find_element_by_xpath("//*[@id='form1']/div[4]/button")
    ActionChains(browser).click(click_btn2).perform()

    # 点击 我知晓
    click_btn3 = browser.find_element_by_xpath("//*[@id='form1']/div[51]/div[1]/input")
    ActionChains(browser).click(click_btn3).perform()

    # 点击上报
    click_btn4 = browser.find_element_by_xpath("//*[@id='form1']/div[52]")
    ActionChains(browser).click(click_btn4).perform()

    # 截屏并保存
    browser.get_screenshot_as_file("success.png")

    # 退出浏览器
    browser.quit()


def send_email(mail_to):
    # 发送带有图片附件和正文的邮件
    MAIL_USER = "邮箱地址"  # 用于发送通知的邮箱
    MAIL_PASS = "授权码"  # 授权码，注意不是邮箱登录密码！！
    
    # 发送邮件
    msg = MIMEMultipart()
    mail_text = "已经成功打卡！"
    # 设置邮件内容，用的是之前签到返回的提示信息
    mail_body = MIMEText(mail_text)

    # 设置邮件主题、发送方和接收方
    msg['Subject'] = "每日健康打卡通知"
    msg['From'] = MAIL_USER
    msg['To'] = mail_to
    msg.attach(mail_body)

    # 添加截图附件
    fp = open("success.png", 'rb')
    images = MIMEImage(fp.read())
    fp.close()
    images.add_header('Content-Disposition', 'attachment', filename='success.png')
    msg.attach(images)

    # 登陆并发送邮件
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.login(MAIL_USER, MAIL_PASS)
    smtp.sendmail(MAIL_USER, mail_to, msg.as_string())
    smtp.quit()


# 打卡
uid = '你的用户名'
pwd = '密码'
mail_to = "接收信息的邮箱"

clock_in(uid, pwd)
send_email(mail_to)







