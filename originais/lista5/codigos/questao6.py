import cv2 as cv
import numpy as np
from pathlib import Path


PASTA = Path(__file__).resolve().parent.parent


def componente_conectado(img, ponto):
    altura, largura = img.shape
    x, y = ponto

    if x < 0 or x >= largura or y < 0 or y >= altura:
        raise ValueError("O ponto informado esta fora da imagem.")

    if img[y, x] == 0:
        raise ValueError("O ponto informado nao pertence a um quadrado branco.")

    visitado = np.zeros((altura, largura), np.uint8)
    pilha = [(x, y)]
    visitado[y, x] = 1

    vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while pilha:
        px, py = pilha.pop()

        for dx, dy in vizinhos:
            nx = px + dx
            ny = py + dy

            if 0 <= nx < largura and 0 <= ny < altura:
                if img[ny, nx] > 0 and visitado[ny, nx] == 0:
                    visitado[ny, nx] = 1
                    pilha.append((nx, ny))

    resultado = np.zeros((altura, largura, 3), np.uint8)
    resultado[visitado == 1] = (0, 255, 255)  # amarelo em BGR
    return resultado


img = cv.imread(str(PASTA / "imagens" / "quadrados.png"), cv.IMREAD_GRAYSCALE)

if img is None:
    print("Erro ao carregar quadrados.png")
else:
    entrada = input("Digite o ponto inicial x y (Enter usa 316 261): ").strip()

    if entrada == "":
        ponto = (316, 261)
    else:
        x, y = map(int, entrada.split())
        ponto = (x, y)

    try:
        resultado = componente_conectado(img, ponto)
        cv.imwrite(str(PASTA / "resultados" / "q6_componente_amarelo.png"), resultado)
        print("Questao 6 concluida. Ponto utilizado:", ponto)
    except ValueError as erro:
        print("Erro:", erro)

