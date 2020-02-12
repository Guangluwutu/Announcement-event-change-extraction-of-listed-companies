# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:25:32 2019

@author: Xu Ying
"""
import json


def strtojson(head_block,person_block):
    data=''
    data= data +'{"' + head_block.split('.')[0] + '": {"证券代码": "' + head_block.split('-')[0] + '", "证券简称": "' + head_block.split('-')[1] + '", "人事变动": ['
    for i in range(len(person_block)) :
        data= data +'{' +'"离职高管姓名": "' + person_block[i][0] + '",' + '"离职高管性别": "' + person_block[i][1] + '",' + '"离职高管职务": "' + person_block[i][2] + '",' + '"离职原因": "' + person_block[i][3] + '",' + '"继任者姓名": ' + 'null' + ',' + '"继任者性别": "' + person_block[i][5] + '",' + '"继任者职务": "' + person_block[i][6] + '"},'

    data=data[:-1]+']}}'
    dic = json.loads(data)
    js = json.dumps(dic, indent=4, separators=(',', ': '), ensure_ascii=False)
    return js


if __name__ == '__main__':
    person_block = [['崔捷', '先生', '副总经理、财务总监、董事会秘书', '工作调动原因', '', '', ''], ['', '', '', '', '', '', '']]
    head_block = '000031-中粮地产-关于公司副总经理、财务总监、董事会秘书辞职的公告'
    print(person_block)
    print(head_block)

    js=strtojson(head_block, person_block)
    print(js)    
