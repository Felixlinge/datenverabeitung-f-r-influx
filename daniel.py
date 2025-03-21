import pygame
import sys
import ctypes

def main():
    pygame.init()
    
    # Fenstergröße
    WIDTH, HEIGHT = 300, 100
    
    # Pygame-Fenster erstellen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bewegendes Fenster mit Text")

    # Erzeuge Schriftart und Text
    font = pygame.font.SysFont(None, 58)  # Standard-Schrift, Größe 48
    text_surface = font.render("Daniel", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Windows-spezifischer Handle des Fensters
    hwnd = pygame.display.get_wm_info()["window"]
    
    # Startposition des Fensters (Pixelkoordinaten)
    x = 100
    y = 100
    
    # Geschwindigkeit für x- und y-Richtung
    speed_x = 3
    speed_y = 3
    
    # Bildschirm-Auflösung ermitteln, um Rand-Kollisionen zu erkennen
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fensterposition verändern
        x += speed_x
        y += speed_y

        # Kollisionsabfrage (linker/rechter Bildschirmrand)
        if x <= 0 or (x + WIDTH) >= screen_width:
            speed_x = -speed_x

        # Kollisionsabfrage (oberer/unterer Bildschirmrand)
        if y <= 0 or (y + HEIGHT) >= screen_height:
            speed_y = -speed_y

        # Fenster mithilfe der Windows-API bewegen
        ctypes.windll.user32.MoveWindow(hwnd, x, y, WIDTH, HEIGHT, True)
        
        # Hintergrund im Fenster füllen
        screen.fill((0, 0, 0))
        
        # Text zeichnen
        screen.blit(text_surface, text_rect)
        
        # Anzeige aktualisieren
        pygame.display.flip()
        clock.tick(60)  # 60 Frames pro Sekunde

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
