import random
import time

import pygame

pygame.init()
pygame.display.set_caption("Meteour Destroyer")
janela = pygame.display.set_mode((1024, 768))
imagem_fundo = pygame.transform.scale(pygame.image.load("images/background.jpg"), (1024, 768))

largura_nave = 192
altura_nave = 192
imagem_nave = pygame.image.load("images/Fighter/Evasion.png")
imagem_nave1 = imagem_nave.subsurface(pygame.Rect(0, 0, largura_nave, altura_nave))
imagem_nave2 = imagem_nave.subsurface(pygame.Rect(1 * largura_nave, 0, largura_nave, altura_nave))
imagem_nave3 = imagem_nave.subsurface(pygame.Rect(6 * largura_nave, 0, largura_nave, altura_nave))

imagem_tiro = pygame.image.load("images/Fighter/Charge_1.png")

imagem_meteoros = []
for index in range(1, 10):
    caminho_imagem = f"images/Meteors/Meteor_0{index}.png"
    imagem_meteoro = pygame.image.load(caminho_imagem)
    tamanho = (50, 50)
    imagem_meteoros.append(pygame.transform.scale(imagem_meteoro, tamanho))

jogando = True

pos_x_imagem_fundo_1 = 0
pos_x_imagem_fundo_2 = 1024

velocidade_jogo = 60
velocidade_fundo = 0.5

velocidade_nave = 5
pos_x_nave = 0
pos_y_nave = 0

velocidade_tiro = 10

tiros = []

relogio = pygame.time.Clock()

temporizador = 10
ultimo_tempo = time.time()

meteoros_no_jogo = []

pygame.mixer.music.load('songs/merx-market-song-33936.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

som_tiro = pygame.mixer.Sound('songs/lasers-1-104277.mp3')
som_tiro.set_volume(0.5)

som_explosao = pygame.mixer.Sound('songs/hq-explosion-6288.mp3')
som_explosao.set_volume(0.1)

prefacio = True
imagem_prefacio = pygame.image.load("images/prefacio.png")

def movimenta_fundo():
    global pos_x_imagem_fundo_1, pos_x_imagem_fundo_2
    pos_x_imagem_fundo_1 -= velocidade_fundo
    if pos_x_imagem_fundo_1 < -1024:
        pos_x_imagem_fundo_1 = 1024
    pos_x_imagem_fundo_2 -= velocidade_fundo
    if pos_x_imagem_fundo_2 < -1024:
        pos_x_imagem_fundo_2 = 1024
    janela.blit(imagem_fundo, (pos_x_imagem_fundo_1, 0))
    janela.blit(imagem_fundo, (pos_x_imagem_fundo_2, 0))


def movimenta_nave(pos_x_nave, pos_y_nave):
    teclas_pressionadas = pygame.key.get_pressed()
    if teclas_pressionadas[pygame.K_LEFT]:
        pos_x_nave -= velocidade_nave
    if teclas_pressionadas[pygame.K_RIGHT]:
        pos_x_nave += velocidade_nave
    if teclas_pressionadas[pygame.K_UP]:
        pos_y_nave -= velocidade_nave
        janela.blit(imagem_nave2, (pos_x_nave, pos_y_nave))
    elif teclas_pressionadas[pygame.K_DOWN]:
        pos_y_nave += velocidade_nave
        janela.blit(imagem_nave3, (pos_x_nave, pos_y_nave))
    else:
        janela.blit(imagem_nave1, (pos_x_nave, pos_y_nave))
    return pos_x_nave, pos_y_nave


def movimenta_tiros():
    global tiros
    tiros_em_tela = []
    for tiro in tiros:
        tiro["pos_x"] += velocidade_tiro
        janela.blit(imagem_tiro, (tiro["pos_x"], tiro["pos_y"]))
        if tiro["pos_x"] < 1024:
            tiros_em_tela.append(tiro)
    tiros = tiros_em_tela


def disparar_tiros():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            pos_x_tiro = pos_x_nave + largura_nave - 20
            pos_y_tiro = pos_y_nave + (altura_nave / 2) - 15
            tiros.append({"pos_x": pos_x_tiro, "pos_y": pos_y_tiro})
            som_tiro.play()


def sair_do_jogo():
    global jogando
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        jogando = False


def cria_meteoros():
    global ultimo_tempo
    tempo_atual = time.time()
    if tempo_atual - ultimo_tempo >= temporizador:
        for _ in range(0, 5):
            meteoro = {
                "subir": random.random() % 2 == 0,
                "index": random.randint(0, 8),
                "pos_x": random.randint(50, 1150) + 1024,
                "pos_y": random.randint(0, 700)
            }
            meteoros_no_jogo.append(meteoro)
        ultimo_tempo = tempo_atual

    for meteoro in meteoros_no_jogo:
        janela.blit(imagem_meteoros[meteoro["index"]], (meteoro["pos_x"], meteoro["pos_y"]))

    for meteoro in meteoros_no_jogo:
        if meteoro["subir"]:
            meteoro["pos_y"] -= 2
            if meteoro["pos_y"] < 10:
                meteoro["subir"] = False

        if not meteoro["subir"]:
            meteoro["pos_y"] += 2
            if meteoro["pos_y"] > 700:
                meteoro["subir"] = True

        meteoro["pos_x"] -= 2


def destroi_meteoros():
    global meteoros_destruidos, tiros_acertados, meteoros_no_jogo, tiros
    meteoros_destruidos = []
    tiros_acertados = []
    for meteoro in meteoros_no_jogo:
        r1 = pygame.Rect(meteoro["pos_x"], meteoro["pos_y"], 50, 50)
        for tiro in tiros:
            r2 = pygame.Rect(tiro["pos_x"], tiro["pos_y"], 28, 28)
            if r1.colliderect(r2):
                meteoros_destruidos.append(meteoro)
                tiros_acertados.append(tiro)
                som_explosao.play()
    meteoros_no_jogo = list(filter(lambda x: x not in meteoros_destruidos, meteoros_no_jogo))
    tiros = list(filter(lambda x: x not in tiros_acertados, tiros))


def game_over():
    global jogando
    for meteoro in meteoros_no_jogo:
        if meteoro["pos_x"] < 0:
            jogando = False


while jogando:
    if prefacio:
        janela.blit(imagem_prefacio, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                prefacio = False
    else:
        movimenta_fundo()
        pos_x_nave, pos_y_nave = movimenta_nave(pos_x_nave, pos_y_nave)
        cria_meteoros()
        movimenta_tiros()
        destroi_meteoros()
        game_over()

        for event in pygame.event.get():
            disparar_tiros()
            sair_do_jogo()

    pygame.display.flip()
    relogio.tick(velocidade_jogo)
