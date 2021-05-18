#Descrição
'''
    Olá, sou Gabriel Carvalho. No momento, sou iniciante em programação então esse jogo é bem simples e conta com poucas
    funcionalidades porém pode ser bem útil para passar o tempo. A dificuldade do jogo aumenta de acordo com a puntuação
    do usuário. Espero que Gostem! <3
    (Open Souce)

'''

#Imports
from random import randint
import pygame
from pygame import display #requerimento de display
from pygame.image import load #requerimento de imagens
from pygame.transform import scale #escalas
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide #sprites
from pygame import event #eventos
from pygame.locals import QUIT, KEYUP, K_SPACE #teclas e saída
from pygame.time import Clock #tempo
from pygame import font #fontes

#iniciar
pygame.init()

#fonte
fonte = font.SysFont('comicsans', 50)
fonte_perdeu = font.SysFont('comicsans', 150)

#Tamanho da janela/nome/tela
tamanho = 1366, 768
superficie = display.set_mode(tamanho, display=0)
display.set_caption(
    'DinoSaveEarth' #Nome da janela
)

fundo =  scale(
    load('fundo.png'), #Imagem de fundo
    tamanho
)

#Classe dinossauro
#controla o personagem 
class Dinossauro(Sprite):
    def __init__(self, Nasa):
        super().__init__()

        self.image = load('dino.png') #Imagem do dinossauro
        self.rect = self.image.get_rect()
        self.Nasa = Nasa   
        self.velocidade = 10

    def tacar_nasas(self): #Jogar objeto(nasas?)
        if len(self.Nasa)<15:
            self.Nasa.add(
                Nasa(*self.rect.center)
            )

#Updates no personagem (teclas)
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: #Esquerda
            self.rect.x -= self.velocidade 
        if keys[pygame.K_RIGHT]: #Direita
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]: #Para cima
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]: #Para baixo
            self.rect.y += self.velocidade
        nasa_fonte = fonte.render(
            f'NASAS: {15 - len(self.Nasa)}',
            True,
            (255, 255, 255)
        )
        superficie.blit(nasa_fonte, (20, 20))

class Nasa(Sprite): #Objeto(que o personagem atira)
    def __init__(self, x, y):
        super().__init__()

        self.image = load('nasa.png') #Imagem
        self.rect = self.image.get_rect(
            center = (x, y)
        )
        self.velocidade = 1000 #Velocidade do objeto

    def update(self): #Updates no objeto
        self.rect.x += 2
        
        if self.rect.x > tamanho[0]:
            self.kill()

class Meteoro(Sprite): #Inimigo(meteoro)
    def __init__(self):
        super().__init__()

        self.image = load('meteoro.png') #Imagem
        self.rect = self.image.get_rect(
            center = (1366, randint(20, 620))#Posicionamento randômico de acordo com o centro
        )
        self.velocidade = 100000 #Velocidade do inimigo

    def update(self): #Updates no inimigo/ perde o jogo
        global perdeu
        self.rect.x -= 2

        if self.rect.x == 0:
            self.kill()
            perdeu = True



#Definindo os grupos
grupo_inimigos = Group()
grupo_nasa = Group()
dinossauro = Dinossauro(grupo_nasa)
grupo_duno = GroupSingle(dinossauro)
grupo_inimigos.add(Meteoro())

#Tempo
clock = Clock()
#variável para contar score
mortes = 0
round = 0
#variavel perdeu (é falsa até que se torne verdadeira)
perdeu = False

#Loop(Inicialização e permanencia do jogo)
while True:
    #loop de eventos
    clock.tick(120)

    #Rodada
    if round % 120 == 0:
        if mortes< 20:
            grupo_inimigos.add(Meteoro())
        for _ in range(int(mortes /10)):            
            grupo_inimigos.add(Meteoro()) #Adiciona inimigos a partir de determinado score
    print(mortes)

    #Espaço dos eventos
    for evento in event.get():
        if evento.type == QUIT:
            pygame.quit() #sair
        if evento.type == KEYUP:
            if evento.key == K_SPACE:
                dinossauro.tacar_nasas()

#Destruição de inimigos ao contato com objetos
    if groupcollide(grupo_nasa, grupo_inimigos, True, True):
        mortes+=1

    #espaço do display
    superficie.blit(fundo, (0, 0))

    #atributos da fonte do contador de Kills
    fonte_kill = fonte.render(
        f'Score: {mortes}',
        True,
        (255, 255, 255)
    )
    superficie.blit(fonte_kill, (20, 50))

    #Densenhar grupos na tela
    grupo_duno.draw(superficie)
    grupo_inimigos.draw(superficie)
    grupo_nasa.draw(superficie)

    #Realizar updates dos grupos
    grupo_duno.update()
    grupo_inimigos.update()
    grupo_nasa.update()

    #Condicional: Caso o jogador perca, o jogo irá travar e aparecerá a seguinte mensagem na tela: 'Voce perdeu'
    if perdeu:
        deu_ruim = fonte_perdeu.render(
            'Voce perdeu', #Mensagem
            True,
            (255, 255, 255) #RGB
        )
        superficie.blit(deu_ruim, (400, 300)) #Ponto de inicialização (x, y)
        display.update()
        pygame.time.delay(10000) #Delay para travar o jogo


    display.update() #Update
    round += 1

#Powered by Gabriel Carvalho