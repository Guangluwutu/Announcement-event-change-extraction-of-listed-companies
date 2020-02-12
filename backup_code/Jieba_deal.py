import jieba
def jieba_deal(data):
    jieba.load_userdict("./name.txt")
   # jieba.load_userdict("./reason.txt")
    #jieba.load_userdict("./position_in.txt")
    #jieba.load_userdict("./position_out.txt")
    word_list = jieba.cut(data, cut_all=False)
    li=[i for i in word_list]
    return li
#line="殷必彤先生因工作变动原因，辞去公司总经理、董事职务，同时辞去董事会战略委员会委员职务"
#print(jieba_deal(line))