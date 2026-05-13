import pygame
import json
import subprocess
import sys
from struttura_dati import BUTTONS, PERSONAGGI
from utility import HEIGHT, WIDTH, VOLUME, MOD, VOLUME_BAR, VOLUME_BAR_COLLISION, WIDTH_SLIDER, HEIGHT_SLIDER, HEIGH_BUTTON, IMPOSTAZIONI, SCELTA_EQUIP, MAIN_GIOCO, WIDHT_BUTTON, SalvaSettings, disegna_animazione
from salvataggio import esiste_salvataggio, EliminaSalvataggio, PERCORSO_SALVATAGGIO
def DrawButtons(schermo, to_button):
    for button in to_button:
        if button in BUTTONS.keys():
            schermo.blit(BUTTONS[button][0], (BUTTONS[button][1].x, BUTTONS[button][1].y))

def Drawtext(schermo, text: list, y_in, font_scelto, colore, spazio_tra_righe):
    y = y_in
    for riga in text:
        testo = font_scelto.render(riga, True, colore)
        testo_rect = testo.get_rect(center=(schermo.get_width() // 2, y))
        schermo.blit(testo, testo_rect)
        y += spazio_tra_righe

def DrawBottoneContinua(schermo):
    schermo.blit(BOTTONE_CONTINUA_IMG, (BOTTONE_CONTINUA_RECT.x, BOTTONE_CONTINUA_RECT.y))

widht_prov = WIDTH
height_prov = HEIGHT
mod_prov = MOD

pygame.init()

bg = pygame.image.load("./assets/sfondi/menu.jpeg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirates of the see")
clock = pygame.time.Clock()

pygame.mixer.music.load("assets/music/menu_music2.mp3")
pygame.mixer.music.set_volume(VOLUME)
pygame.mixer.music.play(-1)

FONT_BOLD = pygame.font.Font("./assets/fonts/PixelifySans-Bold.ttf", int(50 * MOD))
FONT_REGULAR = pygame.font.Font("./assets/fonts/PixelifySans-Regular.ttf", int(40 * MOD))
FONT_AVVISI = pygame.font.Font("./assets/fonts/PixelifySans-Regular.ttf", int(30 * MOD))
salvataggio_presente = esiste_salvataggio(PERCORSO_SALVATAGGIO)

BOTTONE_CONTINUA_IMG = pygame.transform.scale(
    pygame.image.load("assets/tasti/bottone_carica.png"), (WIDHT_BUTTON, HEIGH_BUTTON)
)
BOTTONE_CONTINUA_RECT = pygame.Rect(
    WIDTH / 2 - WIDHT_BUTTON / 2,
    HEIGH_BUTTON * 2,   
    WIDHT_BUTTON,
    HEIGH_BUTTON
)
OFFSET_CON_SALVATAGGIO = HEIGH_BUTTON * (0.4*MOD)
DIMENSIONI_SCHERMO = ["1920x1280", "1080x720"]
SCHERMATA_PRINCIPALE = "main"
SCHERMATA_OPTIONS = "options"

schermata = "main"
slider_x = VOLUME_BAR.x + (VOLUME_BAR.width - WIDTH_SLIDER) * VOLUME
cambio_volume = False

menu_on = True
while menu_on:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_on = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if schermata == SCHERMATA_PRINCIPALE:
                if salvataggio_presente:
                    if BOTTONE_CONTINUA_RECT.collidepoint(mouse):
                        subprocess.Popen([sys.executable, MAIN_GIOCO])
                        sys.exit()
                    elif BUTTONS["play"][1].move(0, OFFSET_CON_SALVATAGGIO).collidepoint(mouse):
                        EliminaSalvataggio(PERCORSO_SALVATAGGIO)
                        subprocess.Popen([sys.executable, SCELTA_EQUIP])
                        sys.exit()
                    elif BUTTONS["options"][1].move(0, OFFSET_CON_SALVATAGGIO).collidepoint(mouse):
                        schermata = SCHERMATA_OPTIONS
                    elif BUTTONS["quit"][1].move(0, OFFSET_CON_SALVATAGGIO).collidepoint(mouse):
                        menu_on = False
                else:
                    if BUTTONS["play"][1].collidepoint(mouse):
                        subprocess.Popen([sys.executable, SCELTA_EQUIP])
                        sys.exit()
                    elif BUTTONS["options"][1].collidepoint(mouse):
                        schermata = SCHERMATA_OPTIONS
                    elif BUTTONS["quit"][1].collidepoint(mouse):
                        menu_on = False
            elif schermata == SCHERMATA_OPTIONS:
                if VOLUME_BAR.collidepoint(mouse):
                    cambio_volume = True
                elif BUTTONS["audio_full"][1].collidepoint(mouse):
                    if VOLUME == 0:
                        VOLUME = 0.5
                        slider_x = VOLUME_BAR.x + VOLUME_BAR.width / 2
                    else:
                        VOLUME = 0
                        slider_x = VOLUME_BAR.x
                elif BUTTONS["arr_right"][1].collidepoint(mouse):
                    if height_prov == 1280:
                        widht_prov = 1080
                        height_prov = 720
                        mod_prov = 1
                    else:
                        widht_prov = 1920
                        height_prov = 1280
                        mod_prov = 1.77
                elif BUTTONS["back"][1].collidepoint(mouse):
                    if height_prov != HEIGHT:
                        SalvaSettings(IMPOSTAZIONI, height_prov, widht_prov, VOLUME, mod_prov)
                        subprocess.Popen([sys.executable] + sys.argv)
                        sys.exit()
                    else:
                        SalvaSettings(IMPOSTAZIONI, HEIGHT, WIDTH, VOLUME, MOD)
                        schermata = SCHERMATA_PRINCIPALE
        elif event.type == pygame.MOUSEBUTTONUP:
            if VOLUME_BAR.collidepoint(mouse):
                cambio_volume = False

    if not VOLUME_BAR_COLLISION.collidepoint(mouse):
        cambio_volume = False
    if cambio_volume:
        slider_x = mouse[0] - WIDTH_SLIDER / 2
        slider_x = max(VOLUME_BAR.x, min(slider_x, VOLUME_BAR.x + VOLUME_BAR.width - WIDTH_SLIDER))
        VOLUME = (slider_x - VOLUME_BAR.x) / (VOLUME_BAR.width - WIDTH_SLIDER)
        pygame.mixer.music.set_volume(VOLUME)
        
        
    screen.blit(bg, (0, 0))
    if schermata == SCHERMATA_PRINCIPALE:
        Drawtext(screen, ["Pirates", "of the sea!"], HEIGH_BUTTON, FONT_BOLD, (255, 255, 255), HEIGH_BUTTON / 1.5)
        if salvataggio_presente:
            DrawBottoneContinua(screen)
            for nome in ["play", "options", "quit"]:
                img = BUTTONS[nome][0]
                rect = BUTTONS[nome][1].move(0, OFFSET_CON_SALVATAGGIO)
                screen.blit(img, (rect.x, rect.y))
        else:
            DrawButtons(screen, ["play", "quit", "options"])
        disegna_animazione(screen, PERSONAGGI[4]["sprites"], "idle", 135, (WIDTH - 270 * MOD, 270 * MOD))
        disegna_animazione(screen, PERSONAGGI[0]["sprites"], "idle", 135, (235 * MOD, 270 * MOD))
       
    else:
        Drawtext(screen, ["OPTIONS"], HEIGH_BUTTON, FONT_BOLD, (255, 255, 255), HEIGH_BUTTON / 1.5)
        if int(VOLUME * 100) > 0:
            DrawButtons(screen, ["audio_full", "empty", "arr_right", "resolution", "back"])
        else:
            DrawButtons(screen, ["no_audio", "empty", "arr_right", "resolution", "back"])
        if height_prov == 1280:
            dim_schermo = DIMENSIONI_SCHERMO[0]
        else:
            dim_schermo = DIMENSIONI_SCHERMO[1]
        dim_schermo_testo = FONT_REGULAR.render(dim_schermo, True, (255, 255, 255))
        dim_schermo_rect = dim_schermo_testo.get_rect()
        dim_schermo_rect.center = BUTTONS["empty"][1].center
        screen.blit(dim_schermo_testo, dim_schermo_rect)
        screen.blit(FONT_REGULAR.render(str(int(VOLUME * 100)), True, (0, 0, 0)), (VOLUME_BAR.x + VOLUME_BAR.width + WIDTH_SLIDER, VOLUME_BAR.y - HEIGHT_SLIDER / 1.25))
        if height_prov != HEIGHT:
            Drawtext(screen, ["Le modifiche veranno apportate", "dopo essere tornati al menu principale"], (BUTTONS["empty"][1].y + HEIGH_BUTTON)+20*MOD, FONT_AVVISI, (168, 255, 62), HEIGH_BUTTON / 2)
        pygame.draw.rect(screen, (255, 177, 27), VOLUME_BAR, border_radius=3)
        slider_rect = pygame.Rect(slider_x, VOLUME_BAR.centery - HEIGHT_SLIDER / 2, WIDTH_SLIDER, HEIGHT_SLIDER)
        pygame.draw.rect(screen, (138, 95, 14), slider_rect, border_radius=2)
        

    pygame.display.update()
    clock.tick(60)

pygame.quit()