import pygame
import asyncio
import json
import random
import copy
import os
import sys
import math

# --- 1. GLOBAL CONSTANTS ---
WIDTH = 800
HEIGHT = 600
INTERNAL_RES = (WIDTH, HEIGHT)
MOD = 0.74  # Fixed as per tech specs
BIANCO = (255, 255, 255)
NERO = (0, 0, 0)
ROSSO_CHIARO = (255, 133, 122)
ROSSO_SCURO = (255, 0, 0)
GIALLO = (255, 215, 0)
ROSA_SCURO = (255, 20, 147)
MARRONE_UI = (161, 88, 0)

PERCORSO_SALVATAGGIO = "salvataggio.json"

# --- 2. UTILITY & RENDERING ---

def scale_it(img, w, h=None):
    if h is None: h = w
    return pygame.transform.smoothscale(img, (int(w), int(h)))

def get_scaled_mouse():
    mx, my = pygame.mouse.get_pos()
    win_w, win_h = pygame.display.get_surface().get_size()
    ratio = min(win_w / WIDTH, win_h / HEIGHT)
    off_x = (win_w - WIDTH * ratio) / 2
    off_y = (win_h - HEIGHT * ratio) / 2
    if ratio <= 0: return 0, 0
    return (mx - off_x) / ratio, (my - off_y) / ratio

