import Read_file
import json

def strtojson(note,code,sname,retire_person,success_person):
    data=''
    data += '{"' + note + '": {"证券代码": "' + code + '", "证券简称": "' + sname + '", "人事变动": ['
    for i in range(len(retire_person)) :
        data += '{' +'"离职高管姓名": "' + retire_person[i].name + '",' + '"离职高管性别": "' + retire_person[i].sex + '",' + '"离职高管职务": "' + retire_person[i].position + '",' + '"离职原因": "' + retire_person[i].reason + '",' + '"继任者姓名": '+'""' + ',' + '"继任者性别":'+'""'+',' + '"继任者职务": ' + '""' + '},'
    for j in range(len(success_person)):
        data += '{' +'"离职高管姓名": ' + '""' + ',' + '"离职高管性别": ' + '""' + ',' + '"离职高管职务": ' + '""' + ',' + '"离职原因": ' + '""' + ',' + '"继任者姓名": "'+success_person[j].name + '",' + '"继任者性别":"'+success_person[j].sex+'",' + '"继任者职务": "' + success_person[j].position + '"},'

    data=data[:-1]+']}}'
    dic = json.loads(data)

    with open("./Data_save/"+ note +'.json', 'w',encoding= "utf-8") as f2:
        json.dumps(dic,f2)
    #js = json.dumps(dic, indent=4, separators=(',', ': '), ensure_ascii=False)
    #f2.close()
    #return js