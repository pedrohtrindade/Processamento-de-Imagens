import cv2
import numpy as np

def prewitt(img):
    mascara_x = np.array([[-1, 0, 1],
                          [-1, 0, 1],
                          [-1, 0, 1]])

    mascara_y = np.array([[-1, -1, -1],
                          [0, 0, 0],
                          [1, 1, 1]])

    img_borda = np.pad(img, 1, mode='constant')
    resultado = np.zeros(img.shape)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            vizinhanca = img_borda[i:i+3, j:j+3]

            gx = (vizinhanca * mascara_x).sum()
            gy = (vizinhanca * mascara_y).sum()

            resultado[i, j] = abs(gx) + abs(gy)

    resultado = np.clip(resultado, 0, 255)
    resultado = resultado.astype(np.uint8)
    return resultado



if __name__ == "__main__":
    img1 = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread('img_aluno.jpeg', cv2.IMREAD_GRAYSCALE)

    bordas1 = prewitt(img1)
    bordas2 = prewitt(img2)
    cv2.imshow('Imagem original', img1)
    cv2.imshow('Detector de Prewitt', bordas1)

    cv2.imwrite('lena_prewitt.png', bordas1)

    cv2.imshow('Imagem original', img2)
    cv2.imshow('Detector de Prewitt', bordas2)

    cv2.imwrite('aluno_prewitt.png', bordas2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
