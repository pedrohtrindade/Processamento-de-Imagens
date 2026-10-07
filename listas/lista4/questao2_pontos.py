import cv2
import numpy as np
from pathlib import Path

PASTA = Path(__file__).parent
SAIDA = PASTA / 'resultados'
# Criação de pasta movida para o bloco de execução abaixo.

def detectar_pontos(img, limiar):
    mascara = np.array([[-1, -1, -1],
                        [-1,  8, -1],
                        [-1, -1, -1]])

    img_borda = np.pad(img, 1, mode='constant')
    filtrada = np.zeros(img.shape)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            vizinhanca = img_borda[i:i+3, j:j+3]
            filtrada[i, j] = (vizinhanca * mascara).sum()

    filtrada[0, :] = 0
    filtrada[-1, :] = 0
    filtrada[:, 0] = 0
    filtrada[:, -1] = 0

    resultado = np.zeros(img.shape, np.uint8)
    resultado[filtrada > limiar] = 255
    return resultado



if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    img = cv2.imread(str(PASTA / 'pontos.png'), cv2.IMREAD_GRAYSCALE)
    assert img is not None, 'pontos.png nao foi carregada'

    resultado = detectar_pontos(img, 100)
    cv2.imwrite(str(SAIDA / 'q2_pontos_detectados.png'), resultado)
