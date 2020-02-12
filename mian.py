import re
import jieba

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import json
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, send_from_directory, abort, redirect
import time
from io import StringIO
import os
import re


#--------------------------------------------------------------------------------------------------------------------------

#每一个事件块由一个类表示
#入职类
class people_in:  #
    def __init__(self, name, sex,  position):
        self.name = name
        self.sex = sex
        self.position = position
#离职类
class people_out:  #
    def __init__(self, name, sex, reason, position):
        self.name = name
        self.sex = sex
        self.reason = reason
        self.position = position
#离职继任类
class people_union:
    def __init__(self, name_out, sex_out, reason, position_out, name_in, sex_in,position_in):
        self.name_out = name_out
        self.sex_out = sex_out
        self.position_out = position_out
        self.reason = reason
        self.position_in = position_in
        self.name_in = name_in
        self.sex_in = sex_in

#该姓氏词典为盘古词典，一定存在漏的词，如果发现了，请添加
dic_name={"王","张","黄","周","徐","胡","高","林","马","于","程","傅","曾","叶","余","夏","钟","田","任","方","石","宁","原","库","逄","苗",
          "熊","白","毛","江","史","候","龙","万","段", "雷","钱","汤","易","常","武","赖","文","查","赵","肖","孙","李","吴","郑","冯","陈",
          "褚","卫","蒋","沈","韩","杨","朱","秦", "尤","许","何","吕","施","桓","孔","曹", "严","华","金","魏","陶","姜","戚","谢",
          "邹","喻","柏","窦","苏","潘","葛","奚","范","彭","鲁","韦","昌","俞","袁","酆", "鲍","唐","费","廉","岑","薛","贺","倪","滕","殷",
          "罗","毕","屈","祝","洪","崔","龚","嵇","邢","韶","郜","黎","蓟","溥","晏","瞿","阎","慕","茹","乜","鞠","丰","蒯","荆",
          "郝","邬","卞","康","卜","顾","孟","穆","萧","尹","姚","邵","湛","汪","祁","禹","狄","贝","臧","伏","戴","宋","茅","庞","纪","舒",
          "董","梁","杜","阮","闵","贾","娄","颜","郭","邱","骆","蔡","樊","凌","霍","虞", "柯","昝","卢","柯","缪","宗","丁","贲","邓","郁","杭",
          "滑","裴","陆","荣","荀","惠","甄","芮","羿","储","靳","汲","邴","糜","隗","侯", "宓","蓬","郗","仲","栾","钭","历","戎", "刘","詹","幸",
          "蒲","邰","鄂","咸","卓","蔺","屠","乔","郁","胥","苍","莘","翟","谭","贡","劳", "冉","郦","雍","璩","桑","桂","濮","扈","冀","浦","庄",
          "习","宦","艾","容","慎","戈","廖","庾","衡","耿","弘","匡","阙","殳","沃","蔚","夔","隆","巩","聂","晁","敖","融","訾","辛","阚","毋",
          "竺","盍","单","欧","司马", "上官", "欧阳", "夏侯", "诸葛", "闻人",
          "东方", "赫连", "皇甫", "尉迟", "公羊", "澹台",
          "公冶", "宗政", "濮阳", "淳于", "单于", "太叔",
          "申屠", "公孙", "仲孙", "轩辕", "令狐", "徐离",
          "宇文", "长孙", "慕容", "司徒", "司空", "万俟"
          }
#原因词典未使用，同时不全，如果要使用，请在这里加上
dic_res = {"因为", "因", "由于", "根据"}

#jieba分词，没有任何NLP高级用法，仅仅为接下来的规则抓取方便
def jieba_deal(text):
    jieba.load_userdict("./name.txt")
    #这里为作弊词典
    jieba.load_userdict("./reason.txt")
    jieba.load_userdict("./position_in.txt")
    jieba.load_userdict("./position_out.txt")
    word_list = jieba.cut(text, cut_all=False)
    li=[i for i in word_list]
    #print("进入Jieba分词")
    print(li)
    return li

