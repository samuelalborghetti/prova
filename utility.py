import json
import pygame

pygame.init()
IMPOSTAZIONI = "./dati/setting.json"
DATI_EQUIP = "./dati/equip.json"
MAIN_GIOCO = "./main_originale.py"

SCELTA_EQUIP = "./scelta_equip.py"
import os
import sys

def resource_path(relative_path):
    """ Ottiene il percorso assoluto per le risorse (funziona per dev e per PyInstaller) """
    try:
        # PyInstaller crea una cartella temporanea in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def CaricaSettings(percorso):
    file = open(percorso, "r", encoding="utf-8")
    dati = json.load(file)
    file.close()
    return dati["width"], dati["height"], dati["audio"], dati["mod"]

def SalvaEquipaggiamento(percorso, pers: list, cibo: list, equip: list, soldi: float):
    file = open(percorso, "w", encoding="utf-8")
    dati = {"personaggi": pers, "cibo": cibo, "equip": equip, "soldi": soldi}
    info = json.dumps(dati)
    file.write(info)
    file.close()

def SalvaSettings(percorso, height, width, audio, mod):
    dati = {"height": height, "width": width, "audio": audio, "mod": mod}
    file = open(percorso, "w", encoding="utf-8")
    info = json.dumps(dati)
    file.write(info)
    file.close()


BIANCO = (255, 255, 255)
ROSSO_CHIARO = (255, 133, 122)
ROSSO_SCURO = (255, 0, 0)
GIALLO = (255, 215, 0)
ROSA_SCURO = (255, 20, 147)

WIDTH, HEIGHT, VOLUME, MOD = CaricaSettings(IMPOSTAZIONI)


font_numeri = pygame.font.Font("assets/fonts/Barrio-Regular.ttf", int(24 * MOD))
title_font = pygame.font.Font("assets/fonts/PixelifySans-Medium.ttf", int(18 * MOD))
info_font = pygame.font.Font("assets/fonts/PixelifySans-SemiBold.ttf", int(14 * MOD))


WIDTH_BUTTON = 85 * MOD
HEIGHT_BUTTON = 95 * MOD
WIDTH_INFO_CHARACHTER = 380 * MOD
HEIGHT_INFO_CHARACHETER = 220 * MOD

WIDHT_BUTTON = 180 * MOD
HEIGH_BUTTON = 90 * MOD
WIDHT_VOLUME_BAR = 200 * MOD
HEIGHT_VOLUME_BAR = 10 * MOD
WIDTH_SLIDER = 18 * MOD
HEIGHT_SLIDER = 30 * MOD
AUDIO_BUTTON_SIZE = 60 * MOD
WIDHT_EMPTY = 220 * MOD
HEIGHT_EMPTY = 75 * MOD
ARROW_SIZE = 50 * MOD

VOLUME_BAR = pygame.Rect(WIDTH/2 - WIDHT_VOLUME_BAR/2,HEIGH_BUTTON * 3, WIDHT_VOLUME_BAR, HEIGHT_VOLUME_BAR)
VOLUME_BAR_COLLISION = pygame.Rect(VOLUME_BAR.centerx - (WIDHT_VOLUME_BAR * 1.2)/2, VOLUME_BAR.centery - (HEIGHT_VOLUME_BAR * 4), WIDHT_VOLUME_BAR * 1.2, HEIGHT_VOLUME_BAR * 8)

def prendi_frame(lista_frame, durata_frame_ms, inizio_ms=0):
    tempo_passato_ms = pygame.time.get_ticks() - inizio_ms
    indice_frame = (tempo_passato_ms // durata_frame_ms) % len(lista_frame)
    return lista_frame[indice_frame]

def WrapText(testo: str, font_testo, rect_testo):
    parole = testo.split(" ")
    testo_fin = ""
    riga_corrente = ""
    for parola in parole:
        prova_testo = riga_corrente + parola
        width_testo, height = font_testo.size(prova_testo)
        if width_testo > rect_testo.width - 15 * MOD:
            testo_fin += riga_corrente + "|"
            riga_corrente = parola + " "
        else:
            riga_corrente += parola + " "
    testo_fin += riga_corrente
    testo_lista = testo_fin.split("|")
    return testo_lista

def Drawtext(schermo, text: list, y_in, x_testo, font_scelto, colore, spazio_tra_righe = 10*MOD):
    y = y_in
    for riga in text:
        testo = font_scelto.render(riga, True, colore)
        schermo.blit(testo, (x_testo, y))
        y += spazio_tra_righe
        
def Drawtext_PFE(schermo, text: list, y_in, x_testo, font_scelto, colore, spazio_tra_righe, testo_colorato, possibilita_colorare):
    y = y_in
    for riga in text:
        if riga in possibilita_colorare:
            testo = font_scelto.render(riga, True, testo_colorato)
        else:
            testo = font_scelto.render(riga, True, colore)
        schermo.blit(testo, (x_testo, y))
        y += spazio_tra_righe

def draw_con_tempo(schermo, testo: list, font_scelto, colore, spazio_tra_righe, tempo_errore, durata_ms=2000, x=0, y=0):
    if tempo_errore and pygame.time.get_ticks() - tempo_errore < durata_ms:
        Drawtext(schermo, testo, y, x, font_scelto, colore, spazio_tra_righe)
        return tempo_errore
    return 0

def disegna_animazione(schermo, sprites, animazione, durata_ms, pos, dimensione=(64*MOD, 78*MOD), flip=False):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_scalato = pygame.transform.scale(frame_grezzo, dimensione)
    frame_flippato = pygame.transform.flip(frame_scalato, flip, False)
    schermo.blit(frame_flippato, pos)
    
def disegna_animazione_non_scale(schermo, sprites, animazione, durata_ms, pos,flip=False):
    frame_grezzo = prendi_frame(sprites[animazione], durata_ms)
    frame_flip = pygame.transform.flip(frame_grezzo, flip, False)
    schermo.blit(frame_flip, pos)

def DrawMoney(screen, soldi_correnti, scaffale_pos, scaffale_img):
    testo = font_numeri.render(f"Soldi: {soldi_correnti}", True, BIANCO)
    rett = testo.get_rect(topright=(screen.get_width() - 20*MOD, 20*MOD))
    screen.blit(scaffale_img, scaffale_pos)
    screen.blit(testo, rett)
    
def gestisci_eventi():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()