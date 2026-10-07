import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def mascara_gaussiana(img, tamanho):
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2

    mask = np.zeros((rows, cols, 2), np.float32)
    mask[crow, ccol, 0] = 1

    mask[:, :, 0] = cv.GaussianBlur(mask[:, :, 0],
                                    (tamanho, tamanho), 0)
    mask[:, :, 0] = mask[:, :, 0] / mask[:, :, 0].max()
    mask[:, :, 1] = mask[:, :, 0]

    return mask

def aplicar_filtro(img, mask):
    dft = cv.dft(np.float32(img), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    filtered_shift = dft_shift * mask
    filtered = np.fft.ifftshift(filtered_shift)
    img_back = cv.idft(filtered)
    img_back = cv.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    img_back = cv.normalize(img_back, None, 0, 255, cv.NORM_MINMAX)
    img_back = img_back.astype(np.uint8)
    return img_back

def passa_baixa_gaussiano(img, tamanho):
    mask = mascara_gaussiana(img, tamanho)
    return aplicar_filtro(img, mask)

def passa_alta_gaussiano(img, tamanho):
    mask = mascara_gaussiana(img, tamanho)
    mask = 1 - mask
    return aplicar_filtro(img, mask)

arquivos = ['teste.tif', 'img_aluno.jpg']
tamanho_gaussiana = 201

for nome in arquivos:
    img = cv.imread(nome, cv.IMREAD_GRAYSCALE)
    assert img is not None, 'Arquivo {} nao foi carregado'.format(nome)

    baixa = passa_baixa_gaussiano(img, tamanho_gaussiana)
    alta = passa_alta_gaussiano(img, tamanho_gaussiana)

    fig, axes = plt.subplots(1, 3)
    ax = axes.ravel()

    ax[0].imshow(img, cmap='gray')
    ax[0].title.set_text('Imagem original')
    ax[0].set_axis_off()

    ax[1].imshow(baixa, cmap='gray')
    ax[1].title.set_text('Passa-baixa gaussiano')
    ax[1].set_axis_off()

    ax[2].imshow(alta, cmap='gray')
    ax[2].title.set_text('Passa-alta gaussiano')
    ax[2].set_axis_off()

    fig.suptitle(nome)
    fig.tight_layout()

    nome_base = nome.rsplit('.', 1)[0]
    cv.imwrite(nome_base + '_passa_baixa.png', baixa)
    cv.imwrite(nome_base + '_passa_alta.png', alta)
    plt.savefig(nome_base + '_filtros_gaussianos.png')

plt.show()