#用于抓人的
def find_sex_name(text):
    sex=""
    name=""
    names=""
    #通用定位规则
    if "先生" in text or "女士" in text:
        if "先生" in text:
            sex = "先生"
        else:
            sex = "女士"
        index_sex = text.index(sex)
        name += text[index_sex - 1]
        temp_name = name
        flag = 1
        #print(index_sex)
        #print("flag0"+name)
        if temp_name =="":
            return sex,name,text

        #适用分词为： 刘/大
        if len(name) < 2 and index_sex-2 >= 0 and text[index_sex-2] in dic_name:
            temp = text[index_sex - 2]
            name = temp + name
            flag = 2
        #适用分词为：刘大/胆
        if len(name) < 2 and index_sex-2 >=0 and len(text[index_sex-2]) >=2 :
            temp = text[index_sex - 2]
            name = temp + name
            flag = 2
            #print("flag1")
        #适用分词为：刘/大胆
        elif len(name) == 2 and index_sex-2 >= 0 and text[index_sex-2] in dic_name:
            temp = text[index_sex - 2]
            name = temp + name
            flag = 2
            #print("flag2")
        #适用分词为：刘/大/胆
        elif len(name) < 2 and index_sex - 3>= 0 and text[index_sex-2] not in dic_name:
            temp = text[index_sex-3] + text[index_sex-2]
            name = temp + name
            flag = 3
            #print("flag3")

        #把剩下的相同人名都清空，防止误抓
        while temp_name in text:
            name_index = text.index(temp_name)
            text[name_index + 1] = ""
            if flag == 1:
                text[name_index] = ""
            if flag == 2:
                text[name_index] = ""
                text[name_index-1] = ""
            if flag == 3:
                text[name_index] = ""
                text[name_index-2] = ""
                text[name_index-3] = ""
                # print(text)

        if index_sex +2 <len(text) and text[index_sex+1] == "、":
            text[index_sex+1]=""
            for i in range(index_sex+2,len(text)):
                if i+1 < len(text):
                    if text[i] == "先生" or text[i] == "女士" and text[i+1] != "、":
                        names += text[i]
                        text[i]=""
                        break
                    else:
                        names +=text[i]
                        text[i]=""
        print("names"+names)
        print(text)
        #这里是抓一个连续的人名

    #print(sex,name)

    return sex.replace(" ",""), name.replace("）","").replace("(",""), names,text

def find_reason(text):
    reason = ""
    #起始规则通用
    if "因为" in text or "因" in text or "由于" in text or "根据" in text or "其因" in text or "因达" in text or "因其" in text:
        if "因为" in text:
            reason_index = text.index("因为")
        elif "因" in text:
            reason_index = text.index("因")
        elif "由于" in text:
            reason_index = text.index("由于")
        elif "其因" in text:
            reason_index = text.index("其因")
        elif "因达" in text:
            reason_index = text.index("因达")
        elif "因其" in text:
            reason_index = text.index("因其")
        else:
            reason_index = text.index("根据")
        text[reason_index] = ""

        if reason_index+1 <len(text):
            for i in range(reason_index+1, len(text)):
                #点停规则通用
                if text[i] == "原因" or text[i] == "，":
                    text[i] = ""
                    break
                #点停规则600270
                if text[i] == "向" and i+1<len(text) and text[i+1] =="公司" :
                    text[i] = ""
                    text[i+1] = ""
                    break
                #点停规则300411
                if text[i] == "申请" and i<len(text):
                    text[i] = ""
                    break
                #获取原因
                reason += text[i]
                #在下一个点停规则发生前把"原因"抓走
                if i+1 < len(text) and text[i + 1] == "原因":
                    reason += text[i + 1]
                #抓到的词在原组中清空，防止下次误抓
                text[i] = ""
    #print(reason, text)
    #传送原因时进行简单处理
    return reason.strip("的").replace("前述",""), text

