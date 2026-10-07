import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def rejeita_banda(img, m):
    m = m > 0
    m = m.astype('uint8')

    rows, cols = m.shape
    mask = np.zeros((rows, cols, 2), np.uint8)
    mask[:, :, 0] = m
    mask[:, :, 1] = m

    dft = cv.dft(np.float32(img), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    spectrum = np.log(1 + cv.magnitude(dft_shift[:, :, 0],
                                       dft_shift[:, :, 1]))

    filtered_shift = dft_shift * mask
    filtered = np.fft.ifftshift(filtered_shift)
    img_back = cv.idft(filtered)
    img_back = cv.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    return img_back, spectrum, mask



if __name__ == "__main__":
    img = cv.imread('arara.png', cv.IMREAD_GRAYSCALE)
    m = cv.imread('arara_filtro.png', cv.IMREAD_GRAYSCALE)

    assert img is not None, 'arara.png nao foi carregada'
    assert m is not None, 'arara_filtro.png nao foi carregada'
    assert img.shape == m.shape, 'A imagem e o filtro devem ter o mesmo tamanho'

    img_back, spectrum, mask = rejeita_banda(img, m)

    resultado = cv.normalize(img_back, None, 0, 255, cv.NORM_MINMAX)
    resultado = resultado.astype(np.uint8)
    cv.imwrite('arara_rejeita_banda.png', resultado)

    fig, axes = plt.subplots(2, 2)
    ax = axes.ravel()

    ax[0].imshow(img, cmap='gray')
    ax[0].title.set_text('Imagem de Entrada')
    ax[0].set_axis_off()

    ax[1].imshow(img_back, cmap='gray')
    ax[1].title.set_text('Imagem Filtrada')
    ax[1].set_axis_off()

    ax[2].imshow(spectrum, cmap='gray')
    ax[2].title.set_text('Espectro de Fourier')
    ax[2].set_axis_off()

    ax[3].imshow(mask[:, :, 0], cmap='gray')
    ax[3].title.set_text('Filtro Rejeita-Banda')
    ax[3].set_axis_off()

    fig.tight_layout()
    plt.savefig('arara_resultado_rejeita_banda.png')
    plt.show()
