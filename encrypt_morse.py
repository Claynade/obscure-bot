def emorse(str1):
    global str2
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
    str3=str1.upper()
    for i in str3:
        if i in dict1:
            str2+=dict1[i]
            str2+=' '
        else:
            str2+=i
    return str2
if __name__=="__main__":
    print(emorse(input()))
