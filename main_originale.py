import pygame
import json
import random
import copy
from struttura_dati import PERSONAGGI, CIBO, BIBITE, MERCI, EVENTI
from gestione_eventi import *
from utility import HEIGHT, WIDTH, MOD, BIANCO, font_numeri, title_font, disegna_animazione_non_scale
from eventi import evento_uomo_in_mare, evento_verdura_in_mare, evento_frutta_in_mare, evento_carne_in_mare, evento_acqua_in_mare, evento_pesca_miracolosa, evento_tempesta_miracolosa, evento_venti_favorevoli, evento_cattivo_tempo, evento_ondata, evento_infestazione_ratti, evento_avvistamento_albatro, evento_scialuppa, evento_epidemia, evento_attacco_pirata, evento_danni_timone, evento_raffiche_vento, evento_avvistamento_isola, step_ricalcolo_settimane, mostra_messaggio_evento, gestisci_razioni_interattivo, step_ammutinamento, disegna_schermata_nera_riepilogo_settimana, e_vivo, hai_bardo, hai_tesoriere
from baratto_permain import *
from salvataggio import SalvaPartita, CaricaPartita, EliminaSalvataggio, esiste_salvataggio, PERCORSO_SALVATAGGIO

numero_settimane = 8
settimana_corrente = 1
ammutinamento = False
albatro_avvistato = 0
albatro_ucciso = None
bonus_morale = 0
esito = None
epidemia = False
uomo_in_mare = False

mazzo_eventi = [
    "UOMO IN MARE", "VERDURA IN MARE", "FRUTTA IN MARE", "CARNE IN MARE", "ACQUA IN MARE",
    "PESCA MIRACOLOSA", "TEMPESTA MIRACOLOSA", "VENTI FAVOREVOLI", "CATTIVO TEMPO", "ONDATA",
    "INFESTAZIONE RATTI", "AVVISTAMENTO ALBATRO", "AVVISTAMENTO SCIALUPPA", "EPIDEMIA",
    "ATTACCO PIRATA", "DANNI AL TIMONE", "RAFFICHE DI VENTO", "AVVISTAMENTO ISOLA",
    "NESSUN IMPREVISTO", "NESSUN IMPREVISTO", "NESSUN IMPREVISTO",
    "NESSUN IMPREVISTO", "NESSUN IMPREVISTO", "NESSUN IMPREVISTO"
]


def Carica_equip(percorso):
    with open(percorso, "r", encoding="utf-8") as f:
        dati = json.load(f)
    return dati["personaggi"], dati["cibo"], dati["equip"], dati["soldi"]

def carica_totali_cibo(cibo_lista):
    totale_verdura = totale_carne = totale_frutta = 0
    for c in cibo_lista:
        tipo = c["stats"].get("tipo_cibo", "altro")
        if tipo == "verdura":
            totale_verdura += c["stats"]["saturazione"]
        elif tipo == "carne":
            totale_carne += c["stats"]["saturazione"]
        elif tipo == "frutta":
            totale_frutta += c["stats"]["saturazione"]
    return totale_carne, totale_verdura, totale_frutta

def carica_acqua_totale(bibite_lista):
    totale = 0
    for b in bibite_lista:
        totale += b["stats"]["saturazione"]
    return totale

def carica_totali_equip(equip_lista):
    medicinali = 0
    armi = 0
    for e in equip_lista:
        if e["info"]["name"] == "medicinale":
            medicinali += 1
        elif e["info"]["name"] == "armi":
            armi += 1
    return medicinali, armi, len(equip_lista)

def calcola_tutti_morti(personaggi):
    for p in personaggi:
        if p["stats"]["alive"]:
            return False
    return True


personaggi_scelti, cibo_scelto_nomi, equip_scelto_nomi, soldi_rimanenti = Carica_equip("dati/equip.json")

