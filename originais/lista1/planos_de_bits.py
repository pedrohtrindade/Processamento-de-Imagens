import cv2

def cinza(img):
    c = img[:, :, 0]//3 + img[:, :, 1]//3 + img[:, :, 2]//3
    return c

def planos_bits(img):
    planos = []
    for i in range(8):
        plano = ((img >> i) & 1) * 255
        planos.append(plano)
    return planos

img1 = cv2.imread('lena.png')
img2 = cv2.imread('img_aluno.jpeg')

c1 = cinza(img1)
c2 = cinza(img2)

planos1 = planos_bits(c1)
planos2 = planos_bits(c2)

cv2.imshow('Lena em niveis de cinza', c1)
cv2.imshow('Imagem aluno em niveis de cinza', c2)

for i in range(8):
    cv2.imshow('Lena - plano de bit {}'.format(i), planos1[i])
    cv2.imshow('Imagem aluno - plano de bit {}'.format(i), planos2[i])

    cv2.imwrite('lena_bit_{}.png'.format(i), planos1[i])
    cv2.imwrite('img_aluno_bit_{}.png'.format(i), planos2[i])

cv2.waitKey(0)
cv2.destroyAllWindows()
