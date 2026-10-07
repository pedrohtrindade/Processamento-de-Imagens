import cv2
import numpy as np

def filtro_k_vizinhos(img, tamanho, k):
    margem = tamanho // 2
    img_borda = np.pad(img, margem, mode='constant')
    resultado = np.zeros(img.shape)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            vizinhanca = img_borda[i:i+tamanho, j:j+tamanho].flatten()

            centro = img[i, j]
            posicao_centro = (tamanho * tamanho) // 2
            vizinhos = np.delete(vizinhanca, posicao_centro)

            diferencas = np.abs(vizinhos.astype(np.int16) - int(centro))
            indices = np.argsort(diferencas)
            mais_proximos = vizinhos[indices[:k]]

            resultado[i, j] = mais_proximos.mean()

    resultado = resultado.astype(np.uint8)
    return resultado

img1 = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('img_aluno.jpeg', cv2.IMREAD_GRAYSCALE)

tamanho_janela = 5
k = 9

suavizada1 = filtro_k_vizinhos(img1, tamanho_janela, k)
suavizada2 = filtro_k_vizinhos(img2, tamanho_janela, k)


cv2.imshow('Imagem original', img1)
cv2.imshow('Media dos {} vizinhos mais proximos'.format(k), suavizada1)

cv2.imwrite('lena_k_vizinhos.png', suavizada1)

cv2.imshow('Imagem original', img2)
cv2.imshow('Media dos {} vizinhos mais proximos'.format(k), suavizada2)

cv2.imwrite('aluno_k_vizinhos.png', suavizada2)

cv2.waitKey(0)
cv2.destroyAllWindows()
