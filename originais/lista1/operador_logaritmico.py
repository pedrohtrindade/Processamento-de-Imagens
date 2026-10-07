import cv2
import numpy as np

def logaritmico(img):
    img = img.astype(np.float32)
    r = img.max()
    c = 255 / np.log(1 + r)
    img = c * np.log(1 + img)
    img = img.astype(np.uint8)
    return img

img1 = cv2.imread('lena.png')
img2 = cv2.imread('img_aluno.jpeg')

l1 = logaritmico(img1)
l2 = logaritmico(img2)

cv2.imshow('Lena original', img1)
cv2.imshow('Lena operador logaritmico', l1)
cv2.imshow('Imagem aluno original', img2)
cv2.imshow('Imagem aluno operador logaritmico', l2)

cv2.imwrite('lena_logaritmico.png', l1)
cv2.imwrite('img_aluno_logaritmico.png', l2)

cv2.waitKey(0)
cv2.destroyAllWindows()
