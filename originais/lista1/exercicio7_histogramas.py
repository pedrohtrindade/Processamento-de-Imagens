import cv2
import numpy as np
import matplotlib.pyplot as plt

def cinza(img):
    c = img[:, :, 0]//3 + img[:, :, 1]//3 + img[:, :, 2]//3
    return c

def histograma(img):
    h = np.zeros(256)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            h[img[i, j]] += 1
    return h

def histograma_normalizado(img):
    h = histograma(img)
    hn = h / img.size
    return hn

def histograma_acumulado(img):
    h = histograma(img)
    ha = np.zeros(256)
    ha[0] = h[0]
    for i in range(1, 256):
        ha[i] = ha[i - 1] + h[i]
    return ha

def histograma_acumulado_normalizado(img):
    ha = histograma_acumulado(img)
    han = ha / img.size
    return han

def mostrar_quatro_histogramas(img, titulo, arquivo):
    h = histograma(img)
    hn = histograma_normalizado(img)
    ha = histograma_acumulado(img)
    han = histograma_acumulado_normalizado(img)

    plt.figure(figsize=(12, 8))
    plt.suptitle(titulo)

    plt.subplot(2, 2, 1)
    plt.bar(range(256), h)
    plt.title('Histograma')

    plt.subplot(2, 2, 2)
    plt.bar(range(256), hn)
    plt.title('Histograma normalizado')

    plt.subplot(2, 2, 3)
    plt.bar(range(256), ha)
    plt.title('Histograma acumulado')

    plt.subplot(2, 2, 4)
    plt.bar(range(256), han)
    plt.title('Histograma acumulado normalizado')

    plt.tight_layout()
    plt.savefig(arquivo)


img1 = cv2.imread('unequalized.jpg')
c1 = cinza(img1)
mostrar_quatro_histogramas(c1, 'Unequalized', 'histogramas_unequalized.png')


img2 = cv2.imread('img_aluno.jpeg')

plt.figure(figsize=(10, 6))
plt.plot(histograma(img2[:, :, 0]), color='blue', label='B')
plt.plot(histograma(img2[:, :, 1]), color='green', label='G')
plt.plot(histograma(img2[:, :, 2]), color='red', label='R')
plt.title('Histogramas B, G e R - img_aluno')
plt.xlabel('Intensidade')
plt.ylabel('Frequencia')
plt.legend()
plt.savefig('histogramas_bgr_img_aluno.png')


c2 = cinza(img2)
mostrar_quatro_histogramas(c2, 'Img_aluno', 'histogramas_img_aluno.png')

plt.show()
