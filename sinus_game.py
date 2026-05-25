import pygame
import math
import sys

WIDTH, HEIGHT = 900, 500
FPS = 60

BG_COLOR = (15, 15, 30)
WAVE_COLOR = (0, 220, 160)
TEXT_COLOR = (180, 180, 200)
GRID_COLOR = (35, 35, 55)

AMPLITUDE_STEP = 5
FREQUENCY_STEP = 0.002
SPEED_STEP = 0.005

def draw_grid(surface):
    for x in range(0, WIDTH, 60):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 60):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))
    pygame.draw.line(surface, (60, 60, 90), (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)

def draw_wave(surface, amplitude, frequency, phase):
    points = []
    for x in range(WIDTH):
        y = HEIGHT // 2 - amplitude * math.sin(frequency * x + phase)
        points.append((x, int(y)))

    if len(points) > 1:
        # Draw with thickness by rendering slightly offset lines
        pygame.draw.lines(surface, WAVE_COLOR, False, points, 2)

def draw_hud(surface, font, amplitude, frequency, speed):
    period_px = (2 * math.pi / frequency) if frequency > 0 else 0
    lines = [
        f"Амплітуда:  {amplitude:.0f} px    [↑/↓]",
        f"Період:     {period_px:.0f} px    [←/→]",
        f"Швидкість:  {speed:.3f} {'→' if speed > 0 else ('←' if speed < 0 else '■')}   [z/c]",
        "",
        "Q — вихід",
    ]
    for i, text in enumerate(lines):
        surf = font.render(text, True, TEXT_COLOR)
        surface.blit(surf, (12, 12 + i * 22))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Біжуча синусоїда")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 16)

    amplitude = 100.0
    frequency = 0.02    # radians per pixel
    speed = 0.05        # phase per frame
    phase = 0.0

    # SDL2 USB HID scancodes — layout-independent physical key positions
    SC_Q = 20
    SC_Z = 29
    SC_C = 6

    held_scancodes = set()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                held_scancodes.add(event.scancode)
                if event.scancode == SC_Q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYUP:
                held_scancodes.discard(event.scancode)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            amplitude = min(amplitude + AMPLITUDE_STEP, HEIGHT // 2 - 10)
        if keys[pygame.K_DOWN]:
            amplitude = max(amplitude - AMPLITUDE_STEP, 5)
        if keys[pygame.K_RIGHT]:
            frequency = max(frequency - FREQUENCY_STEP, 0.003)
        if keys[pygame.K_LEFT]:
            frequency = min(frequency + FREQUENCY_STEP, 0.3)
        if SC_C in held_scancodes:
            speed = min(speed + SPEED_STEP, 1.0)
        if SC_Z in held_scancodes:
            speed = max(speed - SPEED_STEP, -1.0)

        phase -= speed

        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_wave(screen, amplitude, frequency, phase)
        draw_hud(screen, font, amplitude, frequency, speed)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