def render_to_screen(internal_surf, window):
    win_w, win_h = window.get_size()
    ratio = min(win_w / WIDTH, win_h / HEIGHT)
    nw, nh = int(WIDTH * ratio), int(HEIGHT * ratio)
    scaled = pygame.transform.smoothscale(internal_surf, (nw, nh))
    window.fill(NERO)
    window.blit(scaled, ((win_w - nw)//2, (win_h - nh)//2))
    pygame.display.flip()

def Drawtext_centered(surf, lines, y, font, color, spacing=None):
    if spacing is None: spacing = 35 * MOD
    for i, line in enumerate(lines):
        s = font.render(str(line), True, color)
        r = s.get_rect(center=(WIDTH // 2, y + i * spacing))
        surf.blit(s, r)

def Drawtext_simple(surf, lines, x, y, font, color, spacing=None):
    if spacing is None: spacing = 25 * MOD
    for i, line in enumerate(lines):
        s = font.render(str(line), True, color)
        surf.blit(s, (x, y + i * spacing))

def prendi_frame(frames, dur_ms, start_t=0):
    if not frames: return None
    idx = ((pygame.time.get_ticks() - start_t) // dur_ms) % len(frames)
    return frames[idx]

def WrapText(testo, font, width_max):
    parole = testo.split(" ")
    righe, r_corrente = [], ""
    for p in parole:
        w, _ = font.size(r_corrente + p)
        if w > width_max - 15 * MOD:
            righe.append(r_corrente.strip()); r_corrente = p + " "
        else: r_corrente += p + " "
    righe.append(r_corrente.strip())
    return [r for r in righe if r]

# --- 3. DATA AND ASSET MANAGER ---

class AssetManager:
    def __init__(self):
        self.fonts = {}
        self.imgs = {}
        self.PERSONAGGI_TEMPLATES = []
        self.CIBO_TEMPLATES = []
        self.BIBITE_TEMPLATES = []
        self.MERCI_TEMPLATES = []
        self.EVENTI_SPRITES = {}

    def load_all(self):
        # Fonts
        for k, p, s in [('num',"assets/fonts/Barrio-Regular.ttf",24), ('title',"assets/fonts/PixelifySans-Medium.ttf",18), ('info',"assets/fonts/PixelifySans-SemiBold.ttf",14), ('bold',"assets/fonts/PixelifySans-Bold.ttf",50), ('reg',"assets/fonts/PixelifySans-Regular.ttf",40)]:
            try: self.fonts[k] = pygame.font.Font(p, int(s*MOD))
            except: self.fonts[k] = pygame.font.SysFont("Arial", int(s*MOD))

        # Backgrounds
        self.imgs['bg_menu'] = scale_it(pygame.image.load("assets/sfondi/menu.jpeg"), WIDTH, HEIGHT)
        self.imgs['bg_main'] = scale_it(pygame.image.load("assets/sfondi/main.png"), WIDTH, HEIGHT)
        self.imgs['bg_equip'] = scale_it(pygame.image.load("assets/sfondi/default1.png"), WIDTH, HEIGHT)
        self.imgs['bg_drop'] = scale_it(pygame.image.load("assets/sfondi/sfondo_per_caduta.png"), WIDTH, HEIGHT)
        self.imgs['icon'] = pygame.image.load("assets/sfondi/icon.png")

        # UI
        wb, hb = 180*MOD, 90*MOD
        self.imgs['play'] = scale_it(pygame.image.load("assets/tasti/play.png"), wb, hb)
        self.imgs['exit'] = scale_it(pygame.image.load("assets/tasti/exit.png"), wb, hb)
        self.imgs['load'] = scale_it(pygame.image.load("assets/tasti/bottone_carica.png"), wb, hb)
        self.imgs['skip'] = scale_it(pygame.image.load("assets/tasti/burrom_skip.png"), 150*MOD, 75*MOD)
        self.imgs['shelf'] = scale_it(pygame.image.load("assets/tasti/scaffalemain.png"), 330*MOD, 210*MOD)
        self.imgs['shelf_s'] = scale_it(pygame.image.load("assets/tasti/scaffale_money.png"), 240*MOD, 160*MOD)

        self._load_chars()
        self._load_resources()
        self._load_event_sprites()

    def _load_chars(self):
        paths = [("Capitano",20,"capitano",2,"capitanoidle"), ("Cuoco",15,"cuoco",6,"cuocoidle"), ("Navigatore",20,"guardone",8,"guardoneidle"), ("Medico",25,"medico",8,"medicoidle"), ("Marinaio",10,"mozzo",3,"mozzoidle"), ("Meccanico",15,"carpentiere",4,"carpidle"), ("Bardo",10,"bardo",2,"bardoidle"), ("Tesoriere",20,"tesoriere",6,"cercatore_di_tesori_idle")]
        for n, cost, f, ni, prf in paths:
            sp = {"idle": [scale_it(pygame.image.load(f"assets/personaggi/{f}/idle/{prf}{i}.png"), 64*MOD, 78*MOD) for i in range(1, ni+1)],
                  "button": scale_it(pygame.image.load(f"assets/tasti/button_{f}.png"), 85*MOD, 95*MOD)}
            if f=="guardone": sp["idle"] = [pygame.transform.flip(im, True, False) for im in sp["idle"]]
            self.PERSONAGGI_TEMPLATES.append({"stats":{"cost":cost,"alive":True,"morale":100},"info":{"name":n,"ruolo":f},"sprites":sp})

    def _load_resources(self):
        for n, c, s, p in [("verdura",0.5,1.0,"carote"), ("frutta",1.0,1.0,"banane"), ("carne",2.0,1.0,"carne_2"), ("legumi",0.5,1.0,"legumi(piselli)"), ("riso",1.5,1.0,"riso"), ("pesce",1.5,1.0,"pesce")]:
            self.CIBO_TEMPLATES.append({"stats":{"cost":c,"saturazione":s,"tipo":n if n in ["frutta","carne"] else "verdura"},"info":{"name":n},"sprites":{"button": scale_it(pygame.image.load(f"assets/cibo/button/{p}_button.png"), 85*MOD, 95*MOD)}})
        self.BIBITE_TEMPLATES.append({"stats":{"cost":0.5,"saturazione":1.0},"info":{"name":"acqua"},"sprites":{"button": scale_it(pygame.image.load("assets/cibo/button/button_acqua.png"), 85*MOD, 95*MOD)}})
        for n, c, t, p in [("medicinale",1.0,"medicinale","button_medicinale"), ("armi",5.0,"arma","button_ARMI"), ("sale",0.5,"baratto","button_sale"), ("coltelli",0.5,"baratto","button_coltelli"), ("stoffa",2.0,"baratto","button_stoffa"), ("diamanti",1.0,"baratto","button_diamanti")]:
            self.MERCI_TEMPLATES.append({"stats":{"cost":c,"tipo":t},"info":{"name":n},"sprites":{"button": scale_it(pygame.image.load(f"assets/equip/{p}.png"), 85*MOD, 95*MOD)}})

    def _load_event_sprites(self):
        self.EVENTI_SPRITES = {
            "drop_mozzo": [scale_it(pygame.image.load(f"assets/eventi/caduta_personaggio/carpe/mozzoidle{i}.png"), 75*MOD, 96*MOD) for i in range(1, 4)],
            "drop_cuoco": [scale_it(pygame.image.load(f"assets/eventi/caduta_personaggio/cuoco/cuocoidleg{i}.png"), 75*MOD, 96*MOD) for i in range(1, 7)],
            "verdura_mare": [pygame.image.load("assets/eventi/cadutaverdura/legumi(piselli).png")],
            "rain": [pygame.image.load(f"assets/eventi/cattivotempo/rain{i}.png") for i in range(1, 4)],
            "onda": [pygame.image.load(f"assets/ondata/onda{i}.png") for i in range(1, 4)],
            "albatro": [pygame.image.load(f"assets/eventi/albatro/animazione/albatro{i}.png") for i in range(1, 20)],
            "isola": [pygame.image.load(f"assets/eventi/isola/isola{i}.png") for i in range(1, 3)],
            "pirate_bullet": [pygame.image.load(f"assets/eventi/attacco_pirata/proiettile{i}.png") for i in range(1, 8)],
            "timone": [pygame.image.load("assets/timone/timone.png")],
            "vento": [pygame.image.load(f"assets/eventi/venti/soffio/vento{i}.png") for i in range(1, 9)]
        }

G_ASSETS = AssetManager()

# --- 4. ENGINE CORE & GAME LOGIC ---

def e_vivo(p): return p["stats"]["alive"]
def uccidi(p): p["stats"]["alive"] = False
def conta_vivi(pers): return sum(1 for p in pers if e_vivo(p))
def presenza_ruolo(pers, ruolo): return any(e_vivo(p) and p["info"]["ruolo"] == ruolo for p in pers)

def SalvaPartita(dati):
    try:
        d = copy.deepcopy(dati); [char.pop("sprites", None) for char in d["p"]]
        with open(PERCORSO_SALVATAGGIO, "w") as f: json.dump(d, f)
    except: pass

def CaricaPartita():
    try:
        if os.path.exists(PERCORSO_SALVATAGGIO):
            with open(PERCORSO_SALVATAGGIO, "r") as f:
                d = json.load(f)
                for char in d["p"]:
                    char["sprites"] = next(o["sprites"] for o in G_ASSETS.PERSONAGGI_TEMPLATES if o["info"]["name"] == char["info"]["name"])
                return d
    except: pass
    return None

async def msg_box(title, q, m, choices=None):
    if choices is None: choices = ["Continua"]
    while True:
        mx, my = get_scaled_mouse(); click = False
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: click = True
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN: return choices[0]
        G_INTERNAL.fill(NERO)
        Drawtext_centered(G_INTERNAL, [title], 120*MOD, G_ASSETS.fonts['bold'], BIANCO)
        Drawtext_centered(G_INTERNAL, WrapText(str(q), G_ASSETS.fonts['num'], WIDTH-100), 280*MOD, G_ASSETS.fonts['num'], GIALLO)
        Drawtext_centered(G_INTERNAL, WrapText(str(m), G_ASSETS.fonts['info'], WIDTH-100), 380*MOD, G_ASSETS.fonts['info'], BIANCO)
        res = None
        for i, c in enumerate(choices):
            ts = G_ASSETS.fonts['reg'].render(c, True, BIANCO)
            tr = ts.get_rect(center=(WIDTH//2, 480*MOD + i*60*MOD))
            if tr.collidepoint(mx, my): ts = G_ASSETS.fonts['reg'].render("> "+c+" <", True, GIALLO)
            G_INTERNAL.blit(ts, tr)
            if click and tr.collidepoint(mx, my): res = c
        if res: return res
        render_to_screen(G_INTERNAL, G_WINDOW); await asyncio.sleep(0)

# --- 5. EVENTS & ANIMATIONS ---

async def anima_drop(testo):
    spr = random.choice([G_ASSETS.EVENTI_SPRITES["drop_mozzo"], G_ASSETS.EVENTI_SPRITES["drop_cuoco"]])
    x, y = random.randint(100, WIDTH-100), 100
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < 4000:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
        G_INTERNAL.blit(G_ASSETS.imgs['bg_drop'], (0,0))
        f = prendi_frame(spr, 140)
        y += 6 * MOD
        if y > HEIGHT: x, y = random.randint(100, WIDTH-100), 100
        G_INTERNAL.blit(f, (x, y))
        Drawtext_centered(G_INTERNAL, [testo], 100, G_ASSETS.fonts['bold'], BIANCO)
        render_to_screen(G_INTERNAL, G_WINDOW); await asyncio.sleep(0)

# --- 6. STATES: MENU, EQUIP, GAME ---

async def handle_menu():
    while True:
        mx, my = get_scaled_mouse(); click = False
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: click = True
        G_INTERNAL.blit(G_ASSETS.imgs['bg_menu'], (0,0))
        Drawtext_centered(G_INTERNAL, ["PIRATES OF THE SEA"], 100*MOD, G_ASSETS.fonts['bold'], BIANCO)
        btns, y = [], 300*MOD
        if os.path.exists(PERCORSO_SALVATAGGIO):
            rc = pygame.Rect(WIDTH//2-90*MOD, y, 180*MOD, 90*MOD)
            G_INTERNAL.blit(G_ASSETS.imgs['load'], rc); btns.append(("L", rc)); y += 110*MOD
        rp = pygame.Rect(WIDTH//2-90*MOD, y, 180*MOD, 90*MOD)
        G_INTERNAL.blit(G_ASSETS.imgs['play'], rp); btns.append(("P", rp)); y += 110*MOD
        rq = pygame.Rect(WIDTH//2-90*MOD, y, 180*MOD, 90*MOD)
        G_INTERNAL.blit(G_ASSETS.imgs['exit'], rq); btns.append(("Q", rq))
        if click:
            for l, r in btns:
                if r.collidepoint(mx, my):
                    if l=="L": return "GAME", CaricaPartita()
                    if l=="P": return "EQUIP", None
                    if l=="Q": pygame.quit(); sys.exit()
        render_to_screen(G_INTERNAL, G_WINDOW); await asyncio.sleep(0)

async def handle_equip():
    cat, sel_p, sel_c, sel_m, money = "pers", [], [], [], 2000
    while True:
        mx, my = get_scaled_mouse(); click = 0
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p: cat="pers"
                elif ev.key == pygame.K_c: cat="cibo"
                elif ev.key == pygame.K_m: cat="merci"
                elif ev.key == pygame.K_b: cat="bib"
            if ev.type == pygame.MOUSEBUTTONDOWN: click = ev.button
        G_INTERNAL.blit(G_ASSETS.imgs['bg_equip'], (0,0))
        Drawtext_simple(G_INTERNAL, [f"SOLDI: {money}", f"CATEGORIA: {cat.upper()}", "P:Pers, C:Cibo, B:Bib, M:Merc"], 20, 20, G_ASSETS.fonts['num'], BIANCO)
        l = G_ASSETS.PERSONAGGI_TEMPLATES if cat=="pers" else G_ASSETS.CIBO_TEMPLATES if cat=="cibo" else G_ASSETS.MERCI_TEMPLATES if cat=="merci" else G_ASSETS.BIBITE_TEMPLATES
        rects = [pygame.Rect(20*MOD + (i%2)*110*MOD, 120*MOD + (i//2)*110*MOD, 85*MOD, 95*MOD) for i in range(len(l))]
        for i, item in enumerate(l):
            G_INTERNAL.blit(item["sprites"]["button"], rects[i])
            if click == 1 and rects[i].collidepoint(mx, my):
                cost = item["stats"]["cost"]
                if money >= cost:
                    if cat=="pers" and len(sel_p)<16: sel_p.append(copy.deepcopy(item)); money -= cost
                    elif cat in ["cibo","bib","merci"]: (sel_c if cat in ["cibo","bib"] else sel_m).append(copy.deepcopy(item)); money -= cost
            elif click == 3 and rects[i].collidepoint(mx, my):
                target = sel_p if cat=="pers" else sel_c if cat in ["cibo","bib"] else sel_m
                for o in target:
                    if o["info"]["name"] == item["info"]["name"]: target.remove(o); money += o["stats"]["cost"]; break
        bs = pygame.Rect(WIDTH-190*MOD, HEIGHT-100*MOD, 180*MOD, 90*MOD); G_INTERNAL.blit(G_ASSETS.imgs['play'], bs)
        if click == 1 and bs.collidepoint(mx, my) and sel_p:
            roles = [c["info"]["ruolo"] for c in sel_p]
            if all(r in roles for r in ["capitano","cuoco","guardone","medico","mozzo"]):
                return "GAME", {"p": sel_p, "c": sel_c, "m": sel_m, "money": money, "sett_c": 1, "sett_t": 8}
            else: await mostra_msg("RUOLI MANCANTI", "Servono Capitano, Cuoco, Medico, Navigatore e Marinaio.", "")
        render_to_screen(G_INTERNAL, G_WINDOW); await asyncio.sleep(0)

async def handle_game(data):
    p, c, m, money = data["p"], data["c"], data["m"], data["money"]
    sett_c, sett_t = data.get("sett_c", 1), data.get("sett_t", 8)
    rats = {"carne": sum(i["stats"]["saturazione"] for i in c if i["stats"].get("tipo")=="carne"),
            "verdura": sum(i["stats"]["saturazione"] for i in c if i["stats"].get("tipo")=="verdura"),
            "frutta": sum(i["stats"]["saturazione"] for i in c if i["stats"].get("tipo")=="frutta"),
            "acqua": sum(i["stats"]["saturazione"] for i in c if i["info"]["name"]=="acqua")}
    b_pos = [(int((150+(i%4)*120)*MOD), int((300+(i//4)*60)*MOD)) for i in range(16)]
    for i, char in enumerate(p): char["x"], char["y"] = b_pos[i]
    while True:
        mx, my = get_scaled_mouse(); click = False
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: click = True
        G_INTERNAL.blit(G_ASSETS.imgs['bg_main'], (0,0))
        Drawtext_simple(G_INTERNAL, [f"SETTIMANA: {sett_c}/{sett_t}", f"CIBO: {sum(rats.values()):.1f}", f"SOLDI: {money}"], 20, 20, G_ASSETS.fonts['num'], BIANCO)
        for char in p:
            if char["stats"]["alive"]: G_INTERNAL.blit(char["sprites"]["idle"][0], (char["x"], char["y"]))
        bs = pygame.Rect(WIDTH-160*MOD, HEIGHT-90*MOD, 150*MOD, 75*MOD); G_INTERNAL.blit(G_ASSETS.imgs['skip'], bs)
        if click and bs.collidepoint(mx, my):
            ev_n = random.choice(["UOMO IN MARE", "TEMPESTA", "PESCA", "PIRATI", "MALATTIA", "CALMA"])
            if ev_n == "UOMO IN MARE":
                v = [i for i in p if i["stats"]["alive"]]
                if v: vict = random.choice(v); uccidi(vict); await anima_drop(f"{vict['info']['name']} in mare!"); await mostra_msg("UOMO IN MARE!", f"{vict['info']['name']} è caduto.", "")
            elif ev_n == "TEMPESTA":
                l = random.randint(5,15); rats["acqua"]=max(0, rats["acqua"]-l); await mostra_msg("TEMPESTA!", f"Perse {l} razioni acqua.", "")
            elif ev_n == "PESCA":
                g = random.randint(10,25); rats["carne"]+=g; await mostra_msg("PESCA!", f"Successo! +{g} kg carne.", "")
            elif ev_n == "PIRATI":
                armi = [i for i in m if i["stats"].get("tipo")=="arma"]
                if armi: m.remove(armi[0]); await mostra_msg("PIRATI!", "Attacco respinto con le armi!", "")
                else:
                    v = [i for i in p if i["stats"]["alive"]]
                    if v: vict = random.choice(v); uccidi(vict); await mostra_msg("PIRATI!", "Nessuna difesa!", f"{vict['info']['name']} è morto.")
            elif ev_n == "MALATTIA":
                meds = [i for i in m if i["stats"].get("tipo")=="medicinale"]
                if meds: m.remove(meds[0]); await mostra_msg("MALATTIA", "Curata con le medicine.", "")
                else:
                    v = [i for i in p if i["stats"]["alive"]]
                    if v: vict = random.choice(v); uccidi(vict); await mostra_msg("EPIDEMIA", "Niente medicine!", f"{vict['info']['name']} è morto.")
            else: await mostra_msg("SETTIMANA CALMA", "Si naviga in acque tranquille.", "")

            nv = conta_vivi(p)
            for k in rats: rats[k] = max(0, rats[k] - nv*(0.5 if k in ["verdura","acqua"] else 1.0))
            sett_c += 1
            if nv == 0: await mostra_msg("GAME OVER", "Tutti i membri sono morti.", ""); return "MENU"
            if sett_c > sett_t:
                prof = random.randint(500, 2000) + sum(1 for i in m if i["stats"].get("tipo")=="baratto")*60
                paga = sum(char["stats"]["cost"] for char in p) * sett_t
                await mostra_msg("MISSIONE COMPIUTA!", f"Profitto Baratto: {prof}. Paga CIurma: {paga}.", f"Saldo Finale: {money+prof-paga} monete.")
                if os.path.exists(PERCORSO_SALVATAGGIO): os.remove(PERCORSO_SALVATAGGIO)
                return "MENU"
            SalvaPartita({"p": p, "c": c, "m": m, "money": money, "sett_c": sett_c, "sett_t": sett_t})
        render_to_screen(G_INTERNAL, G_WINDOW); await asyncio.sleep(0)

# --- 7. MAIN ENTRY ---
G_WINDOW = None
G_INTERNAL = None

async def main():
    global G_WINDOW, G_INTERNAL
    pygame.init()
    G_WINDOW = pygame.display.set_mode(INTERNAL_RES, pygame.RESIZABLE)
    G_INTERNAL = pygame.Surface(INTERNAL_RES)
    G_ASSETS.load_all()
    pygame.display.set_caption("Pirates of the Sea 800x600")
    pygame.display.set_icon(G_ASSETS.imgs['icon'])
    s, d = "MENU", None
    while True:
        if s == "MENU": s, d = await handle_menu()
        elif s == "EQUIP": s, d = await handle_equip()
        elif s == "GAME": s = await handle_game(d)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
