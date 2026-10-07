import cv2
import numpy as np

def filtro_media(img, tamanho):
    margem = tamanho // 2
    img_borda = np.pad(img, margem, mode='constant')
    resultado = np.zeros(img.shape)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            vizinhanca = img_borda[i:i+tamanho, j:j+tamanho]
            resultado[i, j] = vizinhanca.sum() / (tamanho * tamanho)

    resultado = resultado.astype(np.uint8)
    return resultado



if __name__ == "__main__":
    img1 = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread('img_aluno.jpeg', cv2.IMREAD_GRAYSCALE)

    tamanho_janela = 3
    suavizada1 = filtro_media(img1, tamanho_janela)
    suavizada2 = filtro_media(img2, tamanho_janela)

    cv2.imshow('Imagem original', img1)
    cv2.imshow('Filtro da media {}x{}'.format(tamanho_janela, tamanho_janela), suavizada1)
    cv2.imwrite('lena_media_{}x{}.png'.format(tamanho_janela, tamanho_janela), suavizada1)

    cv2.imshow('Imagem original', img2)
    cv2.imshow('Filtro da media {}x{}'.format(tamanho_janela, tamanho_janela), suavizada2)
    cv2.imwrite('aluno_media_{}x{}.png'.format(tamanho_janela, tamanho_janela), suavizada2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