def find_out_position(text):
    position = ""
    #通用起始规则
    if "辞去" in text:
        position_index = text.index("辞去")
        text[position_index] = ""
        for i in range(position_index+1, len(text)):

            #通用点停规则,加上规则300223改进，现在可以抓有顿号的职位了
            if text[i] == "职务" or text[i] == "，" or text[i] == "一职":
                text[i] = ""
                if i + 2 < len(text) and text[i + 1] == "、":
                    position += "、"
                    for j in range(i + 2, len(text)):
                        if text[j] == "职务" or text[j] == "，" or text[j] == "一职":
                            text[j] = ""
                            break
                        position += text[j]
                        text[j] = ""
                else:
                    break
            position += text[i]
            text[i] = ""

        #规则300223
        if "同时" in text:
            print("进入规则300223，处理 同时")
            same_index = text.index("同时")
            text[same_index] = ""
            if "辞去" in text[same_index:]:
                position_index = text.index("辞去")
                text[position_index] = ""
                position += "、"
                for i in range(position_index + 1, len(text)):
                    # 通用点停规则
                    if text[i] == "职务" or text[i] == "，" or text[i] == "一职":
                        text[i] = ""
                        if i+2 < len(text) and text[i+1] == "、":
                            for j in range(i + 1, len(text)):
                                if text[j] == "职务" or text[j] == "，" or text[j] == "一职":
                                    text[j] = ""
                                    break
                                position += text[j]
                                text[j] = ""
                        else:
                            break
                    position += text[i]
                    text[i] = ""
        #规则000691
        if "并" in text:
            print("进入规则000691，处理 并")
            same_index2 = text.index("并")
            text[same_index2] = ""
            if "辞去" in text[same_index2:]:
                position_index = text.index("辞去")
                text[position_index] = ""
                position += "、"
                for i in range(position_index + 1, len(text)):
                    # 通用点停规则
                    if text[i] == "职务" or text[i] == "，" or text[i] == "一职":
                        text[i] = ""
                        if i + 2 < len(text) and text[i + 1] == "、":
                            for j in range(i + 1, len(text)):
                                if text[j] == "职务" or text[j] == "，" or text[j] == "一职":
                                    text[j] = ""
                                    break
                                position += text[j]
                                text[j] = ""
                        else:
                            break
                    position += text[i]
                    text[i] = ""
    # #规则300499
    # if "不再" in text:
    #     print("进入规则300499","不再")
    #     no_index = text.index("不再")
    #     text[no_index] = ""
    #     if no_index +2 <len(text) and no_index+1 == "担任":
    #         text[no_index+1]=""
    #         for i in range(no_index+2,len(text)):
    #             if text[i] == "职务" or text[i] == "，" or text[i] == "一职":
    #                 text[i] =""
    #                 break
    #             position += text[i]
    #             text[i]= ""
    #     for j in range(no_index,len(text)):
    #         if text[j] == "不再":
    #             text[j] =""


    #这里是对抓出的数据的进一步处理
    position = position.replace("本公司", "").lstrip("其担任").lstrip("所担任").strip("的").replace("一职","").lstrip("公司").lstrip("其")
    if "所有" in position or "相关" in position or "一切" in position:
        position = position
        #print(position)
    else:
        position = position.replace("职务", "")

    #规则000401
    if "一切" in position and "一切职务" not in position:
        position = position + "职务"

    #规则300226
    if "，" in position:
        index = position.index("，")
        position = position[:index]
    print("离职",position,text)
    return position, text

#规则300128，与 find_out_position_extra 同步
def find_out_position_extra(text):
    position = ""
    #通用起始规则
    if "担任" in text:
        position_index = text.index("担任")
        text[position_index] = ""
        for i in range(position_index+1, len(text)):

            #通用点停规则,加上规则300223改进，现在可以抓有顿号的职位了
            if text[i] == "职务" or text[i] == "，" or text[i] == "一职":
                text[i] = ""
                if i + 2 < len(text) and text[i + 1] == "、":
                    position += "、"
                    for j in range(i + 2, len(text)):
                        if text[j] == "职务" or text[j] == "，" or text[j] == "一职":
                            text[j] = ""
                            break
                        position += text[j]
                        text[j] = ""
                else:
                    break
            position += text[i]
            text[i] = ""

        #规则300223
        if "同时" in text:
            print("进入规则300223，处理 同时")
            same_index = text.index("同时")
            text[same_index] = ""
            if "辞去" in text[same_index:]:
                position_index = text.index("辞去")
                text[position_index] = ""
                position += "、"
                for i in range(position_index + 1, len(text)):
                    # 通用点停规则
                    if text[i] == "职务" or text[i] == "，" or text[i] == "一职":
                        text[i] = ""
                        if i+2 < len(text) and text[i+1] == "、":
                            for j in range(i + 1, len(text)):
                                if text[j] == "职务" or text[j] == "，" or text[j] == "一职":
                                    text[j] = ""
                                    break
                                position += text[j]
                                text[j] = ""
                        else:
                            break
                    position += text[i]
                    text[i] = ""
        #规则000691
        if "并" in text:
            print("进入规则000691，处理 并")
            same_index2 = text.index("并")
            text[same_index2] = ""
            if "辞去" in text[same_index2:]:
                position_index = text.index("辞去")
                text[position_index] = ""
                position += "、"
                for i in range(position_index + 1, len(text)):
                    # 通用点停规则
                    if text[i] == "职务" or text[i] == "，" or text[i] == "一职":
                        text[i] = ""
                        if i + 2 < len(text) and text[i + 1] == "、":
                            for j in range(i + 1, len(text)):
                                if text[j] == "职务" or text[j] == "，" or text[j] == "一职":
                                    text[j] = ""
                                    break
                                position += text[j]
                                text[j] = ""
                        else:
                            break
                    position += text[i]
                    text[i] = ""
    # #规则300499
    # if "不再" in text:
    #     print("进入规则300499","不再")
    #     no_index = text.index("不再")
    #     text[no_index] = ""
    #     if no_index +2 <len(text) and no_index+1 == "担任":
    #         text[no_index+1]=""
    #         for i in range(no_index+2,len(text)):
    #             if text[i] == "职务" or text[i] == "，" or text[i] == "一职":
    #                 text[i] =""
    #                 break
    #             position += text[i]
    #             text[i]= ""


    #这里是对抓出的数据的进一步处理
    position = position.replace("本公司", "").strip("其担任").strip("所担任").strip("的").replace("一职","").lstrip("公司").lstrip("其")
    if "所有" in position or "相关" in position or "一切" in position:
        position = position
        #print(position)
    else:
        position = position.replace("职务", "")

    #规则000401
    if "一切" in position and "一切职务" not in position:
        position = position + "职务"

    #规则300226
    if "，" in position:
        index = position.index("，")
        position = position[:index]
    print("离职",position,text)
    return position, text

