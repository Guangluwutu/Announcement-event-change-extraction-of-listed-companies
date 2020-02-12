class people_in:  # 该类表示每个点的坐标
    def __init__(self, name, sex,  position):
        self.name = name
        self.sex = sex
        #self.reason = reason
        self.position = position

def find_man_sex_name(data):
    sex=""
    name=""
    index_sex = 0
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
    return sex, name, index_sex,data

def find_man_position(index_sex,data):
    position = ""
    '''
    if "辞去" in data:
        index_position = data.index("辞去")
        for j2 in range(index_position+1, len(data)):
            if data[j2] == "职务" or data[j2] == "，" or "职"in data[j2]:
                break
            position += data[j2]
            data[j2] = ""
    '''
    dic_index=["同意","提名","推举","推选","聘任","出任","担任"]
    data_temp=data[index_sex:]
    if "为" in data_temp:
        index_position = data_temp.index("为")
        data[index_position-index_sex] = ""
        for i in range(index_position+1,len(data_temp)) :
            if data_temp[i] == "（" or data_temp[i] == "，":
                break
            position += data_temp[i]
            data[i-index_position] = ""
    elif "担任" in data_temp:
        index_position = data_temp.index("担任")
        data[index_position-index_sex] = ""
        for i in range(index_position+1,len(data_temp)) :
            if data_temp[i] == "（" or data_temp[i] == "，":
                break
            position += data_temp[i]
            data[i-index_position] = ""
    elif "补选" in data_temp:
        index_position = data_temp.index("补选")
        data[index_position-index_sex] = ""
        for i in range(index_position+1,len(data_temp)) :
            if data_temp[i] == "（" or data_temp[i] == "，":
                break
            position += data_temp[i]
            data[i-index_position] = ""
    return position.replace("候选人","").replace("本公司","").replace("公司","").strip(" "), data

def find_man_in(data):
    # 这里是抓人
    sex, name, index_sex,data = find_man_sex_name(data)
    # 这里是抓原因
    position,data = find_man_position(index_sex,data)
    #这里是合并数据
    temp = people_in(name, sex, position)
    #print(data)
    return temp, data
    #print(name, sex, reason, position)
    #print(data)

def find_all_man_in(data):
    all_people=[]
    while "先生" in data or "女士" in data:
        temp, data = find_man_in(data)
        all_people.append(temp)
    return all_people, data
'''
line=['根据', '董事会', '提名', '委员会', '的', '建议', '，', '经', '董事会', '审议', '，', '决定', '聘任', '徐刚', '先生', '为', '公司总裁', '，', '任期', '同', '第七届', '董事会', '；', '并', '同时', '解聘', '其', '公司', '高级副总裁', '职务']
temp, data= find_man_in(line)
print(temp.position,temp.name,temp.sex)
print(data)
'''
