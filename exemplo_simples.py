""" 
Este é um exemplo simples da aplicação da meta-heurística simulated annealing 
no contexto de imagens.

O projeto está disponível em: 

https://github.com/rafaelgard/Simulated-annealing
"""

import numpy as np
np.random.seed(5)

solucao = np.array([
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [1, 0, 0, 1]])


print(solucao)

# breakpoint()
l = solucao.shape[0]
c = solucao.shape[1]


def avalia_solucao(solucao, solucao_temporaria):
    """Avalia quantos pixels da solução estão corretos"""

    return np.sum(solucao == solucao_temporaria)/(l*c)


def destroi_solucao(solucao_temporaria):
    """Destroi uma solucao_temporaria deixando apenas uma parte restante 
    e posteriormente retorna essa solução destruida"""

    bits = solucao_temporaria.shape[0]*solucao_temporaria.shape[1]

    parte_destruida = solucao_temporaria.reshape(bits)
    indice = np.random.randint(1, bits)
    parte_destruida = parte_destruida[0:indice]

    return parte_destruida


def reconstroi_solucao(solucao_destruida):
    """Reconstroi uma solucao destruida com parte de uma solução aleatória"""

    sol_reconstruida = gera_solucao_inicial().reshape(l*c)

    sol_reconstruida[0:solucao_destruida.shape[0]] = solucao_destruida

    return sol_reconstruida.reshape(l, c)


def gera_solucao_inicial():
    """Gera uma solução inicial aleatória"""

    return np.random.randint(0, 2, size=l*c).reshape(l, c)


temperatura = 100
ALFA = 0.99

solucao_inicial = gera_solucao_inicial()
best_sol = solucao_inicial
best_aval = avalia_solucao(solucao, solucao_inicial)


while temperatura > 0.001:

    sol_destruida = destroi_solucao(best_sol)

    sol_reconstruida = reconstroi_solucao(sol_destruida)

    aval_nova_sol = avalia_solucao(solucao, sol_reconstruida)

    delta = best_aval - aval_nova_sol

    if delta < 0:
        best_sol = sol_reconstruida
        best_aval = aval_nova_sol

    else:
        numero_aleatorio = np.random.uniform(0, 1)

        if numero_aleatorio < np.exp(-delta/temperatura):
            best_sol = sol_reconstruida
            best_aval = aval_nova_sol

    temperatura = temperatura*ALFA

    print(f'Temperatura:{temperatura} - best_aval:{best_aval}')

print('Melhor solução encontrada:')
print(best_sol)

print(f'Acurácia: {best_aval}')