def find_in_position(text):
    position = ""
    name=""
    sex=""
    names=""
    if "同意" in text or "提名" in text or "推举" in text or "推选" in text or "聘任" in text or "选举" in text or "补选" in text:
        if "同意" in text:
            index = text.index("同意")
        elif "提名" in text:
            index = text.index("提名")
        elif "推举" in text:
            index = text.index("推举")
        elif "推选" in text:
            index = text.index("推选")
        elif "聘任" in text:
            index = text.index("聘任")
        elif "选举" in text:
            index = text.index("选举")
        else:
            index = text.index("补选")
        #print("indx_text_temp",index)
        text_temp = text[index:]
        #专门处理 600516 bug ,然而并没有成功提取 600516 内容。除非这一块出现了问题，否则不要动
        sex,name,names,text_temp=find_sex_name(text_temp)
        print("in name process", sex, name, text_temp)
        if name == "":
            return position, text, name, sex,names
        elif len(name) > 2 and name in text:
            for j in range(len(text)):
                if text[j] == name and j + 1 < len(text):
                    if text[j + 1] == "先生" or text[j + 1] == "女士":
                        text[j] = ""
                        text[j + 1] = ""
            # print("flag22",name,text)
        elif len(name) > 2 and name[1:] in text:
            name_index = text.index(name[1:])
            if name_index + 1 < len(text) and name in text:
                for j in range(len(text)):
                    if text[j] == name and j+1<len(text):
                        if text[j+1] == "先生" or text[j+1] == "女士":
                            text[j]= ""
                            text[j+1]= ""
            # print("flag33",text)

        #这里是通用规则
        if "为" in text_temp or "补选" in text_temp or "担任" in text_temp:
            if "为" in text_temp:
                position_index = text_temp.index("为")
            elif "担任" in text_temp:
                position_index = text_temp.index("担任")
            else:
                position_index = text_temp.index("补选")
            text[index] = ""
            text[position_index+index]=""
            if position_index+1 < len(text_temp):
                for i in range(position_index+1,len(text_temp)):
                    if text_temp[i] == "（" or text_temp[i] == "，":
                        break
                    position += text_temp[i]
                    text[i - position_index] = ""
    position = position.replace("本公司", "").strip(" ").replace("一职", "").replace("新任", "").lstrip("公司").strip("的").lstrip("新任")
    if "所有" in position or "相关" in position or "一切" in position:
        position = position
    else:
        position = position.replace("职务", "")
    if "候选人" in position:
        name = ""
    #规则300672
    position =position.replace("的议案》", "")
    print("入职", position, name, sex,text)
    return position, text, name.replace("）","").replace("(",""), sex, names