if esiste_salvataggio(PERCORSO_SALVATAGGIO):
    stato = CaricaPartita(PERCORSO_SALVATAGGIO, PERSONAGGI, MERCI)
    settimana_corrente = stato["settimana_corrente"]
    numero_settimane = stato["numero_settimane"]
    razioni_attuali = stato["razioni_attuali"]
    merce_attuale = stato["merce_attuale"]
    consumi_base = stato["consumi_base"]
    flag_dimezzamento_razioni = stato["flag_dimezzamento_razioni"]
    soldi_rimanenti = stato["soldi_rimanenti"]
    bonus_morale = stato["bonus_morale"]
    albatro_avvistato = stato["albatro_avvistato"]
    albatro_ucciso = stato["albatro_ucciso"]
    mazzo_eventi  = stato["mazzo_eventi"]
    PERSONAGGI_SCELTI = stato["personaggi_scelti"]  
    lista_merci  = stato["lista_merci"]
    saturazione_totale   = (razioni_attuali["verdura"] + razioni_attuali["acqua"]+ razioni_attuali["carne"] + razioni_attuali["frutta"])

else:
    PERSONAGGI_SCELTI = []
    for nome in personaggi_scelti:
        for p in PERSONAGGI:
            if p["info"]["name"] == nome:
                PERSONAGGI_SCELTI.append({
                    "stats":   copy.deepcopy(p["stats"]),
                    "pos":     copy.deepcopy(p["pos"]),
                    "sprites": p["sprites"],
                    "info":    p["info"],
                })

    CIBO_SCELTO = []
    for nome in cibo_scelto_nomi:
        for c in CIBO:
            if c["info"]["name"] == nome:
                CIBO_SCELTO.append(c)

    BIBITE_SCELTE = []
    for nome in cibo_scelto_nomi:
        for b in BIBITE:
            if b["info"]["name"] == nome:
                BIBITE_SCELTE.append(b)

    lista_merci = []
    for nome in equip_scelto_nomi:
        for e in MERCI:
            if e["info"]["name"] == nome:
                nuova = {"info": e["info"], "stats": copy.deepcopy(e["stats"])}
                if "sprites" in e:
                    nuova["sprites"] = e["sprites"]
                lista_merci.append(nuova)
                
    carne_totale, verdura_totale, frutta_totale = carica_totali_cibo(CIBO_SCELTO)
    acqua_totale = carica_acqua_totale(BIBITE_SCELTE)
    totale_medicinali, totale_armi, totale_merci = carica_totali_equip(lista_merci)

    razioni_attuali = {"verdura": verdura_totale, "frutta": frutta_totale,
                         "carne": carne_totale, "acqua": acqua_totale}
    saturazione_totale = (razioni_attuali["verdura"] + razioni_attuali["acqua"]
                          + razioni_attuali["carne"] + razioni_attuali["frutta"])
    merce_attuale = {"medicinali": totale_medicinali, "armi": totale_armi, "totale": totale_merci}
    consumi_base = {"verdura": 0.5, "frutta": 1.0, "carne": 1.0, "acqua": 0.5}
    flag_dimezzamento_razioni = {"verdura": False, "frutta": False, "carne": False, "acqua": False}

pygame.init()
pygame.display.set_icon(pygame.image.load("assets/sfondi/icon.png"))
schermo = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirates of the Sea")
clock = pygame.time.Clock()

bg = pygame.transform.scale(pygame.image.load("assets/sfondi/main.png"),(WIDTH, HEIGHT))
bg_caduta  = pygame.transform.scale(pygame.image.load("assets/sfondi/sfondo_per_caduta.png"), (WIDTH, HEIGHT))

play = pygame.transform.scale(pygame.image.load("assets/tasti/burrom_skip.png"), (int(150*MOD), int(75*MOD)))
rect_play = play.get_rect(topleft=(WIDTH - 200*MOD, HEIGHT - 100*MOD))
bt_wiew_equip = pygame.transform.scale(pygame.image.load("assets/tasti/butto_wiew_equiip.png"),(int(150*MOD), int(75*MOD)))
rect_bt_wiew_equip = bt_wiew_equip.get_rect(topleft=(50*MOD, HEIGHT - 100*MOD))
SCAFFALE_MONEY  = pygame.transform.scale(pygame.image.load("assets/tasti/scaffalemain.png"), (int(330*MOD), int(210*MOD)))

