import time
import heapq
import tkinter as tk

# Estado que estamos buscando
estado_final = [
    [1, 2, 3],
    [7, 0, 8],
    [4, 5, 6]
]

# Função que verifica se o estado atual é igual ao estado final
def e_final(estado):
    return estado == estado_final

# Função que retorna a posição de um determinado valor/estado
def obterPosicao(valor, estado):
    for i in range(3):
        for j in range(3):
            if estado[i][j] == valor:
                return (i, j)
    return None

# Função que calcula a distância de Manhattan
def distancia_manhattan(estado):
    distancia = 0
    for num in range(1, 9):
        posicao_atual = obterPosicao(num, estado)
        posicao_destino = obterPosicao(num, estado_final)
        distancia += abs(posicao_atual[0] - posicao_destino[0]) + abs(posicao_atual[1] - posicao_destino[1])
    return distancia

# Função que calcula o número de peças que não estão em seu estado final
def numeroPecasFora(estado):
    return sum(1 for i in range(3) for j in range(3) if estado[i][j] != estado_final[i][j] and estado[i][j] != 0)

# Função para geração de movimentos a partir de um estado
def gerarMovimentos(estado):
    linha, col = obterPosicao(0, estado)
    movimentos = []
    for dlinha, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nova_linha, nova_col = linha + dlinha, col + dcol
        if 0 <= nova_linha < 3 and 0 <= nova_col < 3:
            novo_estado = [list(r) for r in estado]
            novo_estado[linha][col], novo_estado[nova_linha][nova_col] = novo_estado[nova_linha][nova_col], novo_estado[linha][col]
            movimentos.append(novo_estado)
    return movimentos

# Função para atualizar a interface gráfica do Tkinter
def atualizar_interface_com_mv(matriz):
    for i in range(3):
        for j in range(3):
            valor = matriz[i][j]
            if valor == 0:
                labels[i][j].config(text='', bg='gray')  # Representa o espaço vazio
            else:
                labels[i][j].config(text=str(valor), bg='white')
    root.update()
    time.sleep(0.5)  # Pequena pausa para visualizar o movimento

def atualizar_interface_sem_mv(matriz):
    for i in range(3):
        for j in range(3):
            valor = matriz[i][j]
            if valor == 0:
                labels[i][j].config(text='', bg='gray')  # Representa o espaço vazio
            else:
                labels[i][j].config(text=str(valor), bg='white')
    root.update()

# Função de busca horizontal com atualização da interface Tkinter
def buscaHorizontal(estado_inicial):
    fila = [(estado_inicial, 0)]
    passou = set()
    passou.add(str(estado_inicial))
    estados_visitados = 0

    while fila:
        estado, profundidade = fila.pop(0)
        estados_visitados += 1

        # Atualiza a interface com o estado atual
        atualizar_interface_sem_mv(estado)

        if e_final(estado):
            print(f"Passos efetuados até a primeira solução {estados_visitados}\nA profundidade da árvore  de opções foi de {profundidade}")
            return profundidade, estados_visitados

        for movimento in gerarMovimentos(estado):
            if str(movimento) not in passou:
                passou.add(str(movimento))
                fila.append((movimento, profundidade + 1))
    print(f"Passos efetuados até a primeira solução {estados_visitados}\n")
    return None

# Função de busca heurística com atualização da interface Tkinter
def buscaHeuristica(estado_inicial):
    fila = []
    heapq.heappush(fila, (0, estado_inicial, 0))
    passou = set()
    passou.add(str(estado_inicial))
    estados_visitados = 0

    while fila:
        f, estado, profundidade = heapq.heappop(fila)
        estados_visitados += 1

        # Atualiza a interface com o estado atual
        atualizar_interface_com_mv(estado)

        if e_final(estado):
            print(f"Passos efetuados até a primeira solução {estados_visitados}\nA profundidade da árvore de opções foi de {profundidade}")
            return profundidade, estados_visitados

        for movimento in gerarMovimentos(estado):
            if str(movimento) not in passou:
                passou.add(str(movimento))
                g = profundidade + 1
                h = numeroPecasFora(movimento) + distancia_manhattan(movimento)
                f = g + h
                heapq.heappush(fila, (f, movimento, g))


    return None

# Função para testar os algoritmos e iniciar a interface Tkinter
def testarAlgoritmo():
    # Estado inicial
    estado_inicial = [
        [1, 2, 3],
        [4, 8, 7],
        [6, 5, 0]
    ]   

    print("Executando Busca Horizontal...")
    buscaHorizontal(estado_inicial)

    print("Executando Busca Heurística...")
    buscaHeuristica(estado_inicial)
    
# Configuração da interface Tkinter
root = tk.Tk()
root.title("Simulação do Puzzle 8")

# Criação da grade de labels para representar a matriz
labels = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        labels[i][j] = tk.Label(root, text='', font=('Helvetica', 20), width=4, height=2, relief='solid')
        labels[i][j].grid(row=i, column=j, padx=5, pady=5)

# Exibe o estado inicial na interface
atualizar_interface_com_mv([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
])

# Botão para iniciar a simulação dos algoritmos
botao_simular = tk.Button(root, text="Iniciar Teste de Algoritmos", command=testarAlgoritmo)
botao_simular.grid(row=3, column=0, columnspan=3)

# Inicia a interface Tkinter
root.mainloop()
