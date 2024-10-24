from collections import deque
from matplotlib import pyplot as plt

# Tamanho da matriz
lines = 400
columns = 400

class Path:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Pontos de inicio e fim
x_ini = 10
y_ini = 10

x_fin = 50
y_fin = 50

goal = (x_fin, y_fin)
start = (x_ini, y_ini)
path = [Path(start[0], start[1])]   

caminho_livre = 1
obstaculo = 0

# Montando matrix do fafa
pgmf = open('src/my_map.pgm', 'rb')
matrix = plt.imread(pgmf)

matrix = (1.0 * (matrix > 220))

# Inicializa a matriz com zeros
matriz = [[0] * columns for _ in range(lines)]
matriz_caminho = [[0] * columns for _ in range(lines)]

matriz[x_fin][y_fin] = 2
matriz[x_ini][y_ini] = 1

# Fila para a busca em largura
fila = deque([(x_fin, y_fin)])

# Wavefront
while fila:
    x, y = fila.popleft()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            i, j = x + dx, y + dy
            if 0 <= i < lines and 0 <= j < columns and matriz[i][j] == 0:
                matriz[i][j] = matriz[x][y] + 1
                fila.append((i, j))
            if (i, j) == (x_ini, y_ini):
                fila.clear()  # Limpa a fila para encerrar o loop   
                break  # Sai do loop for interno
        else:
            continue  # Continua o loop while sem executar o else
        break  # Sai do loop for externo se o ponto inicial foi alcançado

# Para garantir que a célula inicial permaneça com o valor 1
matriz[x_fin][y_fin] = 2
matriz[x_ini][y_ini] = 1

x_atual, y_atual = x_ini, y_ini
def menor_valor(x_atual, y_atual, x_fin, y_fin,matriz):
    menor_valor = float('inf')
    prox_x, prox_y = x_atual, y_atual
    
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            novo_x = x_atual + dx
            novo_y = y_atual + dy
            if (dx, dy) != (0, 0) and 0 <= novo_x < lines and 0 <= novo_y < columns and matriz[novo_x][novo_y] > 0:  #and matrix{novo_x}[novo_y] == caminho_aberto
                valor = matriz[novo_x][novo_y]
                if valor < menor_valor:
                    menor_valor = valor
                    prox_x, prox_y = novo_x, novo_y
                if (novo_x, novo_y) == (x_fin, y_fin):
                    return novo_x, novo_y  
    
    return prox_x, prox_y


matriz[x_ini][y_ini] = float('inf')
while not(x_atual== x_fin and y_atual == y_fin):
    pros_x,pros_y = menor_valor(x_atual, y_atual, x_fin, y_fin,matriz)
    matriz_caminho[pros_x][pros_y] = 1  
    x_atual = pros_x
    y_atual = pros_y
    path.append(Path(x_atual,y_atual))
    
    
path_x = [min(max(cell.x, 0), lines - 1) for cell in path]
path_y = [min(max(cell.y, 0), columns - 1) for cell in path]

plt.imshow(matrix, interpolation='nearest', cmap='gray') 
plt.plot(path_y, path_x, color='red', linewidth=2)
plt.show()