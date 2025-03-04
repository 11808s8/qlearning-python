import json
import random
from colorama import Fore, Back, Style, init
from copy import copy, deepcopy
import matplotlib.pyplot as plt
import time
import numpy as np

# Comando necessário para a biblioteca colorama
init()

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

def print_map(caminho_percorrido, valores_acao = None):
    def corrige_valor(valor):
            if(i <10):
                valor_corrigido = "0" + str(valor)
            else:
                valor_corrigido = str(valor) 
            return valor_corrigido
    
    j=0
    line = ""
    reverse = False
    #monta a lista a ser exibida, em ordem 1 ... 5
    #                                      10 ... 6
    
    pedacitos, pedacitos_correta = monta_mapa_cores()
    
    # itera sobre a lista
    for linha in pedacitos_correta:
        l = ""
        for i in linha:
            
            valor_corrigido = corrige_valor(i)
            valor_print = valor_corrigido

            # Se não há uma lista com os valores, simplesmente
            # monta o mapa com o total de vezes que o algoritmo 
            # passou por uma casa
            if(valores_acao==None):
                total_vezes_percorrido = caminho_percorrido.count("s"+str(i))
                if(total_vezes_percorrido<10):
                    total_vezes_percorrido = "0" + str(total_vezes_percorrido)
                else:
                    total_vezes_percorrido = str(total_vezes_percorrido)
                valor_print = total_vezes_percorrido
            
            # Caso contrário, exibe o valor da ação do estado anterior para o próximo
            else:
                if("s"+str(i) in caminho_percorrido):
                    valor_print = str(round(valores_acao['s'+str(i)],9))
                else:
                    valor_print = "s"+str(i)

            # Se é um valor do objetivo, recebe a cor verde
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

'''
    Função que SEMPRE retorna uma ação possível ALEATÓRIA (desconsidera os com NONE)
'''
def retorna_valor_aleatorio_dicionario(dicionario):
    acao_retorno = random.choice(list(dicionario.items()))
    while(acao_retorno[1] == None):
        acao_retorno = random.choice(list(dicionario.items()))
    return acao_retorno

'''
    Função simples que retorna a ação de maior valor de recompensa
    dentro de um dicionário
'''
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

'''
    Função que retorna um valor máximo que não
    esteja na lista passada como segundo parâmetro
'''
def retorna_maximo_dicionario_nao_esta_na_lista(dicionario,lista_estados_nao_pode_ser):
    
    maximo = acao_retorno = None
    for value in list(dicionario.items()):
        if(value[1]):
            estado = value[1]
            if(list(estado.items())[0][0] not in lista_estados_nao_pode_ser):
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

'''
    Função que verifica se todos os valores na lista
    são -1
'''
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


'''
    Função que exibe no terminal uma versão formatada do conjunto Q
'''
def exibe_matriz_q_formatada(q):
    qLinha = sorted(q) # Ordena qualquer iterável ! :-)
    for estado in qLinha:
        acoes = list(q[estado])
        stringAcoes = ''
        for acao in acoes:
            if(q[estado][acao]):
                stringAcoes +=' ' + acao
                for estadoAcao in q[estado][acao]:
                    stringAcoes += ': ' + estadoAcao + ' -> ' + '{:9.2f}'.format(q[estado][acao][estadoAcao]['r'])
                    
            else:
                stringAcoes +=' ' + acao + ': Parede          '
        
        print('Q(' + estado + ') : ', stringAcoes)
        


'''
    Função que compara cada ação do estado q com o estado qClone para verificar
    se convergiu (não houveram mudanças) ou não
'''
def convergiu_simples(q, qClone):
    
    for estado in q:
        for acao in q[estado]:
            if(q[estado][acao]):
                for estado_recompensa in q[estado][acao]:
                    if(q[estado][acao][estado_recompensa]['r'] != qClone[estado][acao][estado_recompensa]['r']):
                        return False
    return True

'''
    Função que compara cada recompensa para um estado dentro de uma lista ótima com
    uma lista ótima anterior para verificar se convergiu (não houveram mudanças) ou não
'''
def convergiu_lista_otima(lista_otima, lista_otima_anterior):
    
    if(len(list(lista_otima))==len(list(lista_otima_anterior))):
        for estado in lista_otima:
            
            if(estado in lista_otima and estado in lista_otima_anterior):
                if(lista_otima[estado]!=lista_otima_anterior[estado]):
                    return False
            else:
                return False
        return True
    else:
        return False     

'''
    Função que monta a lista ótima de valores com base sempre em pegar o maior valor do conjunto q,
    retornando uma lista com os valores da lista ótima
'''
def monta_lista_otima(q):
    
    lista_otima = list()
    caminho_percorrido = list()
    maximo = None
    
    estado = 's1'
    caminho_percorrido.append(estado)
    while(estado!='s50'):
        
        maximo = retorna_maximo_dicionario_nao_esta_na_lista(q[estado],caminho_percorrido)
        if(maximo==None):
            return None
        estado_acao = list(maximo[1].keys())[0]
        recompensa_estado_acao = list(maximo[1].values())[0].values()
        recompensa_estado_acao = list(recompensa_estado_acao)[0]
        acao = maximo[0]
        passo = estado_acao

        # maximo[0] == acao
        # maximo[1] == { estado, recompensa acao para aquele estado }
        lista_otima.append([acao,estado_acao, recompensa_estado_acao])
        caminho_percorrido.append(estado_acao)
        estado = estado_acao
    return lista_otima

