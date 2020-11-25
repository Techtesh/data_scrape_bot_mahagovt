# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 21:03:52 2020

@author: Hitesh
"""



import selenium
from bs4 import BeautifulSoup as soup
import random
import time
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver 
from PIL import Image
import pytesseract
import sys
import argparse
from subprocess import check_output
import json
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



def get_fromfile():
    file=open("datagrab.txt","r")
    
    Line=file.readlines()
    nos=[]
    for l in Line:
        l=l[:-2]
        print(l)
        nos.append(l)
    return nos
def set_anarray():
    print("enter ids seperated by commas")
    nos =input().split(",")
    print(nos)
    return nos
    pass

def gen_randos():
    states=["AP","AR","AS","BR","GA","GJ","HP","HR","KA","KL","MP","MH","ML","MZ","NL","OR","PB","RJ","SK","TN","TG","TR","UT","UP","WB","AN","CH","DN","DD","DL","JK","LA","LD","PY"]
    int1=random.randint(0,99999)
    if int1<9:int1="0000"+str(int1)
    elif int1<99:int1="000"+str(int1)
    elif int1<999:int1="00"+str(int1)
    elif int1<9999:int1="0"+str(int1)
    else : int1=str(int1)
    int2=random.randint(0,9999)
    if int2<9:int2="000"+str(int2)
    elif int2<99:int2="00"+str(int2)
    elif int2<999:int2="0"+str(int2)
    else :int2=str(int2)   
    int3=random.randint(0,999999)
    if int3<9:int3="00000"+str(int3)
    elif int3<99:int3="0000"+str(int3)
    elif int3<999:int3="000"+str(int3)
    elif int3<9999:int3="00"+str(int3)
    elif int3<99999:int3="0"+str(int3)
    else:int3=str(int3)    
    name="U"+int1+states[random.randint(0,len(states)-1)]+int2+"PTC"+int3    
    return name
    pass

def json_out(jsondata):
    file=open("output_sample.txt","a")
    file.write(jsondata)


base_url="http://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do"
print("select data source \n 1)file \n 2)enter array \n 3)random")
path=int(input())
if path==1:
    nos=get_fromfile()
if path==2:
    nos=set_anarray()
if path==3:
    nos=[]
    n=0
    while n<10:
        name=gen_randos()
        nos.append(name)
        n+=1



for n in nos:
    #open webpage
    driver=webdriver.Chrome("C:/Users/Hitesh/Downloads/chromedriver")
    driver.get(base_url)
    
    #fill first form
    try:
        driver.find_element_by_id('companyID').send_keys(n)
    except:
        driver.find_element_by_name("companyID").sendkeys(n)
    
    captcha=driver.find_element_by_id("captcha")
    location=captcha.location
    size=captcha.size
    driver.save_screenshot("captcha.png")
    x,y=location["x"]+150,location["y"]+100
    width=x+size["width"]
    height=y+size["height"]
    print(x,y,width,height)
    im=Image.open("captcha.png")
    im=im.crop((x,y,width,height))
    im.save("onlycap.png")
    data=pytesseract.image_to_string(im)
    print("op=",data)
    
    try:
        driver.find_element_by_name("userEnteredCaptcha").send_keys(data)
        time.sleep(2)
    except:
        driver.find_element_by_id("userEnteredCaptcha").send_keys(data)
        time.sleep(2)
    driver.find_element_by_id("companyLLPMasterData_0").send_keys(Keys.ENTER)  
    time.sleep(5)
    #WAIT FOR WEBPAGE TO LOAD
    #time.sleep(100)
    input()
    
    #now the webpage is open grab data from the page
    print("grabbing table")
    
    table=driver.find_elements_by_xpath("//table[@name='resultTab1']")#.text
    
    
    t1data={}
    cuts=["CIN","Company Name","ROC Code","Registration Number","Company Category","Company SubCategory","Class of Company","Authorised Capital(Rs)","Paid up Capital(Rs)","Number of Members(Applicable in case of company without Share Capital)","Date of Incorporation","Registered Address","Address other than R/o where all or any books of account and papers are maintained","Email Id","Whether Listed or not","ACTIVE compliance","Suspended at stock exchange","Date of last AGM","Date of Balance Sheet","Company Status(for efiling)"]     
    op={}#"table1":"company/master data"}
    for rows in table:
        
        temp=rows.text
        temp=temp.split("\n")
        for i,t in enumerate(temp):
            t=t[len(cuts[i]):]
            print(f" {t}")
            #t1data.append(t)
            t1data[cuts[i]]=t
    op["table1"]=t1data
    print("grabbing next table")
    table=driver.find_elements_by_xpath("//table[@name='resultTab6']")
    t2data=[]
    
    for i,rows in enumerate(table):
        temp=rows.text
        temp=temp.split("\n")
        for t in temp:
            print(t)
            t2data.append(t)
            #op[str(i)]=t
    op["table2"]=t2data   
    json_dump=json.dumps(op,separators=(".","="))
    print(json_dump)
    json_out(json_dump)
    
   
driver.quit()