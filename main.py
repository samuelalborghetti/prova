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
MOD = 0.74  # Static constant for 800x600 refactoring
BIANCO = (255, 255, 255)
NERO = (0, 0, 0)
ROSSO_CHIARO = (255, 133, 122)
ROSSO_SCURO = (255, 0, 0)
GIALLO = (255, 215, 0)
ROSA_SCURO = (255, 20, 147)
PERCORSO_SALVATAGGIO = "salvataggio.json"

# --- 2. CLASSES: DATA AND UTILITY ---

class Utils:
    @staticmethod
    def scale(img, w, h=None):
        if h is None: h = w
        return pygame.transform.smoothscale(img, (int(w), int(h)))

    @staticmethod
    def get_mouse():
        mx, my = pygame.mouse.get_pos()
        win_w, win_h = pygame.display.get_surface().get_size()
        ratio = min(win_w / WIDTH, win_h / HEIGHT)
        off_x = (win_w - WIDTH * ratio) / 2
        off_y = (win_h - HEIGHT * ratio) / 2
        if ratio == 0: return 0, 0
        return (mx - off_x) / ratio, (my - off_y) / ratio

    @staticmethod
    def render(internal_surf, window):
        win_w, win_h = window.get_size()
        ratio = min(win_w / WIDTH, win_h / HEIGHT)
        nw, nh = int(WIDTH * ratio), int(HEIGHT * ratio)
        scaled = pygame.transform.smoothscale(internal_surf, (nw, nh))
        window.fill(NERO)
        window.blit(scaled, ((win_w - nw)//2, (win_h - nh)//2))
        pygame.display.flip()

    @staticmethod
    def wrap(testo, font, width_max):
        parole = testo.split(" ")
        righe, r_curr = [], ""
        for p in parole:
            if font.size(r_curr + p)[0] > width_max - 10:
                righe.append(r_curr.strip()); r_curr = p + " "
            else: r_curr += p + " "
        righe.append(r_curr.strip())
        return [r for r in righe if r]

class Assets:
    def __init__(self):
        self.fonts = {}
        self.imgs = {}
        self.PERSONAGGI = []
        self.CIBO = []
        self.BIBITE = []
        self.MERCI = []

    def load_all(self):
        # Fonts
        for k, p, s in [('num',"assets/fonts/Barrio-Regular.ttf",24), ('title',"assets/fonts/PixelifySans-Medium.ttf",18), ('info',"assets/fonts/PixelifySans-SemiBold.ttf",14), ('bold',"assets/fonts/PixelifySans-Bold.ttf",50), ('reg',"assets/fonts/PixelifySans-Regular.ttf",40)]:
            try: self.fonts[k] = pygame.font.Font(p, int(s*MOD))
            except: self.fonts[k] = pygame.font.SysFont("Arial", int(s*MOD))

        # UI & BG
        self.imgs['bg_menu'] = Utils.scale(pygame.image.load("assets/sfondi/menu.jpeg"), WIDTH, HEIGHT)
        self.imgs['bg_main'] = Utils.scale(pygame.image.load("assets/sfondi/main.png"), WIDTH, HEIGHT)
        self.imgs['bg_equip'] = Utils.scale(pygame.image.load("assets/sfondi/default1.png"), WIDTH, HEIGHT)
        self.imgs['icon'] = pygame.image.load("assets/sfondi/icon.png")
        self.imgs['play'] = Utils.scale(pygame.image.load("assets/tasti/play.png"), 180*MOD, 90*MOD)
        self.imgs['exit'] = Utils.scale(pygame.image.load("assets/tasti/exit.png"), 180*MOD, 90*MOD)
        self.imgs['load'] = Utils.scale(pygame.image.load("assets/tasti/bottone_carica.png"), 180*MOD, 90*MOD)
        self.imgs['skip'] = Utils.scale(pygame.image.load("assets/tasti/burrom_skip.png"), 150*MOD, 75*MOD)
        self.imgs['shelf'] = Utils.scale(pygame.image.load("assets/tasti/scaffale_money.png"), 240*MOD, 160*MOD)

        # Chars
        c_info = [("Capitano",20,"capitano",2,"capitanoidle"), ("Cuoco",15,"cuoco",6,"cuocoidle"), ("Navigatore",20,"guardone",8,"guardoneidle"), ("Medico",25,"medico",8,"medicoidle"), ("Marinaio",10,"mozzo",3,"mozzoidle"), ("Meccanico",15,"carpentiere",4,"carpidle"), ("Bardo",10,"bardo",2,"bardoidle"), ("Tesoriere",20,"tesoriere",6,"cercatore_di_tesori_idle")]
        for n, cost, f, ni, prf in c_info:
            sp = {"idle": [Utils.scale(pygame.image.load(f"assets/personaggi/{f}/idle/{prf}{i}.png"), 64*MOD, 78*MOD) for i in range(1, ni+1)],
                  "button": Utils.scale(pygame.image.load(f"assets/tasti/button_{f}.png"), 85*MOD, 95*MOD)}
            if f=="guardone": sp["idle"] = [pygame.transform.flip(im, True, False) for im in sp["idle"]]
            self.PERSONAGGI.append({"stats":{"cost":cost,"alive":True,"morale":100},"info":{"name":n,"ruolo":f},"sprites":sp})

        # Resources
        for n, c, s, p in [("verdura",0.5,1.0,"carote"), ("frutta",1.0,1.0,"banane"), ("carne",2.0,1.0,"carne_2"), ("legumi",0.5,1.0,"legumi(piselli)"), ("riso",1.5,1.0,"riso"), ("pesce",1.5,1.0,"pesce")]:
            self.CIBO.append({"stats":{"cost":c,"saturazione":s,"tipo":n if n in ["frutta","carne"] else "verdura"},"info":{"name":n},"sprites":{"button": Utils.scale(pygame.image.load(f"assets/cibo/button/{p}_button.png"), 85*MOD, 95*MOD)}})
        self.BIBITE.append({"stats":{"cost":0.5,"saturazione":1.0},"info":{"name":"acqua"},"sprites":{"button": Utils.scale(pygame.image.load("assets/cibo/button/button_acqua.png"), 85*MOD, 95*MOD)}})
        for n, c, t, p in [("medicinale",1.0,"medicinale","button_medicinale"), ("armi",5.0,"arma","button_ARMI"), ("sale",0.5,"baratto","button_sale"), ("coltelli",0.5,"baratto","button_coltelli"), ("stoffa",2.0,"baratto","button_stoffa"), ("diamanti",1.0,"baratto","button_diamanti")]:
            self.MERCI.append({"stats":{"cost":c,"tipo":t},"info":{"name":n},"sprites":{"button": Utils.scale(pygame.image.load(f"assets/equip/{p}.png"), 85*MOD, 95*MOD)}})

G_ASSETS = Assets()

# --- 3. CLASSES: GAME LOGIC ---

class GameLogic:
    @staticmethod
    async def msg(internal_surf, window, title, q, m, choices=None):
        if choices is None: choices = ["Continua"]
        while True:
            mx, my = Utils.get_mouse(); click = False
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: click = True
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN: return choices[0]
            internal_surf.fill(NERO)
            s_bold = G_ASSETS.fonts['bold']; s_num = G_ASSETS.fonts['num']; s_info = G_ASSETS.fonts['info']
            for i, line in enumerate([title]):
                img = s_bold.render(line, True, BIANCO); internal_surf.blit(img, img.get_rect(center=(WIDTH//2, 120*MOD)))
            for i, line in enumerate(Utils.wrap(q, s_num, WIDTH-100)):
                img = s_num.render(line, True, GIALLO); internal_surf.blit(img, img.get_rect(center=(WIDTH//2, 280*MOD + i*30*MOD)))
            for i, line in enumerate(Utils.wrap(m, s_info, WIDTH-100)):
                img = s_info.render(line, True, BIANCO); internal_surf.blit(img, img.get_rect(center=(WIDTH//2, 380*MOD + i*20*MOD)))
            res = None
            for i, c in enumerate(choices):
                ts = G_ASSETS.fonts['reg'].render(c, True, BIANCO)
                tr = ts.get_rect(center=(WIDTH//2, 480*MOD + i*60*MOD))
                if tr.collidepoint(mx, my): ts = G_ASSETS.fonts['reg'].render("> "+c+" <", True, GIALLO)
                internal_surf.blit(ts, tr)
                if click and tr.collidepoint(mx, my): res = c
            if res: return res
            Utils.render(internal_surf, window); await asyncio.sleep(0)

    @staticmethod
    def save(d):
        try:
            sd = copy.deepcopy(d); [c.pop("sprites", None) for c in sd["p"]]
            with open(PERCORSO_SALVATAGGIO, "w") as f: json.dump(sd, f)
        except: pass

    @staticmethod
    def load():
        try:
            if os.path.exists(PERCORSO_SALVATAGGIO):
                with open(PERCORSO_SALVATAGGIO, "r") as f:
                    d = json.load(f)
                    for c in d["p"]: c["sprites"] = next(o["sprites"] for o in G_ASSETS.PERSONAGGI if o["info"]["name"] == c["info"]["name"])
                    return d
        except: pass
        return None

# --- 4. CLASSES: MENUS ---

class MenuSystem:
    def __init__(self, internal_surf, window):
        self.surf = internal_surf
        self.win = window

    async def run_menu(self):
        while True:
            mx, my = Utils.get_mouse(); click = False
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: click = True
            self.surf.blit(G_ASSETS.imgs['bg_menu'], (0,0))
            img_t = G_ASSETS.fonts['bold'].render("PIRATES OF THE SEA", True, BIANCO)
            self.surf.blit(img_t, img_t.get_rect(center=(WIDTH//2, 100*MOD)))
            btns, y = [], 300*MOD
            if os.path.exists(PERCORSO_SALVATAGGIO):
                rc = pygame.Rect(WIDTH//2-90*MOD, y, 180*MOD, 90*MOD)
                self.surf.blit(G_ASSETS.imgs['load'], rc); btns.append(("L", rc)); y += 110*MOD
            rp = pygame.Rect(WIDTH//2-90*MOD, y, 180*MOD, 90*MOD)
            self.surf.blit(G_ASSETS.imgs['play'], rp); btns.append(("P", rp)); y += 110*MOD
            rq = pygame.Rect(WIDTH//2-90*MOD, y, 180*MOD, 90*MOD)
            self.surf.blit(G_ASSETS.imgs['exit'], rq); btns.append(("Q", rq))
            if click:
                for l, r in btns:
                    if r.collidepoint(mx, my):
                        if l=="L": return "GAME", GameLogic.load()
                        if l=="P": return "EQUIP", None
                        if l=="Q": pygame.quit(); sys.exit()
            Utils.render(self.surf, self.win); await asyncio.sleep(0)

    async def run_equip(self):
        cat, sel_p, sel_c, sel_m, money = "pers", [], [], [], 2000
        while True:
            mx, my = Utils.get_mouse(); click = 0
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_p: cat="pers"
                    elif ev.key == pygame.K_c: cat="cibo"
                    elif ev.key == pygame.K_m: cat="merci"
                    elif ev.key == pygame.K_b: cat="bib"
                if ev.type == pygame.MOUSEBUTTONDOWN: click = ev.button
            self.surf.blit(G_ASSETS.imgs['bg_equip'], (0,0))
            txts = [f"SOLDI: {money}", f"CATEGORIA: {cat.upper()}", "P:Pers, C:Cibo, B:Acqua, M:Merci"]
            for i, t in enumerate(txts):
                img = G_ASSETS.fonts['num'].render(t, True, BIANCO)
                self.surf.blit(img, (20, 20 + i*30*MOD))
            l = G_ASSETS.PERSONAGGI if cat=="pers" else G_ASSETS.CIBO if cat=="cibo" else G_ASSETS.MERCI if cat=="merci" else G_ASSETS.BIBITE
            for i, item in enumerate(l):
                r = pygame.Rect(20*MOD + (i%2)*110*MOD, 120*MOD + (i//2)*110*MOD, 85*MOD, 95*MOD)
                self.surf.blit(item["sprites"]["button"], r)
                if click == 1 and r.collidepoint(mx, my):
                    cost = item["stats"]["cost"]
                    if money >= cost:
                        if cat=="pers" and len(sel_p)<16: sel_p.append(copy.deepcopy(item)); money -= cost
                        elif cat in ["cibo","bib","merci"]: (sel_c if cat in ["cibo","bib"] else sel_m).append(copy.deepcopy(item)); money -= cost
                elif click == 3 and r.collidepoint(mx, my):
                    t_list = sel_p if cat=="pers" else sel_c if cat in ["cibo","bib"] else sel_m
                    for o in t_list:
                        if o["info"]["name"] == item["info"]["name"]: t_list.remove(o); money += o["stats"]["cost"]; break
            bs = pygame.Rect(WIDTH-190*MOD, HEIGHT-100*MOD, 180*MOD, 90*MOD)
            self.surf.blit(G_ASSETS.imgs['play'], bs)
            if click == 1 and bs.collidepoint(mx, my) and sel_p:
                roles = [c["info"]["ruolo"] for c in sel_p]
                if all(r in roles for r in ["capitano","cuoco","guardone","medico","mozzo"]):
                    return "GAME", {"p": sel_p, "c": sel_c, "m": sel_m, "money": money, "sett_c": 1, "sett_t": 8}
                else: await GameLogic.msg(self.surf, self.win, "RUOLI MANCANTI", "Servono Capitano, Cuoco, Medico,", "Navigatore e Marinaio per partire.")
            Utils.render(self.surf, self.win); await asyncio.sleep(0)

    async def run_game(self, data):
        p, c, m, money = data["p"], data["c"], data["m"], data["money"]
        sett_c, sett_t = data.get("sett_c", 1), data.get("sett_t", 8)
        rats = {"carne": sum(i["stats"]["saturazione"] for i in c if i["stats"].get("tipo")=="carne"),
                "verdura": sum(i["stats"]["saturazione"] for i in c if i["stats"].get("tipo")=="verdura"),
                "frutta": sum(i["stats"]["saturazione"] for i in c if i["stats"].get("tipo")=="frutta"),
                "acqua": sum(i["stats"]["saturazione"] for i in c if i["info"]["name"]=="acqua")}
        b_pos = [(int((150 + (i%4)*120)*MOD), int((250 + (i//4)*60)*MOD)) for i in range(16)]
        for i, char in enumerate(p): char["x"], char["y"] = b_pos[i]
        while True:
            mx, my = Utils.get_mouse(); click = False
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: click = True
            self.surf.blit(G_ASSETS.imgs['bg_main'], (0,0))
            inf = [f"SETTIMANA: {sett_c}/{sett_t}", f"CIBO: {sum(rats.values()):.1f}", f"SOLDI: {money}"]
            for i, t in enumerate(inf):
                img = G_ASSETS.fonts['num'].render(t, True, BIANCO); self.surf.blit(img, (20, 20 + i*30*MOD))
            for char in p:
                if char["stats"]["alive"]: self.surf.blit(char["sprites"]["idle"][0], (char["x"], char["y"]))
            bs = pygame.Rect(WIDTH-160*MOD, HEIGHT-90*MOD, 150*MOD, 75*MOD); self.surf.blit(G_ASSETS.imgs['skip'], bs)
            if click and bs.collidepoint(mx, my):
                ev_n = random.choice(["CALMA", "TEMPESTA", "PESCA", "PIRATI", "MALATTIA"])
                if ev_n == "TEMPESTA":
                    l = random.randint(5,10); rats["acqua"] = max(0, rats["acqua"]-l)
                    await GameLogic.msg(self.surf, self.win, "TEMPESTA!", f"Persi {l} barili acqua.", "La ciurma è bagnata.")
                elif ev_n == "PESCA":
                    g = random.randint(10,20); rats["carne"] += g
                    await GameLogic.msg(self.surf, self.win, "PESCA!", f"Fortuna! +{g} kg carne.", "")
                elif ev_n == "PIRATI":
                    armi = [i for i in m if i["stats"].get("tipo")=="arma"]
                    if armi: m.remove(armi[0]); await GameLogic.msg(self.surf, self.win, "PIRATI!", "Respinti con le armi!", "")
                    else:
                        v = [i for i in p if i["stats"]["alive"]]
                        if v: vict = random.choice(v); vict["stats"]["alive"] = False; await GameLogic.msg(self.surf, self.win, "PIRATI!", "Nessuna difesa!", f"{vict['info']['name']} ucciso.")
                elif ev_n == "MALATTIA":
                    meds = [i for i in m if i["stats"].get("tipo")=="medicinale"]
                    if meds: m.remove(meds[0]); await GameLogic.msg(self.surf, self.win, "MALATTIA", "Curata.", "")
                    else:
                        v = [i for i in p if i["stats"]["alive"]]
                        if v: vict = random.choice(v); vict["stats"]["alive"] = False; await GameLogic.msg(self.surf, self.win, "EPIDEMIA", f"{vict['info']['name']} morto.")
                else: await GameLogic.msg(self.surf, self.win, "SETTIMANA CALMA", "Si naviga tranquilli.", "")
                nv = sum(1 for char in p if char["stats"]["alive"])
                for k in rats: rats[k] = max(0, rats[k] - nv*(0.5 if k in ["verdura","acqua"] else 1.0))
                sett_c += 1
                if nv == 0: await GameLogic.msg(self.surf, self.win, "GAME OVER", "Tutti morti.", ""); return "MENU", None
                if sett_c > sett_t:
                    prof = random.randint(300, 1000) + sum(1 for i in m if i["stats"].get("tipo")=="baratto")*40
                    paga = sum(char["stats"]["cost"] for char in p) * sett_t
                    await GameLogic.msg(self.surf, self.win, "ARRIVATI!", f"Viaggio concluso. Profitto: {prof}. Paga: {paga}.", f"Saldo: {money+prof-paga}")
                    if os.path.exists(PERCORSO_SALVATAGGIO): os.remove(PERCORSO_SALVATAGGIO)
                    return "MENU", None
                GameLogic.save({"p": p, "c": c, "m": m, "money": money, "sett_c": sett_c, "sett_t": sett_t})
            Utils.render(self.surf, self.win); await asyncio.sleep(0)

# --- 5. MAIN ASYNC FUNCTION ---

async def main():
    global G_WINDOW, G_INTERNAL
    pygame.init()
    G_WINDOW = pygame.display.set_mode(INTERNAL_RES, pygame.RESIZABLE)
    G_INTERNAL = pygame.Surface(INTERNAL_RES)
    G_ASSETS.load_all()
    pygame.display.set_caption("Pirates of the Sea 800x600")
    pygame.display.set_icon(G_ASSETS.imgs['icon'])

    menus = MenuSystem(G_INTERNAL, G_WINDOW)
    state, data = "MENU", None
    while True:
        if state == "MENU": state, data = await menus.run_menu()
        elif state == "EQUIP": state, data = await menus.run_equip()
        elif state == "GAME": state, data = await menus.run_game(data)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
