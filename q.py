import json
import random
from colorama import Fore, Back, Style, init
from copy import copy, deepcopy
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

def monta_mapa_cores():
    pedacitos = [list(reversed(color_map[i:i+5])) if (i+5)%2==0 else color_map[i:i+5] for i in range(0, len(color_map), 5)]
    #ordena a lista de linha por coluna para a exibição
    pedacitos_correta = list(reversed([[pedacitos[j][i] for j in range(len(pedacitos))] for i in range(len(pedacitos[0]))]))

    return pedacitos, pedacitos_correta

def print_map(caminho_percorrido, recompensas = None):
    def corrige_valor(valor):
            if(i <10):
                valor_corrigido = "0" + str(valor)
            else:
                valor_corrigido = str(valor) 
            return valor_corrigido
    #@TODO: REFATORAR
    j=0
    line = ""
    reverse = False
    #monta a lista a ser exibida, em ordem 1 ... 5
    #                                      10 ... 6
    
    pedacitos, pedacitos_correta = monta_mapa_cores()
    # exibe
    for linha in pedacitos_correta:
        l = ""
        for i in linha:
            
            valor_corrigido = corrige_valor(i)
            valor_print = valor_corrigido

            if(recompensas==None):
                total_vezes_percorrido = caminho_percorrido.count("s"+str(i))
                if(total_vezes_percorrido<10):
                    total_vezes_percorrido = "0" + str(total_vezes_percorrido)
                else:
                    total_vezes_percorrido = str(total_vezes_percorrido)
                valor_print = total_vezes_percorrido
            else:
                if("s"+str(i) in caminho_percorrido):
                    valor_print = str(round(recompensas['s'+str(i)],9))
                else:
                    valor_print = "s"+str(i)

            if("s"+str(i) in objetivo):
                
                l += Back.GREEN + "|" +  valor_corrigido +"|" + Style.RESET_ALL
            elif ("s"+str(i) in invalidas):

                if("s"+str(i) in caminho_percorrido):
                    l +=  Back.MAGENTA + "|" + Fore.YELLOW + valor_print + Fore.WHITE + "|"+ Style.RESET_ALL    
                else:
                    l +=  Back.RED + "|" + valor_corrigido + "|"+ Style.RESET_ALL

            elif("s"+str(i) in caminho_percorrido):
                    
                if(i==1):
                    background_color = Back.GREEN
                else:
                    background_color = Back.BLUE

                
                l +=  background_color + "|" + Fore.YELLOW + valor_print + Fore.WHITE + "|"+ Style.RESET_ALL
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


def exibe_matriz_q_formatada(q):
    qLinha = list(q)
    for estado in q:
        acoes = list(q[estado])
        stringAcoes = ''
        for acao in acoes:
            if(q[estado][acao]):
                stringAcoes +=' ' + acao
                for estadoAcao in q[estado][acao]:
                    # if(str(q[estado][acao][estadoAcao]['r']).count()<4):

                    stringAcoes += ': ' + estadoAcao + ' -> ' + str(q[estado][acao][estadoAcao]['r'])
                    # print(q[estado][acao])
            else:
                stringAcoes +=' ' + acao + ': Parede     '
        # input()
        print('Q(' + estado + ') : ', stringAcoes)
        # input()
        # print(estado,q[estado])
    input()


'''
    Função que compara cada ação do estado q com o estado qClone para verificar
    se convergiu (não houveram mudanças) ou não
'''
def convergiu_simples(q, qClone):
    ret = q is qClone
    for estado in q:
        for acao in q[estado]:
            if(q[estado][acao]):
                for estado_recompensa in q[estado][acao]:
                    if(q[estado][acao][estado_recompensa]['r'] != qClone[estado][acao][estado_recompensa]['r']):
                        return False
    return True
                    

def monta_lista_otima(q):
    print("Monta lista ótima")
    lista_otima = list()
    maximo = None
    
    estado = 's1'
    
    while(estado!='s50'):
        # print(estado)
        maximo = retorna_maximo_dicionario(q[estado])
        estado_acao = list(maximo[1].keys())[0]
        recompensa_estado_acao = list(maximo[1].values())[0].values()
        recompensa_estado_acao = list(recompensa_estado_acao)[0]
        acao = maximo[0]
        passo = estado_acao

        # maximo[0] == acao
        # maximo[1] == { estado, recompensa acao para aquele estado }
        lista_otima.append([acao,estado_acao, recompensa_estado_acao])
        estado = estado_acao
    # print(" LISTA OTIMA ")
    # exibe_lista_linha_por_linha(lista_otima)
    # input()
    return lista_otima

def extrai_estado_lista_otima(lista_otima):
    nova_lista = list()
    for linha in lista_otima:
        nova_lista.append(linha[1])
    return nova_lista

def extrai_estado_recompensa_lista_otima(lista_otima):
    nova_lista = list()
    lista_estado = list()
    lista_recompensa = list()

    for linha in lista_otima:
        lista_estado.append(linha[1]) 
        lista_recompensa.append(linha[2])

    nova_lista = dict(zip(lista_estado,lista_recompensa))
    return nova_lista

