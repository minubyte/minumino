import pygame

screen_width, screen_height = 1280, 720

font32 = pygame.font.Font("data/Galmuri7.ttf", 32)
font64 = pygame.font.Font("data/Galmuri7.ttf", 64)
font128 = pygame.font.Font("data/Galmuri7.ttf", 128)
def draw_text(screen, text, x=100, y=100, color="#eeeeee", font=font32, center=False, opacity=255):
    render = font.render(text, False, color)
    render.set_alpha(opacity)
    if center:
        x -= render.get_width() / 2
        y -= render.get_height() / 2
    screen.blit(render, (x, y))