posizioni = [
    (400*MOD, 420*MOD), (455*MOD, 420*MOD), (500*MOD, 430*MOD), (550*MOD, 430*MOD),
    (70*MOD,  340*MOD), (165*MOD, 330*MOD), (23*MOD,  365*MOD), (600*MOD, 480*MOD),
    (400*MOD, 480*MOD), (117*MOD, 370*MOD), (600*MOD, 420*MOD), (650*MOD, 450*MOD),
    (330*MOD, 380*MOD), (455*MOD, 470*MOD), (500*MOD, 480*MOD), (550*MOD, 470*MOD),
]

def shell_sort_per_profondita(personaggi):
    n = len(personaggi)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = personaggi[i]
            j = i
            while j >= gap and personaggi[j-gap]["pos"]["main"]["y_attuale"] > temp["pos"]["main"]["y_attuale"]:
                personaggi[j] = personaggi[j-gap]
                j -= gap
            personaggi[j] = temp
        gap //= 2

def assegna_posizioni(pers, pos):
    for i in range(min(len(pers), len(pos))):
        pers[i]["pos"]["main"]["x_attuale"] = pos[i][0]
        pers[i]["pos"]["main"]["y_attuale"] = pos[i][1]

def DrawMoney(screen, soldi):
    t = font_numeri.render(f"Soldi: {soldi:.1f}", True, BIANCO)
    screen.blit(t, t.get_rect(topright=(screen.get_width() - 35*MOD, 22*MOD)))

def draw_settimana(screen, corrente):
    t = font_numeri.render(f"Settimana: {corrente}/{numero_settimane}", True, BIANCO)
    screen.blit(t, t.get_rect(topright=(screen.get_width() - 20*MOD, 85*MOD)))

def draw_cibo_totale(screen, sat):
    t = font_numeri.render(f"Cibo: {sat:.1f}", True, BIANCO)
    screen.blit(t, t.get_rect(topright=(screen.get_width() - 58*MOD, 147*MOD)))

def draw_cibo_info_box(screen, mouse_pos, sat, acqua, verdura, frutta, carne, rect_cibo):
    if not rect_cibo.collidepoint(mouse_pos):
        return
    r = pygame.Rect(rect_cibo.x + 20*MOD, rect_cibo.y + rect_cibo.height + 19*MOD, 200*MOD, 170*MOD)
    pygame.draw.rect(screen, (161, 88, 0), r, 0, 10)
    pygame.draw.rect(screen, (0, 0, 0), r, 3, 10)
    txt0 = title_font.render("Risorse",               True, BIANCO)
    txt1 = title_font.render(f"Cibo totale: {sat:.1f}", True, BIANCO)
    txt2 = title_font.render(f"Acqua: {acqua:.1f}",    True, BIANCO)
    txt3 = title_font.render(f"Verdura: {verdura:.1f}", True, BIANCO)
    txt4 = title_font.render(f"Frutta: {frutta:.1f}",  True, BIANCO)
    txt5 = title_font.render(f"Carne: {carne:.1f}",    True, BIANCO)
    x = r.x + 10*MOD
    screen.blit(txt0, (x, r.y + 10*MOD))
    screen.blit(txt1, (x, r.y + 35*MOD))
    screen.blit(txt2, (x, r.y + 60*MOD))
    screen.blit(txt3, (x, r.y + 85*MOD))
    screen.blit(txt4, (x, r.y + 110*MOD))
    screen.blit(txt5, (x, r.y + 135*MOD))

