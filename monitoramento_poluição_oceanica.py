import os
import time
import numpy as np

# Função para limpar o terminal, útil para manter a interface do usuário limpa.
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para calcular a distância euclidiana entre dois pontos dados.
def calcular_distancia(ponto1, ponto2):
    return np.sqrt((ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2)

# Função para gerar pontos aleatórios dentro de um limite superior fornecido.
def gerar_pontos_aleatorios(n, limite_superior):
    return [(round(np.random.uniform(0, limite_superior), 2), round(np.random.uniform(0, limite_superior), 2)) for _ in range(n)]

# Função para solicitar ao usuário a entrada manual dos pontos.
def obter_pontos_manuais():
    num_pontos = int(input("Digite o número de pontos: "))
    pontos = []
    for i in range(num_pontos):
        x = float(input(f"Digite a coordenada x do ponto {i+1}: "))
        y = float(input(f"Digite a coordenada y do ponto {i+1}: "))
        pontos.append((x, y))
    return pontos

# Função para otimizar a distribuição dos sensores usando programação dinâmica.
def otimizar_distribuicao_sensores(pontos, num_sensores):
    n = len(pontos)  # Número total de pontos a serem monitorados
    dp = np.full((n + 1, num_sensores + 1), np.inf)  # Matriz DP inicializada com infinito
    dp[0][0] = 0  # Ponto de partida sem sensores tem custo zero

    # Preenchendo a matriz DP
    for i in range(1, n + 1):
        for j in range(1, num_sensores + 1):
            for k in range(i):
                # Calcula o custo de colocar um sensor do ponto k ao ponto i
                cost = sum(calcular_distancia(pontos[m], pontos[k]) for m in range(k, i))
                # Atualiza a matriz DP com o menor custo possível
                dp[i][j] = min(dp[i][j], dp[k][j - 1] + cost)

    # Reconstrução da solução a partir da matriz DP
    distribuicao = []
    i, j = n, num_sensores
    while i > 0 and j > 0:
        for k in range(i):
            cost = sum(calcular_distancia(pontos[m], pontos[k]) for m in range(k, i))
            if dp[i][j] == dp[k][j - 1] + cost:
                distribuicao.append(pontos[k:i])  # Adiciona o cluster de pontos monitorados por um sensor
                i = k
                j -= 1
                break

    return distribuicao[::-1]  # Inverte a lista para obter a ordem correta

# Função de menu para permitir ao usuário escolher entre inserir dados manualmente ou gerar dados aleatoriamente.
def menu():
    limpar_terminal()
    print("Menu:")
    print("1. Inserir dados manualmente")
    print("2. Gerar dados aleatoriamente")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        limpar_terminal()
        pontos = obter_pontos_manuais()
        limite_superior = None  # Não se aplica a entrada manual
        return pontos, limite_superior
    elif escolha == '2':
        limpar_terminal()
        while True:
            try:
                num_pontos = int(input("Digite o número de pontos a serem gerados aleatoriamente: "))
                if num_pontos <= 0:
                    raise ValueError
                break
            except ValueError:
                limpar_terminal()
                print("Por favor, digite um número inteiro positivo para o número de pontos.")

        while True:
            try:
                limite_superior = float(input("Digite o limite superior para as coordenadas dos pontos: "))
                if limite_superior <= 0:
                    raise ValueError
                break
            except ValueError:
                limpar_terminal()
                print("Por favor, digite um número positivo para o limite superior.")

        return gerar_pontos_aleatorios(num_pontos, limite_superior), limite_superior
    else:
        print("Opção inválida. Por favor, escolha 1 ou 2.")
        return menu()

# Loop principal do programa.
while True:
    # Menu
    pontos_aleatorios, limite_superior = menu()
    num_pontos = len(pontos_aleatorios)

    # Número de sensores disponíveis
    while True:
        try:
            print("")
            num_sensores = int(input("Digite o número de sensores disponíveis: "))
            if num_sensores <= 0:
                raise ValueError
            break
        except ValueError:
            limpar_terminal()
            print("Por favor, digite um número inteiro positivo para o número de sensores.")

    # Nomeia os pontos para facilitar a leitura
    pontos_nomeados = {f"P{i+1}": pontos_aleatorios[i] for i in range(num_pontos)}

    # Exibe informações antes de calcular as distâncias
    limpar_terminal()
    print(f"\nNúmero de pontos: {num_pontos}")
    if limite_superior:
        print(f"Limite superior para coordenadas: {limite_superior}")
    print(f"Número de sensores disponíveis: {num_sensores}")

    # Encontra a distribuição ótima dos sensores
    distribuicao_otima = otimizar_distribuicao_sensores(list(pontos_nomeados.values()), num_sensores)

    # Calcular e imprimir a distância entre todos os pares de pontos
    print("\nDistâncias entre os pontos (em metros):")
    for i in range(len(pontos_nomeados)):
        for j in range(i + 1, len(pontos_nomeados)):
            ponto1 = pontos_nomeados[f"P{i+1}"]
            ponto2 = pontos_nomeados[f"P{j+1}"]
            distancia = calcular_distancia(ponto1, ponto2)
            print(f"Distância entre P{i+1} {ponto1} e P{j+1} {ponto2}: {distancia:.2f} metros")

    # Exibe a distribuição ótima dos sensores
    print("\nDistribuição dos sensores:")
    for i, cluster in enumerate(distribuicao_otima):
        cluster_nomeado = [f"P{list(pontos_nomeados.values()).index(p)+1}" for p in cluster]
        print(f"Sensor {i+1}: monitora os pontos {cluster_nomeado}")

    # Pergunta ao usuário se deseja continuar ou finalizar
    print("\nDeseja executar o programa novamente? (Insira 1 ou 2)")
    print("1. Sim")
    print("2. Não")
    continuar = input("Escolha uma opção: ")

    if continuar != '1':
        limpar_terminal()
        print("Finalizando o programa...")
        time.sleep(3)
        limpar_terminal()
        print("Programa encerrado.")
        break
