import pygame # importa biblioteca pyga,e

pygame.init() # inicializa o pygame (carrega variaveis, dados etc)

# Propriedades da janela do jogo
largura_da_tela = 800 # define a largura da janela do jogo
altura_da_tela = 600 # define a altura da janela do jogo
janela_do_jogo = pygame.display.set_mode((largura_da_tela, altura_da_tela)) # Cria a janela do jogo
relogio = pygame.time.Clock() # Cria um relogio para controlar o FPS do jogo

# Propriedades do meteoro
imagem_do_meteoro = pygame.image.load("images/Meteors/Meteor_01.png") # carrega a imagem do meteoro na memória
tamanho_meteoro = 75 # define altura e largura do meteoro
imagem_do_meteoro = pygame.transform.scale(imagem_do_meteoro, (tamanho_meteoro, tamanho_meteoro)) # redimenciona imagem do meteoro
posicao_x_meteoro = largura_da_tela # define posicao inicial do meteoro no eixo x da tela
posicao_y_meteoro = altura_da_tela / 2 # define posicao inicial do meteoro no eixo y da tela
velocidade_meteoro = 3 # define a velocidade do meteoro em pixels por loop

# Propriedades da espaco nave
imagem_da_nave = pygame.image.load("images/Fighter/Evasion.png") # carrega a imagem da nave na memória
tamanho_nave = 192 # define a altura e largura da nave
sprite_da_nave = imagem_da_nave.subsurface(pygame.Rect(0, 0, tamanho_nave, tamanho_nave)) # carrega primeira imagem do sprite
velocidade_nave = 5 # define a velocidade da nave em pixels por loop
posicao_x_nave = 0 # define posicao inicial da nave eixo x
posicao_y_nave = 0 # define posicao iniical da nave eixo y
vida_nave = 1 # define o numero de vidas da nave

# Sons do jogo
pygame.mixer.init() # inicializa mixer para reproduzir sons durante o jogo
som_explosao = pygame.mixer.Sound('songs/hq-explosion-6288.mp3') # carrega som de explosão na memória
pygame.mixer.music.load('songs/merx-market-song-33936.mp3') # carrega musica de fundo
pygame.mixer.music.play(-1) # toca musica de fundo repetidamente
pygame.mixer.music.set_volume(0.1) # define volume da musica para 10%

def sair_do_jogo(): # Função para fechar o jogo quando precionado o botão X da janela do jogo
    for event in pygame.event.get(): # percorre eventos capturados pelo pygame
        if event.type == pygame.QUIT: # verifica se o evento é para fechar o jogo
            return False # retorna false para encerrar o loop principal do jogo
    return True # retorna true para continuar com o loop principal do jogo


jogando = True # define variavel de controle para fechar jogo
while jogando: # loop principal do jogo

    jogando = sair_do_jogo() # verifica se é para fechar o jogo

    janela_do_jogo.fill("black") # preenche a janela do jogo com fundo preto

    # RENDER YOUR GAME HERE

    if posicao_x_meteoro < 0 - tamanho_meteoro: # verifica se o meteoro já passou da tela
        posicao_x_meteoro = largura_da_tela # define posição inicial pro meteoro

    posicao_x_meteoro -= velocidade_meteoro # incrementa o eixo x do meteoro para move-lo na tela

    janela_do_jogo.blit(imagem_do_meteoro, (posicao_x_meteoro, posicao_y_meteoro)) # desenha o meteoro na tela

    if vida_nave > 0: # verifica se a nave está viva

        teclas = pygame.key.get_pressed() # detecta teclas pressionadas e salva em um array

        if teclas[pygame.K_LEFT]: # verifica se foi pressionada a tela seta para esquerda
            posicao_x_nave -= velocidade_nave # decrementa a posicao X da nave com base na velocidade da nave fazendo ela ir para esquerda
        if teclas[pygame.K_RIGHT]: # verifica se foi pressionada a tela seta para direita
            posicao_x_nave += velocidade_nave # incrementa a posicao X da nave com base na velocidade da nave fazendo ela ir para direita
        if teclas[pygame.K_UP]: # verifica se foi pressionada a tela seta para cima
            posicao_y_nave -= velocidade_nave # decrementa a posicao Y da nave com base na velocidade da nave fazendo ela ir para cima
        if teclas[pygame.K_DOWN]: # verifica se foi pressionada a tela seta para baixo
            posicao_y_nave += velocidade_nave # incrementa a posicao Y da nave com base na velocidade da nave fazendo ela ir para baixo

        area_colisao_nave = pygame.Rect((posicao_x_nave, posicao_y_nave), (tamanho_nave, tamanho_nave)) # define area de colisao da nave
        area_colisao_meteoro = pygame.Rect((posicao_x_meteoro, posicao_y_meteoro), (tamanho_meteoro, tamanho_meteoro)) # define area de colisao do meteoro

        if area_colisao_nave.colliderect(area_colisao_meteoro): # verifica colisao entre nave e meteoro
            vida_nave -= 1 # decrementa vida da nave
            som_explosao.play() # toca som de explosao

        janela_do_jogo.blit(sprite_da_nave, (posicao_x_nave, posicao_y_nave)) # desenha espaço nave na janela do jogo

    pygame.display.flip() # coloca todas as imagem em cena (obrigatório)

    relogio.tick(60)  # define o FPS do jogo

pygame.quit() # descarrega tudo da memória para finalizar o jogo