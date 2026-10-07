import cv2
import numpy as np

def potencia(img, c, gama):
    img = img.astype(np.float32) / 255
    img = c * (img ** gama)
    img = img * 255
    img = np.clip(img, 0, 255)
    img = img.astype(np.uint8)
    return img

img1 = cv2.imread('lena.png')
img2 = cv2.imread('img_aluno.jpeg')

p1 = potencia(img1, 2, 2)
p2 = potencia(img2, 2, 2)

cv2.imshow('Lena original', img1)
cv2.imshow('Lena operador de potencia', p1)
cv2.imshow('Imagem aluno original', img2)
cv2.imshow('Imagem aluno operador de potencia', p2)

cv2.imwrite('lena_potencia.png', p1)
cv2.imwrite('img_aluno_potencia.png', p2)

cv2.waitKey(0)
cv2.destroyAllWindows()
