from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from PIL import Image as PILImage

PASTA = Path(__file__).parent
RESULTADOS = PASTA / 'resultados'
PDF = PASTA / 'Lista_4_PDI_Resultados.pdf'

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='TituloLista', parent=styles['Title'], alignment=TA_CENTER,
    fontSize=22, leading=27, textColor=colors.HexColor('#17365D')
))
styles.add(ParagraphStyle(
    name='Questao', parent=styles['Heading1'], fontSize=16, leading=20,
    textColor=colors.HexColor('#17365D'), spaceAfter=8
))
styles.add(ParagraphStyle(
    name='Legenda', parent=styles['Normal'], alignment=TA_CENTER,
    fontSize=9, leading=11
))

def imagem(caminho, largura, altura):
    with PILImage.open(caminho) as im:
        w, h = im.size
    escala = min(largura / w, altura / h)
    return Image(str(caminho), width=w * escala, height=h * escala)

def bloco_imagem(caminho, legenda, largura=8*cm, altura=6*cm):
    return [imagem(caminho, largura, altura),
            Paragraph(legenda, styles['Legenda'])]

def tabela_imagens(itens, colunas, larg=8*cm, alt=6*cm):
    celulas = [bloco_imagem(c, l, larg, alt) for c, l in itens]
    linhas = []
    for i in range(0, len(celulas), colunas):
        linha = celulas[i:i+colunas]
        while len(linha) < colunas:
            linha.append('')
        linhas.append(linha)
    tabela = Table(linhas, colWidths=[(27*cm)/colunas]*colunas)
    tabela.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#BBBBBB')),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor('#DDDDDD')),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    return tabela

def cabecalho_rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(1.5*cm, 0.8*cm, 'Processamento Digital de Imagens')
    canvas.drawRightString(28.2*cm, 0.8*cm, 'Página {}'.format(doc.page))
    canvas.restoreState()

story = []
story += [Spacer(1, 2.5*cm),
          Paragraph('Processamento Digital de Imagens', styles['TituloLista']),
          Spacer(1, 0.5*cm),
          Paragraph('Lista de Exercícios 4 - Segmentação de Imagens', styles['TituloLista']),
          Spacer(1, 1.2*cm),
          Paragraph('<b>Aluno:</b> Pedro Henrique Trindade', styles['Heading2']),
          Spacer(1, 0.6*cm),
          Paragraph('Relatório dos resultados obtidos com os algoritmos de filtragem, detecção de linhas e bordas, crescimento de região e limiarização de Otsu. Todas as imagens foram processadas em níveis de cinza.', styles['BodyText']),
          PageBreak()]

story += [Paragraph('Questão 1 - Filtro de mediana', styles['Questao']),
          Paragraph('O filtro de mediana 3x3 foi aplicado três vezes consecutivas. A cada aplicação, os ruídos do tipo sal e pimenta foram reduzidos.', styles['BodyText']),
          Spacer(1, 0.3*cm),
          tabela_imagens([
              (PASTA/'circuito.tif', 'Imagem original'),
              (RESULTADOS/'q1_mediana_1.png', 'Primeira aplicação'),
              (RESULTADOS/'q1_mediana_2.png', 'Segunda aplicação'),
              (RESULTADOS/'q1_mediana_3.png', 'Terceira aplicação')
          ], 4, 6.2*cm, 10.5*cm), PageBreak()]

story += [Paragraph('Questão 2 - Detecção de pontos isolados', styles['Questao']),
          Paragraph('Foi aplicada a máscara com centro 8 e vizinhos -1. Em seguida, a resposta foi limiarizada em 100, isolando os três pontos brancos.', styles['BodyText']),
          Spacer(1, 0.4*cm),
          tabela_imagens([
              (PASTA/'pontos.png', 'Imagem original'),
              (RESULTADOS/'q2_pontos_detectados.png', 'Três pontos detectados')
          ], 2, 11*cm, 12*cm), PageBreak()]

