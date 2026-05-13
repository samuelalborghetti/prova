
import json
import copy
import os

PERCORSO_SALVATAGGIO = "./dati/salvataggio.json"


def personaggi(personaggi_scelti: list) -> list:
    risultato = []
    for p in personaggi_scelti:
        risultato.append({
            "name":  p["info"]["name"],
            "stats": copy.deepcopy(p["stats"]),
            "pos":   copy.deepcopy(p["pos"]),
            "info":  copy.deepcopy(p["info"]),
        })
    return risultato


def merci(lista_merci: list) -> list:
    risultato = []
    for m in lista_merci:
        voce = {
            "name":  m["info"]["name"],
            "info":  copy.deepcopy(m["info"]),
            "stats": copy.deepcopy(m["stats"]),
        }
        risultato.append(voce)
    return risultato


def Carica_personaggi(dati_salvati: list, PERSONAGGI_ORIGINALI: list) -> list:
    personaggi_interi= []
    for dati in dati_salvati:
        nome = dati["name"]
        sprites_originali = None
        for p_orig in PERSONAGGI_ORIGINALI:
            if p_orig["info"]["name"] == nome:
                sprites_originali = p_orig["sprites"]
                break

        personaggio = {
            "stats":   dati["stats"],
            "pos":     dati["pos"],
            "sprites": sprites_originali,   # oggetti pygame, non salvabili → si ricollegano qui
            "info":    dati["info"],
        }
        personaggi_interi.append(personaggio)
    return personaggi_interi


def Carica_merci(dati_salvati: list, MERCI_ORIGINALI: list) -> list:
    merci_intere = []
    for dati in dati_salvati:
        nome = dati["name"]
        sprites_originali = None
        for m_orig in MERCI_ORIGINALI:
            if m_orig["info"]["name"] == nome:
                if "sprites" in m_orig:
                    sprites_originali = m_orig["sprites"]
                break

        merce = {
            "info":  dati["info"],
            "stats": dati["stats"],
        }
        if sprites_originali:
            merce["sprites"] = sprites_originali

        merci_intere.append(merce)
    return merci_intere

#Funzione da usare anche di là
def esiste_salvataggio(percorso: str = PERCORSO_SALVATAGGIO) -> bool:
    try:
        with open(percorso, "r", encoding="utf-8") as f:
            dati = json.load(f)
        # Controlla che i campi obbligatori siano presenti
        campi_richiesti = [
            "settimana_corrente", "numero_settimane", "razioni_attuali",
            "merce_attuale", "consumi_base", "flag_dimezzamento_razioni",
            "soldi_rimanenti", "bonus_morale", "albatro_avvistato",
            "albatro_ucciso", "mazzo_eventi", "personaggi", "lista_merci"
        ]
        return all(campo in dati for campo in campi_richiesti)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return False


def SalvaPartita(
    percorso: str,
    settimana_corrente: int,
    numero_settimane: int,
    razioni_attuali: dict,
    merce_attuale: dict,
    consumi_base: dict,
    flag_dimezzamento_razioni: dict,
    soldi_rimanenti: float,
    bonus_morale: int,
    albatro_avvistato: int,
    albatro_ucciso,
    mazzo_eventi: list,
    personaggi_scelti: list,
    lista_merci: list,
):
    dati = {
        "settimana_corrente":        settimana_corrente,
        "numero_settimane":          numero_settimane,
        "razioni_attuali":           razioni_attuali,
        "merce_attuale":             merce_attuale,
        "consumi_base":              consumi_base,
        "flag_dimezzamento_razioni": flag_dimezzamento_razioni,
        "soldi_rimanenti":           soldi_rimanenti,
        "bonus_morale":              bonus_morale,
        "albatro_avvistato":         albatro_avvistato,
        "albatro_ucciso":            albatro_ucciso,
        "mazzo_eventi":              mazzo_eventi,
        "personaggi":                personaggi(personaggi_scelti),
        "lista_merci":               merci(lista_merci),
    }

    with open(percorso, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=4)


def CaricaPartita(
    percorso: str,
    PERSONAGGI_ORIGINALI: list,
    MERCI_ORIGINALI: list,
):

    with open(percorso, "r", encoding="utf-8") as f:
        dati = json.load(f)

    stato = {
        "settimana_corrente":        dati["settimana_corrente"],
        "numero_settimane":          dati["numero_settimane"],
        "razioni_attuali":           dati["razioni_attuali"],
        "merce_attuale":             dati["merce_attuale"],
        "consumi_base":              dati["consumi_base"],
        "flag_dimezzamento_razioni": dati["flag_dimezzamento_razioni"],
        "soldi_rimanenti":           dati["soldi_rimanenti"],
        "bonus_morale":              dati["bonus_morale"],
        "albatro_avvistato":         dati["albatro_avvistato"],
        "albatro_ucciso":            dati["albatro_ucciso"],
        "mazzo_eventi":              dati["mazzo_eventi"],
        "personaggi_scelti":         Carica_personaggi(dati["personaggi"], PERSONAGGI_ORIGINALI),
        "lista_merci":               Carica_merci(dati["lista_merci"], MERCI_ORIGINALI),
    }
    return stato


def EliminaSalvataggio(percorso: str = PERCORSO_SALVATAGGIO):
    try:
        os.remove(percorso)
    except FileNotFoundError:
        pass