def exibe_lista_linha_por_linha(lista):
    for linha in lista:
        print(linha)

invalid = {}
DEBUG =False
gama = 0.000001
# if DEBUG:
#     print_map()
# else:
# episodio = input("Digite quantos episodios deseja executar:")
episodio = 1000


# 1
with open('mapa_inicial.recompensas_certas.json') as json_file:
    with open('mapa_inicial.recompensas_zeradas.json') as json_file_q_table:
        # Le o mapa resetado

        arquivo_recompensas_ambiente = json.load(json_file)
        arquivo = json.load(json_file_q_table)
        convergiu_n_vezes = 0

        #@TODO: Adicionar o FOR para executar até a convergência ou FIM
        #@TODO: DESCOBRIR QUAL A FUNÇÃO CONVERGÊNCIA

        
        for passo in range(0, episodio):

            # 2.1 - Inicializações 
            conjunto_q = dict(arquivo.items())
            conjunto_q_convergencia = None
            recompensas_ambiente = dict(arquivo_recompensas_ambiente.items())
            caminho_otimo = list()
            #Escolhe sempre a primeira posição para iniciar
            estado, escolha = 's1', arquivo.get('s1')
            teste = 1
            caminho_percorrido = list()
            sequencia_selecoes = list()
            
            # 2.2 - Repetição para cada passo do episódio até o ESTADO ser terminal
            while(estado):

                # @TODO: Transformar esta parte em uma função fábrica

                
                
                caminho_percorrido.append(estado)
                
                # 2.2.1 (Escolha do Alfa)
                if random.randint(0,100) < 70 and not(todos_menos_um(escolha)):
                    sequencia_selecoes.append("Seleciona max")
                    acao_retornada = retorna_maximo_dicionario(escolha) #@TODO: SE N ENCONTRAR MAX, RETORNAR O MELHOR
                    recompensa_ambiente_limpar = (acao_retornada[0], recompensas_ambiente[estado][acao_retornada[0]])
                else:
                    sequencia_selecoes.append("Seleciona aleatório")
                    acao_retornada = retorna_valor_aleatorio_dicionario(escolha)
                    recompensa_ambiente_limpar = (acao_retornada[0], recompensas_ambiente[estado][acao_retornada[0]])
                

                # 2.2.3
                recompensa_ambiente = recompensa_para_acao(recompensa_ambiente_limpar)
                estado_retornado = retorna_estado_para_acao(acao_retornada)

                # 2.2.4
                if(estado_retornado in objetivo):
                    soma = objetivo[estado_retornado]
                else:
                    qmax = recompensa_para_acao(retorna_maximo_dicionario(conjunto_q[estado_retornado]))
                    soma = recompensa_ambiente + gama * qmax

                # 2.2.5
                conjunto_q[estado][acao_retornada[0]][estado_retornado]['r'] = soma
                
                teste+=1
                
                # Encontrou o 50, entao, comeca novamente
                # Encontrou o OBJETIVO
                if(estado_retornado in objetivo):
                    break
                estado = estado_retornado
                escolha = conjunto_q[estado]

                
            if(DEBUG):
                if(passo%100==0):
                    print("Execucao ", passo)
                    print("Execucao ate o caminho", teste)

                    # Para observar o comportamento
                    # if(teste>100):
                    
                    print(caminho_percorrido)
                    input()
                    # print(sequencia_selecoes)
                    # input()
                    # Pretty print do JSON!
                    # print(json.dumps(conjunto_q, indent=4, sort_keys=True))
                    exibe_matriz_q_formatada(conjunto_q)
                    input()
                    print("Total percorrido: ", len(caminho_percorrido))
                    print_map(caminho_percorrido)
                    input()

            # @TODO: Modificar a convergência para lidar com
            if(conjunto_q_convergencia == None):
                conjunto_q_convergencia = deepcopy(conjunto_q)
            elif(not(convergiu_simples(conjunto_q,conjunto_q_convergencia))):
                conjunto_q_convergencia = deepcopy(conjunto_q)
            else:
                convergiu_n_vezes +=1
                if(convergiu_n_vezes==100):
                    print("CONVERGIU!")
                    print("Execucao ", passo)
                    print("Execucao ate o caminho", teste)
                    input()
                    print_map(caminho_percorrido)
                    exibe_matriz_q_formatada(conjunto_q)
                    # break

            # print("Caminho: ", caminho_percorrido)
            # @TODO: FINALIZAR A IMPLEMENTAÇÃO DA LISTA ÓTIMA
            if(passo>10 and passo%1000==0):
                caminho_otimo = monta_lista_otima(conjunto_q)         
                lista_recompensa_caminho_otimo = extrai_estado_recompensa_lista_otima(caminho_otimo)            
                lista_estados_caminho_otimo = extrai_estado_lista_otima(caminho_otimo)
                print_map(lista_estados_caminho_otimo,lista_recompensa_caminho_otimo)
            print("p")
            # if(passo%25==0):
            #     input()
            # print(conjunto_q)
            # input()
                
            
        
