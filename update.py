# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# time: 2019/12/19
# __author__ = 'HaoBingo'

from __future__ import print_function
import requests
import re
import time
import json
import subprocess
import random
import urllib3
urllib3.disable_warnings()

debug = False


s = requests.Session()

if debug == True:
    s.proxies = {"https": "127.0.0.1:8080"}

    
def getApplymail():
    url = "https://bccto.me/"
    headers = {"Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7"}
    req = s.get(url,headers=headers,verify=False).text
    mail = re.findall(u'showmail">(.+?\@bccto.me)</span>',req)[0]
    print("[+]get mail:\t%s" %mail)
    url = "https://bccto.me/applymail"
    data = {"mail": mail}
    req = s.post(url,data=data,headers=headers,verify=False).text
    #print(req)
    return mail


def getMail(mail):
    print("[+]wait to receive mail...")
    url = "https://bccto.me/getmail"
    data = {"mail": mail}
    headers = {"Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7"}
    req = s.post(url,headers=headers,data=data,verify=False).text
    try:
        data = json.loads(req)
        if data["mail"]:
            print("[+]get mail...")
            sub = data["mail"][0][4]
            url = "https://bccto.me/win/%s/%s" %(mail.replace("@","(a)").replace(".","-_-"),sub)
            print("[+]email url:\t%s" %url)
            html = s.get(url,headers=headers,verify=False).text
            code = re.findall(u'(\S{4}-\S{4}-\S{4}-\S{4}-\S{4})<br><br>',html)[0]
            print("[+]Active Code:\t%s" %code)
            return code
        else:
            print("[-]retry...")
            time.sleep(5)
            return getMail(mail)
    except:
        print("[!]%s" %req)
        print("[-]retry...")
        time.sleep(5)
        return getMail(mail)
       
    
def register(email):
    print("[+]Register Nessus...")
    url = "https://zh-cn.tenable.com/products/nessus/nessus-essentials?tns_redirect=true"
    html = s.get(url,verify=False).text
    token = re.findall(r'token" type="hidden" value="(.+?)"',html)[0]
    print("[+]get the register token: %s" %token)
    first_name = ["alex","bob","cidy","doge","frank","editon"]
    last_name  = ["John","Gary","Viola","Judy","Sylvia"]
    payloads = {"first_name": random.choice(first_name),
                "last_name": random.choice(last_name),
                "email": email,
                "org_name": "",
                "robot": "human",
                "type": "homefeed",
                "token": token,
                "country": "CN",
                "submit": r"注册"               
               }
    req = s.post(url,data=payloads,verify=False)

    
def getParam(code):
    print("[+]get param")
    url = "https://plugins.nessus.org/register.php?serial=%s" %code
    res = s.get(url,verify=False).text
    if "SUCCESS" in res:
        u = res.split("\n")[1]
        p = res.split("\n")[2]
        print("[+]get u:\t"+u)
        print("[+]get p:\t"+p)
        return u,p       
    else:
        print("[!]Get u&p Fail!")

def down(url,retry=3):
    print("[+]download the data...")
    success = False
    while retry > 0 and not success:
        try:
            req = s.get(url,stream=True)
            #print(req.headers)
            #print(req.status_code)
            chunk_size = 1024
            size = 0
            content_size = int(req.headers['Content-Length'])
            print("[+]File size: %0.2f MB" %(content_size / chunk_size / 1024))
            with open("all-2.0.tar.gz","wb") as f:
                for data in req.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    size += len(data)
                    print("\r[*]prcess: %s%.2f%%" %(">"*int(50*size/content_size),(size/content_size*100)) , end="")
                    f.flush()
            print("\n[*]download successful")
            success = True
            #return True
        except Exception as e:
            print("[!]Error:\t%s" %e)
            retry -= 1
            return down(url,retry)
    
def getUpdatePackage(code):
    u,p = getParam(code)
    url = "https://plugins.nessus.org/v2/nessus.php?f=all-2.0.tar.gz&u=%s&p=%s" %(u,p)
    print("[+]Down link:\t%s" %url) 
    down(url)

def doUpdate():
    print("[!]Do update plugins...")
    print("[!]Please be patient...")
    print("[!]It tasks long time...")
    try:
        retcode = subprocess.call("/opt/nessus/sbin/nessuscli update all-2.0.tar.gz")
        if retcode == 0:
            print("[*]Update successful.  The changes will be automatically processed by Nessus.")
        else:
            print("[!]automatic update faid!")
            print("[-]you can update manually...")
            print("[-]Run /opt/nessus/sbin/nessuscli update all-2.0.tar.gz")
    except:
        print("[!]automatic update faid!")
        print("[-]you can update manually...")
        print("[-]Run /opt/nessus/sbin/nessuscli update all-2.0.tar.gz")
        
    print("[*]have a nice day ^_^")
    
def main():
    mail = getApplymail()
    register(mail)
    time.sleep(2)
    code = getMail(mail)
    getUpdatePackage(code)
    doUpdate()   

if __name__ == "__main__":
    main()


