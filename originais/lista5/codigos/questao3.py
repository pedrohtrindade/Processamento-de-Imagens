import cv2 as cv
import numpy as np
from pathlib import Path


PASTA = Path(__file__).resolve().parent.parent


def abertura(img, elemento):
    erosao = cv.erode(img, elemento)
    resultado = cv.dilate(erosao, elemento)
    return resultado


def fechamento(img, elemento):
    dilatacao = cv.dilate(img, elemento)
    resultado = cv.erode(dilatacao, elemento)
    return resultado


img = cv.imread(str(PASTA / "imagens" / "ruidos.png"), cv.IMREAD_GRAYSCALE)

if img is None:
    print("Erro ao carregar ruidos.png")
else:
    elemento = np.ones((15, 15), np.uint8)

    img_abertura = abertura(img, elemento)
    img_fechamento = fechamento(img, elemento)

    cv.imwrite(str(PASTA / "resultados" / "q3_abertura.png"), img_abertura)
    cv.imwrite(str(PASTA / "resultados" / "q3_fechamento.png"), img_fechamento)

    print("Questao 3 concluida.")

