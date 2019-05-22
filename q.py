import json
from colorama import Fore, Back, Style, init
init()



objetivo = {
    "s50":100
}
invalidas ={
"s7":-100,
"s14":-100,
"s10":-100,
"s11":-100,
"s20":-100,
"s19":-100,
"s24":-100,
"s21":-100,
"s30":-100,
"s27":-100,
"s31":-100,
"s40":-100,
"s39":-100,
"s37":-100,
"s41":-100
}


color_map = [i for i in range(1,51)]


def print_map():
    j=0
    line = ""
    reverse = False
    pedacitos = [list(reversed(color_map[i:i+5])) if (i+5)%2==0 else color_map[i:i+5] for i in range(0, len(color_map), 5)]
    pedacitos_correta = list(reversed([[pedacitos[j][i] for j in range(len(pedacitos))] for i in range(len(pedacitos[0]))]))
    
    for linha in pedacitos_correta:
        l = ""
        for i in linha:
            if i == 1 or ("s"+str(i) in objetivo):
                l += Back.GREEN + "|" +  str(i) +"|" + Style.RESET_ALL
            elif ("s"+str(i) in invalidas):
                l +=  Fore.WHITE + "|" + str(i) + "|"+ Style.RESET_ALL
            else:
                l += Back.BLUE + "|" + str(i) + "|"+ Style.RESET_ALL
        print(l)



invalid = {}
batata =True
if batata:
    print_map()
else:
    with open('mapa_inicial.recompensas_zeradas.json') as json_file:
        q = json.load(json_file)
        for key,value in q.items():
            print(key)
            for key1, value1 in value.items():
                if(value1):
                    for key2,value2 in value1.items():
                        if(key2 in objetivo):
                            value1.update({key2:objetivo[key2]})
                            # value.update(value1)
                            # q.update(value)
                            # print(key2,value2)
        print("pos")
        for key,value in q.items():
            
            for key1, value1 in value.items():
                if value1:
                    for key2, value2 in value1.items():
                        if key2 in objetivo:
                            print(key)
        # print(q["s"+str(49)])
        # print_map()
        # for key,value in q.items():
        #     # print(key,value)
        #     print(key)
            # for key2, value2 in value.items():
            #     print(key2, value2)
