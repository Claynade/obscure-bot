def dmorse(str1):
    str2=''
    dict1={'A':".-",
           'B':"-...",
           "C":"-.-.",
           "D":"-..",
           "E":".",
           "F":"..-.",
           "G":"--.",
           "H":"....",
           "I":"..",
           "J":".---",
           "K":"-.-",
           "L":".-..",
           "M":"--",
           "N":"-.",
           "O":"---",
           "P":".--.",
           "Q":"--.-",
           "R":".-.",
           "S":"...",
           "T":"-",
           "U":"..-",
           "V":"...-",
           "W":".--",
           "X":"-..-",
           "Y":"-.--",
           'Z':'--..'}
    key_list = list(dict1.keys())
    val_list = list(dict1.values())
    list1=str1.split(' ')
    print(list1)
    for i in list1:
        if i in val_list:
            position = val_list.index(i)
            str3=key_list[position]
            str2+=str3
        elif i=='':
            str2+=' '
        else:
            str2+=i
    return str2
    
            
if __name__=="__main__":
    print(dmorse(input()))
