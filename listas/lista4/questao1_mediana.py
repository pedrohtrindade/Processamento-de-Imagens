import cv2
import numpy as np
from pathlib import Path

PASTA = Path(__file__).parent
SAIDA = PASTA / 'resultados'
# Criação de pasta movida para o bloco de execução abaixo.

def filtro_mediana(img, tamanho):
    margem = tamanho // 2
    img_borda = np.pad(img, margem, mode='constant')
    resultado = np.zeros(img.shape)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            vizinhanca = img_borda[i:i+tamanho, j:j+tamanho].flatten()
            vizinhanca = np.sort(vizinhanca)
            resultado[i, j] = vizinhanca[len(vizinhanca) // 2]

    return resultado.astype(np.uint8)



if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    img = cv2.imread(str(PASTA / 'circuito.tif'), cv2.IMREAD_GRAYSCALE)
    assert img is not None, 'circuito.tif nao foi carregada'

    resultado1 = filtro_mediana(img, 3)
    resultado2 = filtro_mediana(resultado1, 3)
    resultado3 = filtro_mediana(resultado2, 3)

    cv2.imwrite(str(SAIDA / 'q1_mediana_1.png'), resultado1)
    cv2.imwrite(str(SAIDA / 'q1_mediana_2.png'), resultado2)
    cv2.imwrite(str(SAIDA / 'q1_mediana_3.png'), resultado3)
