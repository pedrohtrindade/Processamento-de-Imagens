import cv2
import numpy as np
from collections import deque
from pathlib import Path

PASTA = Path(__file__).parent
SAIDA = PASTA / 'resultados'
# Criação de pasta movida para o bloco de execução abaixo.

def crescimento_regiao(img, semente, tolerancia):
    x, y = semente
    valor_semente = int(img[y, x])

    visitados = np.zeros(img.shape, np.uint8)
    regiao = np.zeros(img.shape, np.uint8)
    fila = deque([(y, x)])
    visitados[y, x] = 1

    while fila:
        atual_y, atual_x = fila.popleft()
        regiao[atual_y, atual_x] = 255

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                novo_y = atual_y + dy
                novo_x = atual_x + dx

                dentro = (0 <= novo_y < img.shape[0] and
                          0 <= novo_x < img.shape[1])

                if dentro and visitados[novo_y, novo_x] == 0:
                    visitados[novo_y, novo_x] = 1
                    valor = int(img[novo_y, novo_x])

                    if abs(valor - valor_semente) <= tolerancia:
                        fila.append((novo_y, novo_x))

    resultado = img.copy()
    resultado[regiao == 255] = 0
    return resultado, regiao



if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    img = cv2.imread(str(PASTA / 'root.jpg'), cv2.IMREAD_GRAYSCALE)
    assert img is not None, 'root.jpg nao foi carregada'

    semente = (350, 105)
    tolerancia = 15
    resultado, regiao = crescimento_regiao(img, semente, tolerancia)

    cv2.imwrite(str(SAIDA / 'q5_root_cinza.png'), img)
    cv2.imwrite(str(SAIDA / 'q5_regiao_detectada.png'), resultado)
    cv2.imwrite(str(SAIDA / 'q5_mascara_regiao.png'), regiao)