'''
    Função que extrai os estados de uma lista ótima, iterando sobre ela e retornando uma nova lista com estes estados
'''
def extrai_estado_lista_otima(lista_otima):
    nova_lista = list()
    for linha in lista_otima:
        nova_lista.append(linha[1])
    return nova_lista

'''
    Função que extrai as recompensas de uma lista ótima, iterando sobre ela e retornando uma nova lista com as recompensas das mesmas
    (Recompensas == valor de uma ação de um estado A para estado B)
'''
def extrai_estado_recompensa_lista_otima(lista_otima):
    nova_lista = list()
    lista_estado = list()
    lista_recompensa = list()

    for linha in lista_otima:
        lista_estado.append(linha[1]) 
        lista_recompensa.append(linha[2])

    nova_lista = dict(zip(lista_estado,lista_recompensa))
    return nova_lista

'''
    Função simples que exibe os valores de uma lista linha a linha
'''
def exibe_lista_linha_por_linha(lista):
    for linha in lista:
        print(linha)

# ------------------------------------------------------------ #

# Dicionário de qual o objetivo a ser alcançado e qual sua recompensa

objetivo = {
    "s50":100
}

# Dicionário de posições inválidas do mapa

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

# List comprehension para o mapa de cores, montando o array com os valores de 1 à 50
color_map = [i for i in range(1,51)]

# Valor para exibir informações de debugging
DEBUG =False

total_rodadas_cada_gama = list()

# -------------------------------
#Variáveis para testes
# Separar os gamas por virgula
tipos_de_gama = [0.1,0.2,0.8,0.9,0.95, 0.5 , 0.4, 0.3, 0.7, 0.6]
porcentagem_escolha_maiores = 70


# Define se o programa executará até o fim dos N episódios definidos, sem parar quando converge
roda_ate_o_fim = False

# Define o gráfico será gerado com base na quantidade de passos do episódio executados ou 
# na quantidade de execuções mesmo internas de quando está buscando o OBJETIVO
salvar_por_episodio = True
episodios = 5000
# Tipos aceitaveis de convergencia:
# lista_otima
# conjunto_q
# tipo_de_convergencia = 'conjunto_q'
tipo_de_convergencia = 'lista_otima'

# Gama para o cálculo de propagação de recompensas
gama = 0.5

# Variável que define quantas vezes uma lista ficou sem mudar para ser convergência
quando_converge = 100

# Variável que define partindo de quantas execuções a lista de caminho ótimo passará a ser buscada
quando_comeca_a_armazenar_lista_caminho_otimo = 5

# Variável que define se a matriz Q será exibida de N em N episódios da execução
# Com o valor -1, não exibirá a matriz Q
exibir_matriz_q_de_n_em_n_passos = -1

# -------------------------------


