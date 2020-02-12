import os
import Find_sentence
import Find_title
import Get_poeple
import Wash_people
import Find_success_people
import Find_retire_people
import save_js
def read_file(readpath):
    re_people=[]
    su_people=[]
    for parent, dirnames, filenames in os.walk(readpath):
        for filename in filenames:
            f = open(readpath + filename, 'r', encoding="utf-8")
            mark_note = filename[:-4]
            mark_code, mark_sname=Find_title.find_title(mark_note)
            data = f.read().replace(" ", "").replace("\n", "").replace("\t", "").replace("；","").split("。")
            #data = str(data).split("；")
            #print(mark_note, mark_code, mark_sname)
            #print(mark_note+" "+mark_code+" "+mark_sname+" ")
            for i in range(1, len(data)):
                if "感谢" in data[i] or "是否" in data[i] or "尽责" in data[i] or "不得担任" in data[i] or "代为" in data[i] or "生效" in data[i] or "保证" in data[i]:
                    i += 1
                else:
                    line1 = Find_sentence.find_retire(data[i])
                    if line1 != "" :
                        temp_people1=Get_poeple.get_all_retire_people(line1)
                        #Get_poeple.get_all_retire_people(line1)
                        re_people +=temp_people1

                    line2 = Find_sentence.find_employ(data[i])
                    if line2 != "" :
                        if "任何" in line2:
                            i +=1
                            continue
                        temp_people2=Get_poeple.get_all_success_people(line2)
                        #Get_poeple.get_all_success_people(line2)
                        su_people +=temp_people2
            if re_people ==[] and su_people ==[]:
                re_people.append(Find_retire_people.people_out("","","",""))
                su_people.append(Find_success_people.people_in("","",""))

            save_js.strtojson(mark_note,mark_code, mark_sname,Wash_people.wash_retire_people(re_people),Wash_people.wash_success_people(su_people))
            re_people = []
            su_people = []
            f.close()


    #return mark_note,mark_code, mark_sname,Wash_people.wash_retire_people(re_people),Wash_people.wash_success_people(su_people)

