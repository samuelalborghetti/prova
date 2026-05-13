import random
import pygame
import math
from utility import HEIGHT, MOD,WIDTH, prendi_frame, disegna_animazione_non_scale, gestisci_eventi

pygame.font.init()
FONT_BOLD = pygame.font.Font("./assets/fonts/PixelifySans-Bold.ttf", int(50 * MOD))



def Drawtext(schermo, text: list, y_in, font_scelto, colore, spazio_tra_righe):
    y = y_in
    for riga in text:
        testo = font_scelto.render(riga, True, colore)
        testo_rect = testo.get_rect(center=(schermo.get_width() // 2, y))
        schermo.blit(testo, testo_rect)
        y += spazio_tra_righe


def anima_caduta_in_mare(schermo, clock, sprites_caduta, WIDTH_S, HEIGHT_S, bg,elemento,dim_w, dim_h,scelta, durata_ms=9000, FONT_BOLD=FONT_BOLD):
    oggetto_w = dim_w
    oggetto_h = dim_h

    x = random.randint(0, WIDTH_S - oggetto_w)
    y = 200

    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        gestisci_eventi()

        frame = prendi_frame(sprites_caduta[elemento], 140)
        frame_scalato = pygame.transform.scale(frame, (oggetto_w, oggetto_h))
        y += 5 * MOD

        schermo.blit(bg, (0, 0))
        
        if y < 600 * MOD:
            schermo.blit(frame_scalato, (x, y))
        else:
            x = random.randint(0, WIDTH_S - oggetto_w)
            y = 200
        
        Drawtext(schermo, scelta, int((HEIGHT_S // 2) - HEIGHT_S // 4), FONT_BOLD, (255, 255, 255), 40 * MOD)
        
        pygame.display.update()
        clock.tick(60)
    
def anima_tempesta_miracolosa(schermo, clock, sprites_caduta, WIDTH_S, HEIGHT_S, bg, elemento, dim_w, PERSONAGGI_SCELTI, dim_h, scelta=["Una tempesta miracolosa colpisce la nave!"], durata_ms=8000, FONT_BOLD=FONT_BOLD):
    oggetto_w = dim_w
    oggetto_h = dim_h

    x = random.randint(0, WIDTH_S - oggetto_w)
    y = -oggetto_h
    contatore = 0
    pos = [(320*MOD, 335*MOD), (710*MOD, 335*MOD), (320*MOD, 415*MOD), (710*MOD, 415*MOD)]

    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        gestisci_eventi()

        frame = prendi_frame(sprites_caduta[elemento], 140)
        frame_scalato = pygame.transform.scale(frame, (oggetto_w, oggetto_h))
        y += 5 * MOD

        schermo.blit(bg, (0, 0))
        for p in PERSONAGGI_SCELTI:
            if p["stats"]["alive"]:
                disegna_animazione_non_scale(schermo, p["sprites"], "idle", 135, (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))

        if y < (380 * MOD if x < 350 * MOD else HEIGHT_S - 300 * MOD):
            schermo.blit(frame_scalato, (x, y))
        else:
            x = random.randint(0, WIDTH_S - oggetto_w)
            y = -oggetto_h
            contatore += 1

        for i in range(contatore):
            schermo.blit(frame_scalato, pos[i])
            if i == 3:
                contatore = 0
            
        
        Drawtext(schermo, scelta, int((HEIGHT_S // 2) - HEIGHT_S // 4), FONT_BOLD, (255, 255, 255), 40 * MOD)
        
        pygame.display.update()
        clock.tick(60)
    
def anima_cattivo_tempo(schermo, clock, sprites_pioggia, WIDTH_S, HEIGHT_S, bg, PERSONAGGI_SCELTI, scelta=["Il cattivo tempo ha colpito la nave!"], durata_ms=7000, FONT_BOLD=FONT_BOLD):
    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        gestisci_eventi()
        frame = prendi_frame(sprites_pioggia["cattivo_tempo"], 140)
        frame_scalato = pygame.transform.scale(frame, (WIDTH_S, HEIGHT_S))
        schermo.blit(bg, (0, 0))
        for p in PERSONAGGI_SCELTI:
            if p["stats"]["alive"]:
                disegna_animazione_non_scale(schermo, p["sprites"], "idle", 135, (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        schermo.blit(frame_scalato, (0, 0))

        Drawtext(schermo, scelta, int((HEIGHT_S // 2) - HEIGHT_S // 4), FONT_BOLD, (255, 255, 255), 40 * MOD)
        
        pygame.display.update()
        clock.tick(60)

def animazione_ondata(schermo, clock, sprites_ondata, WIDTH_S, HEIGHT_S, bg, PERSONAGGI_SCELTI, scelta=["Siete colpiti da un'onda altissima!"], durata_ms=6000, FONT_BOLD=FONT_BOLD):
    x= - WIDTH_S//3
    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:

        gestisci_eventi()
        frame = prendi_frame(sprites_ondata["ondata"], 140)
        frame_scalato = pygame.transform.scale(frame, (WIDTH_S//3, HEIGHT_S))
        schermo.blit(bg, (0, 0))
        for p in PERSONAGGI_SCELTI:
            if p["stats"]["alive"]:
                disegna_animazione_non_scale(schermo, p["sprites"], "idle", 135, (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        schermo.blit(frame_scalato, (x, 20))
        x += 4 * MOD

        Drawtext(schermo, scelta, int((HEIGHT_S // 2) - HEIGHT_S // 4), FONT_BOLD, (255, 255, 255), 40 * MOD)
        
        pygame.display.update()
        clock.tick(60)

def animazione_scialuppa(schermo, clock, sprites_scialuppa, WIDTH_S, HEIGHT_S, scelta=["Avvistate una scialuppa con 4 naufraghi!"], durata_ms=6000, FONT_BOLD=FONT_BOLD):
    inizio = pygame.time.get_ticks()
    x = WIDTH_S - 250
    while pygame.time.get_ticks() - inizio < durata_ms:
        gestisci_eventi()
        frame = prendi_frame(sprites_scialuppa["scialuppa"], 140)
        frame_scalato = pygame.transform.scale(frame, (250*MOD, 120*MOD))
        bg = prendi_frame(sprites_scialuppa["sfondo"], 200)
        bg_scalato = pygame.transform.scale(bg, (WIDTH_S, HEIGHT_S))
        schermo.blit(bg_scalato, (0, 0))
        schermo.blit(frame_scalato, (x, HEIGHT_S//2))
        x -= 4 * MOD
        
        Drawtext(schermo, scelta, int((HEIGHT_S // 2) - HEIGHT_S // 4), FONT_BOLD, (255, 255, 255), 40 * MOD)
        
        pygame.display.update()
        clock.tick(60)
# ------------------------------------------------------------------------gemini style-----------------------------------------------------------------------
def animazione_timone_rotto(schermo, clock, sprites_timone, WIDTH_S, HEIGHT_S, bg, PERSONAGGI_SCELTI, scelta=["Il timone è stato danneggiato!"], durata_ms=3500):
    inizio = pygame.time.get_ticks()
    
    # 1. Recupero immagine
    img = sprites_timone["timone"]
    if isinstance(img, list): img = img[0]
    
    dim = int(100 * MOD)
    timone_base = pygame.transform.scale(img, (dim, dim)).convert_alpha()
    
    # 2. Setup POSIZIONI (Partenza da FUORI SCHERMO a destra)
    x_partenza = WIDTH_S + 150  # 150 pixel oltre il bordo destro
    x_arrivo = -150             # Finisce oltre il bordo sinistro
    
    y_base = int(HEIGHT_S * 0.75) - 100 # Leggermente più basso
    
    while True:
        ms_passati = pygame.time.get_ticks() - inizio
        if ms_passati > durata_ms: break
        
        gestisci_eventi()
        
        # 3. Calcolo PROGRESSIONE (0.0 a 1.0)
        p = ms_passati / durata_ms 
        
        # --- LOGICA ULTRA-VELOCE E ALTA ---
        
        # SPOSTAMENTO: Copre tutta la distanza da destra a sinistra
        distanza_totale = x_partenza - x_arrivo
        x_attuale = x_partenza - (distanza_totale * p)
        
        # ROTAZIONE: Molto veloce (12 giri completi)
        angolo = -(p * 360 * 12) 
        
        # SALTELLI: Ancora più alti (60 pixel) e più frequenti (p * 25)
        # Usiamo abs(math.sin) se vogliamo che "rimbalzi" solo verso l'alto
        offset_y = -abs(math.sin(p * 25)) * 60 
        
        # --- RENDERING ---
        schermo.blit(bg, (0, 0))
        
        for p_char in PERSONAGGI_SCELTI:
            if p_char["stats"]["alive"]:
                disegna_animazione_non_scale(schermo, p_char["sprites"], "idle", 135, (p_char["pos"]["main"]["x_attuale"], p_char["pos"]["main"]["y_attuale"]))
        
        timone_ruotato = pygame.transform.rotate(timone_base, angolo)
        # Usiamo y_base + offset_y
        rect = timone_ruotato.get_rect(center=(int(x_attuale), int(y_base + offset_y)))
        
        schermo.blit(timone_ruotato, rect.topleft)
        
        # Testo Bianco
        Drawtext(schermo, scelta, int(HEIGHT_S // 4), FONT_BOLD, (255, 255, 255), 40 * MOD)
        Drawtext(schermo, ["(non lho fatto io giuro)"], int(HEIGHT_S - 100), FONT_BOLD, (255, 255, 255), 40 * MOD)
        
        pygame.display.update()
        clock.tick(60)
        
# ----------------------------------------------------------------------------------------------------------------------------------------------- 

def anima_topo(schermo, clock, sprites_topo, WIDTH_S, HEIGHT_S, PERSONAGGI_SCELTI, bg, durata_ms=9000, FONT_BOLD=FONT_BOLD):
    frame = prendi_frame(sprites_topo["run right"], 120)
    frame_scalato = pygame.transform.scale(frame, (int(64 * MOD), int(64 * MOD)))
    topo_w = frame_scalato.get_width()
    topo_h = frame_scalato.get_height()

    x = random.randint(0, WIDTH_S - topo_w)
    y = random.randint(0, HEIGHT_S - topo_h)

    direzioni = ["run right", "run left", "run up", "run down"]
    direzione = random.choice(direzioni)
    velocita = 1 * MOD
    tempo_cambio = pygame.time.get_ticks()

    inizio = pygame.time.get_ticks()
    colpito_bordo = False
    while pygame.time.get_ticks() - inizio < durata_ms:
        gestisci_eventi()
        if not colpito_bordo and pygame.time.get_ticks() - tempo_cambio > 1500:
            direzione = random.choice(direzioni)
            tempo_cambio = pygame.time.get_ticks()
        if direzione == "run right":
            x += velocita
        elif direzione == "run left":
            x -= velocita
        elif direzione == "run up":
            y -= velocita
        elif direzione == "run down":
            y += velocita
        frame = prendi_frame(sprites_topo[direzione], 120)
        frame_scalato = pygame.transform.scale(frame, (int(64 * MOD), int(64 * MOD)))
        topo_w = frame_scalato.get_width()
        topo_h = frame_scalato.get_height()
        colpito_bordo = False
        if x < 320*MOD+topo_w:
            x = 320*MOD+topo_w
            direzione = random.choice(["run right", "run up", "run down"])
            tempo_cambio = pygame.time.get_ticks()
            colpito_bordo = True
        elif x > 710*MOD-topo_w:
            x = 710*MOD-topo_w
            direzione = random.choice(["run left", "run down", "run up"])
            tempo_cambio = pygame.time.get_ticks()
            colpito_bordo = True
        if y < 485*MOD-topo_h:
            y = 485*MOD-topo_h
            direzione = random.choice(["run down", "run right", "run left"])
            tempo_cambio = pygame.time.get_ticks()
            colpito_bordo = True
        elif y > 565*MOD-topo_h:
            y = 565*MOD-topo_h
            direzione = random.choice(["run up", "run right", "run left"])
            tempo_cambio = pygame.time.get_ticks()
            colpito_bordo = True
        schermo.blit(bg, (0, 0))
        for p in PERSONAGGI_SCELTI:
            disegna_animazione_non_scale(schermo, p["sprites"], "idle", 135, (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        schermo.blit(frame_scalato, (x, y))
        Drawtext(schermo, ["Un infestazione si è diffusa!"], int((HEIGHT_S // 2)- HEIGHT_S//4), FONT_BOLD, (255, 255, 255), 40*MOD)
        pygame.display.update()
        clock.tick(60)


def animazione_epidemia(schermo, clock, personaggi, bg, durata_ms=9000, FONT_BOLD=FONT_BOLD, HEIGHT_S=HEIGHT):

    DIREZIONI = ["right", "left", "up", "down"]
    VELOCITA = 2 * MOD
    tempo_cambio = pygame.time.get_ticks()
    stati = {}
    for p in personaggi:
        direzione = random.choice(DIREZIONI)
        stati[id(p)] = {
            "direzione": direzione,
            "flip": direzione == "left",
            "colpito_bordo": False,
        }

    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        gestisci_eventi()

        cambia_ora = pygame.time.get_ticks() - tempo_cambio > 1500
        if cambia_ora:
            tempo_cambio = pygame.time.get_ticks()

        schermo.blit(bg, (0, 0))

        for p in personaggi:
            stato = stati[id(p)]
            x = p["pos"]["main"]["x_attuale"]
            y = p["pos"]["main"]["y_attuale"]
            direzione = stato["direzione"]
            colpito_bordo = stato["colpito_bordo"]

            if cambia_ora and not colpito_bordo:
                direzione = random.choice(DIREZIONI)
                stato["direzione"] = direzione

            if direzione == "right":
                x += VELOCITA
                stato["flip"] = False
            elif direzione == "left":
                x -= VELOCITA
                stato["flip"] = True
            elif direzione == "up":
                y -= VELOCITA
            elif direzione == "down":
                y += VELOCITA

            w = int(64 * MOD)
            h = int(78 * MOD)

            colpito_bordo = False
            if x < 320 * MOD + w:
                x = 320 * MOD + w
                direzione = random.choice(["right", "up", "down"])
                stato["flip"] = False
                colpito_bordo = True
            elif x > 710 * MOD - w:
                x = 710 * MOD - w
                direzione = random.choice(["left", "up", "down"])
                stato["flip"] = True
                colpito_bordo = True
            if y < 485 * MOD - h:
                y = 485 * MOD - h
                direzione = random.choice(["down", "right", "left"])
                colpito_bordo = True
            elif y > 565 * MOD - h:
                y = 565 * MOD - h
                direzione = random.choice(["up", "right", "left"])
                colpito_bordo = True

            stato["direzione"] = direzione
            stato["colpito_bordo"] = colpito_bordo
            p["pos"]["main"]["x_attuale"] = x
            p["pos"]["main"]["y_attuale"] = y

            disegna_animazione_non_scale(
                schermo, p["sprites"], "walk_cycle_sick", 120,
                (x, y), flip=stato["flip"]
            )
            Drawtext(schermo, ["L'epidemia si è diffusa!"], int((HEIGHT_S // 2)- HEIGHT_S//4), FONT_BOLD, (255, 255, 255), 40*MOD)

        pygame.display.update()
        clock.tick(60)


def animazione_albatro(schermo, clock, sprites_albatro, WIDTH_S, HEIGHT_S, PERSONAGGI_SCELTI, bg, durata_ms=9000, FONT_BOLD=FONT_BOLD):
    frame = prendi_frame(sprites_albatro["run right"], 120)
    frame_scalato = pygame.transform.scale(frame, (int(64 * MOD), int(64 * MOD)))
    albatro_w = frame_scalato.get_width()
    albatro_h = frame_scalato.get_height()

    x = ((WIDTH_S // 2) - (albatro_w // 2)) - 90*MOD
    y = 80

    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        gestisci_eventi()
        frame = prendi_frame(sprites_albatro["run right"], 120)
        frame_scalato = pygame.transform.scale(frame, (int(300 * MOD), int(150 * MOD)))
        schermo.blit(bg, (0, 0))
        for p in PERSONAGGI_SCELTI:
            disegna_animazione_non_scale(schermo, p["sprites"], "idle", 135, (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        Drawtext(schermo, ["Un albatro si avvicina alla nave!"], int((HEIGHT_S // 2)- HEIGHT_S//4), FONT_BOLD, (255, 255, 255), 40*MOD)
        schermo.blit(frame_scalato, (x, y))
        pygame.display.update()
        clock.tick(60)


def animazione_attacco_pirata_caduta_proiettili(schermo, clock, sprites_proiettile, WIDTH_S, HEIGHT_S, PERSONAGGI_SCELTI, bg, durata_ms=9000, FONT_BOLD=FONT_BOLD):
    oggetto_w = int(37 * MOD)
    oggetto_h = int(66 * MOD)

    x = random.randint(0, WIDTH_S - oggetto_w)
    y = -oggetto_h

    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        gestisci_eventi()

        frame = prendi_frame(sprites_proiettile["proiettile"], 140)
        frame_scalato = pygame.transform.scale(frame, (oggetto_w, oggetto_h))
        y += 5 * MOD

        schermo.blit(bg, (0, 0))
        for p in PERSONAGGI_SCELTI:
            disegna_animazione_non_scale(schermo, p["sprites"], "idle", 135, (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        if y < (380 * MOD if x < 350 * MOD else HEIGHT_S - 300 * MOD):
            schermo.blit(frame_scalato, (x, y))
        else:
            x = random.randint(0, WIDTH_S - oggetto_w)
            y = -oggetto_h
        Drawtext(schermo, ["Siete sotto attacco! da parte dei pirati!"], int((HEIGHT_S // 2) - HEIGHT_S // 4), FONT_BOLD, (255, 255, 255), 40 * MOD)

        pygame.display.update()
        clock.tick(60)
        


def animazione_divento(schermo, clock, sprites_vento, WIDTH_S, HEIGHT_S, PERSONAGGI_SCELTI, bg, durata_ms=9000, FONT_BOLD=None, favorevole=True):
    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        gestisci_eventi()
        frame = prendi_frame(sprites_vento["vento"], 120)
        frame_scalato = pygame.transform.scale(frame, (int(160 * MOD), int(110 * MOD)))
        schermo.blit(bg, (0, 0))
        for p in PERSONAGGI_SCELTI:
            disegna_animazione_non_scale(schermo, p["sprites"], "idle", 135, (p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        if favorevole:
            schermo.blit(frame_scalato, ((WIDTH_S // 2)-100*MOD, (HEIGHT_S // 2)- 200*MOD))
            Drawtext(schermo, ["venti favorevoli!"], int((HEIGHT_S // 2)- HEIGHT_S//3), FONT_BOLD, (255, 255, 255), 40*MOD)
        else:
            schermo.blit(frame_scalato, ((WIDTH_S // 2)-100*MOD, (HEIGHT_S // 2)- 200*MOD))
            Drawtext(schermo, ["venti contrari!"], int((HEIGHT_S // 2)- HEIGHT_S//3), FONT_BOLD, (255, 255, 255), 40*MOD)
        pygame.display.update()
        clock.tick(60)



def animazione_isola(schermo, clock, sprites_isola, WIDTH_S, HEIGHT_S, durata_ms=6000, FONT_BOLD=FONT_BOLD):
    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        gestisci_eventi()
        frame = prendi_frame(sprites_isola["isola"], 500)
        frame_scalato = pygame.transform.scale(frame, (WIDTH_S, HEIGHT_S))
        schermo.blit(frame_scalato, (0, 0))
        Drawtext(schermo, ["Intravedi un isola Misteriosa..."], int((HEIGHT_S // 2)- HEIGHT_S//3), FONT_BOLD, (255, 255, 255), 40*MOD)
        pygame.display.update()
        clock.tick(60)

def anima_pescamiracolosa(schermo, clock, sprites_pesca, WIDTH_S, HEIGHT_S, scelta=["Hai pescato un grande pesce!"], durata_ms=6000, FONT_BOLD=FONT_BOLD):
    oggetto_w = int(140 * MOD)
    oggetto_h = int(130 * MOD)
    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        gestisci_eventi()
        frame = prendi_frame(sprites_pesca["pesce"], 140)
        frame_scalato = pygame.transform.scale(frame, (oggetto_w, oggetto_h))
        schermo.fill((255, 165, 0))#arancione
        schermo.blit(frame_scalato, ((WIDTH_S // 2) - (oggetto_w // 2), (HEIGHT_S // 2) - (oggetto_h // 2)))
        
        Drawtext(schermo, scelta, int((HEIGHT_S // 2) - HEIGHT_S // 4), FONT_BOLD, (255, 255, 255), 40 * MOD)
        pygame.display.update()
        clock.tick(60)
        
        
       