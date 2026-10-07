import cv2
import numpy as np
from pathlib import Path


def converter_para_cinza(img_colorida):
    """Converte uma imagem BGR para cinza pela media dos tres canais."""
   
    img_float = img_colorida.astype(np.float32)

    azul = img_float[:, :, 0]
    verde = img_float[:, :, 1]
    vermelho = img_float[:, :, 2]

    cinza = (vermelho + verde + azul) / 3

    # Retorna ao formato de imagem com valores inteiros de 0 a 255.
    return cinza.astype(np.uint8)


def encontrar_imagem(nome_base):
    """Aceita um nome com extensao ou procura extensoes comuns."""
    caminho = Path(nome_base)
    if caminho.is_file():
        return caminho

    for extensao in (".png", ".jpg", ".jpeg", ".bmp"):
        candidato = Path(f"{nome_base}{extensao}")
        if candidato.is_file():
            return candidato

    return None


def processar_imagem(nome_base):
    caminho = encontrar_imagem(nome_base)
    if caminho is None:
        print(f"Imagem nao encontrada: {nome_base}")
        return

    img = cv2.imread(str(caminho), cv2.IMREAD_COLOR)
    if img is None:
        print(f"Nao foi possivel abrir a imagem: {caminho}")
        return

    img_cinza = converter_para_cinza(img)
    caminho_saida = caminho.with_name(f"{caminho.stem}_cinza.png")
    cv2.imwrite(str(caminho_saida), img_cinza)

    cv2.imshow(f"Original - {caminho.name}", img)
    cv2.imshow(f"Cinza - {caminho.name}", img_cinza)
    print(f"Imagem em niveis de cinza salva em: {caminho_saida}")



if __name__ == "__main__":
    # As imagens devem estar na mesma pasta deste programa.
    processar_imagem("lena.png")
    processar_imagem("img_aluno")

    cv2.waitKey(0)
    cv2.destroyAllWindows()
