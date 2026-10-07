import cv2 as cv
import numpy as np
from pathlib import Path


PASTA = Path(__file__).resolve().parent.parent


def eliminar_quadrados_menores(img, tamanho=51):
    elemento = np.ones((tamanho, tamanho), np.uint8)

    erosao = cv.erode(img, elemento)
    restaurada = cv.dilate(erosao, elemento)

    return erosao, restaurada



if __name__ == "__main__":
    img = cv.imread(str(PASTA / "imagens" / "quadrados.png"), cv.IMREAD_GRAYSCALE)

    if img is None:
        print("Erro ao carregar quadrados.png")
    else:
        erosao, restaurada = eliminar_quadrados_menores(img, 51)

        cv.imwrite(str(PASTA / "resultados" / "q2_erosao.png"), erosao)
        cv.imwrite(str(PASTA / "resultados" / "q2_restaurada.png"), restaurada)

        print("Questao 2 concluida.")
        print("Elemento estruturante utilizado: 51 x 51 pixels")