def find_people_out(text):
    people = []
    while "辞去" in text:
        sex, name, names,text = find_sex_name(text)
        reason, text = find_reason(text)
        position, text = find_out_position(text)
        if "有关规定" in reason:
            name = ""
        if "公司章程" in position:
            name = ""
        if "公司法" in position:
            name = ""
        if name == "":
            return people
        people.append(people_out(name, sex, reason, position))
        if names !="":
            temp_names = names.split("、")
            for i in temp_names:
                if len(i) > 1:
                    people.append((people_out(i[:-2], i[-2:], reason, position)))
    return people

#规则 300128 ，与 find_people_out 同步
def find_people_out_extra(text):
    people = []
    while "不再" in text:
        sex, name, names,text = find_sex_name(text)
        reason, text = find_reason(text)
        position, text = find_out_position_extra(text)
        if "有关规定" in reason:
            name = ""
        if "公司章程" in position:
            name = ""
        if "公司法" in position:
            name = ""
        if "任何" in position:
            name = ""
        if name == "":
            return people
        people.append(people_out(name, sex, reason, position))
        if names !="":
            temp_names = names.split("、")
            for i in temp_names:
                if len(i) > 1:
                    people.append((people_out(i[:-2], i[-2:], reason, position)))
        #print(names)
    return people



def find_people_in(text):
    people = []
    #names =[]
    while "先生" in text or "女士" in text:
        # sex, name, text = find_sex_name(text)
        # if name == "":
        #     return people
        # print(name)
        # print(text)
        #这里改了一下，用职务的定位词去抓人名
        position, text, name, sex,names = find_in_position(text)
        if position == "" or name == "":
            return people
        people.append(people_in(name, sex, position))
        # print(position)
        # print(text)
        print("in name",name)
        print("in_names",names)
        if names !="":
            temp_names = names.split("、")
            for i in temp_names:
                if len(i) > 1 and i != "":
                    print(i)
                    people.append(people_in(i[:-2], i[-2:], position))
    return people

def deal_texts(texts):
    in_people = []
    out_people = []
    union_people = []
    for k in texts:
        #这里是跳过的句式，用于处理离职的人
        if "感谢" in k or "是否" in k or "尽责" in k or "不得担任" in k or "代为" in k or "低于" in k or "勤勉" in k or "敬业" in k or "二分之一" in k:
            continue
        elif re.search("[因由根].*[，原].*辞去.*[职]", k) is not None and "保证" not in k:
            out_people += find_people_out(jieba_deal(k))
        #处理中间含有 向公司辞去 句式
        elif re.search("[因由根].*向公司.*辞去.*[职]", k) is not None and "保证" not in k:
            out_people += find_people_out(jieba_deal(k))
        #处理中间含有 申请辞去 句式
        elif re.search("[因由根].*申请辞去.*[职]", k) is not None and "保证" not in k:
            out_people += find_people_out(jieba_deal(k))
        #规则300499 处理中间含有 不再担任 句式
        elif re.search("[因由根].*不再担任.*[职]", k) is not None and "保证" not in k:
            print("进入离职分类")
            out_people += find_people_out_extra(jieba_deal(k))
        #这里是跳过的句式，用于处理进来的人
        # "生效" 600476
        if "尽责" in k or "符合" in k or "勤勉" in k or "感谢" in k or "继续" in k or "留任" in k:
            continue
        elif re.search("[同提推选聘任].*[担为]", k) is not None:
            in_people += find_people_in(jieba_deal(k))


    #处理就职中出现的大量重复
    if in_people !=[] and len(in_people) > 1:
        print("进入就职重复处理")
        for m in range(len(in_people)):
            for n in range(m+1,len(in_people)):
                if in_people[m].name == in_people[n].name and in_people[m].name!= "":
                    if in_people[m].position in in_people[n].position:
                        in_people[m].name = ""
                    elif in_people[n].position in in_people[m].position:
                        in_people[n].name = ""

    #这里是就职任职的联合
    if in_people != [] and out_people !=[]:
        print("进入联合处理")
        for i in range(len(out_people)):
            for j in range(len(in_people)):
                if in_people[j].position in out_people[i].position and in_people[j].position !="" and in_people[j].name !="" and out_people[i].name !="":
                    union_people.append(people_union(out_people[i].name,out_people[i].sex,out_people[i].reason,out_people[i].position,in_people[j].name,in_people[j].sex,in_people[j].position))
                    in_people[j].name = ""
                    out_people[i].name = ""
                    if i+1<len(out_people):
                        i+=1

    # 这里是用来输出测试
    if union_people !=[]:
        for k in union_people:
            print("union" + k.name_out +k.sex_out + k.name_in +k.sex_in+k.reason+k.position_out)
    if in_people != []:
        for p in in_people:
            if p.name != "":
                print("in"+p.name+p.sex+p.position)
    else:
        print("no people in")

    if out_people !=[]:
        for n in out_people:
            if n.name != "":
                print("out"+n.name+n.sex+n.reason+n.position)
    else:
        print("no people out ")

    return out_people,in_people,union_people


