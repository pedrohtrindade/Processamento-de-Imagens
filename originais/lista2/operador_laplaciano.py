import cv2
import numpy as np

def laplaciano(img):
    mascara = np.array([[0, -1, 0],
                        [-1, 4, -1],
                        [0, -1, 0]])

    img_borda = np.pad(img, 1, mode='constant')
    resultado = np.zeros(img.shape)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            vizinhanca = img_borda[i:i+3, j:j+3]
            resultado[i, j] = (vizinhanca * mascara).sum()

    resultado = np.abs(resultado)
    resultado = np.clip(resultado, 0, 255)
    resultado = resultado.astype(np.uint8)
    return resultado

img1 = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('img_aluno.jpeg', cv2.IMREAD_GRAYSCALE)

bordas1 = laplaciano(img1)
bordas2 = laplaciano(img2)

cv2.imshow('Imagem original', img1)
cv2.imshow('Operador Laplaciano', bordas1)

cv2.imwrite('lena_laplaciano.png', bordas1)

cv2.imshow('Imagem original', img2)
cv2.imshow('Operador Laplaciano', bordas2)

cv2.imwrite('aluno_laplaciano.png', bordas2)

cv2.waitKey(0)
cv2.destroyAllWindows()