def draw_equip_info_box(screen, mouse_pos, med, armi, merci_tot, rect_bt):
    if not rect_bt.collidepoint(mouse_pos):
        return
    w, h = int(220*MOD), int(120*MOD)
    r = pygame.Rect(rect_bt.x, rect_bt.y - h - 10*MOD, w, h)
    pygame.draw.rect(screen, (161, 88, 0), r, 0, 10)
    pygame.draw.rect(screen, (0, 0, 0), r, 3, 10)
    txt0 = title_font.render("Equipaggiamento",          True, BIANCO)
    txt1 = title_font.render(f"Medicinali: {med:.1f}",   True, BIANCO)
    txt2 = title_font.render(f"Armi: {armi:.1f}",        True, BIANCO)
    txt3 = title_font.render(f"Totale merci: {merci_tot:.1f}", True, BIANCO)
    x = r.x + 10*MOD
    screen.blit(txt0, (x, r.y + 10*MOD))
    screen.blit(txt1, (x, r.y + 40*MOD))
    screen.blit(txt2, (x, r.y + 67*MOD))
    screen.blit(txt3, (x, r.y + 92*MOD))

def schermata_nera(durata_ms=3000):
    inizio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inizio < durata_ms:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()
        schermo.fill((0, 0, 0))
        pygame.display.update()
        clock.tick(60)

def gestisci_razioni(razioni_attuali):
    for t in ["verdura", "frutta", "carne", "acqua"]:
        if razioni_attuali[t] < 0:
            razioni_attuali[t] = 0
    return razioni_attuali

def gestisci_merce_totale(merce_attuale):
    for t in ["medicinali", "armi", "totale"]:
        if merce_attuale[t] < 0:
            merce_attuale[t] = 0
    return merce_attuale

def visualizza_morale(schermo, personaggi, mouse_pos):
    if rect_bt_wiew_equip.collidepoint(mouse_pos):
        for i, p in enumerate(personaggi):
            testo = title_font.render(f"{p['info']['name']} - Morale: {p['stats']['morale']}", True, BIANCO)
            schermo.blit(testo, (int(18*MOD), int(10*MOD + i*30*MOD)))


assegna_posizioni(PERSONAGGI_SCELTI, posizioni)
shell_sort_per_profondita(PERSONAGGI_SCELTI)