# 1
for teste in range(0,len(tipos_de_gama)):
    with open('mapa_inicial.recompensas_certas.json') as json_recompensas_ambiente:
        with open('mapa_inicial.recompensas_zeradas.json') as json_mapa_zerado:
        # Le o mapa resetado
        
            arquivo_recompensas_ambiente = json.load(json_recompensas_ambiente)
            arquivo = json.load(json_mapa_zerado)
            convergiu_n_vezes = 0

            caminho_otimo_convergencia = None
            convergiu_caminho = 0

            # Conjunto Q
            conjunto_q = dict(arquivo.items())

            # Conjunto Q para caso a convergência seja verificada por ele
            conjunto_q_convergencia = None
            rodou_n_vezes = 0
            for passo in range(0, episodios):
                
                # 2.1 - Inicializações 

                # Recompensas do Ambiente
                recompensas_ambiente = dict(arquivo_recompensas_ambiente.items())

                # Cainho Ótimo
                caminho_otimo = list()
                
                #Escolhe sempre a primeira posição para iniciar
                estado, escolha = 's1', arquivo.get('s1')
                caminho_percorrido = list()
                sequencia_selecoes = list()
                
                # 2.2 - Repetição para cada passo do episódio até o ESTADO ser terminal
                while(estado):
                    rodou_n_vezes += 1
                    # @TODO: Transformar esta parte em uma função fábrica
                    caminho_percorrido.append(estado)
                    
                    # 2.2.1 (Escolha do Alfa)
                    if random.randint(0,100) < porcentagem_escolha_maiores and not(todos_menos_um(escolha)):
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
                        soma = recompensa_ambiente + tipos_de_gama[teste] * qmax

                    # 2.2.5
                    conjunto_q[estado][acao_retornada[0]][estado_retornado]['r'] = soma
                    
                    
                    # Encontrou o 50, entao, comeca novamente
                    # Encontrou o OBJETIVO
                    if(estado_retornado in objetivo):
                        break
                    estado = estado_retornado
                    escolha = conjunto_q[estado]

                if(exibir_matriz_q_de_n_em_n_passos!=-1 and passo>1 and passo%exibir_matriz_q_de_n_em_n_passos==0):
                    print("Episodio numero: ", passo)
                    exibe_matriz_q_formatada(conjunto_q)
                    
                if(DEBUG==True):
                    if(passo%100==0):
                        print("Execucao ", passo)
                        
                        print(caminho_percorrido)
                        input()
                        exibe_matriz_q_formatada(conjunto_q)
                        input()
                        print("Total percorrido: ", len(caminho_percorrido))
                        print_map(caminho_percorrido)
                        input()

                if(tipo_de_convergencia=='conjunto_q'):

                    if(conjunto_q_convergencia == None):
                        conjunto_q_convergencia = deepcopy(conjunto_q)
                    elif(not(convergiu_simples(conjunto_q,conjunto_q_convergencia))):
                        conjunto_q_convergencia = deepcopy(conjunto_q)
                    else:
                        convergiu_n_vezes +=1
                    
                    if(convergiu_n_vezes == quando_converge):
                        print("Convergiu conjunto q!")
                        print('Tipo de gama {}'.format(tipos_de_gama[teste]))
                        exibe_matriz_q_formatada(conjunto_q)
                        print("\nRodou ", passo,"vezes")
                        input()
                        if(salvar_por_episodio):
                            total_rodadas_cada_gama.append(passo)    
                        else:
                            total_rodadas_cada_gama.append(rodou_n_vezes)
                        # print_map(conjunto_q_convergencia)
                        # input()
                        if(not(roda_ate_o_fim)):
                            break    

                elif(tipo_de_convergencia=='lista_otima'):
                    if(passo>5):
                    
                        caminho_otimo = monta_lista_otima(conjunto_q)         
                        # Retorna NONE quando não consegue encontrar o caminho pelos valores máximos sem repetir passos
                        if(caminho_otimo != None): 
                            lista_recompensa_caminho_otimo = extrai_estado_recompensa_lista_otima(caminho_otimo) 
                            
                            lista_estados_caminho_otimo = extrai_estado_lista_otima(caminho_otimo)
                            
                            if(caminho_otimo_convergencia==None):
                                caminho_otimo_convergencia = deepcopy(lista_recompensa_caminho_otimo)
                            elif(not(convergiu_lista_otima(lista_recompensa_caminho_otimo, caminho_otimo_convergencia))):
                                caminho_otimo_convergencia = deepcopy(lista_recompensa_caminho_otimo)
                            else:
                                convergiu_caminho += 1
                            
                            if(convergiu_caminho == quando_converge):
                                print("Convergiu caminho otimo!")
                                print('Tipo de gama {}'.format(tipos_de_gama[teste]))
                                exibe_matriz_q_formatada(conjunto_q)

                                print("\nMapa do caminho ótimo")
                                print_map(lista_estados_caminho_otimo,lista_recompensa_caminho_otimo)
                                print("Executou ", passo,"episódios")
                                input()
                                if(salvar_por_episodio):
                                    total_rodadas_cada_gama.append(passo)    
                                else:
                                    total_rodadas_cada_gama.append(rodou_n_vezes)
                                # print(rodou_n_vezes)
                                # print(passo)
                                
                                # input()
                                if(not(roda_ate_o_fim)):
                                    break
                

# Unifica as listas formando tuplas com os tipos de gama e a quantidade total de rodadas para cada gama
# e ordena a lista gerada
listas_ordenadas = sorted(zip(tipos_de_gama, total_rodadas_cada_gama))

# Monta com list comprehension uma lista com o tipo, na mesma ordem da lista acima

# Pega o primeiro valor da tupla
listas_ordenadas_tipo = [chave for chave,_ in listas_ordenadas] 
# Pega o segundo valor da tupla
listas_ordenadas_total_rodadas = [valor for _,valor in listas_ordenadas] 

# Monta a lista de índices para o gráfico
indices = [i for i in range(0,len(listas_ordenadas_tipo))]

# Plot do Gráfico!
plt.bar(indices, listas_ordenadas_total_rodadas)
plt.xlabel('Gamas', fontsize=10)
plt.ylabel('Quantidades de Rodadas', fontsize=10)
plt.xticks(indices, listas_ordenadas_tipo, fontsize=5, rotation=30)
plt.title('Quantidades de Rodada a cada Gama')
nome_arquivo_grafico = 'graficos/grafico_de_barra_convergencia_por_{}_escolha_maiores_{}_{}.png'.format(tipo_de_convergencia,porcentagem_escolha_maiores,time.strftime("%Y%m%d%H%M%S"))
plt.savefig(nome_arquivo_grafico, bbox_inches='tight')