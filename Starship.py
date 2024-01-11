import numpy as np
import pygame
import time
import random
import math

# Entry dimensions for the ship
radio = int(input("Radius of the shuttle: "))
altura = int(input("Height of the ship: "))
area = math.pi * radio
volumen_metros = area * altura
volumen_litros = volumen_metros * 1000

# Simulation start
pygame.init()

# window size
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("¿Ready for launch?")

# Grid dimensions
nxC, nyC = 100, 100
dimCW = width / nxC
dimCH = height / nyC

bg = 10, 10, 10
screen.fill(bg)

gamestate = np.zeros((nxC, nyC))

# Ship coordinates
nav_coords = [
    (8, 98), (12, 98), (11, 97), (11, 96), (9, 94), (11, 93),
    (8, 97), (12, 97), (11, 95), (10, 94), (9, 93),
    (9, 97), (9, 96), (10, 95), (11, 94), (10, 92),
    (10, 97), (10, 96), (9, 95), (10, 93)
]

# Ensure coordinates are within the screen
for i, coord in enumerate(nav_coords):
    x, y = coord
    x = max(0, min(x, nxC - 1))
    y = max(0, min(y, nyC - 1))
    nav_coords[i] = (x, y)

# All the squares of the ship are set equal to 1 so that they can be drawn later since they will have a property that the rest of the grids do not have.
for coord in nav_coords:
    gamestate[coord] = 1

# Define the ship's fuel (consumption increases)
combustible = volumen_litros // 50000

def draw_moon():
    # Draw the moon with shades of gray
    moon_center = (width - 70, 70)
    moon_radius = 50

    for i in range(moon_radius, 0, -1):
        shade = 255 - i * 3
        moon_color = (shade, shade, shade)
        pygame.draw.circle(screen, moon_color, moon_center, i)

while True:
    newgamestate = np.copy(gamestate)
    screen.fill(bg)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    combustible -= 0.5  # Reduce fuel faster
    print(f"Fuel: {max(combustible, 0):.2f} L") # f indicates the start of fstring and 2f causes only 2 decimal places to be output

    # Move the ship up
    for i in range(len(nav_coords)):
        x, y = nav_coords[i]
        nav_coords[i] = (x, max(0, y - 1))

    # Update the game matrix with the new ship position
    newgamestate = np.zeros((nxC, nyC))
    for coord in nav_coords:
        newgamestate[coord] = 1

    # Draw the grid with the ship's state changes
    for y in range(0, nyC):
        for x in range(0, nxC):
            poly = [
                ((x) * dimCW, (y) * dimCH),
                ((x + 1) * dimCW, (y) * dimCH),
                ((x + 1) * dimCW, (y + 1) * dimCH),
                ((x) * dimCW, (y + 1) * dimCH),
            ]

            if newgamestate[x, y] == 0:
                probabilidad = random.random()
                if probabilidad < 0.01:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 1)
                else:
                    pygame.draw.polygon(screen, (0, 0, 0), poly, 1)
            else:
                pygame.draw.polygon(screen, (20, 50, 30), poly, 0)

    # draw the moon
    draw_moon()

    pygame.display.flip()
    gamestate = np.copy(newgamestate)
    time.sleep(0.1)  # Makes the simulation slower

    # Check if the fuel has run out or if the ship has left the screen
    if combustible <= 0:
        print("Run out of gas. Simulation ended.")
        break
    elif max(nav_coords, key=lambda x: x[1])[1] <= 0:
        print("The spaceship came out of the bounds. Simulation ended.")
        break

pygame.quit()
