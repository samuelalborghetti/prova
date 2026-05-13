import random
import pygame
import gestione_eventi
from utility import HEIGHT, WIDTH, MOD, WIDHT_BUTTON, HEIGH_BUTTON, AUDIO_BUTTON_SIZE, WIDHT_EMPTY, HEIGHT_EMPTY, ARROW_SIZE, VOLUME_BAR, WIDTH_BUTTON, HEIGHT_BUTTON

# ─── BUTTONS ──────────────────────────────────────────────────────────────────

BUTTONS = {
    "play":       [pygame.transform.scale(pygame.image.load("assets/tasti/play.png"),         (WIDHT_BUTTON, HEIGH_BUTTON)),         pygame.Rect(WIDTH/2 - WIDHT_BUTTON/2,              HEIGH_BUTTON * 3,           WIDHT_BUTTON,      HEIGH_BUTTON)],
    "options":    [pygame.transform.scale(pygame.image.load("assets/tasti/settings.png"),     (WIDHT_BUTTON, HEIGH_BUTTON)),         pygame.Rect(WIDTH/2 - WIDHT_BUTTON/2,              HEIGH_BUTTON * 4.5,         WIDHT_BUTTON,      HEIGH_BUTTON)],
    "quit":       [pygame.transform.scale(pygame.image.load("assets/tasti/exit.png"),         (WIDHT_BUTTON, HEIGH_BUTTON)),         pygame.Rect(WIDTH/2 - WIDHT_BUTTON/2,              HEIGH_BUTTON * 6,           WIDHT_BUTTON,      HEIGH_BUTTON)],
    "audio_full": [pygame.transform.scale(pygame.image.load("assets/tasti/audio_full.png"),   (AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)), pygame.Rect(VOLUME_BAR.x - HEIGH_BUTTON,          VOLUME_BAR.y - AUDIO_BUTTON_SIZE/2, AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)],
    "no_audio":   [pygame.transform.scale(pygame.image.load("assets/tasti/no_audio.png"),     (AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)), pygame.Rect(VOLUME_BAR.x - HEIGH_BUTTON,          VOLUME_BAR.y - AUDIO_BUTTON_SIZE/2, AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)],
    "empty":      [pygame.transform.scale(pygame.image.load("assets/tasti/empty_button.png"), (WIDHT_EMPTY, HEIGHT_EMPTY)),          pygame.Rect(WIDTH/2 - WIDHT_EMPTY/2,               HEIGHT/2 + HEIGHT_EMPTY/2,  WIDHT_EMPTY,       HEIGHT_EMPTY)],
    "arr_right":  [pygame.transform.scale(pygame.image.load("assets/tasti/arrow_right.png"),  (ARROW_SIZE, ARROW_SIZE)),             pygame.Rect(WIDTH/2 + WIDHT_EMPTY/2 + ARROW_SIZE/2, HEIGHT/2 + HEIGHT_EMPTY/1.6, ARROW_SIZE,       ARROW_SIZE)],
    "resolution": [pygame.transform.scale(pygame.image.load("assets/tasti/resolution.png"),   (AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)), pygame.Rect(WIDTH/2 - WIDHT_EMPTY/2 - ARROW_SIZE*1.5, HEIGHT/2 + HEIGHT_EMPTY/1.8, AUDIO_BUTTON_SIZE, AUDIO_BUTTON_SIZE)],
    "back":       [pygame.transform.scale(pygame.image.load("assets/tasti/back.png"),         (WIDHT_BUTTON, HEIGH_BUTTON)),         pygame.Rect(WIDTH/2 - WIDHT_BUTTON/2,              HEIGHT - HEIGH_BUTTON * 1.5, WIDHT_BUTTON,     HEIGH_BUTTON)],
}

