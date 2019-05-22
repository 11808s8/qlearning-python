import json
from colorama import Fore, Back, Style, init
init()

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


