"""Liga a interface às funções das listas e aos complementos do trabalho.

Os algoritmos das listas não são reescritos aqui. Seus arquivos estão em listas/.
"""
import numpy as np
from listas.lista1.conversao_niveis_cinza import converter_para_cinza as cinza_lista
from listas.lista1.negativo import negativo as negativo_lista
from listas.lista1.exercicio7_histogramas import histograma
from listas.lista2.filtro_media import filtro_media as media_lista
from listas.lista2.filtro_mediana import filtro_mediana as mediana_lista
from listas.lista4.questao6_otsu import otsu as otsu_lista
from complementos import (validar_imagem, validar_tamanho, canny, erosao,
                          dilatacao, abertura, fechamento, diametro,
                          rotular_componentes)


def converter_para_cinza(img):
    validar_imagem(img)
    if img.ndim == 2:
        return img.copy()
    return cinza_lista(img)


def negativo(img):
    validar_imagem(img)
    return negativo_lista(img)


def otsu(img):
    cinza = converter_para_cinza(img)
    return otsu_lista(cinza)


def filtro_media(img, tamanho=3):
    validar_imagem(img)
    tamanho = validar_tamanho(tamanho)
    if img.ndim == 2:
        return media_lista(img, tamanho)
    # A função original trabalha com um canal. Chamamos para cada cor.
    azul = media_lista(img[:, :, 0], tamanho)
    verde = media_lista(img[:, :, 1], tamanho)
    vermelho = media_lista(img[:, :, 2], tamanho)
    return np.stack([azul, verde, vermelho], axis=2)


def filtro_mediana(img, tamanho=3):
    validar_imagem(img)
    tamanho = validar_tamanho(tamanho)
    if img.ndim == 2:
        return mediana_lista(img, tamanho)
    azul = mediana_lista(img[:, :, 0], tamanho)
    verde = mediana_lista(img[:, :, 1], tamanho)
    vermelho = mediana_lista(img[:, :, 2], tamanho)
    return np.stack([azul, verde, vermelho], axis=2)


OPERACOES = ('Original', 'Cinza', 'Negativo', 'Otsu', 'Média', 'Mediana',
             'Canny', 'Erosão', 'Dilatação', 'Abertura', 'Fechamento')


def processar(img, operacao, tamanho=3, baixo=50, alto=150):
    validar_imagem(img)
    if operacao == 'Original':
        return img.copy(), 'Imagem original'
    if operacao == 'Cinza':
        return converter_para_cinza(img), 'Cinza pela função original da Lista 1'
    if operacao == 'Negativo':
        return negativo(img), 'Negativo da Lista 1: correção de 250 para 255'
    if operacao == 'Otsu':
        resultado, limiar = otsu(img)
        return resultado, f'Otsu da Lista 4: limiar automático = {limiar}'
    if operacao == 'Média':
        return filtro_media(img, tamanho), f'Média da Lista 2: janela {tamanho} x {tamanho}'
    if operacao == 'Mediana':
        return filtro_mediana(img, tamanho), f'Mediana da Lista 2: janela {tamanho} x {tamanho}'
    if operacao == 'Canny':
        return canny(img, baixo, alto), f'Canny próprio (complemento): {baixo} / {alto}'
    if operacao == 'Erosão':
        return erosao(img, tamanho), f'Erosão própria: elemento {tamanho} x {tamanho}'
    if operacao == 'Dilatação':
        return dilatacao(img, tamanho), f'Dilatação própria: elemento {tamanho} x {tamanho}'
    if operacao == 'Abertura':
        return abertura(img, tamanho), f'Abertura: elemento {tamanho} x {tamanho}'
    if operacao == 'Fechamento':
        return fechamento(img, tamanho), f'Fechamento: elemento {tamanho} x {tamanho}'
    raise ValueError('Operação desconhecida.')
