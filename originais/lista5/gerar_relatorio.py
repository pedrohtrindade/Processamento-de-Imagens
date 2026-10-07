from pathlib import Path

import cv2 as cv
import numpy as np
from PIL import Image
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


BASE = Path(__file__).resolve().parent
SAIDA = BASE / "Lista5_PDI_Resultados.pdf"
LARGURA, ALTURA = A4

AZUL = HexColor("#17365D")
AZUL_CLARO = HexColor("#EAF1F8")
CINZA = HexColor("#555555")
FUNDO = HexColor("#F7F9FC")


def cabecalho(pdf, titulo, numero):
    pdf.setFillColor(AZUL)
    pdf.rect(0, ALTURA - 2.0 * cm, LARGURA, 2.0 * cm, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(1.5 * cm, ALTURA - 1.25 * cm, titulo)
    pdf.setFillColor(CINZA)
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(LARGURA - 1.4 * cm, 0.8 * cm, f"Lista 5 - pagina {numero}")


def texto(pdf, conteudo, x, y, tamanho=10, cor=CINZA):
    pdf.setFillColor(cor)
    pdf.setFont("Helvetica", tamanho)
    pdf.drawString(x, y, conteudo)


def imagem_ajustada(pdf, caminho, x, y, largura, altura, moldura=True):
    with Image.open(caminho) as im:
        iw, ih = im.size

    escala = min(largura / iw, altura / ih)
    w = iw * escala
    h = ih * escala
    px = x + (largura - w) / 2
    py = y + (altura - h) / 2

    if moldura:
        pdf.setStrokeColor(HexColor("#C9D2DC"))
        pdf.setFillColor(FUNDO)
        pdf.roundRect(x, y, largura, altura, 6, fill=1, stroke=1)

    pdf.drawImage(str(caminho), px, py, w, h, preserveAspectRatio=True, mask="auto")


def painel_imagem(pdf, caminho, legenda, x, y, largura, altura):
    texto(pdf, legenda, x, y + altura + 0.18 * cm, 9, AZUL)
    imagem_ajustada(pdf, caminho, x, y, largura, altura)


def desenhar_grade(pdf, matriz, x, y, largura, altura, legenda):
    linhas, colunas = matriz.shape
    celula = min(largura / colunas, altura / linhas)
    gw = colunas * celula
    gh = linhas * celula
    gx = x + (largura - gw) / 2
    gy = y + (altura - gh) / 2

    texto(pdf, legenda, x, y + altura + 0.1 * cm, 9, AZUL)

    for lin in range(linhas):
        for col in range(colunas):
            px = gx + col * celula
            py = gy + (linhas - 1 - lin) * celula
            pdf.setFillColor(HexColor("#777777") if matriz[lin, col] else white)
            pdf.setStrokeColor(HexColor("#B5B5B5"))
            pdf.rect(px, py, celula, celula, fill=1, stroke=1)


pdf = canvas.Canvas(str(SAIDA), pagesize=A4)
pdf.setTitle("Lista de Exercicios 5 - Morfologia Matematica")

# Capa
pdf.setFillColor(AZUL)
pdf.rect(0, 0, LARGURA, ALTURA, fill=1, stroke=0)
pdf.setFillColor(white)
pdf.setFont("Helvetica-Bold", 25)
pdf.drawCentredString(LARGURA / 2, ALTURA - 7.0 * cm, "Processamento Digital de Imagens")
pdf.setFont("Helvetica-Bold", 21)
pdf.drawCentredString(LARGURA / 2, ALTURA - 9.0 * cm, "Lista de Exercicios 5")
pdf.setFont("Helvetica", 16)
pdf.drawCentredString(LARGURA / 2, ALTURA - 10.2 * cm, "Morfologia Matematica")
pdf.setFillColor(HexColor("#BFD7EE"))
pdf.roundRect(4.0 * cm, ALTURA - 16.0 * cm, LARGURA - 8.0 * cm, 2.2 * cm, 10, fill=1, stroke=0)
pdf.setFillColor(AZUL)
pdf.setFont("Helvetica-Bold", 12)
pdf.drawCentredString(LARGURA / 2, ALTURA - 14.9 * cm, "Resultados das questoes 1 a 7")
pdf.setFillColor(white)
pdf.setFont("Helvetica", 10)
pdf.drawCentredString(LARGURA / 2, 2.0 * cm, "Imagens carregadas em niveis de cinza")
pdf.showPage()

# Questao 1
cabecalho(pdf, "Questao 1 - Resolucao manual", 2)
texto(pdf, "Aplicacao dos elementos estruturantes 3 x 3 sobre a Figura 1.", 1.5 * cm, ALTURA - 2.7 * cm)

original = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
], dtype=np.uint8)

