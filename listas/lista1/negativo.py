import cv2

def negativo(img):
    c = 255 - img  # Correção: intensidade máxima de uma imagem uint8.
    return c



if __name__ == "__main__":
    img1 = cv2.imread('lena.png')
    img2 = cv2.imread('img_aluno.jpeg')

    n1 = negativo(img1)
    n2 = negativo(img2)

    cv2.imshow('Lena original', img1)
    cv2.imshow('Lena negativo', n1)
    cv2.imshow('Imagem aluno original', img2)
    cv2.imshow('Imagem aluno negativo', n2)

    cv2.imwrite('lena_negativo.png', n1)
    cv2.imwrite('img_aluno_negativo.png', n2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
