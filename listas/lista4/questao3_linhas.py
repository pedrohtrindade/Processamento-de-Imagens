import cv2
import numpy as np
from pathlib import Path

PASTA = Path(__file__).parent
SAIDA = PASTA / 'resultados'
# Criação de pasta movida para o bloco de execução abaixo.

def detectar_linhas(img, mascara, limiar):
    img_borda = np.pad(img, 1, mode='constant')
    filtrada = np.zeros(img.shape)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            vizinhanca = img_borda[i:i+3, j:j+3]
            filtrada[i, j] = (vizinhanca * mascara).sum()

    resultado = np.zeros(img.shape, np.uint8)
    resultado[filtrada > limiar] = 255
    return resultado



if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    horizontal = np.array([[-1, -1, -1],
                           [ 2,  2,  2],
                           [-1, -1, -1]])

    diagonal_45 = np.array([[-1, -1,  2],
                            [-1,  2, -1],
                            [ 2, -1, -1]])

    vertical = np.array([[-1,  2, -1],
                         [-1,  2, -1],
                         [-1,  2, -1]])

    diagonal_menos_45 = np.array([[ 2, -1, -1],
                                  [-1,  2, -1],
                                  [-1, -1,  2]])

    img = cv2.imread(str(PASTA / 'linhas.png'), cv2.IMREAD_GRAYSCALE)
    assert img is not None, 'linhas.png nao foi carregada'

    limiar = 300
    r_horizontal = detectar_linhas(img, horizontal, limiar)
    r_45 = detectar_linhas(img, diagonal_45, limiar)
    r_vertical = detectar_linhas(img, vertical, limiar)
    r_menos_45 = detectar_linhas(img, diagonal_menos_45, limiar)

    resultado_final = cv2.bitwise_or(r_horizontal, r_45)
    resultado_final = cv2.bitwise_or(resultado_final, r_vertical)
    resultado_final = cv2.bitwise_or(resultado_final, r_menos_45)

    cv2.imwrite(str(SAIDA / 'q3_horizontal.png'), r_horizontal)
    cv2.imwrite(str(SAIDA / 'q3_mais_45.png'), r_45)
    cv2.imwrite(str(SAIDA / 'q3_vertical.png'), r_vertical)
    cv2.imwrite(str(SAIDA / 'q3_menos_45.png'), r_menos_45)
    cv2.imwrite(str(SAIDA / 'q3_resultado_final.png'), resultado_final)
