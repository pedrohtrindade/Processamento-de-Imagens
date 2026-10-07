import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def espectro_fourier(nome):
    img = cv.imread(nome, cv.IMREAD_GRAYSCALE)
    assert img is not None, 'Arquivo {} nao foi carregado'.format(nome)

    dft = cv.dft(np.float32(img), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    espectro = np.log(1 + cv.magnitude(dft_shift[:, :, 0],
                                       dft_shift[:, :, 1]))

    return img, espectro

arquivos = [
    'arara.png',
    'barra1.png',
    'barra2.png',
    'barra3.png',
    'barra4.png',
    'teste.tif',
    'img_aluno.jpg'
]

for nome in arquivos:
    img, espectro = espectro_fourier(nome)

    fig, axes = plt.subplots(1, 2)
    ax = axes.ravel()

    ax[0].imshow(img, cmap='gray')
    ax[0].title.set_text('Imagem de Entrada')
    ax[0].set_axis_off()

    ax[1].imshow(espectro, cmap='gray')
    ax[1].title.set_text('Espectro de Fourier')
    ax[1].set_axis_off()

    fig.suptitle(nome)
    fig.tight_layout()

    nome_saida = 'espectro_' + nome.rsplit('.', 1)[0] + '.png'
    plt.savefig(nome_saida)

plt.show()
