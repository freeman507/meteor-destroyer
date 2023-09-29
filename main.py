import random # biblioteca para gerar numeros aleatorios
import time # biblioteca para controlar tempo

import pygame # bibliteca que controla o jogo

pygame.init() # inicializa o pygame
pygame.display.set_caption("Meteour Destroyer") # adiciona titulo na tela do jogo
largura_janela = 800 # define largura da janela do jogo em pixels
altura_janela = 600 # define altura da janela do jogo em pixels
janela = pygame.display.set_mode((largura_janela, altura_janela)) # abre a janela do jogo
imagem_fundo = pygame.image.load("images/background.jpg") # carrega a imagem de fundo do jogo
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura_janela, altura_janela)) # redimenciona a imagem de fundo

largura_nave = 192 # define largura da nave em pixels
altura_nave = 192 # define altura da nave em pixels
imagem_nave = pygame.image.load("images/Fighter/Evasion.png") # carrega sprites da nave (imagens da anve)
imagem_nave1 = imagem_nave.subsurface(pygame.Rect(0, 0, largura_nave, altura_nave)) # carrega primeira imagem do sprite
imagem_nave2 = imagem_nave.subsurface(pygame.Rect(1 * largura_nave, 0, largura_nave, altura_nave)) # carrega 2° do sprite
imagem_nave3 = imagem_nave.subsurface(pygame.Rect(6 * largura_nave, 0, largura_nave, altura_nave)) # carrega 7° do sprite

imagem_tiro = pygame.image.load("images/Fighter/Charge_1.png") # carrega imagem do tiro

imagem_meteoros = [] # array para armazenar imagens de meteoros
for index in range(1, 10): # loop de 1 a 10
    caminho_imagem = f"images/Meteors/Meteor_0{index}.png" # caminho da imagem baseado no index
    imagem_meteoro = pygame.image.load(caminho_imagem) # carrega imagem de meteoro
    tamanho = (50, 50) # define tamanho do meteoro
    meteoro = pygame.transform.scale(imagem_meteoro, tamanho) # ajusta tamanho da imagem do meteoro
    imagem_meteoros.append(meteoro) # armazena imagens de meteoros

pos_x_imagem_fundo_1 = 0 # posicao inicial do eixo x da imagem de fundo 1
pos_x_imagem_fundo_2 = largura_janela # posicao inicial do eixo x da imagem de fundo 2

relogio = pygame.time.Clock() # Objeto necessario para controlar o FPS(Frames per second) do jogo
velocidade_jogo = 60 # velocidade do jogo em FPS (Frames per second)
velocidade_fundo = 0.5 # velocidade que as imagens de fundo do jogo se movem (é relativo a velocidade_jogo)

velocidade_nave = 5 # velocidade que a nave se mexe na tela quando pressionado uma tecla (é relativo a velocidade_jogo)
pos_x_nave = 0 # posicao inicial do eixo x da nave
pos_y_nave = 0 # posicao inicial do eixo y da nave

velocidade_tiro = 10 # velocidade do tiro na tela (é relativo a velocidade_jogo)

tiros = [] # array para armazenar os tiros disparados pelo jogador

temporizador = 10 # tempo em segundos para spawn de novos meteoros
ultimo_tempo = time.time() # variavel para controlar o tempo de spawn de novos meteoros

meteoros_no_jogo = [] # array para armazenar meteoros do jogo

pygame.mixer.music.load('songs/merx-market-song-33936.mp3') # carrega musica de fundo
pygame.mixer.music.play(-1) # toca musica de fundo repetidamente
pygame.mixer.music.set_volume(0.1) # define volume da musica para 10%

som_tiro = pygame.mixer.Sound('songs/lasers-1-104277.mp3') # carrega o som do tiro
som_tiro.set_volume(0.5) # define o volume do tiro para 50%

som_explosao = pygame.mixer.Sound('songs/hq-explosion-6288.mp3') # carrega o som de explosao do meteoro
som_explosao.set_volume(0.1) # define o som de explosao para 10%

prefacio = True # variavel que controla a tela inial do jogo, quando False o jogo começa
imagem_prefacio = pygame.image.load("images/prefacio.png") # carrega imagem de prefacio
imagem_prefacio = pygame.transform.scale(imagem_prefacio, (largura_janela, altura_janela)) # redimenciona imagem de prefacio