#----------------------------------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['pdf'])

# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 用于测试上传，稍后用到
@app.route('/test/upload')
def upload_test():
    return render_template('upload.html')

# 上传文件
@app.route('/ccks_pdf/annualreport', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值

    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        uppath = os.path.join(file_dir, f.filename)
        f.save(uppath)  # 保存文件到upload目录
        jsons = getdata(uppath)
        jsonfilename = f.filename.split('.')[0]+'.json'
        downfile = os.path.join(file_dir, jsonfilename)
        fp = open(downfile, 'w+', encoding='UTF-8')
        fp.write(jsons)
        fp.close()
        return redirect('/download/' + jsonfilename)
    else:
        return jsonify({"errno": 1001, "errmsg": "上传失败"})

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == "GET":
        directory = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
        return send_from_directory(directory, filename, as_attachment=True)
    abort(404)
#----------------------------------------------------------------------------------------------------------------------------
def getdata(savepath) :
    filename = os.path.basename(savepath)  # 取名字

    if (filename.endswith('pdf') or filename.endswith('PDF')):
        # 这里是读取Pdf单个文件，功能完整，勿动
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(savepath + filename, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)

        # 我们读出来的单个文件，第一次处理，去除异常符号，将其转换成以句号为分割的列表,把 特此公告 以后的所有消息去掉。
        text = retstr.getvalue().replace(u'\xa9', u'').replace(u'\xa0', u'').replace(u'\xad', u'').replace(u'\x0c', u'') \
            .replace(u'\u037e', u'').replace(" ", "").replace("\n", "").replace("\t", "").replace("；", "。").replace("！",
                                                                                                                    "。")

        out_people, in_people, union_people = deal_texts(text)

        data = ""
        flag = 0
        data += '{"' + filename.split('.')[0].replace("_", "*") + '": {"证券代码": "' + filename.split('-')[0] + '", "证券简称": "' + filename.split('-')[1].replace("_", "*") + '", "人事变动": ['
        if union_people != []:
            for i in union_people:
                if i.name_in != "":
                    flag = 1
                    data = data + '{' + '"离职高管姓名": "' + i.name_out + '",' + '"离职高管性别": "' + i.sex_out + '",' + '"离职高管职务": "' + i.position_out + '",' + '"离职原因": "' + i.reason + '",' + '"继任者姓名": "' + i.name_in + '",' + '"继任者性别": "' + i.sex_in + '",' + '"继任者职务": "' + i.position_in + '"},'
        if out_people != []:
            for i in out_people:
                if i.name != "":
                    flag = 1
                    data = data + '{' + '"离职高管姓名": "' + i.name + '",' + '"离职高管性别": "' + i.sex + '",' + '"离职高管职务": "' + i.position + '",' + '"离职原因": "' + i.reason + '",' + '"继任者姓名": ' + 'null' + ',' + '"继任者性别": ' + 'null' + ',' + '"继任者职务": ' + 'null' + '},'
        if in_people != []:
            for j in in_people:
                if j.name != "":
                    flag = 1
                    data = data + '{' + '"离职高管姓名": ' + 'null' + ',' + '"离职高管性别": ' + 'null' + ',' + '"离职高管职务": ' + 'null' + ',' + '"离职原因": ' + 'null' + ',' + '"继任者姓名": "' + j.name + '",' + '"继任者性别": " ' + j.sex + '",' + '"继任者职务": "' + j.position + '"},'
        if flag == 0:
            data = data + '{' + '"离职高管姓名": ' + 'null' + ',' + '"离职高管性别": ' + 'null' + ',' + '"离职高管职务": ' + 'null' + ',' + '"离职原因": ' + 'null' + ',' + '"继任者姓名": ' + 'null' + ',' + '"继任者性别": ' + 'null' + ',' + '"继任者职务": ' + 'null' + '},'
        data = data[:-1] + ']}}'
        data = data.replace(" ", "")

        print("json", data)

        dic = json.loads(data)
        js = json.dumps(dic, indent=4, separators=(',', ': '), ensure_ascii=False)
        return js

