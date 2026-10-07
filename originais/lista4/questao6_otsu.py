import cv2
import numpy as np
from pathlib import Path

PASTA = Path(__file__).parent
SAIDA = PASTA / 'resultados'
SAIDA.mkdir(exist_ok=True)

def otsu(img):
    histograma = np.zeros(256)

    for valor in img.flatten():
        histograma[valor] += 1

    total = img.size
    soma_total = 0

    for i in range(256):
        soma_total += i * histograma[i]

    peso_fundo = 0
    soma_fundo = 0
    maior_variancia = 0
    melhor_limiar = 0

    for t in range(256):
        peso_fundo += histograma[t]

        if peso_fundo == 0:
            continue

        peso_objeto = total - peso_fundo

        if peso_objeto == 0:
            break

        soma_fundo += t * histograma[t]
        media_fundo = soma_fundo / peso_fundo
        media_objeto = (soma_total - soma_fundo) / peso_objeto

        variancia = peso_fundo * peso_objeto * (media_fundo - media_objeto)**2

        if variancia > maior_variancia:
            maior_variancia = variancia
            melhor_limiar = t

    resultado = np.zeros(img.shape, np.uint8)
    resultado[img > melhor_limiar] = 255
    return resultado, melhor_limiar

arquivos = ['harewood.jpg', 'nuts.jpg', 'snow.jpg', 'img_aluno.jpeg']

for nome in arquivos:
    img = cv2.imread(str(PASTA / nome), cv2.IMREAD_GRAYSCALE)
    assert img is not None, '{} nao foi carregada'.format(nome)

    resultado, limiar = otsu(img)
    nome_base = Path(nome).stem
    cv2.imwrite(str(SAIDA / ('q6_' + nome_base + '_cinza.png')), img)
    cv2.imwrite(str(SAIDA / ('q6_' + nome_base + '_otsu.png')), resultado)
    print('{}: limiar de Otsu = {}'.format(nome, limiar))
