import Get_poeple
import Find_retire_people
import Find_success_people
def wash_retire_people(people):
    people_all_name=[]
    all_people=[]
    for i in range(len(people)):
        if people[i].name !="" :
            if people[i].name not in people_all_name:
                if people[i].position !="" and people[i].reason == "" and all_people != []:
                    people[i].reason=all_people[-1].reason
                    people_all_name.append(people[i].name)
                    all_people.append(people[i])
                if people[i].position != "" and people[i].reason != "":
                    people_all_name.append(people[i].name)
                    all_people.append(people[i])
        elif people[i].position !="" and all_people !=[]:
            all_people[-1].position +="、"+people[i].position
    for i  in all_people:
        print(i.sex + " " + i.name + " " + i.position + " " + i.reason)
    return all_people
    #for i  in all_people:
        #print(i.sex + " " + i.name + " " + i.position + " " + i.reason)



def wash_success_people(people):
    people_all_name=[]
    all_people=[]
    for i in range(len(people)):
        if people[i].name !="" :
            if people[i].name not in people_all_name:
                if people[i].position !="":
                    people_all_name.append(people[i].name)
                    all_people.append(people[i])
            elif people[i].position !="" and all_people is not None:
                    if all_people[-1].position !=people[i].position:
                        all_people[-1].position +="、"+people[i].position
    for i  in all_people:
        print(i.sex + " " + i.name + " " + i.position)
    return all_people

