import cv2
import numpy as np

def cinza(img):
    c = img[:, :, 0]//3 + img[:, :, 1]//3 + img[:, :, 2]//3
    return c

def histograma(img):
    h = np.zeros(256)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            h[img[i, j]] += 1
    return h

def histograma_acumulado(img):
    h = histograma(img)
    ha = np.zeros(256)
    ha[0] = h[0]
    for i in range(1, 256):
        ha[i] = ha[i - 1] + h[i]
    return ha

def equalizacao(img):
    ha = histograma_acumulado(img)
    ha_min = ha[ha > 0].min()
    total = img.size

    tabela = ((ha - ha_min) / (total - ha_min)) * 255
    tabela = np.clip(tabela, 0, 255)
    tabela = tabela.astype(np.uint8)

    img_equalizada = tabela[img]
    return img_equalizada



if __name__ == "__main__":
    img1 = cv2.imread('lena.png')
    img2 = cv2.imread('unequalized.jpg')
    img3 = cv2.imread('img_aluno.jpeg')

    c1 = cinza(img1)
    c2 = cinza(img2)
    c3 = cinza(img3)

    e1 = equalizacao(c1)
    e2 = equalizacao(c2)
    e3 = equalizacao(c3)

    cv2.imshow('Lena original', c1)
    cv2.imshow('Lena equalizada', e1)
    cv2.imshow('Unequalized original', c2)
    cv2.imshow('Unequalized equalizada', e2)
    cv2.imshow('Imagem aluno original', c3)
    cv2.imshow('Imagem aluno equalizada', e3)

    cv2.imwrite('lena_equalizada.png', e1)
    cv2.imwrite('unequalized_equalizada.png', e2)
    cv2.imwrite('img_aluno_equalizada.png', e3)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
