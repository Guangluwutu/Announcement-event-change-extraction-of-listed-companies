class people_out:  # 该类表示每个点的坐标
    def __init__(self, name, sex, reason, position):
        self.name = name
        self.sex = sex
        self.reason = reason
        self.position = position

def find_man_sex_name(data):
    sex=""
    name=""
    if "先生" in data:
        index_sex = data.index("先生")
        sex += "先生"
        name = data[index_sex - 1]
        if len(name) < 2:
            name = data[index_sex - 2] + name
            data[index_sex] = ""
            data[index_sex - 1] = ""
            data[index_sex - 2] = ""
        else:
            name = data[index_sex - 1]
            data[index_sex] = ""
            data[index_sex - 1] = ""
    elif "女士" in data:
        index_sex = data.index("女士")
        sex += "女士"
        name = data[index_sex - 1]
        if len(name) < 2:
            name = data[index_sex - 2] + name
            data[index_sex] = ""
            data[index_sex - 1] = ""
            data[index_sex - 2] = ""
        else:
            name = data[index_sex - 1]
            data[index_sex] = ""
            data[index_sex - 1] = ""

    return sex, name.strip("）"), data

def find_man_reason(data):
    reason = ""
    dic_res1 = ["因为", "因", "由于", "根据"]
    for i in dic_res1:
        if i in data:
            index_reason = data.index(i)
            data[index_reason] = ""
            for i2 in range(index_reason+1,len(data)):
                if data[i2] == "原因" or data[i2] == "，":
                    data[i2] = ""
                    break
                reason += data[i2]
                if i2+1< len(data) and data[i2+1]=="原因":
                    reason +=data[i2+1]
                data[i2] = ""
            break
    return reason.strip("的"), data

def find_man_position(data):
    position = ""
    if "辞去" in data:
        index_position = data.index("辞去")
        data[index_position] = ""
        for j2 in range(index_position+1,len(data)):
            if data[j2] == "职务" or data[j2] == "，":
                data[j2] = ""
                break
            position += data[j2]
            data[j2] = ""
    return position.replace("本公司","").replace("公司","").strip("的"), data


def find_man_out(data):
    # 这里是抓人
    sex, name, data = find_man_sex_name(data)
    # 这里是抓原因
    reason, data = find_man_reason(data)
    # 这里是抓职务
    position,data = find_man_position(data)
    #这里是合并数据
    temp = people_out(name, sex, reason, position)
    #print(data)
    return temp, data
    #print(name, sex, reason, position)

def find_all_man_out(data):
    all_people=[]
    while "辞去" in data:
        temp, data = find_man_out(data)
        all_people.append(temp)
    return all_people, data
'''
line = ['殷必彤', '先生', '因', '工作变动', '原因', '，', '辞去', '公司', '总经理', '、', '董事', '职务', '，', '同时', '辞去', '董事会', '战略', '委员会', '委员', '职务']
temp, data = find_all_man_out(line)
#print(data)
for i in temp:
    print(i.sex,i.name,i.position,i.reason)
'''
'''
line = ['廖绮云', '女士', '表示', '因', '工作', '精力', '和', '工作', '安排', '等', '原因', '，', '申请', '辞去', '公司', '非', '职工', '代表', '职工代表',
        '监事', '职务', '。']
temp, data = find_man_out(line)
print(data)
print(temp.sex,temp.name,temp.position,temp.reason)
'''



