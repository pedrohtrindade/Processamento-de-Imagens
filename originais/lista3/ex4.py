import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def criar_filtros(img, raio_interno, raio_externo):
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2

    passa = np.zeros((rows, cols), np.float32)

    for i in range(rows):
        for j in range(cols):
            distancia = np.sqrt((i - crow)**2 + (j - ccol)**2)

            if raio_interno <= distancia <= raio_externo:
                passa[i, j] = 1

    rejeita = 1 - passa

    mask_passa = np.zeros((rows, cols, 2), np.float32)
    mask_passa[:, :, 0] = passa
    mask_passa[:, :, 1] = passa

    mask_rejeita = np.zeros((rows, cols, 2), np.float32)
    mask_rejeita[:, :, 0] = rejeita
    mask_rejeita[:, :, 1] = rejeita

    return mask_passa, mask_rejeita

def aplicar_filtro(dft_shift, mask):
    filtered_shift = dft_shift * mask
    filtered = np.fft.ifftshift(filtered_shift)
    img_back = cv.idft(filtered)
    img_back = cv.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    img_back = cv.normalize(img_back, None, 0, 255, cv.NORM_MINMAX)
    img_back = img_back.astype(np.uint8)
    return img_back

arquivos = ['teste.tif', 'img_aluno.jpg']

raio_interno = 20
raio_externo = 60

for nome in arquivos:
    img = cv.imread(nome, cv.IMREAD_GRAYSCALE)
    assert img is not None, 'Arquivo {} nao foi carregado'.format(nome)

    dft = cv.dft(np.float32(img), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    espectro = np.log(1 + cv.magnitude(dft_shift[:, :, 0],
                                       dft_shift[:, :, 1]))

    mask_passa, mask_rejeita = criar_filtros(
        img, raio_interno, raio_externo
    )

    img_passa = aplicar_filtro(dft_shift, mask_passa)
    img_rejeita = aplicar_filtro(dft_shift, mask_rejeita)

    nome_base = nome.rsplit('.', 1)[0]
    cv.imwrite(nome_base + '_passa_banda.png', img_passa)
    cv.imwrite(nome_base + '_rejeita_banda.png', img_rejeita)

    fig, axes = plt.subplots(2, 3)
    ax = axes.ravel()

    ax[0].imshow(img, cmap='gray')
    ax[0].title.set_text('Imagem original')

    ax[1].imshow(espectro, cmap='gray')
    ax[1].title.set_text('Espectro de Fourier')

    ax[2].imshow(mask_passa[:, :, 0], cmap='gray')
    ax[2].title.set_text('Filtro passa-banda')

    ax[3].imshow(img_passa, cmap='gray')
    ax[3].title.set_text('Resultado passa-banda')

    ax[4].imshow(mask_rejeita[:, :, 0], cmap='gray')
    ax[4].title.set_text('Filtro rejeita-banda')

    ax[5].imshow(img_rejeita, cmap='gray')
    ax[5].title.set_text('Resultado rejeita-banda')

    for eixo in ax:
        eixo.set_axis_off()

    fig.suptitle(nome)
    fig.tight_layout()
    plt.savefig(nome_base + '_filtros_de_banda.png')

plt.show()
