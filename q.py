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



'''
    Legenda para o mapa:
    
    Casas verdes: estado inicial e objetivo
    Casas azuis: Casa percorrida
    Casas vermelhas: Casas inválidas definidas para o problema
    Casas pretas: Casa não percorrida

    Letra amarela: Quantidade de vezes que foi percorrida
    
    
'''
def print_map(caminho_percorrido):
    #@TODO: REFATORAR
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
            if(i <10):
                valor_corrigido = "0" + str(i)
            else:
                valor_corrigido = str(i) 

            if("s"+str(i) in objetivo):
                
                l += Back.GREEN + "|" +  valor_corrigido +"|" + Style.RESET_ALL
            elif ("s"+str(i) in invalidas):
                if("s"+str(i) in caminho_percorrido):
                    total_vezes_percorrido = caminho_percorrido.count("s"+str(i))
                    if(total_vezes_percorrido<10):
                        total_vezes_percorrido = "0" + str(total_vezes_percorrido)
                    else:
                        total_vezes_percorrido = str(total_vezes_percorrido)
                    l +=  Back.MAGENTA + "|" + Fore.YELLOW + total_vezes_percorrido + Fore.WHITE + "|"+ Style.RESET_ALL    
                else:
                    l +=  Back.RED + "|" + valor_corrigido + "|"+ Style.RESET_ALL
            elif("s"+str(i) in caminho_percorrido):
                total_vezes_percorrido = caminho_percorrido.count("s"+str(i))
                if(i==1):
                    background_color = Back.GREEN
                else:
                    background_color = Back.BLUE
                if(total_vezes_percorrido<10):
                    total_vezes_percorrido = "0" + str(total_vezes_percorrido)
                else:
                    total_vezes_percorrido = str(total_vezes_percorrido)
                l +=  background_color + "|" + Fore.YELLOW + total_vezes_percorrido + Fore.WHITE + "|"+ Style.RESET_ALL
            else:
                l +=  Fore.WHITE + "|" + valor_corrigido + "|"+ Style.RESET_ALL
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
DEBUG =True
gama = 0.5
# if DEBUG:
#     print_map()
# else:
# episodio = input("Digite quantos episodios deseja executar:")
episodio = 10



# for i in range(0, episodio):
with open('mapa_inicial.recompensas_certas.json') as json_file:
    # Le o mapa resetado

    q = json.load(json_file)


    #@TODO: Adicionar o FOR para executar até a convergência ou FIM
    #@TODO: DESCOBRIR QUAL A FUNÇÃO CONVERGÊNCIA


    #Escolhe sempre a primeira posição para iniciar
    # 1
    conjunto_q = dict(q.items())

    #@TODO: Alterar este nome 'episodio' pois nao condiz com a semantica do problema
    for i in range(0, episodio):
        estado, escolha = 's1', q.get('s1')
        teste = 1
        caminho_percorrido = list()
        sequencia_selecoes = list()
        # print("estado i " + estado)
        
        while(estado):

            # @TODO: Transformar esta parte em uma função fábrica

            
            
            caminho_percorrido.append(estado)
            
            # 2.2.1 (Escolha do Alfa)
            if random.randint(0,100) < 70 and not(todos_menos_um(escolha)):
            # if not(todos_menos_um(escolha)):
                sequencia_selecoes.append("Seleciona max")
                acao_retornada = retorna_maximo_dicionario(escolha) #@TODO: SE N ENCONTRAR MAX, RETORNAR O MELHOR
            else:
                sequencia_selecoes.append("Seleciona aleatório")
                acao_retornada = retorna_valor_aleatorio_dicionario(escolha)
            
            recompensa_retornada = recompensa_para_acao(acao_retornada)

            
            estado_retornado = retorna_estado_para_acao(acao_retornada)
            if(estado_retornado in objetivo):
                soma = recompensa_retornada
                # print(estado_retornado)
                # print("Estado retorno")
            else:
            # print("estado retornado " + estado_retornado)
                qmax = recompensa_para_acao(retorna_maximo_dicionario(conjunto_q[estado_retornado]))
                soma = recompensa_retornada + gama * qmax
            if(soma>50):
                print("Estado anterior: ", estado)
                print("Estado: ", estado_retornado)
                print("Acoes: ", acao_retornada)
                print("Escolha: ", escolha)
                print("Soma maluca: ", soma)
                print("Recompensa retornada: ", recompensa_retornada)
                print("Recompensa máxima: ", qmax)
                print("Gama: ", gama)
                input()
            
            
            # print("Conjunto", estado, conjunto_q[estado])
            # input()
            # break
            # FAZENDO O UPDATE
            
            conjunto_q[estado][acao_retornada[0]][estado_retornado]['r'] = soma
            
            # if(recompensa_retornada==100):
            #     print(json.dumps(conjunto_q, indent=4, sort_keys=True))
            #     input()
            teste+=1
            # break
            # if(objetivo[estado_retornado]):
            #     break # Encontrou o 50, entao, comeca novamente
            # Encontrou o OBJETIVO
            if(estado_retornado in objetivo):
                break
            estado = estado_retornado
            escolha = conjunto_q[estado]

            
        if(DEBUG):
            if(i%100==0):
                print("Execucao ", i)
                print("Execucao ate o caminho", teste)

                # Para observar o comportamento
                if(teste>100):
                    
                    print(caminho_percorrido)
                    input()
                    print(sequencia_selecoes)
                    input()
                    # Pretty print do JSON!
                    print(json.dumps(conjunto_q, indent=4, sort_keys=True))
                    input()
                print("Total percorrido: ", len(caminho_percorrido))
                print_map(caminho_percorrido)
                input()
                
        # print("Caminho: ", caminho_percorrido)

        
        # print(conjunto_q)
        # input()
            
        
    
