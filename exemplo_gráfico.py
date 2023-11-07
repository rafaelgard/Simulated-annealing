import numpy as np
from PIL import Image 
import matplotlib.pyplot as plt

np.random.seed(1)

solucao = np.array([
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [1, 0, 0, 1]])


# solucao = np.array([
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
#     [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
#     [1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
#     [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
#     [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
#     [1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
#     [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
#     [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    
    
#     ])


# tamanho_matriz = (10,10)
# solucao = np.random.randint(0,2,tamanho_matriz) 

print(solucao)

# breakpoint()

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
    

# solucao_inicial = gera_solucao_inicial()
# print('solucao_inicial')
# print(solucao_inicial)


# aval = avalia_solucao(solucao, solucao_inicial)

# print('aval')
# print(aval)

# sol_destruida = destroi_solucao(solucao_inicial)

# sol_reconstruida = reconstroi_solucao(sol_destruida)


# print('sol_reconstruida')
# print(sol_reconstruida)


# aval_nova_sol = avalia_solucao(solucao, sol_reconstruida)

# print('aval')
# print(aval)


temperatura = 1000
ALFA = 0.99

# aval_best = avalia_solucao(solucao, solucao_inicial)


solucao_inicial = gera_solucao_inicial()
best_sol = solucao_inicial
best_aval = avalia_solucao(solucao, solucao_inicial)

# Inicialize a figura fora do loop
plt.figure(figsize=(10, 8))

# Subplot para a segunda imagem (solucao)
plt.subplot(2, 2, 1)
# solucao = Image.open('caminho_da_imagem2.jpg')
solucao_plot = plt.imshow(solucao)
plt.title('Solução Esperada')


# Subplot para o gráfico da temperatura
# plt.subplot(1, 3, 3)

temperatura_values = []
best_aval_values = []


i=0
while temperatura>0.001:
# while best_aval<1:

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


    best_aval_values.append(best_aval)

    temperatura = temperatura*ALFA

    temperatura_values.append(temperatura)

    print(f'Temperatura:{temperatura} - best_aval:{best_aval}')

    # if temperatura<0.01 and best_aval<0.9:
    #     temperatura+=1

    i+=1
    if i%10==0:
        # Limpe o subplot da primeira imagem (best_sol) e adicione a nova imagem
        plt.subplot(2, 2, 3)
        # plt.cla()
        plt.imshow(best_sol)
        plt.title('Melhor Solução Encontrada')

        # Atualize o subplot da segunda imagem (solucao)
        # solucao = Image.open('caminho_da_imagem2.jpg')
        solucao_plot.set_data(solucao)
        plt.subplot(2, 2, 2)

        plt.cla()
        plt.plot(temperatura_values, color='r')
        plt.title('Temperatura')


        plt.subplot(2, 2, 4)
        plt.cla()
        plt.plot(best_aval_values)
        plt.title(f'Acurácia')

        plt.pause(0.0001)  # Tempo de pausa entre as iterações em segundos
        plt.draw()

plt.show()
print('best_sol')
print(best_sol)

print('best_aval')
print(best_aval)