def movimenta_fundo(): # função que movimenta as duas imagens de fundo
    global pos_x_imagem_fundo_1, pos_x_imagem_fundo_2 # usa o global para dizer que as variaveis sao as declaradas nas linhas 31 e 32 do codigo
    pos_x_imagem_fundo_1 -= velocidade_fundo # movimenta imagem de fundo 1 para esquerda
    if pos_x_imagem_fundo_1 < -largura_janela: # verifica se a imagem de fundo 1 chegou ao fim da tela (até o fim do lado esquerdo)
        pos_x_imagem_fundo_1 = largura_janela # reposiciona a imagem de fundo 1 para o incio da tela
    pos_x_imagem_fundo_2 -= velocidade_fundo # movimenta imagem de fundo 2 para esquerda
    if pos_x_imagem_fundo_2 < -largura_janela: # verifica se a imagem de fundo 2 chegou ao fim da tela (até o fim do lado esquerdo)
        pos_x_imagem_fundo_2 = largura_janela # reposiciona a imagem de fundo 2 para o incio da tela
    janela.blit(imagem_fundo, (pos_x_imagem_fundo_1, 0)) # desenha imagem de fundo 1 na tela
    janela.blit(imagem_fundo, (pos_x_imagem_fundo_2, 0)) # desenha imagem de fundo 2 na tela

def movimenta_nave(pos_x_nave, pos_y_nave): # função que movimenta a nave
    teclas_pressionadas = pygame.key.get_pressed() # captura teclas prescionadas e salva em um array
    if teclas_pressionadas[pygame.K_LEFT]: # verifica se a tecla seta para esquerda esta pressionada
        pos_x_nave -= velocidade_nave # movimenta a nave para esquerda
    if teclas_pressionadas[pygame.K_RIGHT]: # verifica se a tecla seta para direita esta pressioanda
        pos_x_nave += velocidade_nave # movimenta nave para direita
    if teclas_pressionadas[pygame.K_UP]: # verifica se a tecla seta para cima esta pressionada
        pos_y_nave -= velocidade_nave # movimenta nave para cima
        janela.blit(imagem_nave2, (pos_x_nave, pos_y_nave)) # desenha sprite da nave virando pra cima
    elif teclas_pressionadas[pygame.K_DOWN]: # verifica se a tecla seta para baixo esta pressionada
        pos_y_nave += velocidade_nave # movimenta nave para baixo
        janela.blit(imagem_nave3, (pos_x_nave, pos_y_nave)) # desenha sprite da nave virando para baixo
    else: # else para verificar se a nave nao esta virando pra cima ou pra baixo
        janela.blit(imagem_nave1, (pos_x_nave, pos_y_nave)) # desenha nave normal
    return pos_x_nave, pos_y_nave # retorna a posicao x e y da nave na janela para ser usada em outras funcoes


def movimenta_tiros(): # função que movimenta tidos na tela
    global tiros # usa o global para dizer que é o array declarado na linha 44 do codigo
    tiros_em_tela = [] # array auxiliar para armazenar tiros em tela
    for tiro in tiros: # loop para cada tiro
        tiro["pos_x"] += velocidade_tiro # movimenta tiro para direita
        janela.blit(imagem_tiro, (tiro["pos_x"], tiro["pos_y"])) # desenha tiro nas coordenadas x, y
        if tiro["pos_x"] < largura_janela: # verifica se o tiro está visivel na tela
            tiros_em_tela.append(tiro) # adiciona tiro ao array auxiliar
    tiros = tiros_em_tela # atualiza o array global apenas com os tiros em tela


def disparar_tiros(): # função que cria os tiros do jogo
    if event.type == pygame.KEYDOWN: # verifica se tecla foi clicada (clicada != pressionada)
        if event.key == pygame.K_SPACE: # verifica se a tela é a barra de espaço
            pos_x_tiro = pos_x_nave + largura_nave - 20 # define posição horizontal inicial do tiro em relação a posicao e largura da nave
            pos_y_tiro = pos_y_nave + (altura_nave / 2) - 15 # define posição vertical inicial do tiro em relação a posicao e altura da nave
            tiros.append({"pos_x": pos_x_tiro, "pos_y": pos_y_tiro}) # salva tiro no array de tiros no formato de dicionario
            som_tiro.play() # toca som do tiro


def sair_do_jogo(): # função que fecha o jogo quando clicado ESC ou fechar da janela
    global jogando # usa o global para dizer que é a variavel declarada na linha 172 do codigo
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): # verifica se foi clicado ESC ou fechado a janela
        jogando = False # encerra o jogo interrompendo o loop do jogo