story += [Paragraph('Questão 3 - Detecção de linhas', styles['Questao']),
          Paragraph('Foram aplicadas quatro máscaras direcionais e limiar 300. Os resultados foram combinados com operações lógicas OR.', styles['BodyText']),
          Spacer(1, 0.3*cm),
          tabela_imagens([
              (PASTA/'linhas.png', 'Imagem original'),
              (RESULTADOS/'q3_horizontal.png', 'Linhas horizontais'),
              (RESULTADOS/'q3_mais_45.png', 'Linhas em +45°'),
              (RESULTADOS/'q3_vertical.png', 'Linhas verticais'),
              (RESULTADOS/'q3_menos_45.png', 'Linhas em -45°'),
              (RESULTADOS/'q3_resultado_final.png', 'Combinação dos quatro resultados')
          ], 3, 7.5*cm, 7*cm), PageBreak()]

story += [Paragraph('Questão 4 - Detector de bordas de Canny', styles['Questao']),
          Paragraph('O detector Canny do OpenCV foi utilizado com limiar inferior 100 e superior 200.', styles['BodyText']),
          Spacer(1, 0.4*cm),
          tabela_imagens([
              (PASTA/'igreja.png', 'Imagem original'),
              (RESULTADOS/'q4_canny.png', 'Bordas detectadas pelo Canny')
          ], 2, 11*cm, 12*cm), PageBreak()]

story += [Paragraph('Questão 5 - Crescimento de região', styles['Questao']),
          Paragraph('Foi escolhida a semente (350, 105), dentro de uma célula clara, com tolerância 15. A célula encontrada foi destacada em preto.', styles['BodyText']),
          Spacer(1, 0.3*cm),
          tabela_imagens([
              (RESULTADOS/'q5_root_cinza.png', 'Imagem em níveis de cinza'),
              (RESULTADOS/'q5_mascara_regiao.png', 'Máscara da região encontrada'),
              (RESULTADOS/'q5_regiao_detectada.png', 'Célula destacada em preto')
          ], 3, 8*cm, 10*cm), PageBreak()]

story += [Paragraph('Questão 6 - Método de Otsu', styles['Questao']),
          Paragraph('O algoritmo de Otsu foi implementado pela maximização da variância entre as classes. Limiares obtidos: harewood = 146; nuts = 116; snow = 148; img_aluno = 131.', styles['BodyText']),
          Spacer(1, 0.3*cm),
          tabela_imagens([
              (RESULTADOS/'q6_harewood_cinza.png', 'Harewood - cinza'),
              (RESULTADOS/'q6_harewood_otsu.png', 'Harewood - Otsu'),
              (RESULTADOS/'q6_nuts_cinza.png', 'Nuts - cinza'),
              (RESULTADOS/'q6_nuts_otsu.png', 'Nuts - Otsu'),
              (RESULTADOS/'q6_snow_cinza.png', 'Snow - cinza'),
              (RESULTADOS/'q6_snow_otsu.png', 'Snow - Otsu')
          ], 3, 7.5*cm, 6.2*cm), PageBreak()]

story += [Paragraph('Questão 6 - Método de Otsu: img_aluno', styles['Questao']),
          Paragraph('A imagem fornecida como img_aluno foi inicialmente convertida para níveis de cinza e depois limiarizada pelo valor 131 calculado pelo algoritmo.', styles['BodyText']),
          Spacer(1, 0.4*cm),
          tabela_imagens([
              (RESULTADOS/'q6_img_aluno_cinza.png', 'img_aluno em níveis de cinza'),
              (RESULTADOS/'q6_img_aluno_otsu.png', 'img_aluno após Otsu')
          ], 2, 10.5*cm, 13*cm)]

doc = SimpleDocTemplate(
    str(PDF), pagesize=landscape(A4),
    rightMargin=1.2*cm, leftMargin=1.2*cm,
    topMargin=1.2*cm, bottomMargin=1.2*cm,
    title='Lista de Exercícios 4 - Segmentação de Imagens',
    author='Pedro Henrique Trindade'
)
doc.build(story, onFirstPage=cabecalho_rodape, onLaterPages=cabecalho_rodape)
print(PDF)
