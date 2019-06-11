# Q-learning algorithm in python

Para executar o projeto é necessário ter o pip3 e o python versão 3 instalado em sua máquina.

Na pasta do projeto, execute 

```bash
$ pip3 install -r requirements.txt
```

Após o fim do comando, execute

```bash
$ python3 q.py
```

### Valores alteráveis no código:

 Lista que define sobre quais gamas ocorrerá a execução (separar gamas por vírgula)
 ```python
tipos_de_gama = [0.1,0.2,0.8,0.9,0.95, 0.5 , 0.4, 0.3, 0.7, 0.6]
```
```python
porcentagem_escolha_maiores = 70
```

 Define se o programa executará até o fim dos N episódios definidos, sem parar quando converge
```python
roda_ate_o_fim = False
```
 Define o gráfico será gerado com base na quantidade de passos do episódio executados ou na quantidade de execuções mesmo internas de quando está buscando o OBJETIVO

```python
salvar_por_episodio = True
```
```python
episodios = 1000
```

Tipos aceitaveis de convergencia:
tipo_de_convergencia = 'conjunto_q'
tipo_de_convergencia = 'lista_otima'

Gama para o cálculo de propagação de recompensas
```python
gama = 0.5
```
Variável que define quantas vezes uma lista ficou sem mudar para ser convergência
```python
quando_converge = 100
```
Variável que define partindo de quantas execuções a lista de caminho ótimo passará a ser buscada

```python
quando_comeca_a_armazenar_lista_caminho_otimo = 5
```

Variável que define se a matriz Q será exibida de N em N episódios da execução
Com o valor -1, não exibirá a matriz Q

```python
exibir_matriz_q_de_n_em_n_passos = -1
```