def cria_meteoros(): # função que cria meteoros de forma aleatória na tela
    global ultimo_tempo # usa o global para dizer que é a variavel declarada na linha 47 do codigo
    tempo_atual = time.time() # captura hora atual para controlar o spawn dos meteoros
    if tempo_atual - ultimo_tempo >= temporizador: # verifica se está no momento de criar os meteodos
        for _ in range(0, 5): # loop de 5x
            meteoro = { # cria um meteoro em forma de dicionario
                "subir": random.random() % 2 == 0, # define de forma aleatoria se o meteoro tem que se movimentar pra cima ou pra baixo
                "index": random.randint(0, 8), # define de forma aleatoria qual imagem vai ser usada do meteoro
                "pos_x": random.randint(0, largura_janela) + largura_janela, # define de forma aleatoria a posição horizontal do meteoro
                "pos_y": random.randint(0, altura_janela - 50) # define de forma aleatoria a posição vertial do meteoro
            } # encerra a criação do meteoro
            meteoros_no_jogo.append(meteoro) # adiciona o meteoro no jogo
        ultimo_tempo = tempo_atual # atualiza variavel de controle para fazer o spawn dos meteoros

    for meteoro in meteoros_no_jogo: # faz um loop para cada meteoro no jogo
        janela.blit(imagem_meteoros[meteoro["index"]], (meteoro["pos_x"], meteoro["pos_y"])) # desenha meteoro

    for meteoro in meteoros_no_jogo: # faz um loop para cada meteoro no jogo
        if meteoro["subir"]: # verifica se meteoro tem que se movimentar para cima
            meteoro["pos_y"] -= 2 # movimenta meteoro para cima
            if meteoro["pos_y"] < 0: # se meteoro alcançou topo da tela
                meteoro["subir"] = False # define para o meteoro parar de subir

        if not meteoro["subir"]: # verifica se o meteoro nao tem que subir
            meteoro["pos_y"] += 2 # movimenta o meteoro para baixo
            if meteoro["pos_y"] > (altura_janela - 50): # verifica se o meteoro alcançou a base da tela
                meteoro["subir"] = True # define para o moteoro para de descer

        meteoro["pos_x"] -= 2 # movimenta o meteoro para esquerda


def destroi_meteoros(): # verifica a colisão dos tiros e meteoros e os remove do jogo
    global meteoros_destruidos, tiros_acertados, meteoros_no_jogo, tiros # globais...
    meteoros_destruidos = [] # array para armazenar meteoros que foram destruidos
    tiros_acertados = [] # array para armazenar tiros que acertaram meteoros
    for meteoro in meteoros_no_jogo: # faz loop para cada meteoro em jogo
        r1 = pygame.Rect(meteoro["pos_x"], meteoro["pos_y"], 50, 50) # cria retangulo invisivel de mesmo tamanho e posisao do meteoro para verificar area de colisao do meteoro
        for tiro in tiros: # faz loop para cada tiro em jogo
            r2 = pygame.Rect(tiro["pos_x"], tiro["pos_y"], 28, 28) # cria retangulo invisivel de mesmo tamanho e posisao do tiro para verificar a area de colisao do tiro
            if r1.colliderect(r2): # verifica se existe colisao entre o tiro e o meteoro
                meteoros_destruidos.append(meteoro) # adiciona meteoro ao array de meteoros destruidos
                tiros_acertados.append(tiro) # adiciona tiro ao array de tiros que acertaram o meteoro
                som_explosao.play() # toca som de explosao
    meteoros_no_jogo = list(filter(lambda x: x not in meteoros_destruidos, meteoros_no_jogo)) # remove do jogo os meteoros destruidos
    tiros = list(filter(lambda x: x not in tiros_acertados, tiros)) # remove do jogo os tiros que acertaram os meteoros


def game_over(): # função que verifica se o jogador perdeu
    global jogando # global...
    for meteoro in meteoros_no_jogo: # faz um loop para cada meteoro em jogo
        if meteoro["pos_x"] < 0: # verifica se o meteoro conseguiu alcançar o final da tela
            jogando = False # encerra o jogo

jogando = True # variavel que controla o jogo, quando definida para False o jogo encerra
while jogando: # loop principal do jogo, a cada interação do loop as imagens são desenhadas e apagadas
    if prefacio: # verifica se é para fazer o prefacio do jogo
        janela.blit(imagem_prefacio, (0, 0)) # exibe imagem de prefario (texto com a historia do jogo)
        for event in pygame.event.get(): # verifica se ocorreu algum evento no jogo
            if event.type == pygame.KEYDOWN: # verifica se alguma tecla foi clicada
                prefacio = False # encerra o prefacio do jogo
    else: # começa o jogo após encerrar o prefacio
        movimenta_fundo() # chama a funçãoq que movimenta as imagens de fundo do jogo
        pos_x_nave, pos_y_nave = movimenta_nave(pos_x_nave, pos_y_nave) # chama a função que movimenta a nave e captura a posicao da nave
        cria_meteoros() # chama a função que faz o spawn dos meteoros
        movimenta_tiros() # chama a função que faz o movimento dos tiros
        destroi_meteoros() # chama a função que verifica a colisão dos meteoros com os tiros
        game_over() # chama a função que verifica se o usuario perdeu o jogo

        for event in pygame.event.get(): # verifia se ocorreu algum evento no jogo (ex: tecla clicada)
            disparar_tiros() # chama a função que cria os tiros da nave
            sair_do_jogo() # chama a função que fecha o jogo quando pressionado ESC ou fechado a janela

    pygame.display.flip() # limpa a janela (apaga todas as imagens da tela)
    relogio.tick(velocidade_jogo) # controla a velocidade do jogo