se_a = np.ones((3, 3), np.uint8)
se_b = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)

resultados_q1 = [
    (cv.erode(original, se_a, borderType=cv.BORDER_CONSTANT, borderValue=0), "i) Erosao com SE (a)"),
    (cv.erode(original, se_b, borderType=cv.BORDER_CONSTANT, borderValue=0), "ii) Erosao com SE (b)"),
    (cv.dilate(original, se_a, borderType=cv.BORDER_CONSTANT, borderValue=0), "iii) Dilatacao com SE (a)"),
    (cv.dilate(original, se_b, borderType=cv.BORDER_CONSTANT, borderValue=0), "iv) Dilatacao com SE (b)"),
]

posicoes = [
    (1.3 * cm, 15.2 * cm), (10.5 * cm, 15.2 * cm),
    (1.3 * cm, 7.0 * cm), (10.5 * cm, 7.0 * cm),
]

for (matriz, legenda), (x, y) in zip(resultados_q1, posicoes):
    desenhar_grade(pdf, matriz, x, y, 8.0 * cm, 5.9 * cm, legenda)

texto(pdf, "As celulas cinza representam os pixels de primeiro plano apos cada operacao.",
      1.5 * cm, 2.0 * cm, 9)
pdf.showPage()

# Questao 2
cabecalho(pdf, "Questao 2 - Erosao e restauracao", 3)
texto(pdf, "Elemento estruturante quadrado de 51 x 51 pixels: maior que 40 e menor que 60.",
      1.5 * cm, ALTURA - 2.8 * cm)
painel_imagem(pdf, BASE / "imagens" / "quadrados.png", "Imagem original", 1.3 * cm, 15.4 * cm, 5.8 * cm, 7.0 * cm)
painel_imagem(pdf, BASE / "resultados" / "q2_erosao.png", "Apos erosao", 7.6 * cm, 15.4 * cm, 5.8 * cm, 7.0 * cm)
painel_imagem(pdf, BASE / "resultados" / "q2_restaurada.png", "Apos dilatacao", 13.9 * cm, 15.4 * cm, 5.8 * cm, 7.0 * cm)
pdf.setFillColor(AZUL_CLARO)
pdf.roundRect(1.5 * cm, 7.0 * cm, LARGURA - 3.0 * cm, 5.8 * cm, 8, fill=1, stroke=0)
texto(pdf, "Resultado", 2.0 * cm, 11.6 * cm, 12, AZUL)
texto(pdf, "- Os quadrados de 20 e 40 pixels desapareceram na erosao.", 2.0 * cm, 10.6 * cm)
texto(pdf, "- A dilatacao restaurou os quadrados de 60 e 80 pixels ao tamanho original.", 2.0 * cm, 9.7 * cm)
texto(pdf, "- A operacao completa corresponde a uma abertura morfologica.", 2.0 * cm, 8.8 * cm)
pdf.showPage()

# Questao 3
cabecalho(pdf, "Questao 3 - Abertura e fechamento", 4)
texto(pdf, "Elemento estruturante quadrado de 15 x 15 pixels.", 1.5 * cm, ALTURA - 2.8 * cm)
painel_imagem(pdf, BASE / "imagens" / "ruidos.png", "Imagem original", 1.3 * cm, 15.0 * cm, 5.8 * cm, 8.0 * cm)
painel_imagem(pdf, BASE / "resultados" / "q3_abertura.png", "Abertura", 7.6 * cm, 15.0 * cm, 5.8 * cm, 8.0 * cm)
painel_imagem(pdf, BASE / "resultados" / "q3_fechamento.png", "Fechamento", 13.9 * cm, 15.0 * cm, 5.8 * cm, 8.0 * cm)
texto(pdf, "A abertura remove os pequenos objetos brancos do fundo.", 1.6 * cm, 12.2 * cm, 10)
texto(pdf, "O fechamento preenche os pequenos buracos pretos no objeto principal.", 1.6 * cm, 11.2 * cm, 10)
pdf.showPage()

