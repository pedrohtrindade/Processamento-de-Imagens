"""Verificações reproduzíveis: python testar_algoritmos.py (sem câmera)."""
import itertools
import math
import unittest
import numpy as np
import cv2
import processamento as pdi
from video import processar_frame, GatilhoPresenca, criar_rastreador


class TestesPDI(unittest.TestCase):
    def test_cinza_negativo_histograma(self):
        img = np.array([[[0, 0, 0], [255, 255, 255], [10, 20, 30]]], np.uint8)
        np.testing.assert_array_equal(pdi.converter_para_cinza(img), [[0, 255, 20]])
        np.testing.assert_array_equal(pdi.negativo(np.array([[0, 250, 255]], np.uint8)), [[255, 5, 0]])
        h = pdi.histograma(pdi.converter_para_cinza(img))
        self.assertEqual(h.sum(), 3)
        self.assertEqual(h[255], 1)

    def test_otsu(self):
        rng = np.random.default_rng(42)
        for img in [np.zeros((3, 4), np.uint8), np.full((4, 5), 255, np.uint8),
                    np.array([[0, 0, 255, 255]], np.uint8),
                    rng.integers(0, 256, (60, 80), dtype=np.uint8)]:
            binaria, limiar = pdi.otsu(img)
            referencia, esperada = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            self.assertEqual(limiar, referencia)
            np.testing.assert_array_equal(binaria, esperada)

    def test_filtros_preservam_lista(self):
        img = np.array([[0, 10, 20], [30, 200, 50], [60, 70, 80]], np.uint8)
        media = pdi.filtro_media(img, 3)
        mediana = pdi.filtro_mediana(img, 3)
        self.assertEqual(media[1, 1], int(img.sum() / 9))
        self.assertEqual(mediana[1, 1], 50)
        self.assertEqual(mediana[0, 0], 0)  # borda zero da lista
        bgr = np.stack([img, img, img], axis=2)
        np.testing.assert_array_equal(pdi.filtro_media(bgr)[:, :, 0], media)
        np.testing.assert_array_equal(pdi.filtro_mediana(bgr)[:, :, 1], mediana)
        np.testing.assert_array_equal(pdi.filtro_media(img, 1), img)
        with self.assertRaises(ValueError):
            pdi.filtro_mediana(img, 4)

    def test_morfologia_comparada(self):
        rng = np.random.default_rng(42)
        for img in [rng.integers(0, 256, (14, 18), dtype=np.uint8),
                    (rng.integers(0, 2, (20, 24), dtype=np.uint8) * 255)]:
            for tamanho in (1, 3, 5):
                elemento = np.ones((tamanho, tamanho), np.uint8)
                np.testing.assert_array_equal(pdi.erosao(img, tamanho), cv2.erode(img, elemento))
                np.testing.assert_array_equal(pdi.dilatacao(img, tamanho), cv2.dilate(img, elemento))
                np.testing.assert_array_equal(pdi.abertura(img, tamanho), cv2.morphologyEx(img, cv2.MORPH_OPEN, elemento))
                np.testing.assert_array_equal(pdi.fechamento(img, tamanho), cv2.morphologyEx(img, cv2.MORPH_CLOSE, elemento))

    def test_canny(self):
        for valor in (0, 128, 255):
            self.assertFalse(pdi.canny(np.full((20, 30), valor, np.uint8)).any())
        img = np.zeros((80, 90), np.uint8)
        img[20:60, 25:65] = 255
        bordas = pdi.canny(img, 50, 150)
        self.assertGreater(np.count_nonzero(bordas), 100)
        self.assertEqual(bordas[40, 45], 0)
        self.assertTrue(set(np.unique(bordas)).issubset({0, 255}))
        self.assertGreater(np.count_nonzero(bordas[19:22, 30:60]), 20)
        # Degraus diagonais: valida direções distintas da supressão.
        y, x = np.indices((50, 50))
        for mascara in (x > y, x+y > 50):
            imagem = mascara.astype(np.uint8) * 255
            borda = pdi.canny(imagem)
            self.assertGreater(np.count_nonzero(borda), 30)
        for shape in ((1, 1), (1, 8), (8, 1), (2, 2)):
            self.assertEqual(pdi.canny(np.zeros(shape, np.uint8)).shape, shape)
        with self.assertRaises(ValueError):
            pdi.canny(img, 150, 50)

    def test_componentes_medidas(self):
        img = np.zeros((12, 14), np.uint8)
        img[1:3, 1:4] = 255  # retângulo 2x3
        img[6:9, 6:9] = 255
        img[7, 7] = 0  # anel 3x3
        img[11, 13] = 255
        rotulos, objetos, visual = pdi.rotular_componentes(img)
        self.assertEqual(len(objetos), 3)
        self.assertEqual((objetos[0]['area'], objetos[0]['perimetro']), (6, 10))
        self.assertAlmostEqual(objetos[0]['diametro'], math.sqrt(5))
        self.assertEqual((objetos[1]['area'], objetos[1]['perimetro']), (8, 16))
        self.assertAlmostEqual(objetos[1]['diametro'], math.sqrt(8))
        self.assertEqual((objetos[2]['area'], objetos[2]['perimetro'], objetos[2]['diametro']), (1, 4, 0))
        self.assertEqual(rotulos[7, 7], 0)
        self.assertEqual(visual.shape, (12, 14, 3))
        rotulos, objetos, _ = pdi.rotular_componentes(img, area_minima=7)
        self.assertEqual(len(objetos), 1)
        self.assertEqual(set(np.unique(rotulos)), {0, 1})

    def test_conectividade_e_bordas(self):
        img = np.eye(3, dtype=np.uint8)*255
        self.assertEqual(len(pdi.rotular_componentes(img, 4)[1]), 3)
        self.assertEqual(len(pdi.rotular_componentes(img, 8)[1]), 1)
        self.assertEqual(len(pdi.rotular_componentes(np.zeros((4, 4), np.uint8))[1]), 0)
        cheio = pdi.rotular_componentes(np.full((2, 3), 255, np.uint8))[1][0]
        self.assertEqual((cheio['area'], cheio['perimetro']), (6, 10))
        with self.assertRaises(ValueError):
            pdi.rotular_componentes(np.full((4, 4), 100, np.uint8))

    def test_rotulos_comparados_opencv(self):
        rng = np.random.default_rng(99)
        for conexao in (4, 8):
            for _ in range(8):
                img = (rng.random((30, 40)) > 0.7).astype(np.uint8) * 255
                n, rotulos, stats, _ = cv2.connectedComponentsWithStats(img, connectivity=conexao)
                nossos, objetos, _ = pdi.rotular_componentes(img, conexao)
                self.assertEqual(len(objetos), n-1)
                self.assertEqual(sorted(o['area'] for o in objetos), sorted(stats[1:, cv2.CC_STAT_AREA].tolist()))
                # As mesmas partições, independentemente da ordem dos IDs.
                for objeto in objetos:
                    indices = np.unique(rotulos[nossos == objeto['id']])
                    self.assertEqual(len(indices), 1)
                    self.assertNotEqual(indices[0], 0)

    def test_diametro_exato(self):
        rng = np.random.default_rng(12)
        self.assertEqual(pdi.diametro([]), 0)
        self.assertEqual(pdi.diametro([(4, 5)]), 0)
        for _ in range(100):
            pontos = [tuple(map(int, p)) for p in rng.integers(-20, 21, (30, 2))]
            esperado = max(math.dist(a, b) for a, b in itertools.combinations(pontos, 2))
            self.assertAlmostEqual(pdi.diametro(pontos), esperado)

    def test_operacoes_video(self):
        frame = np.zeros((100, 120, 3), np.uint8)
        frame[30:60, 30:60] = 255
        for op in pdi.OPERACOES:
            resultado = processar_frame(frame, op)
            self.assertEqual(resultado.shape[:2], frame.shape[:2])
            self.assertEqual(resultado.dtype, np.uint8)

    def test_gatilho_musica(self):
        gatilho = GatilhoPresenca()
        self.assertEqual([gatilho.atualizar(x) for x in [True, True, True, True, False, True]],
                         [False, True, False, False, False, False])
        self.assertEqual([gatilho.atualizar(x) for x in [False, False, False, True, True]],
                         [False, False, False, False, True])
        gatilho.reset()
        self.assertFalse(gatilho.atualizar(False))

    def test_rastreador(self):
        rastreador = criar_rastreador()
        rng = np.random.default_rng(8)
        textura = rng.integers(0, 256, (60, 50, 3), dtype=np.uint8)
        inicial = np.zeros((180, 240, 3), np.uint8)
        inicial[50:110, 70:120] = textura
        rastreador.init(inicial, (70, 50, 50, 60))
        for deslocamento in (3, 6, 9):
            seguinte = np.zeros_like(inicial)
            seguinte[50:110, 70+deslocamento:120+deslocamento] = textura
            ok, caixa = rastreador.update(seguinte)
            self.assertTrue(ok)
            self.assertLess(abs(caixa[0]-(70+deslocamento)), 12)


if __name__ == '__main__':
    unittest.main(verbosity=2)
