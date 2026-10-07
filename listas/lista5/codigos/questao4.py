import cv2 as cv
import numpy as np
from pathlib import Path


PASTA = Path(__file__).resolve().parent.parent


def fronteira_interna(img, elemento):
    erosao = cv.erode(img, elemento)
    borda = cv.subtract(img, erosao)
    return borda


def fronteira_externa(img, elemento):
    dilatacao = cv.dilate(img, elemento)
    borda = cv.subtract(dilatacao, img)
    return borda



if __name__ == "__main__":
    img = cv.imread(str(PASTA / "imagens" / "cachorro.png"), cv.IMREAD_GRAYSCALE)

    if img is None:
        print("Erro ao carregar cachorro.png")
    else:
        elemento = np.ones((3, 3), np.uint8)

        interna = fronteira_interna(img, elemento)
        externa = fronteira_externa(img, elemento)

        cv.imwrite(str(PASTA / "resultados" / "q4_fronteira_interna.png"), interna)
        cv.imwrite(str(PASTA / "resultados" / "q4_fronteira_externa.png"), externa)

        print("Questao 4 concluida.")