# Questao 4
cabecalho(pdf, "Questao 4 - Extracao de fronteiras", 5)
texto(pdf, "Fronteira interna: A - (A erodido).  Fronteira externa: (A dilatado) - A.",
      1.5 * cm, ALTURA - 2.8 * cm)
painel_imagem(pdf, BASE / "imagens" / "cachorro.png", "Imagem original", 1.3 * cm, 11.0 * cm, 5.8 * cm, 12.0 * cm)
painel_imagem(pdf, BASE / "resultados" / "q4_fronteira_interna.png", "Fronteira interna", 7.6 * cm, 11.0 * cm, 5.8 * cm, 12.0 * cm)
painel_imagem(pdf, BASE / "resultados" / "q4_fronteira_externa.png", "Fronteira externa", 13.9 * cm, 11.0 * cm, 5.8 * cm, 12.0 * cm)
pdf.showPage()

# Questao 5
cabecalho(pdf, "Questao 5 - Preenchimento de regiao", 6)
texto(pdf, "Semente utilizada: ponto (150, 180), localizado dentro do corpo do gato.",
      1.5 * cm, ALTURA - 2.8 * cm)
painel_imagem(pdf, BASE / "imagens" / "gato.png", "Bordas originais", 1.5 * cm, 7.0 * cm, 8.5 * cm, 16.0 * cm)
painel_imagem(pdf, BASE / "resultados" / "q5_gato_preenchido.png", "Regiao preenchida", 11.0 * cm, 7.0 * cm, 8.5 * cm, 16.0 * cm)
texto(pdf, "A dilatacao geodesica e repetida ate que nenhuma nova regiao seja acrescentada.",
      1.5 * cm, 5.6 * cm, 9)
pdf.showPage()

# Questao 6
cabecalho(pdf, "Questao 6 - Componente conectado", 7)
texto(pdf, "Ponto inicial usado no resultado: (316, 261), dentro de um quadrado de 80 x 80 pixels.",
      1.5 * cm, ALTURA - 2.8 * cm)
painel_imagem(pdf, BASE / "imagens" / "quadrados.png", "Imagem original", 1.5 * cm, 7.0 * cm, 8.5 * cm, 16.0 * cm)
painel_imagem(pdf, BASE / "resultados" / "q6_componente_amarelo.png", "Componente extraido em amarelo", 11.0 * cm, 7.0 * cm, 8.5 * cm, 16.0 * cm)
texto(pdf, "O programa solicita ao usuario as coordenadas x e y e percorre os vizinhos conectados.",
      1.5 * cm, 5.6 * cm, 9)
pdf.showPage()

# Questao 7
cabecalho(pdf, "Questao 7 - Morfologia na img_aluno", 8)
texto(pdf, "Imagem carregada em niveis de cinza. Elemento estruturante quadrado de 5 x 5 pixels.",
      1.5 * cm, ALTURA - 2.8 * cm)

itens_q7 = [
    (BASE / "resultados" / "q7_img_aluno_cinza.png", "Imagem em cinza"),
    (BASE / "resultados" / "q7_dilatacao.png", "Dilatacao"),
    (BASE / "resultados" / "q7_erosao.png", "Erosao"),
    (BASE / "resultados" / "q7_gradiente.png", "Gradiente = dilatacao - erosao"),
]
posicoes_q7 = [
    (1.4 * cm, 14.7 * cm), (10.7 * cm, 14.7 * cm),
    (1.4 * cm, 3.0 * cm), (10.7 * cm, 3.0 * cm),
]

for (caminho, legenda), (x, y) in zip(itens_q7, posicoes_q7):
    painel_imagem(pdf, caminho, legenda, x, y, 8.8 * cm, 9.6 * cm)

pdf.save()
print("PDF gerado em:", SAIDA)
