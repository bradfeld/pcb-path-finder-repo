import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Test Window")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((255, 0, 0))  # Red background
    pygame.draw.circle(screen, (0, 255, 0), (200, 200), 50)  # Green circle
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit() 