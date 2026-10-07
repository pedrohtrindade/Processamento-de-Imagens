import cv2
import numpy as np

def normalizacao(img, c, d):
    a = img.min()
    b = img.max()
    img = (img - a) * ((d - c) / (b - a)) + c
    img = img.astype(np.uint8)
    return img



if __name__ == "__main__":
    img1 = cv2.imread('lena.png')
    img2 = cv2.imread('img_aluno.jpeg')

    n1 = normalizacao(img1, 0, 100)
    n2 = normalizacao(img2, 0, 100)

    cv2.imshow('Lena original', img1)
    cv2.imshow('Lena normalizada', n1)
    cv2.imshow('Imagem aluno original', img2)
    cv2.imshow('Imagem aluno normalizada', n2)

    cv2.imwrite('lena_normalizada.png', n1)
    cv2.imwrite('img_aluno_normalizada.png', n2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
