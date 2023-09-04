# start: 04.09.23
import pygame
import numpy as np
import time

# constantes
num_filas = 50
num_columnas = 50
ventana_ancho = 800
ventana_alto = 800
bg = 12, 12, 12
tamano_celda = 16
#cuadrícula
cuadricula = np.zeros((num_filas, num_columnas))
        
#pausa
pause_exe = False

# pygame setup
pygame.init()
screen = pygame.display.set_mode((ventana_ancho, ventana_alto))
clock = pygame.time.Clock()
pygame.display.set_caption("El juego de la vida by Xinbo")

running = True



#
cuadricula[5,3] = 1
cuadricula[5,4] = 1
cuadricula[5,5] = 1
#
cuadricula[21,21] = 1
cuadricula[22,22] = 1
cuadricula[22,23] = 1
cuadricula[21,23] = 1
cuadricula[20,23] = 1


while running:
    # pygame.QUIT para cerrar la ventana abierta con el ratón (al clickar X) o pulsando q
    key_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key_pressed[pygame.K_q]:
            running = False
        if key_pressed[pygame.K_s]:
            pause_exe = not pause_exe

        mouse_click = pygame.mouse.get_pressed()

        
        if sum(mouse_click) > 0: 
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / tamano_celda)), int(np.floor(posY / tamano_celda))
            cuadricula[celX, celY] = not mouse_click[2]

    
    screen.fill(bg)
    time.sleep(0.1)

    new_cuadricula = np.copy(cuadricula)
    # pintamos la rejilla
    for x in range(num_filas):
        for y in range(num_columnas):

            if not pause_exe:
                num_vecinos = cuadricula[(x-1) % num_filas, (y-1) % num_columnas] + \
                                cuadricula[(x) % num_filas, (y-1) % num_columnas] + \
                                cuadricula[(x+1) % num_filas, (y-1) % num_columnas] + \
                                cuadricula[(x-1) % num_filas, (y)]  % num_columnas+ \
                                cuadricula[(x+1) % num_filas, (y)]  % num_columnas+ \
                                cuadricula[(x-1) % num_filas, (y+1) % num_columnas] + \
                                cuadricula[(x) % num_filas, (y+1) % num_columnas] + \
                                cuadricula[(x+1) % num_filas, (y+1) % num_columnas]
                
                # regla 1: if cel muerta w/3 cel vivas -> revive
                if cuadricula[x,y] == 0 and num_vecinos == 3:
                    new_cuadricula[x, y] = 1
                # regla 2: if cel viva w/ <2 or >3 cel vecinas muere
                elif cuadricula[x,y] == 1 and (num_vecinos < 2 or num_vecinos > 3):
                    new_cuadricula[x, y] = 0

            rejilla = [(x * tamano_celda, y * tamano_celda),
                        ((x+1) * tamano_celda, y * tamano_celda),
                        ((x+1) * tamano_celda, (y+1) * tamano_celda),
                        (x * tamano_celda, (y+1) * tamano_celda)]
            
            if cuadricula[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), rejilla, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), rejilla, 0)


            
    # Actualizamos el estado del juego
    cuadricula = np.copy(new_cuadricula)


    # flip() - actualiza la pantalla
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

