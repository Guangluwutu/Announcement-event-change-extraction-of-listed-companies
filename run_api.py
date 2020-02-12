from flask import Flask, g
from flask_restful import reqparse, Api, Resource
from flask_httpauth import HTTPTokenAuth

import requests
url = "http://59.71.234.59:5000//Data_deal"
files = {'myfile':open("000010-美丽生态-关于总经理辞职的公告.pdf",'rb')}
r = requests.post(url,files=files)
print(r.text)

out_people=[]
if out_people != [] and len(out_people) > 1:
    # print("进入就职重复处理")
    for m in range(len(out_people)):
        for n in range(m + 1, len(out_people)):
            if out_people[m].name == out_people[n].name and out_people[m].name != "":
                if out_people[m].position in out_people[n].position:
                    out_people[m].name = ""
                elif out_people[n].position in out_people[m].position:
                    out_people[n].name = ""