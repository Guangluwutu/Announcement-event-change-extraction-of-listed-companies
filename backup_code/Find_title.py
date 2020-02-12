import Jieba_deal

def find_title(data):
    # mark_code, mark_sname = get_head(data[0])
    mark_code = ""
    mark_sname = ""
    mark_title = Jieba_deal.jieba_deal(data)
    mark_code = mark_title[0]
    for mark_i in range(2, len(mark_title)):
        if mark_title[mark_i] == "-":
            break
        else:
            mark_sname += mark_title[mark_i]
    return mark_code,mark_sname