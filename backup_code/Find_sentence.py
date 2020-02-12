
import re
def find_retire(line):
    if re.search("[因由根].*[，原].*辞去.*[职]",line) is not None:
        #print(line)
        return line
    else:
        return ""

def find_employ(line):
    if re.search("([同提推选聘任].*[担为])", line) is not None:
        #print(line)
        return line
    else:
        return ""