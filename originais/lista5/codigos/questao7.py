import cv2 as cv
import numpy as np
from pathlib import Path


PASTA = Path(__file__).resolve().parent.parent


def gradiente_morfologico(img, elemento):
    dilatacao = cv.dilate(img, elemento)
    erosao = cv.erode(img, elemento)
    gradiente = cv.subtract(dilatacao, erosao)
    return dilatacao, erosao, gradiente


img = cv.imread(str(PASTA / "imagens" / "img_aluno.jpeg"), cv.IMREAD_GRAYSCALE)

if img is None:
    print("Erro ao carregar img_aluno.jpeg")
else:
    elemento = np.ones((5, 5), np.uint8)
    dilatacao, erosao, gradiente = gradiente_morfologico(img, elemento)

    cv.imwrite(str(PASTA / "resultados" / "q7_img_aluno_cinza.png"), img)
    cv.imwrite(str(PASTA / "resultados" / "q7_dilatacao.png"), dilatacao)
    cv.imwrite(str(PASTA / "resultados" / "q7_erosao.png"), erosao)
    cv.imwrite(str(PASTA / "resultados" / "q7_gradiente.png"), gradiente)

    print("Questao 7 concluida.")

