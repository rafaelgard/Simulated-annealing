import numpy as np
from PIL import Image 
import matplotlib.pyplot as plt

solucao = np.array([
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [1, 0, 0, 1]])


# tamanho_matriz = (10,10)
# solucao = np.random.randint(0,2,tamanho_matriz) 

print(solucao)

l = solucao.shape[0]
c = solucao.shape[1]

def avalia_solucao(solucao, solucao_temporaria):
    return np.sum(solucao==solucao_temporaria)/(l*c)

def destroi_solucao(solucao_temporaria):

    bits = solucao_temporaria.shape[0]*solucao_temporaria.shape[1]

    parte_destruida = solucao_temporaria.reshape(bits)
    indice = np.random.randint(1,bits)
    parte_destruida = parte_destruida[0:indice]

    return parte_destruida


def reconstroi_solucao(solucao_destruida):

    sol_reconstruida = gera_solucao_inicial()

    sol_reconstruida = sol_reconstruida.reshape(l*c)

    sol_reconstruida[0:solucao_destruida.shape[0]] = solucao_destruida

    return sol_reconstruida.reshape(l,c)
    
def gera_solucao_inicial():
    '''Gera uma solução inicial aleatória'''
    return np.random.randint(0,2, size=l*c).reshape(l,c)
    

temperatura = 100
ALFA = 0.99

solucao_inicial = gera_solucao_inicial()
best_sol = solucao_inicial
best_aval = avalia_solucao(solucao, solucao_inicial)


while temperatura>0.001:

    sol_destruida = destroi_solucao(best_sol)

    sol_reconstruida = reconstroi_solucao(sol_destruida)

    aval_nova_sol = avalia_solucao(solucao, sol_reconstruida)

    delta = best_aval - aval_nova_sol

    if delta<0:
        best_sol = sol_reconstruida
        best_aval = aval_nova_sol

    else:
        numero_aleatorio = np.random.uniform(0, 1)

        if numero_aleatorio<np.exp(-delta/temperatura):
            best_sol = sol_reconstruida
            best_aval = aval_nova_sol

    temperatura = temperatura*ALFA

    print(f'Temperatura:{temperatura} - best_aval:{best_aval}')

print('best_sol')
print(best_sol)

print('best_aval')
print(best_aval)








