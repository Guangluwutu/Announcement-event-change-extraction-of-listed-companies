import Jieba_deal
import Find_retire_people
import Find_success_people
import Wash_people
def get_retire_people(line):
    jieba_line = Jieba_deal.jieba_deal(line)
    print(jieba_line)
    people, find_line = Find_retire_people.find_man_out(jieba_line)
    #print(people.sex + " " + people.name + " " + people.position + " " + people.reason)

def get_success_people(line):
    jieba_line = Jieba_deal.jieba_deal(line)
    print(jieba_line)
    poeple, finde_line = Find_success_people.find_man_in(jieba_line)
    #print(poeple.sex + " " + poeple.name + " " + poeple.position)

def get_all_retire_people(line):
    jieba_line = Jieba_deal.jieba_deal(line)
    #print(jieba_line)
    people, find_line = Find_retire_people.find_all_man_out(jieba_line)
    #wash_people = Wash_people.wash_retire_people(people)
    return people

def get_all_success_people(line):
    jieba_line = Jieba_deal.jieba_deal(line)
    #print(jieba_line)
    people, find_line = Find_success_people.find_all_man_in(jieba_line)
    #wash_people = Wash_people.wash_success_people(people)
    return people