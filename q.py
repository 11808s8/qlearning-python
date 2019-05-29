import json
import random
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
    #monta a lista a ser exibida, em ordem 1 ... 5
    #                                      10 ... 6
    pedacitos = [list(reversed(color_map[i:i+5])) if (i+5)%2==0 else color_map[i:i+5] for i in range(0, len(color_map), 5)]
    
    #ordena a lista de linha por coluna para a exibição
    pedacitos_correta = list(reversed([[pedacitos[j][i] for j in range(len(pedacitos))] for i in range(len(pedacitos[0]))]))
    
    # exibe
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


# Método que SEMPRE retorna um caminho possível (desconsidera os com NONE)
def retorna_valor_aleatorio_dicionario(dicionario):
    acao_retorno = random.choice(list(dicionario.items()))
    while(acao_retorno[1] == None):
        acao_retorno = random.choice(list(dicionario.items()))
    return acao_retorno


def retorna_maximo_dicionario(dicionario):
    
    maximo = acao_retorno = None
    for value in list(dicionario.items()):
        
        if(value[1]):
            estado = value[1]
            acao = list(estado.values())[0]

            #recompensa
            recompensa = acao['r']
            if(maximo==None or maximo<recompensa):
                acao_retorno, maximo = value,recompensa
    return  acao_retorno

def recompensa_para_acao(acao):
    recompensa_acao = list(list(acao)[1].values())[0]['r']
    return recompensa_acao

def retorna_estado_para_acao(acao):
    estado_acao = [*list(acao)[1]][0]
    return estado_acao

def todos_menos_um(dicionario):

    for value in list(dicionario.items()):

        # Considera só os estados que pode mover
        if(value[1]):

            #pega o estado
            estado = value[1]

            #pega a acao 
            acao = list(estado.values())[0]

            #recompensa
            recompensa = acao['r']

            #se for diferente...
            if(recompensa!=-1 and recompensa!=None):
                return False

    return True

invalid = {}
batata =False
epsilon = 0.5
if batata:
    print_map()
else:
    # episodio = input("Digite quantos episodios deseja executar:")
    episodio = 1
    for i in range(0, episodio):
        
        # Le o mapa resetado
        with open('mapa_inicial.recompensas_zeradas.json') as json_file:
            q = json.load(json_file)


            #@TODO: Adicionar o FOR para executar até a convergência ou FIM

            #Escolhe sempre a primeira posição para iniciar
            # 1
            conjunto_q = dict(q.items())
            estado, escolha = list(q.items())[0]
            # print(estado, escolha)

            # print()


            # @TODO: Transformar esta parte em uma função fábrica

            
            # 2.2.1 (Escolha do Alfa)
            if random.randint(0,100) < 70 and not(todos_menos_um(escolha)):
            # if not(todos_menos_um(escolha)):
            # if not(todos_menos_um(escolha)):
                acao_retornada = retorna_maximo_dicionario(escolha) #@TODO: SE N ENCONTRAR MAX, RETORNAR O MELHOR
            else:
                acao_retornada = retorna_valor_aleatorio_dicionario(escolha)
            
            recompensa_retornada = recompensa_para_acao(acao_retornada)

            
            estado_retornado = retorna_estado_para_acao(acao_retornada)
            print(estado_retornado)
            qmax = recompensa_para_acao(retorna_maximo_dicionario(conjunto_q[estado_retornado]))
            soma = recompensa_retornada + epsilon * qmax
            

            # FAZENDO O UPDATE
            for key,value in q.items():
                # print(key)
                if(key==estado):
                    print(conjunto_q[estado][acao_retornada[0]][estado_retornado]['r'])
                    print(conjunto_q[estado])
                    conjunto_q[estado][acao_retornada[0]][estado_retornado]['r'] = soma

                    print(conjunto_q[estado][acao_retornada[0]][estado_retornado]['r'])
                    print(conjunto_q[estado])
                    print(key)
                        
            print(soma)
            break
            # AQUI ELE ESCOLHE O MELHOR FILHO 70% das vezes ou 30% aleatório
            # se todos -1, escolhe aleatório
            # estado, escolha_arbitraria = random.choice(list(q.items()))
            
            # print(estado)
            # print(escolha_arbitraria)
            # break
            
            # estado = escolha_arbitraria[0]
            
            # print(escolha_arbitraria)
            # 2
            # for k in q.values()[estado]:

            # print(dict(escolha_arbitraria))

            # escolhe para qual ALFA vai
            alfa = random.choice(list(escolha_arbitraria))
            # retorna_se_todos_menos_um(list
            # Melhoria pedida pela prof
            
            # print(alfa)
            # print(escolha_arbitraria)

            # para selecionar qual estado acessar
            # print([*escolha_arbitraria[alfa]])
            
            # break

            if escolha_arbitraria[alfa]:
                sLinha = [*escolha_arbitraria[alfa]] # pega a chave do dicionario (sLinha)
                # for recompensa in escolha_arbitraria[alfa].values():
                    
                #     r = recompensa['r']
                    # print(r)
                # print(sLinha[0])
                
                print(sLinha[0])
                print(conjunto_q[sLinha[0]])
                print('teste', retorna_valor_aleatorio_dicionario(conjunto_q[sLinha[0]]))
                break
                
                # soma = r + epsilon*
            
            # print("pos")
            # for key,value in q.items():
                
            #     for key1, value1 in value.items():
            #         if value1:
            #             for key2, value2 in value1.items():
            #                 if key2 in objetivo:
            #                     print(key)
            # print(q["s"+str(49)])
            # print_map()
            # for key,value in q.items():
            #     # print(key,value)
            #     print(key)
                # for key2, value2 in value.items():
                #     print(key2, value2)

