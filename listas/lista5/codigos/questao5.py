import cv2 as cv
import numpy as np
from pathlib import Path


PASTA = Path(__file__).resolve().parent.parent


def preenchimento_regiao(img, ponto):
    complemento = cv.bitwise_not(img)
    elemento = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))

    x, y = ponto
    preenchida = np.zeros_like(img)
    preenchida[y, x] = 255

    while True:
        anterior = preenchida.copy()
        preenchida = cv.dilate(preenchida, elemento)
        preenchida = cv.bitwise_and(preenchida, complemento)

        if np.array_equal(preenchida, anterior):
            break

    resultado = cv.bitwise_or(img, preenchida)
    return resultado



if __name__ == "__main__":
    img = cv.imread(str(PASTA / "imagens" / "gato.png"), cv.IMREAD_GRAYSCALE)

    if img is None:
        print("Erro ao carregar gato.png")
    else:
        # O ponto (150, 180) fica dentro do corpo do gato.
        resultado = preenchimento_regiao(img, (150, 180))
        cv.imwrite(str(PASTA / "resultados" / "q5_gato_preenchido.png"), resultado)

        print("Questao 5 concluida.")
