import pygame

screen_width, screen_height = 1280, 720

font32 = pygame.font.SysFont("Gulim", 32)
# font32 = pygame.font.Font("Galmuri7.ttf", 32)
def draw_text(screen, text, x=100, y=100, color="#000000"):
    render = font32.render(text, False, color)
    screen.blit(render, (x, y))
