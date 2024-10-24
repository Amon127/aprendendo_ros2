import math
from matplotlib import pyplot as plt

class Path:
    def __init__(self, x, y):
        self.x = x
        self.y = y

x_ini = 50
y_ini = 50

x_fin = 178
y_fin = 138
chegada = (x_fin, y_fin)

start = (x_ini, y_ini)
path = [Path(start[0], start[1])]   

#Montando a matriz obstaculo
pgmf = open('map.pgm', 'rb')
matrix = plt.imread(pgmf)
print (matrix)

matrix = 1 - (1.0 * (matrix > 220))
matriz_obstac = [[0] * 400 for _ in range(400)] # 0 par vazio, 40000000 para obstaculo

for i in range(400):
     for j in range(400):
         if(matrix[i][j] == 0):
            matriz_obstac[i][j] = 40000
         else:
            matriz_obstac[i][j] = 0    
              
# Criando uma matriz vazia de 400x400 para g,h,f e obstaculo

matriz_g = [[0] * 400 for _ in range(400)] #Recebe 1(Cruzinha) ou 1,4(Diagonal)
matriz_h = [[0] * 400 for _ in range(400)] #Distâncai até o objetivo final (y e x final) (cte)
matriz_obstac = [[0] * 400 for _ in range(400)] # 0 par vazio, 40000000 para obstaculo
matriz_f = [[0] * 400 for _ in range(400)] #Soma de g + h + obstaculo
matriz_caminho = [[" "] * 400 for _ in range(400)] #Para poder observar o caminho gerado

#FUNÇÕED PRA CHAMAR NA MAIN

def adjacentes(x_atual, y_atual):
    for i in range(max(0, x_atual - 1), min(400, x_atual + 2)):
        for j in range(max(0, y_atual - 1), min(400, y_atual + 2)): 
            # Analisa apenas os elementos adjacentes ao ponto atual
            if (i, j) != (x_atual, y_atual):
                # Define os valores de G para o ponto adjacente
                if (y_atual == j) or (x_atual == i):
                    matriz_g[i][j] = 1
                else:
                    matriz_g[i][j] = 1.4
                # Calcula a distância H para o ponto adjacente
                matriz_h[i][j] = math.sqrt((x_fin - i )* 2 + (y_fin - j) * 2)
                # Calcula F considerando obstáculos
                if matrix[i][j] == 1:
                    matriz_f[i][j] = 40000
                else:
                    matriz_f[i][j] = matriz_g[i][j] + matriz_h[i][j] + matriz_obstac[i][j]

def diagonais(x_atual, y_atual):
    for i in [x_atual-1, x_atual+1]:
        for j in [y_atual-1, y_atual+1]:
            if 0 <= i < 400 and 0 <= j < 400:  # Verifica se a célula está dentro dos limites da matriz
                # Define os valores de G para a célula diagonal adjacente
                matriz_g[i][j] = 1.4
                # Calcula a distância H para a célula diagonal adjacente
                matriz_h[i][j] = math.sqrt((x_fin - i )* 2 + (y_fin - j) * 2)
                # Calcula F considerando obstáculos
                if matrix[i][j] == 1:
                    matriz_f[i][j] = 40000
                else:
                    matriz_f[i][j] = matriz_g[i][j] + matriz_h[i][j] + matriz_obstac[i][j]

def menor_valor(matriz_f, x_atual, y_atual, x_fin, y_fin):
    menor_valor = float('inf')  # Inicialize o menor valor como infinito
    menor_x = x_atual  # Inicialize a coordenada x do menor valor com a atual
    menor_y = y_atual  # Inicialize a coordenada y do menor valor com a atual
    matriz_f[x_fin][y_fin] = 1
    # Loop apenas sobre as células adjacentes ao ponto atual
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:  # Verifica se não é a célula atual
                novo_x = x_atual + i
                novo_y = y_atual + j
                # Verifique se as coordenadas estão dentro dos limites da matriz
                if 0 <= novo_x < 400 and 0 <= novo_y < 400:
                    valor = matriz_f[novo_x][novo_y]
                    if valor < menor_valor:
                        menor_valor = valor
                        menor_x = novo_x
                        menor_y = novo_y
            elif(i == x_fin and j == y_fin):
                x_atual = menor_x
                y_atual = menor_y
    return menor_valor, menor_x, menor_y


x_atual = x_ini
y_atual = y_ini
qtd = 0

while not(x_atual== x_fin and y_atual == y_fin):
    matriz_caminho[x_atual][y_atual] = 
    # print("x_atual é:",x_atual)
    # print("y_atual é:",y_atual)
    # for linha in matriz_caminho:
    #     print(linha)
    qtd += 1
    adjacentes(x_atual,y_atual)
    diagonais(x_atual,y_atual)
    menor, x_atual, y_atual = menor_valor(matriz_f, x_atual, y_atual,x_fin,y_fin)
    
# Initialize the path
path = [Path(start[0], start[1])]

while path[-1].x != chegada[0] or path[-1].y != chegada[1]:
    matriz_caminho[path[-1].x][path[-1].y] = '*'
    adjacentes(path[-1].x, path[-1].y)
    diagonais(path[-1].x, path[-1].y)
    menor, next_x, next_y = menor_valor(matriz_f, path[-1].x, path[-1].y,x_fin,y_fin)
    path.append(Path(next_x, next_y))

# Visualize the path
plt.imshow(matrix, interpolation='nearest', cmap='gray')
for cell in path:
    plt.scatter(x=cell.x, y=cell.y, c='r', s=5)
plt.show()