animazione_attiva = False
schermata = 1
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and schermata == 1:
            if rect_play.collidepoint(pygame.mouse.get_pos()):
                schermata_nera()
                animazione_attiva = False
                schermata = 2
    if schermata == 1:
        schermo.blit(bg, (0, 0))
        for p in PERSONAGGI_SCELTI:
            if p["stats"]["alive"]:
                disegna_animazione_non_scale(schermo, p["sprites"], "idle", 135,(p["pos"]["main"]["x_attuale"], p["pos"]["main"]["y_attuale"]))
        schermo.blit(SCAFFALE_MONEY, (WIDTH - 260*MOD, -10*MOD))
        visualizza_morale(schermo, PERSONAGGI_SCELTI, pygame.mouse.get_pos())
        DrawMoney(schermo, soldi_rimanenti)
        draw_settimana(schermo, settimana_corrente)
        rect_cibo = pygame.Rect(WIDTH - 240*MOD, 147*MOD, 200*MOD, 30*MOD)
        draw_cibo_totale(schermo, saturazione_totale)
        draw_cibo_info_box(schermo, pygame.mouse.get_pos(), saturazione_totale, razioni_attuali["acqua"], razioni_attuali["verdura"], razioni_attuali["frutta"], razioni_attuali["carne"], rect_cibo)
        schermo.blit(play, rect_play.topleft)
        schermo.blit(bt_wiew_equip, rect_bt_wiew_equip.topleft)
        draw_equip_info_box(schermo, pygame.mouse.get_pos(), merce_attuale["medicinali"], merce_attuale["armi"], merce_attuale["totale"], rect_bt_wiew_equip)
    elif schermata == 2:
        if not animazione_attiva:
            animazione_attiva = True

            if not mazzo_eventi:
                evento_estratto = "NESSUN IMPREVISTO"
            else:
                evento_estratto = random.choice(mazzo_eventi)

            if evento_estratto == "AVVISTAMENTO ALBATRO":
                albatro_avvistato += 1
                if albatro_avvistato >= 2:
                    mazzo_eventi.remove(evento_estratto)
            elif evento_estratto != "NESSUN IMPREVISTO":
                mazzo_eventi.remove(evento_estratto)

            if evento_estratto == "UOMO IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[0]["sprites"], WIDTH, HEIGHT,bg_caduta, f"idle{random.randint(1,2)}", int(75*MOD), int(96*MOD),["Un uomo e' caduto in mare!"])
                PERSONAGGI_SCELTI = evento_uomo_in_mare(PERSONAGGI_SCELTI)
                if calcola_tutti_morti(PERSONAGGI_SCELTI):
                    uomo_in_mare = True

            elif evento_estratto == "VERDURA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[1]["sprites"], WIDTH, HEIGHT, bg_caduta, "verdura", int(75*MOD), int(96*MOD), ["Tempesta! Verdura in mare!"])
                razioni_attuali["verdura"] -= evento_verdura_in_mare(razioni_attuali["verdura"])

            elif evento_estratto == "FRUTTA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[2]["sprites"], WIDTH, HEIGHT,bg_caduta, "frutta", int(75*MOD), int(96*MOD), ["Tempesta! Frutta in mare!"])
                razioni_attuali["frutta"] -= evento_frutta_in_mare(razioni_attuali["frutta"])

            elif evento_estratto == "CARNE IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[3]["sprites"], WIDTH, HEIGHT, bg_caduta, "carne", int(75*MOD), int(96*MOD), ["Tempesta! Carne in mare!"])
                razioni_attuali["carne"] -= evento_carne_in_mare(razioni_attuali["carne"])

            elif evento_estratto == "ACQUA IN MARE":
                anima_caduta_in_mare(schermo, clock, EVENTI[4]["sprites"], WIDTH, HEIGHT,  bg_caduta, "acqua", int(50*MOD), int(86*MOD), ["Tempesta! Acqua in mare!"])
                razioni_attuali["acqua"] -= evento_acqua_in_mare(razioni_attuali["acqua"])

            elif evento_estratto == "PESCA MIRACOLOSA":
                anima_pescamiracolosa(schermo, clock, EVENTI[5]["sprites"], WIDTH, HEIGHT)
                razioni_attuali["carne"] = evento_pesca_miracolosa(razioni_attuali["carne"])

            elif evento_estratto == "TEMPESTA MIRACOLOSA":
                anima_tempesta_miracolosa(schermo, clock, EVENTI[6]["sprites"], WIDTH, HEIGHT,bg, "barile", int(165*MOD), PERSONAGGI_SCELTI, int(190*MOD))
                razioni_attuali["acqua"] = evento_tempesta_miracolosa(razioni_attuali["acqua"])

            elif evento_estratto == "VENTI FAVOREVOLI":
                animazione_divento(schermo, clock, EVENTI[17]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg, 5000, title_font, favorevole=True)
                numero_settimane, bonus_morale = evento_venti_favorevoli(numero_settimane, bonus_morale)

            elif evento_estratto == "CATTIVO TEMPO":
                anima_cattivo_tempo(schermo, clock, EVENTI[8]["sprites"], WIDTH, HEIGHT,bg, PERSONAGGI_SCELTI, ["Il cattivo tempo rovescia medicinali!"])
                lista_merci = evento_cattivo_tempo(lista_merci)

            elif evento_estratto == "ONDATA":
                animazione_ondata(schermo, clock, EVENTI[9]["sprites"], WIDTH, HEIGHT,bg, PERSONAGGI_SCELTI, ["Siete colpiti da un'onda!"])
                lista_merci = evento_ondata(lista_merci)

            elif evento_estratto == "INFESTAZIONE RATTI":
                anima_topo(schermo, clock, EVENTI[10]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg)
                lista_merci = evento_infestazione_ratti(lista_merci)

            elif evento_estratto == "AVVISTAMENTO ALBATRO":
                animazione_albatro(schermo, clock, EVENTI[11]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg)
                razioni_attuali["carne"], albatro_avvistato, albatro_ucciso = evento_avvistamento_albatro(PERSONAGGI_SCELTI, lista_merci, razioni_attuali["carne"], albatro_avvistato, albatro_ucciso)

            elif evento_estratto == "AVVISTAMENTO SCIALUPPA":
                animazione_scialuppa(schermo, clock, EVENTI[12]["sprites"], WIDTH, HEIGHT)
                PERSONAGGI_SCELTI, lista_merci = evento_scialuppa(
                    PERSONAGGI_SCELTI, lista_merci, PERSONAGGI, MERCI)

            elif evento_estratto == "EPIDEMIA":
                animazione_epidemia(schermo, clock, PERSONAGGI_SCELTI, bg)
                PERSONAGGI_SCELTI, lista_merci = evento_epidemia(PERSONAGGI_SCELTI, lista_merci)
                if calcola_tutti_morti(PERSONAGGI_SCELTI):
                    epidemia = True 

            elif evento_estratto == "ATTACCO PIRATA":
                animazione_attacco_pirata_caduta_proiettili(schermo, clock, EVENTI[14]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg)
                PERSONAGGI_SCELTI, lista_merci = evento_attacco_pirata(PERSONAGGI_SCELTI, lista_merci)

            elif evento_estratto == "DANNI AL TIMONE":
                animazione_timone_rotto(schermo, clock, EVENTI[15]["sprites"], WIDTH, HEIGHT, bg, PERSONAGGI_SCELTI, ["Il timone e' stato danneggiato!"], durata_ms=7000)
                numero_settimane = evento_danni_timone(numero_settimane, PERSONAGGI_SCELTI)

            elif evento_estratto == "RAFFICHE DI VENTO":
                animazione_divento(schermo, clock, EVENTI[16]["sprites"], WIDTH, HEIGHT, PERSONAGGI_SCELTI, bg, 5000, title_font, favorevole=False)
                numero_settimane = evento_raffiche_vento(numero_settimane, PERSONAGGI_SCELTI)

            elif evento_estratto == "AVVISTAMENTO ISOLA":
                animazione_isola(schermo, clock, EVENTI[18]["sprites"], WIDTH, HEIGHT, 5000)
                numero_settimane, merce_attuale["medicinali"] = evento_avvistamento_isola( lista_merci, merce_attuale["medicinali"], numero_settimane, albatro_avvistato, albatro_ucciso, MERCI)

            else:  # NESSUN IMPREVISTO
                mostra_messaggio_evento("NESSUN IMPREVISTO", "Il mare e' calmo.","Non succede nulla di speciale questa settimana.")

            hai_bardo(PERSONAGGI_SCELTI)
            hai_tesoriere(PERSONAGGI_SCELTI, lista_merci, MERCI)

            razioni_attuali = gestisci_razioni(razioni_attuali)
            merce_attuale   = gestisci_merce_totale(merce_attuale)
            merce_attuale["medicinali"], merce_attuale["armi"], merce_attuale["totale"] = carica_totali_equip(lista_merci)
            saturazione_totale = (razioni_attuali["verdura"] + razioni_attuali["acqua"] + razioni_attuali["carne"] + razioni_attuali["frutta"])
            settimane_rimaste = numero_settimane - settimana_corrente
            razioni_attuali, consumi_base, bonus_morale, flag_dimezzamento_razioni = gestisci_razioni_interattivo( PERSONAGGI_SCELTI, settimane_rimaste, razioni_attuali, consumi_base, bonus_morale, flag_dimezzamento_razioni)
            razioni_attuali = gestisci_razioni(razioni_attuali)
            merce_attuale   = gestisci_merce_totale(merce_attuale)

            for pers in PERSONAGGI_SCELTI:
                if e_vivo(pers):
                    pers["stats"]["morale"] += bonus_morale
                    if pers["stats"]["morale"] > 100:
                        pers["stats"]["morale"] = 100
                    elif pers["stats"]["morale"] < 0:
                        pers["stats"]["morale"] = 0
            for personaggio in PERSONAGGI_SCELTI:
                nomi_morti_lista = []
                testo_nomi = ""

                for personaggio in PERSONAGGI_SCELTI:
                    if e_vivo(personaggio) and personaggio["stats"]["morale"] <= 0:
                        personaggio["stats"]["alive"] = False
                        nomi_morti_lista.append(personaggio["info"]["name"])
                if len(nomi_morti_lista) > 0:
                    for nome in nomi_morti_lista:
                        testo_nomi += nome + " "
                    mostra_messaggio_evento(
                        titolo="MORTE PER DISPERAZIONE!",
                        domanda="I seguenti membri sono morti: " + testo_nomi,
                        motivo="Il loro morale è sceso a zero.",
                        scelte=["Continua"],
                    )

            if calcola_tutti_morti(PERSONAGGI_SCELTI):
                if epidemia:
                    mostra_messaggio_evento(
                        titolo="TUTTI MORTI!",
                        domanda="Tutti i membri dell'equipaggio sono morti a causa dell'epidemia!",
                        motivo="La nave e' alla deriva senza nessuno a guidarla.",
                        scelte=["Fine partita"]
                    )
                elif uomo_in_mare:
                    mostra_messaggio_evento(
                        titolo="TUTTI MORTI!",
                        domanda="L'ultimo uomo è caduto in mare!",
                        motivo="La nave e' alla deriva senza nessuno a guidarla.",
                        scelte=["Fine partita"]
                    )
                else:
                    mostra_messaggio_evento(
                        titolo="TUTTI MORTI!",
                        domanda="Tutti i membri dell'equipaggio sono morti!",
                        motivo="La nave e' alla deriva senza nessuno a guidarla.",
                        scelte=["Fine partita"]
                    )
                EliminaSalvataggio(PERCORSO_SALVATAGGIO)
                running = False

            else:
                saturazione_totale = (razioni_attuali["verdura"] + razioni_attuali["acqua"] + razioni_attuali["carne"] + razioni_attuali["frutta"])
                ammutinamento = step_ammutinamento(flag_dimezzamento_razioni, PERSONAGGI_SCELTI, albatro_ucciso, numero_settimane)
                if ammutinamento:
                    mostra_messaggio_evento(
                        titolo="AMMUTINAMENTO!",
                        domanda="L'equipaggio si e' ammutinato contro di te!",
                        motivo="L'equipaggio abbandona la nave.",
                        scelte=["Fine partita"]
                    )
                    EliminaSalvataggio(PERCORSO_SALVATAGGIO)
                    running = False

                else:
                    numero_settimane = step_ricalcolo_settimane(PERSONAGGI_SCELTI, numero_settimane)
                    disegna_schermata_nera_riepilogo_settimana(
                        PERSONAGGI_SCELTI, razioni_attuali, consumi_base, merce_attuale)

                    settimana_corrente += 1
                    SalvaPartita(
                        percorso=PERCORSO_SALVATAGGIO,
                        settimana_corrente=settimana_corrente,
                        numero_settimane=numero_settimane,
                        razioni_attuali=razioni_attuali,
                        merce_attuale=merce_attuale,
                        consumi_base=consumi_base,
                        flag_dimezzamento_razioni=flag_dimezzamento_razioni,
                        soldi_rimanenti=soldi_rimanenti,
                        bonus_morale=bonus_morale,
                        albatro_avvistato=albatro_avvistato,
                        albatro_ucciso=albatro_ucciso,
                        mazzo_eventi=mazzo_eventi,
                        personaggi_scelti=PERSONAGGI_SCELTI,
                        lista_merci=lista_merci,
                    )

                    assegna_posizioni(PERSONAGGI_SCELTI, posizioni)
                    shell_sort_per_profondita(PERSONAGGI_SCELTI)
                    schermata_nera(durata_ms=3000)
                    schermata = 1

                    if settimana_corrente >= numero_settimane:
                        mostra_messaggio_evento(
                            titolo="VIAGGIO COMPLETATO!",
                            domanda="Congratulazioni, avete completato il viaggio!",
                            motivo="L'equipaggio raggiunge la destinazione sano e salvo.",
                            scelte=["Vai al nuovo mondo!"]
                        )
                        schermata = 3

    elif schermata == 3:
        running, esito = baratto( PERSONAGGI_SCELTI, lista_merci, soldi_rimanenti, numero_settimane, albatro_avvistato, albatro_ucciso )

    pygame.display.update()
    clock.tick(60)

pygame.quit()