PERSONAGGI = [
    # ── CAPITANO ─────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 20, "alive": True, "morale": 100},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle":           [pygame.transform.scale(pygame.image.load(f"assets/personaggi/capitano/idle/capitanoidle{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 3)],
            "walk_forward":   [pygame.transform.scale(pygame.image.load(f"assets/personaggi/capitano/camminata_in_avanti/capitano{i}_camminatainavanti.png"), (64*MOD, 78*MOD)) for i in range(1, 5)],
            "walk_cycle":     [pygame.transform.scale(pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip/camminata_laterale{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 5)],
            "walk_cycle_sick":[pygame.transform.scale(pygame.image.load(f"assets/personaggi/capitano/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticapitanoammalato{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 6)],
            "button":          pygame.image.load("assets/tasti/button_capitan.png"),
        },
        "info": {
            "name": "Capitano",
            "descrizione": "Il leader della spedizione. La sua presenza garantisce stabilità e disciplina.",
            "abilita": "Bonus al morale generale. Se muore, il morale crolla drasticamente.",
            "ruolo": "capitano",
        },
    },
    # ── CUOCO ─────────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 15, "alive": True, "morale": 100},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle":           [pygame.transform.scale(pygame.image.load(f"assets/personaggi/cuoco/idle/cuocoidle{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 7)],
            "walk_forward":   [pygame.transform.scale(pygame.image.load(f"assets/personaggi/cuoco/camminata_in_avanti/cuoco{i}_camminatainavanti.png"), (64*MOD, 78*MOD)) for i in range(1, 3)],
            "walk_cycle":     [pygame.transform.scale(pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip/camminata_laterale{i}cuoco.png"), (64*MOD, 78*MOD)) for i in range(1, 7)],
            "walk_cycle_sick":[pygame.transform.scale(pygame.image.load(f"assets/personaggi/cuoco/camminata_a_destrasinistra_con_flip_ammalato/camminataavanticuocoammalato{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 7)],
            "button":          pygame.image.load("assets/tasti/button_cuoco.png"),
        },
        "info": {
            "name": "Cuoco",
            "descrizione": "Specializzato nella preparazione del cibo. Senza di lui il morale cala.",
            "abilita": "Senza cuoco: +30 punti ammutinamento ogni settimana.",
            "ruolo": "cuoco",
        },
    },
    # ── NAVIGATORE ────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 20, "alive": True, "morale": 100},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle":           [pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"assets/personaggi/guardone/idle/guardoneidle{i}.png"), True, False), (64*MOD, 78*MOD)) for i in range(1, 9)],
            "walk_forward":   [pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"assets/personaggi/guardone/camminata_in_avanti/guardone{i}_camminatainavanti.png"), True, False), (64*MOD, 78*MOD)) for i in range(1, 5)],
            "walk_cycle":     [pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip/camminata_lateraleguardone{i}.png"), True, False), (64*MOD, 78*MOD)) for i in range(1, 8)],
            "walk_cycle_sick":[pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"assets/personaggi/guardone/camminata_a_destrasinistra_con_flip_ammalato/camminataavantiguardoneammalato{i}.png"), True, False), (64*MOD, 78*MOD)) for i in range(1, 8)],
            "button":          pygame.image.load("assets/tasti/button_guardone.png"),
        },
        "info": {
            "name": "Navigatore",
            "descrizione": "Sa leggere le stelle e le mappe. Con lui le rotte sono più sicure.",
            "abilita": "Raffiche di vento: solo +1 settimana invece di 2-4. Ritorno: isola a 1 sett invece di 2.",
            "ruolo": "navigatore",
        },
    },
    # ── MEDICO ────────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 25, "alive": True, "morale": 100},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle":           [pygame.transform.scale(pygame.image.load(f"assets/personaggi/medico/idle/medicoidle{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 9)],
            "walk_forward":   [pygame.transform.scale(pygame.image.load(f"assets/personaggi/medico/camminata_in_avanti/medico{i}_camminatainavanti.png"), (64*MOD, 78*MOD)) for i in range(1, 9)],
            "walk_cycle":     [pygame.transform.scale(pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip/camminata_lateralecuoco{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 7)],
            "walk_cycle_sick":[pygame.transform.scale(pygame.image.load(f"assets/personaggi/medico/camminata_a_destrasinistra_con_flip_ammalato/camminatainavanticuocoammalato{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 7)],
            "button":          pygame.image.load("assets/tasti/button_medico.png"),
        },
        "info": {
            "name": "Medico",
            "descrizione": "Curatore dell'equipaggio. Può salvare vite durante le epidemie.",
            "abilita": "Epidemia: cura i malati usando 1 medicinale per persona.",
            "ruolo": "medico",
        },
    },
    # ── MARINAIO ──────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 10, "alive": True, "morale": 100},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle":           [pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"assets/personaggi/mozzo/idle/mozzoidle{i}.png"), True, False), (64*MOD, 78*MOD)) for i in range(1, 4)],
            "walk_forward":   [pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"assets/personaggi/mozzo/camminata_in_avanti/mozzo{i}_camminatainavanti.png"), True, False), (64*MOD, 78*MOD)) for i in range(1, 4)],
            "walk_cycle":     [pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip/camminata_lateralemozzo{i}.png"), True, False), (64*MOD, 78*MOD)) for i in range(1, 4)],
            "walk_cycle_sick":[pygame.transform.scale(pygame.transform.flip(pygame.image.load(f"assets/personaggi/mozzo/camminata_a_destrasinistra_con_flip_ammalato/camminatalateralemalatomozzo{i}.png"), True, False), (64*MOD, 78*MOD)) for i in range(1, 4)],
            "button":          pygame.image.load("assets/tasti/button_mozzo.png"),
        },
        "info": {
            "name": "Marinaio",
            "descrizione": "Forza lavoro base della nave. Necessario per le manovre.",
            "abilita": "Più marinai = più difensori contro i pirati.",
            "ruolo": "marinaio",
        },
    },
    # ── MECCANICO ─────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 15, "alive": True, "morale": 100},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle":           [pygame.transform.scale(pygame.image.load(f"assets/personaggi/carpentiere/idle/carpidle{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 5)],
            "walk_forward":   [pygame.transform.scale(pygame.image.load(f"assets/personaggi/carpentiere/camminata_in_avanti/carpentiere_camminatainavanti{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 5)],
            "walk_cycle":     [pygame.transform.scale(pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip/carpentiere_camminatalaterale{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 5)],
            "walk_cycle_sick":[pygame.transform.scale(pygame.image.load(f"assets/personaggi/carpentiere/camminata_a_destrasinistra_con_flip_ammalato/carpentiere_camminatalateraleammalato{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 5)],
            "button":          pygame.image.load("assets/tasti/button_carpentiere.png"),
        },
        "info": {
            "name": "Meccanico",
            "descrizione": "Esperto nella riparazione della nave. Gestisce i danni al timone.",
            "abilita": "Danni al timone: solo +1 settimana invece di 2-4.",
            "ruolo": "meccanico",
        },
    },
    # ── BARDO ─────────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 10, "alive": True, "morale": 100},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle":           [pygame.transform.scale(pygame.image.load(f"assets/personaggi/bardo/idle/bardoidle{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 3)],
            "walk_forward":   [pygame.transform.scale(pygame.image.load(f"assets/personaggi/bardo/camminata_in_avanti/bardo_camminatainavanti{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 4)],
            "walk_cycle":     [pygame.transform.scale(pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip/bardo_camminatalaterale{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 4)],
            "walk_cycle_sick":[pygame.transform.scale(pygame.image.load(f"assets/personaggi/bardo/camminata_a_destrasinistra_con_flip_ammalato/bardo_camminatalateraleammalato{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 4)],
            "button":          pygame.image.load("assets/tasti/button_bardo.png"),
        },
        "info": {
            "name": "Bardo",
            "descrizione": "Intrattiene l'equipaggio con musica e storie. Sostiene il morale.",
            "abilita": "Riduce il consumo di morale durante le tempeste.",
            "ruolo": "bardo",
        },
    },
    # ── TESORIERE ─────────────────────────────────────────────────────────────
    {
        "stats": {"cost": 20, "alive": True, "morale": 100},
        "pos": {
            "scelta_equip": {
                "x": WIDTH // 10,
                "y": (HEIGHT // 2) + (HEIGHT // 10),
                "x_fine": (WIDTH // 2) + (WIDTH // 10),
                "y_fine": (HEIGHT // 2) - (HEIGHT // 16),
            },
            "main": {
                "x_attuale": random.randint(int(400*MOD), int(WIDTH - 420*MOD)),
                "y_attuale": random.randint(int(430*MOD), int(470*MOD)),
            },
        },
        "sprites": {
            "idle":           [pygame.transform.scale(pygame.image.load(f"assets/personaggi/tesoriere/idle/cercatore_di_tesori_idle{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 7)],
            "walk_forward":   [pygame.transform.scale(pygame.image.load(f"assets/personaggi/tesoriere/camminata_in_avanti/camminata_in_avanti{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 7)],
            "walk_cycle":     [pygame.transform.scale(pygame.image.load(f"assets/personaggi/tesoriere/camminata_a_destrasinistra_con_flip/camminata_lateralec{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 8)],
            "walk_cycle_sick":[pygame.transform.scale(pygame.image.load(f"assets/personaggi/tesoriere/camminata_a_destrasinistra_con_flip_ammalato/camminata_lateralecmalato{i}.png"), (64*MOD, 78*MOD)) for i in range(1, 8)],
            "button":          pygame.image.load("assets/tasti/button_tesoriere.png"),
        },
        "info": {
            "name": "Tesoriere",
            "descrizione": "Esperto di affari e commerci. Sa come ottenere il massimo dalle trattative.",
            "abilita": "Aumenta l'efficacia del baratto nel nuovo mondo.",
            "ruolo": "tesoriere",
        },
    },
]

# ─── CIBO ─────────────────────────────────────────────────────────────────────
# "cost"       = monete per 1 acquisto  (pagate subito)
# "saturazione"= kg (o barili) aggiunti a ogni acquisto
# "tipo_cibo"  = usato in main.py per sommare le scorte per categoria
#
# Consumi settimanali per persona (dal PDF):
#   verdura  0.5 kg  →  1 acquisto da 1 kg copre 2 persone per 1 settimana
#   frutta   1.0 kg  →  1 acquisto da 1 kg copre 1 persona  per 1 settimana
#   carne    1.0 kg  →  1 acquisto da 1 kg copre 1 persona  per 1 settimana
#   acqua    0.5 bar →  1 acquisto da 1 bar copre 2 persone per 1 settimana

CIBO = [
    # ── VERDURA (PDF: 0.5 monete/kg) ──────────────────────────────────────────
    {
        "stats": {"cost": 0.5, "saturazione": 1.0, "tipo_cibo": "verdura"},
        "info": {"name": "verdura", "descrizione": "Verdura fresca - 1 kg per acquisto (0.5 monete/kg)"},
        "sprites": {
            "sprite": pygame.image.load("assets/cibo/trasparenti/carote.png"),
            "button": pygame.image.load("assets/cibo/button/carote_button.png"),
        }
    },
    # ── FRUTTA (PDF: 1 moneta/kg) ─────────────────────────────────────────────
    {
        "stats": {"cost": 1.0, "saturazione": 1.0, "tipo_cibo": "frutta"},
        "info": {"name": "frutta", "descrizione": "Frutta fresca - 1 kg per acquisto (1 moneta/kg)"},
        "sprites": {
            "sprite": pygame.image.load("assets/cibo/trasparenti/banane.png"),
            "button": pygame.image.load("assets/cibo/button/banane_button.png"),
        }
    },
    # ── CARNE (PDF: 2 monete/kg) ──────────────────────────────────────────────
    {
        "stats": {"cost": 2.0, "saturazione": 1.0, "tipo_cibo": "carne"},
        "info": {"name": "carne", "descrizione": "Carne salata - 1 kg per acquisto (2 monete/kg)"},
        "sprites": {
            "sprite": pygame.image.load("assets/cibo/trasparenti/carne_2.png"),
            "button": pygame.image.load("assets/cibo/button/carne_2_button.png"),
        }
    },
    # ── LEGUMI (extra, conta come verdura — stesso prezzo) ────────────────────
    {
        "stats": {"cost": 0.5, "saturazione": 1.0, "tipo_cibo": "verdura"},
        "info": {"name": "legumi", "descrizione": "Legumi - 1 kg per acquisto, contano come verdura (0.5 monete/kg)"},
        "sprites": {
            "sprite": pygame.image.load("assets/cibo/trasparenti/legumi(piselli).png"),
            "button": pygame.image.load("assets/cibo/button/legumi(piselli)_button.png"),
        }
    },
    # ── RISO (extra, conta come carne — carboidrati/proteine) ─────────────────
    {
        "stats": {"cost": 1.5, "saturazione": 1.0, "tipo_cibo": "carne"},
        "info": {"name": "riso", "descrizione": "Riso - 1 kg per acquisto, conta come carne (1.5 monete/kg)"},
        "sprites": {
            "sprite": pygame.image.load("assets/cibo/trasparenti/riso.png"),
            "button": pygame.image.load("assets/cibo/button/riso_button.png"),
        }
    },
    # ── PESCE (extra, conta come carne) ───────────────────────────────────────
    {
        "stats": {"cost": 1.5, "saturazione": 1.0, "tipo_cibo": "carne"},
        "info": {"name": "pesce", "descrizione": "Pesce essiccato - 1 kg per acquisto, conta come carne (1.5 monete/kg)"},
        "sprites": {
            "sprite": pygame.image.load("assets/cibo/trasparenti/pesce.png"),
            "button": pygame.image.load("assets/cibo/button/pesce_button.png"),
        }
    },
]


BIBITE = [
    # ── ACQUA (PDF: 0.5 monete/barile) ───────────────────────────────────────
    {
        "stats": {"cost": 0.5, "saturazione": 1.0},
        "info": {"name": "acqua", "descrizione": "Acqua potabile - 1 barile per acquisto (0.5 monete/barile)"},
        "sprites": {"button": pygame.image.load("assets/cibo/button/button_acqua.png")}
    },
    # ── BIRRA (extra, idrata a metà rispetto all'acqua) ───────────────────────
    {
        "stats": {"cost": 1.5, "saturazione": 0.5},
        "info": {"name": "birra", "descrizione": "Birra - 1 bottiglia per acquisto, idrata 0.5 barili (1.5 monete)"},
        "sprites": {"button": pygame.image.load("assets/cibo/button/button_birra.png")}
    },
    # ── ENERGIZZANTE (extra, idrata a metà) ───────────────────────────────────
    {
        "stats": {"cost": 2.0, "saturazione": 0.5},
        "info": {"name": "Energizzante", "descrizione": "Energizzante - 1 bottiglia per acquisto, idrata 0.5 barili (2 monete)"},
        "sprites": {"button": pygame.image.load("assets/cibo/button/button_energizante.png")}
    },
    # ── VINO (extra, idrata pochissimo — lusso) ───────────────────────────────
    {
        "stats": {"cost": 3.0, "saturazione": 0.25},
        "info": {"name": "vino", "descrizione": "Vino pregiato - 1 bottiglia per acquisto, idrata 0.25 barili (3 monete)"},
        "sprites": {"button": pygame.image.load("assets/cibo/button/button_calice.png")}
    },
]

MERCI = [
    # ── MEDICINALE (PDF: 1 moneta/bottiglia) ──────────────────────────────────
    {
        "stats": {"cost": 1.0, "tipo": "medicinale"},
        "info": {"name": "medicinale", "descrizione": "Medicinale - 1 bottiglia (1 moneta). Cura 1 malato durante l'epidemia."},
        "sprites": {"button": pygame.transform.scale(pygame.image.load("assets/equip/button_medicinale.png"), (120, 120))}
    },
    # ── ARMI (PDF: 5 monete/arma) ─────────────────────────────────────────────
    {
        "stats": {"cost": 5.0, "tipo": "arma"},
        "info": {"name": "armi", "descrizione": "Arma - 1 pezzo (5 monete). Difende dai pirati. NON barattabile."},
        "sprites": {"button": pygame.transform.scale(pygame.image.load("assets/equip/button_ARMI.png"), (120, 120))}
    },
    # ── SALE (PDF: 0.5 monete/sacco) ──────────────────────────────────────────
    {
        "stats": {"cost": 0.5, "tipo": "baratto"},
        "info": {"name": "sale", "descrizione": "Sale - 1 sacco (0.5 monete). Barattabile nel nuovo mondo."},
        "sprites": {"button": pygame.transform.scale(pygame.image.load("assets/equip/button_sale.png"), (120, 120))}
    },
    # ── COLTELLI (PDF: 0.5 monete/pezzo) ─────────────────────────────────────
    {
        "stats": {"cost": 0.5, "tipo": "baratto"},
        "info": {"name": "coltelli", "descrizione": "Coltello - 1 pezzo (0.5 monete). Barattabile nel nuovo mondo."},
        "sprites": {"button": pygame.transform.scale(pygame.image.load("assets/equip/button_coltelli.png"), (120, 120))}
    },
    # ── STOFFA (PDF: 2 monete/telo) ───────────────────────────────────────────
    {
        "stats": {"cost": 2.0, "tipo": "baratto"},
        "info": {"name": "stoffa", "descrizione": "Stoffa - 1 telo (2 monete). Barattabile nel nuovo mondo."},
        "sprites": {"button": pygame.transform.scale(pygame.image.load("assets/equip/button_stoffa.png"), (120, 120))}
    },
    # ── DIAMANTI (PDF: 1 moneta/pezzo) ────────────────────────────────────────
    {
        "stats": {"cost": 1.0, "tipo": "baratto"},
        "info": {"name": "diamanti", "descrizione": "Diamante - 1 pezzo (1 moneta). Barattabile nel nuovo mondo."},
        "sprites": {"button": pygame.transform.scale(pygame.image.load("assets/equip/button_diamanti.png"), (120, 120))}
    },
]


EVENTI = [
    # [0] UOMO IN MARE
    {
        "nome": "UOMO IN MARE",
        "descrizione": "Un membro a caso finisce in mare e muore.",
        "funzione": gestione_eventi.anima_caduta_in_mare,
        "sprites": {
            "idle1": [pygame.image.load(f"assets/eventi/caduta_personaggio/carpe/mozzoidle{i}.png") for i in range(1, 4)],
            "idle2": [pygame.image.load(f"assets/eventi/caduta_personaggio/cuoco/cuocoidleg{i}.png") for i in range(1, 7)],
        }
    },
    # [1] VERDURA IN MARE
    {
        "nome": "VERDURA IN MARE",
        "descrizione": "Una tempesta disperde 1/2, 1/3, 1/4 o 1/5 della verdura.",
        "funzione": gestione_eventi.anima_caduta_in_mare,
        "sprites": {"verdura": [pygame.image.load("assets/eventi/cadutaverdura/legumi(piselli).png")]}
    },
    # [2] FRUTTA IN MARE
    {
        "nome": "FRUTTA IN MARE",
        "descrizione": "Una tempesta disperde 1/2, 1/3, 1/4 o 1/5 della frutta.",
        "funzione": gestione_eventi.anima_caduta_in_mare,
        "sprites": {"frutta": [pygame.image.load("assets/eventi/caduta_frutta/banane.png")]}
    },
    # [3] CARNE IN MARE
    {
        "nome": "CARNE IN MARE",
        "descrizione": "Una tempesta disperde 1/2, 1/3, 1/4 o 1/5 della carne.",
        "funzione": gestione_eventi.anima_caduta_in_mare,
        "sprites": {"carne": [pygame.image.load("assets/eventi/caduta_carne/carne_2.png")]}
    },
    # [4] ACQUA IN MARE
    {
        "nome": "ACQUA IN MARE",
        "descrizione": "Una tempesta disperde 1/2, 1/3, 1/4 o 1/5 dell'acqua.",
        "funzione": gestione_eventi.anima_caduta_in_mare,
        "sprites": {"acqua": [pygame.image.load("assets/eventi/caduta_acqua/acqua.png")]}
    },
    # [5] PESCA MIRACOLOSA
    {
        "nome": "PESCA MIRACOLOSA",
        "descrizione": "L'equipaggio pesca: +11/20 kg di carne.",
        "funzione": gestione_eventi.anima_pescamiracolosa,
        "sprites": {"pesce": [pygame.image.load(f"assets/eventi/pesca_miracolosa/pesce/pesce{i}.png") for i in range(1, 7)]}
    },
    # [6] TEMPESTA MIRACOLOSA
    {
        "nome": "TEMPESTA MIRACOLOSA",
        "descrizione": "Raccolgono acqua piovana: +11/20 barili di acqua.",
        "funzione": gestione_eventi.anima_caduta_in_mare,
        "sprites": {"barile": [pygame.image.load("assets/eventi/tempesta_miracolosa/barile.png")]}
    },
    # [7] VENTI FAVOREVOLI
    {
        "nome": "VENTI FAVOREVOLI",
        "descrizione": "Il viaggio si accorcia di 1 settimana. Morale +5/+15.",
        "funzione": gestione_eventi.animazione_divento,
    },
    # [8] CATTIVO TEMPO
    {
        "nome": "CATTIVO TEMPO",
        "descrizione": "Rovesciate 1/2, 1/3, 1/4 o 1/5 dei medicinali.",
        "funzione": gestione_eventi.animazione_divento,
        "sprites": {"cattivo_tempo": [pygame.image.load(f"assets/eventi/cattivotempo/rain{i}.png") for i in range(1, 4)]}
    },
    # [9] ONDATA
    {
        "nome": "ONDATA",
        "descrizione": "Un'onda rovescia 1/2, 1/3, 1/4 o 1/5 delle armi.",
        "funzione": gestione_eventi.animazione_ondata,
        "sprites": {"ondata": [pygame.image.load(f"assets/ondata/onda{i}.png") for i in range(1, 4)]}
    },
    # [10] INFESTAZIONE RATTI
    {
        "nome": "INFESTAZIONE RATTI",
        "descrizione": "I ratti rovinano 1/2, 1/3, 1/4 o 1/5 delle stoffe.",
        "funzione": gestione_eventi.anima_topo,
        "sprites": {
            "run up":    [pygame.image.load(f"assets/eventi/infestazioneratti/runuptopo/runuptopo{i}.png") for i in range(1, 5)],
            "run down":  [pygame.image.load(f"assets/eventi/infestazioneratti/rundowtopo/rundowtopo{i}.png") for i in range(1, 5)],
            "run right": [pygame.transform.flip(pygame.image.load(f"assets/eventi/infestazioneratti/rundirectiontopo/runrighttopo{i}.png"), True, False) for i in range(1, 5)],
            "run left":  [pygame.transform.flip(pygame.image.load(f"assets/eventi/infestazioneratti/rundirectiontopo/runrighttopo{i}.png"), False, False) for i in range(1, 5)],
        }
    },
    # [11] AVVISTAMENTO ALBATRO
    {
        "nome": "AVVISTAMENTO ALBATRO",
        "descrizione": "Puoi sparare all'albatro per ottenere carne, ma attiri sfortuna. Max 3 avvistamenti.",
        "funzione": gestione_eventi.animazione_albatro,
        "sprites": {"run right": [pygame.image.load(f"assets/eventi/albatro/animazione/albatro{i}.png") for i in range(1, 20)]},
    },
    # [12] AVVISTAMENTO SCIALUPPA
    {
        "nome": "AVVISTAMENTO SCIALUPPA",
        "descrizione": "4 naufraghi con una cassa. Se li salvi: +4 membri e +10/20 unità per ogni merce.",
        "funzione": gestione_eventi.animazione_scialuppa,
        "sprites": {
            "scialuppa": [pygame.image.load(f"assets/eventi/avvistamento_scialuppa/barca/barca{i}.png") for i in range(1, 3)],
            "sfondo":    [pygame.image.load(f"assets/eventi/avvistamento_scialuppa/sfondo/sfondobarca{i}.png") for i in range(1, 5)],
        }
    },
    # [13] EPIDEMIA
    {
        "nome": "EPIDEMIA",
        "descrizione": "Ogni membro non-medico ha 70% di ammalarsi. Il medico cura usando 1 medicinale/persona.",
        "funzione": gestione_eventi.animazione_epidemia,
    },
    # [14] ATTACCO PIRATA
    {
        "nome": "ATTACCO PIRATA",
        "descrizione": "3-10 pirati attaccano. Difensori = min(armi, membri vivi). Perdite = pirati - difensori.",
        "funzione": gestione_eventi.animazione_attacco_pirata_caduta_proiettili,
        "sprites": {"proiettile": [pygame.image.load(f"assets/eventi/attacco_pirata/proiettile{i}.png") for i in range(1, 8)]}
    },
    # [15] DANNI AL TIMONE
    {
        "nome": "DANNI AL TIMONE",
        "descrizione": "Con meccanico: +1 sett. Senza: +2/4 sett.",
        "funzione": gestione_eventi.animazione_timone_rotto,
        "sprites": {"timone": [pygame.image.load("assets/timone/timone.png")]}
    },
    # [16] RAFFICHE DI VENTO
    {
        "nome": "RAFFICHE DI VENTO",
        "descrizione": "Con navigatore: +1 sett. Senza: +2/4 sett.",
        "funzione": gestione_eventi.animazione_divento,
        "sprites": {"vento": [pygame.transform.flip(pygame.image.load(f"assets/eventi/venti/soffio/vento{i}.png"), True, False) for i in range(1, 9)]}
    },
    # [17] VENTO FAVOREVOLE (usato da main.py per l'animazione dei venti favorevoli)
    {
        "nome": "VENTO FAVOREVOLE",
        "descrizione": "Vento favorevole — accorcia il viaggio di 1 settimana.",
        "funzione": gestione_eventi.animazione_divento,
        "sprites": {"vento": [pygame.image.load(f"assets/eventi/venti/soffio/vento{i}.png") for i in range(1, 9)]},
    },
    # [18] AVVISTAMENTO ISOLA
    {
        "nome": "AVVISTAMENTO ISOLA",
        "descrizione": "Approdi? +1/2 sett. 50% abitata, 50% ostili. Se amichevoli: +5/20 merci (o +20/40 con albatro).",
        "funzione": gestione_eventi.animazione_isola,
        "sprites": {"isola": [pygame.image.load(f"assets/eventi/isola/isola{i}.png") for i in range(1, 3)]}
    },
    # [19] NESSUN IMPREVISTO
    {
        "nome": "NESSUN IMPREVISTO",
        "descrizione": "Non succede nulla in questa settimana.",
    },
]

# ─── BUTTON RECTS (schermata scelta equipaggiamento) ──────────────────────────

BUTTON_RECTS = [
    pygame.Rect( 10 * MOD,  10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
    pygame.Rect( 10 * MOD, 125 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
    pygame.Rect(115 * MOD, 125 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
    pygame.Rect(115 * MOD,  10 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
    pygame.Rect( 10 * MOD, 225 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
    pygame.Rect(115 * MOD, 225 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
    pygame.Rect( 10 * MOD, 345 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
    pygame.Rect(115 * MOD, 345 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
    pygame.Rect( 10 * MOD, 445 * MOD, WIDTH_BUTTON, HEIGHT_BUTTON),
]

# ─── POSIZIONI SULLA BARCA (scelta equipaggiamento) ───────────────────────────

BARCA_POS = [
    (HEIGHT//2-HEIGHT//16+510*MOD, HEIGHT//2-HEIGHT//16-79*MOD),
    (HEIGHT//2-HEIGHT//16+510*MOD+63*MOD, HEIGHT//2-HEIGHT//16-79*MOD-22*MOD),
    (HEIGHT//2-HEIGHT//16+510*MOD+120*MOD, HEIGHT//2-HEIGHT//16-79*MOD-20*MOD),
    (HEIGHT//2-HEIGHT//16+510*MOD+120*MOD, HEIGHT//2-HEIGHT//16-79*MOD+12*MOD),
    (HEIGHT//2-HEIGHT//16+510*MOD+120*MOD, HEIGHT//2-HEIGHT//16-79*MOD+32*MOD),
    (HEIGHT//2+230*MOD, HEIGHT//2-HEIGHT//16-50*MOD),
    (HEIGHT//2-HEIGHT//16+390*MOD, HEIGHT//2-HEIGHT//16-40*MOD),
    ((HEIGHT//2-HEIGHT//16+440*MOD+HEIGHT//2+215*MOD)//2-10*MOD, HEIGHT//2-HEIGHT//16-10*MOD-40*MOD),
    (HEIGHT//2-HEIGHT//16+110*MOD, HEIGHT//2-HEIGHT//16-30*MOD),
    (HEIGHT//2-HEIGHT//16+205*MOD, HEIGHT//2-HEIGHT//16-20*MOD),
    (HEIGHT//2-HEIGHT//16+440*MOD, HEIGHT//2-HEIGHT//16-10*MOD),
    ((HEIGHT//2-HEIGHT//16+440*MOD+HEIGHT//2+215*MOD)//2-10*MOD, HEIGHT//2-HEIGHT//16-10*MOD+15*MOD),
    (HEIGHT//2+215*MOD, HEIGHT//2-HEIGHT//16),
    (HEIGHT//2-HEIGHT//16+408*MOD, HEIGHT//2-HEIGHT//16),
    (HEIGHT//2-HEIGHT//16+110*MOD-60*MOD, HEIGHT//2-HEIGHT//16-30*MOD-13*MOD),
    (HEIGHT//2-HEIGHT//16+110*MOD-60*MOD, HEIGHT//2-HEIGHT//16-30*MOD-40*MOD),
]