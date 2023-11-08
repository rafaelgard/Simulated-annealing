""" 
Este modulo centraliza a utilização da meta-heurística simulated annealing 
no contexto de imagens.

O projeto está disponível em: 

https://github.com/rafaelgard/Simulated-annealing
"""

import copy
import numpy as np
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt


class Simulated_annealing:
    def __init__(self):
        self.l = 0
        self.c = 0
        self.solucao = 0
        self.temperatura = 1000
        self.alfa = 0.99
        self.busca_local_ativada = False
        self.taxa_busca_local = 0.01
        self.min_value = 0
        self.max_value = 0

    def get_sol(self):
        '''Configura uma solução que deve ser buscada pela metaheurística'''

        self.solucao = np.array([
            [1, 0, 0, 1],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [1, 0, 0, 1]])

        self.l = self.solucao.shape[0]
        self.c = self.solucao.shape[1]

    def get_image(self):
        '''Transforma uma imagem em um array'''

        img = Image.open('cat.png').resize(
            (10, 10))  # diminui o tamanho da imagem

        # img = img.convert("L")
        # img = img.filter(FIND_EDGES)
        img = img.filter(ImageFilter.FIND_EDGES)
        img_as_array = np.array(img)[0:, 0:, 0]  # pega apenas o primeiro canal
        # print(img.format)
        # print(img.size)
        # print(img.mode)

        self.solucao = img_as_array

        self.l = self.solucao.shape[0]
        self.c = self.solucao.shape[1]

    def avalia_solucao(self, solucao_temporaria):
        '''Avalia quantos pixels da solução estão corretos'''

        # breakpoint()
        return np.sum(self.solucao == solucao_temporaria)/(self.l*self.c)

    def destroi_solucao(self, solucao_temporaria):
        '''Destroi uma solucao_temporaria deixando apenas uma parte restante 
        e posteriormente retorna essa solução destruida'''

        bits = solucao_temporaria.shape[0]*solucao_temporaria.shape[1]

        parte_destruida = solucao_temporaria.reshape(bits)
        indice = np.random.randint(1, bits)
        parte_destruida = parte_destruida[0:indice]

        return parte_destruida

    def reconstroi_solucao(self, solucao_destruida):
        '''Reconstroi uma solucao destruida com parte de uma solução aleatória'''

        sol_reconstruida = self.gera_solucao_inicial()

        sol_reconstruida = sol_reconstruida.reshape(self.l*self.c)

        sol_reconstruida[0:solucao_destruida.shape[0]] = solucao_destruida

        return sol_reconstruida.reshape(self.l, self.c)

    def gera_solucao_inicial(self):
        '''Gera uma solução inicial aleatória'''

        sol_inicial = np.random.randint(
            self.min_value, self.max_value+1, size=self.l*self.c)
        sol_inicial = sol_inicial.reshape(self.l, self.c
                                          )
        return sol_inicial

    def get_sa_configs(self):
        '''Define e modifica os parâmetros'''

        self.temperatura = 1000
        self.alfa = 0.99
        self.taxa_busca_local = 0.3
        self.min_value = np.min(self.solucao)
        self.max_value = np.max(self.solucao)

    def busca_local(self, solucao):
        '''Realiza uma busca local na solução'''

        if np.random.uniform(0, 1) < self.taxa_busca_local:

            melhor_solucao = copy.deepcopy(solucao)
            melhor_pontuacao = self.avalia_solucao(solucao)

            i = 0
            while i < 1000:

                solucao_provisoria = melhor_solucao

                linha_aleatoria = np.random.randint(solucao[0].shape[0])

                valor_sorteado = np.random.randint(
                    self.min_value, self.max_value+1)

                solucao_provisoria[linha_aleatoria][np.random.randint(
                    solucao[linha_aleatoria].shape[0])] = valor_sorteado

                nova_pontuacao = self.avalia_solucao(solucao_provisoria)

                if nova_pontuacao > melhor_pontuacao:
                    melhor_pontuacao = nova_pontuacao
                    melhor_solucao = solucao_provisoria

                i += 1

            return melhor_solucao

        else:

            return solucao

    def main(self):
        '''Chama os métodos necessários em sequencia'''

        # configura a solução
        self.get_sol()

        # configura os parâmetros
        self.get_sa_configs()

        # define a solução inicial como a melhor solução
        best_sol = self.gera_solucao_inicial()
        best_aval = self.avalia_solucao(best_sol)

        plt.figure(figsize=(10, 8))

        plt.subplot(2, 2, 1)
        solucao_plot = plt.imshow(self.solucao)
        plt.title('Solução Esperada')

        temperatura_values = []
        best_aval_values = []

        temperatura = self.temperatura

        i = 0

        # a partir daqui de fato começa a aplicação da meta-heurística
        while temperatura > 0.001 and best_aval < 1:

            sol_destruida = self.destroi_solucao(best_sol)

            sol_reconstruida = self.reconstroi_solucao(sol_destruida)

            if self.busca_local_ativada:
                sol_reconstruida = self.busca_local(sol_reconstruida)

            aval_nova_sol = self.avalia_solucao(sol_reconstruida)

            delta = best_aval - aval_nova_sol

            if delta < 0:
                best_sol = sol_reconstruida
                best_aval = aval_nova_sol

            else:
                numero_aleatorio = np.random.uniform(0, 1)

                if numero_aleatorio < np.exp(-delta/temperatura):
                    best_sol = sol_reconstruida
                    best_aval = aval_nova_sol

            best_aval_values.append(best_aval)

            temperatura = temperatura*self.alfa

            temperatura_values.append(temperatura)

            i += 1
            if i % 10 == 0:  # define uma taxa de atualização da imagem
                plt.subplot(2, 2, 3)
                plt.imshow(best_sol)
                plt.title('Melhor Solução Encontrada')

                solucao_plot.set_data(self.solucao)
                plt.subplot(2, 2, 2)
                plt.cla()
                plt.plot(temperatura_values, color='r')
                plt.title('Temperatura')

                plt.subplot(2, 2, 4)
                plt.cla()
                plt.plot(best_aval_values)
                plt.title(f'Acurácia')

                # Tempo de pausa entre as iterações em segundos
                plt.pause(0.0001)
                plt.draw()

        plt.show()
        print('best_sol')
        print(best_sol)

        print('best_aval')
        print(best_aval)


if __name__ == '__main__':

    np.random.seed(1)

    sa = Simulated_annealing()
    sa.main()
