import pygame
import random
from utility import MOD, HEIGHT, WIDTH, font_numeri, title_font, info_font, BIANCO
from eventi import mostra_messaggio_evento

TASSI_CAMBIO = {
    "sale": [0.5, 0.5, 1.0],
    "stoffa": [5, 7, 3],
    "coltelli": [1, 3, 6],
    "diamanti": [2, 4, 4],
}

LISTA_VALUTE = ["perle", "manufatti", "spezie"]
LISTA_MERCI_BARATTABILI = ["sale", "stoffa", "coltelli", "diamanti"]

VALORE_IN_PATRIA = {
    "perle": 2,
    "manufatti": 2,
    "spezie": 1,
}

LISTA_OFFERTE_ASTA = [50, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 1200]
OFFERTE_SEMPRE_RIPROPONIBILI = [50, 300, 400, 450]

def conta_merce_per_nome(lista_equip, nome_cercato):
    contatore = 0
    for oggetto in lista_equip:
        if oggetto["info"]["name"] == nome_cercato:
            contatore += 1
    return contatore

def presenza_ruolo(personaggi, ruolo_cercato):
    for personaggio in personaggi:
        if personaggio["stats"]["alive"] and personaggio["info"]["ruolo"] == ruolo_cercato:
            return True
    return False

def divisione_intera(dividendo, divisore):
    risultato = 0
    accumulatore = divisore
    while accumulatore <= dividendo:
        risultato += 1
        accumulatore += divisore
    return risultato

def valore_assoluto(numero):
    if numero < 0:
        return numero * -1
    return numero

def arrotonda_intero(numero_decimale):
    parte_intera = int(numero_decimale)
    parte_decimale = numero_decimale - parte_intera
    if parte_decimale >= 0.5:
        return parte_intera + 1
    return parte_intera

def trova_offerta_col_profitto_maggiore(lista_offerte):
    posizione_migliore = 0
    profitto_piu_alto = lista_offerte[0]["profitto_stimato"]
    posizione_corrente = 1
    while posizione_corrente < len(lista_offerte):
        profitto_corrente = lista_offerte[posizione_corrente]["profitto_stimato"]
        if profitto_corrente > profitto_piu_alto:
            profitto_piu_alto = profitto_corrente
            posizione_migliore = posizione_corrente
        posizione_corrente += 1
    return posizione_migliore

def calcola_offerte_baratto(nome_merce, quantita_merce):
    tassi_merce = TASSI_CAMBIO[nome_merce]
    lista_offerte = []
    posizione = 0
    while posizione < len(LISTA_VALUTE):
        nome_valuta = LISTA_VALUTE[posizione]
        tasso_corrente = tassi_merce[posizione]
        quantita_ottenuta = divisione_intera(quantita_merce, tasso_corrente)
        profitto_stimato = quantita_ottenuta * VALORE_IN_PATRIA[nome_valuta]
        lista_offerte.append({
            "valuta": nome_valuta,
            "quantita_ottenuta": quantita_ottenuta,
            "profitto_stimato": profitto_stimato,
        })
        posizione += 1
    return lista_offerte

def calcola_paga_totale_equipaggio(personaggi_ingaggiati, numero_settimane_totali):
    totale_paga = 0
    for personaggio in personaggi_ingaggiati:
        paga_settimanale = personaggio["stats"]["cost"]
        totale_paga += paga_settimanale * numero_settimane_totali
    return totale_paga

def rimuovi_tutte_le_armi(lista_equip):
    posizione = 0
    while posizione < len(lista_equip):
        if lista_equip[posizione]["stats"]["tipo"] == "arma":
            lista_equip.pop(posizione)
        else:
            posizione += 1

def testo_saldo(saldo_finale):
    if saldo_finale > 0:
        return "Il viaggio e' stato profittevole!"
    elif saldo_finale == 0:
        return "Pari e patta: niente guadagno, niente debiti."
    else:
        return "Le spese superano i profitti. Servono " + str(valore_assoluto(saldo_finale)) + " monete extra."

def arrivo_nuovo_mondo(lista_equip):
    nave_ha_armi = False
    for oggetto in lista_equip:
        if oggetto["stats"]["tipo"] == "arma":
            nave_ha_armi = True
    if nave_ha_armi:
        scelta = mostra_messaggio_evento(
            titolo="AVVISTAMENTO INDIGENI!",
            domanda="Indigeni curiosi e armati spiano l'arrivo della nave.",
            motivo="L'equipaggio chiede: apriamo il fuoco?",
            scelte=["Apri il fuoco", "Non sparare"]
        )
        if scelta == "Apri il fuoco":
            mostra_messaggio_evento(
                titolo="FINE PARTITA",
                domanda="Avete aperto il fuoco sugli indigeni.",
                motivo="L'intera spedizione viene annientata. Fine del viaggio.",
                scelte=["Fine partita"]
            )
            return False
    mostra_messaggio_evento(
        titolo="BENVENUTI NEL NUOVO MONDO!",
        domanda="Gli indigeni vi accolgono con grande entusiasmo.",
        motivo="Domani inizia il baratto con il capo tribu'."
    )
    return True

def fase_baratto(lista_equip):
    mostra_messaggio_evento(
        titolo="IL BARATTO HA INIZIO",
        domanda="Il capo tribu' e' pronto a trattare.",
        motivo="Non accetta armi ne' medicinali. Si baratta solo sale, stoffa, coltelli e diamanti."
    )
    carico_nave = {"perle": 0, "manufatti": 0, "spezie": 0}
    posizione_merce = 0
    while posizione_merce < len(LISTA_MERCI_BARATTABILI):
        nome_merce = LISTA_MERCI_BARATTABILI[posizione_merce]
        quantita_merce = conta_merce_per_nome(lista_equip, nome_merce)
        if quantita_merce == 0:
            mostra_messaggio_evento(
                titolo="BARATTO " + nome_merce.upper(),
                domanda="Non hai " + nome_merce + " da barattare.",
                motivo="Il capo tribu' passa alla merce successiva."
            )
            posizione_merce += 1
            continue
        lista_offerte = calcola_offerte_baratto(nome_merce, quantita_merce)
        posizione_migliore = trova_offerta_col_profitto_maggiore(lista_offerte)
        scelte_da_mostrare = []
        posizione_offerta = 0
        while posizione_offerta < len(lista_offerte):
            offerta_corrente = lista_offerte[posizione_offerta]
            if posizione_offerta == posizione_migliore:
                prefisso = "* "
            else:
                prefisso = "  "
            testo_offerta = (prefisso + str(posizione_offerta + 1) + ") " + str(offerta_corrente["quantita_ottenuta"]) + " " + offerta_corrente["valuta"] + "  (stimato: " + str(offerta_corrente["profitto_stimato"]) + " monete)")
            scelte_da_mostrare.append(testo_offerta)
            posizione_offerta += 1
        scelta_giocatore = mostra_messaggio_evento(
            titolo="BARATTO: " + nome_merce.upper() + " (x" + str(quantita_merce) + ")",
            domanda="Il capo tribu' propone tre scambi. Scegli uno:",
            motivo="* = offerta con profitto stimato maggiore",
            scelte=scelte_da_mostrare
        )
        offerta_scelta = lista_offerte[0]
        posizione_ricerca = 0
        while posizione_ricerca < len(scelte_da_mostrare):
            if scelte_da_mostrare[posizione_ricerca] == scelta_giocatore:
                offerta_scelta = lista_offerte[posizione_ricerca]
            posizione_ricerca += 1
        nome_valuta_scelta = offerta_scelta["valuta"]
        quantita_valuta_ottenuta = offerta_scelta["quantita_ottenuta"]
        carico_nave[nome_valuta_scelta] += quantita_valuta_ottenuta
        mostra_messaggio_evento(
            titolo="BARATTO CONFERMATO",
            domanda=(str(quantita_merce) + " " + nome_merce + " scambiati con " + str(quantita_valuta_ottenuta) + " " + nome_valuta_scelta + "."),
            motivo="Profitto stimato: " + str(offerta_scelta["profitto_stimato"]) + " monete d'oro."
        )
        posizione_merce += 1
    mostra_messaggio_evento(
        titolo="BARATTO COMPLETATO",
        domanda="Tutti i baratti sono stati conclusi.",
        motivo=("Carico: "+ str(carico_nave["perle"]) + " perle | "+ str(carico_nave["manufatti"]) + " manufatti | "+ str(carico_nave["spezie"]) + " spezie."))
    return carico_nave

def fase_tradimento(lista_equip, carico_nave, albatro_avvistato, albatro_ucciso):
    numero_armi = conta_merce_per_nome(lista_equip, "armi")
    if numero_armi == 0:
        return carico_nave, True
    
    perle_offerte_dal_rivale = numero_armi * 30
    scelta = mostra_messaggio_evento(
        titolo="OFFERTA NELLA NOTTE...",
        domanda=("Un rivale del capo tribu' ti offre " + str(perle_offerte_dal_rivale) + " perle per tutte le " + str(numero_armi) + " armi."),
        motivo="Le sue intenzioni non sembrano buone... Accetti?",
        scelte=["Accetta l'offerta", "Rifiuta"]
    )
    
    if scelta == "Accetta l'offerta":
        if albatro_avvistato > 0 and albatro_ucciso == True:
            mostra_messaggio_evento(
                titolo="SCOPERTO!",
                domanda="Il capo tribu' ha saputo del tradimento!",
                motivo="La sfortuna dell'albatro ucciso vi perseguita. Fine del viaggio.",
                scelte=["Fine partita"]
            )
            return carico_nave, False
        
        elif albatro_avvistato > 0 and albatro_ucciso == False:
            carico_nave["perle"] += perle_offerte_dal_rivale
            rimuovi_tutte_le_armi(lista_equip)
            mostra_messaggio_evento(
                titolo="TRADIMENTO RIUSCITO!",
                domanda="Il capo tribu' non ha scoperto nulla.",
                motivo=("L'albatro risparmiato ha portato fortuna! +" + str(perle_offerte_dal_rivale) + " perle. Armi azzerate."))
        
        else:
            dado = random.randint(1, 2)
            if dado == 1:
                mostra_messaggio_evento(
                    titolo="SCOPERTO!",
                    domanda="Il capo tribu' ha scoperto il tradimento!",
                    motivo="Fine del viaggio. L'intero equipaggio viene annientato.",
                    scelte=["Fine partita"]
                )
                return carico_nave, False
            else:
                carico_nave["perle"] += perle_offerte_dal_rivale
                rimuovi_tutte_le_armi(lista_equip)
                mostra_messaggio_evento(
                    titolo="TRADIMENTO RIUSCITO!",
                    domanda="Fortuna! Il capo tribu' non ha scoperto nulla.",
                    motivo="+" + str(perle_offerte_dal_rivale) + " perle. Armi azzerate."
                )
    else: 
        if albatro_avvistato > 0 and albatro_ucciso == True:
            perle_bonus = random.randint(5, 20)
        else:
            perle_bonus = random.randint(30, 50)
        carico_nave["perle"] += perle_bonus
        mostra_messaggio_evento(
            titolo="LEALTA' PREMIATA",
            domanda="Il capo tribu' ti ringrazia per aver rifiutato il rivale.",
            motivo="+" + str(perle_bonus) + " perle in segno di riconoscimento."
        )
    
    return carico_nave, True

def fase_epilogo(personaggi, settimane_viaggio_fin_qui, albatro_avvistato, albatro_ucciso):
    ha_navigatore = presenza_ruolo(personaggi, "navigatore")
    if ha_navigatore:
        settimane_ritorno = 1
        testo_navigatore = "Il navigatore conosce la rotta: 1 settimana base."
    else:
        settimane_ritorno = 2
        testo_navigatore = "Senza navigatore ci si perde: 2 settimane base."
    if albatro_avvistato > 0 and albatro_ucciso == True:
        settimane_ritorno += 1
        testo_navigatore += " +1 settimana per la sfortuna dell'albatro ucciso."
    mostra_messaggio_evento(
        titolo="RIENTRO IN PATRIA",
        domanda=("Il capo tribu' rifornisce le scorte per " + str(settimane_ritorno) + " settimane di ritorno."),
        motivo=testo_navigatore
    )
    return settimane_viaggio_fin_qui + settimane_ritorno

def fase_asta(monete_residue, profitto_merci, paga_da_coprire):
    scelta_asta = mostra_messaggio_evento(
        titolo="METTI ALL'ASTA LA NAVE?",
        domanda="Le monete non bastano a pagare l'equipaggio.",
        motivo="Vuoi mettere la nave all'asta per coprire il debito?",
        scelte=["Si, metti all'asta", "No, tieni la nave"]
    )
    if scelta_asta == "No, tieni la nave":
        return 0
    offerte_gia_proposte = []
    while True:
        offerte_disponibili = []
        posizione_lista = 0
        while posizione_lista < len(LISTA_OFFERTE_ASTA):
            valore_da_controllare = LISTA_OFFERTE_ASTA[posizione_lista]
            e_riproponibile = False
            posizione_riprop = 0
            while posizione_riprop < len(OFFERTE_SEMPRE_RIPROPONIBILI):
                if OFFERTE_SEMPRE_RIPROPONIBILI[posizione_riprop] == valore_da_controllare:
                    e_riproponibile = True
                posizione_riprop += 1
            gia_estratta = False
            posizione_estratte = 0
            while posizione_estratte < len(offerte_gia_proposte):
                if offerte_gia_proposte[posizione_estratte] == valore_da_controllare:
                    gia_estratta = True
                posizione_estratte += 1
            if e_riproponibile or not gia_estratta:
                offerte_disponibili.append(valore_da_controllare)
            posizione_lista += 1
        offerta_proposta = random.choice(offerte_disponibili)
        e_riproponibile = False
        posizione_riprop = 0
        while posizione_riprop < len(OFFERTE_SEMPRE_RIPROPONIBILI):
            if OFFERTE_SEMPRE_RIPROPONIBILI[posizione_riprop] == offerta_proposta:
                e_riproponibile = True
            posizione_riprop += 1
        if not e_riproponibile:
            offerte_gia_proposte.append(offerta_proposta)
        saldo_con_questa_offerta = monete_residue + profitto_merci + offerta_proposta - paga_da_coprire
        if saldo_con_questa_offerta >= 0:
            testo_copertura = "V Questa offerta copre il debito!"
            testo_saldo_risultante = "+" + str(saldo_con_questa_offerta) + " monete."
        else:
            testo_copertura = "X Offerta insufficiente a coprire il debito."
            testo_saldo_risultante = str(saldo_con_questa_offerta) + " monete."
        risposta_giocatore = mostra_messaggio_evento(
            titolo="OFFERTA ASTA: " + str(offerta_proposta) + " monete d'oro",
            domanda=testo_copertura,
            motivo="Saldo risultante: " + testo_saldo_risultante,
            scelte=["Accetta", "Passa alla prossima offerta"]
        )
        if risposta_giocatore == "Accetta":
            mostra_messaggio_evento(
                titolo="NAVE VENDUTA",
                domanda="La nave e' stata venduta per " + str(offerta_proposta) + " monete d'oro.",
                motivo="Speriamo basti a coprire i debiti."
            )
            return offerta_proposta

def fase_profitti(carico_nave, monete_residue, personaggi_ingaggiati, numero_settimane_totali):
    fattore_mercato = random.choice([0.5, 1.0, 2.0])
    profitto_merci = 0
    for nome_valuta in LISTA_VALUTE:
        quantita_valuta = carico_nave[nome_valuta]
        valore_unitario = VALORE_IN_PATRIA[nome_valuta]
        profitto_merci += quantita_valuta * valore_unitario * fattore_mercato
    profitto_merci = arrotonda_intero(profitto_merci)
    paga_equipaggio = calcola_paga_totale_equipaggio(personaggi_ingaggiati, numero_settimane_totali)
    saldo_finale = monete_residue + profitto_merci - paga_equipaggio
    if fattore_mercato == 0.5:
        descrizione_mercato = "Mercato depresso (valore dimezzato)"
    elif fattore_mercato == 2.0:
        descrizione_mercato = "Mercato in fermento (valore raddoppiato)"
    else:
        descrizione_mercato = "Mercato normale (valore standard)"
    mostra_messaggio_evento(
        titolo="RIEPILOGO FINALE",
        domanda=descrizione_mercato,
        motivo=("Profitto merci: +" + str(profitto_merci) + "  |  Monete residue: +" + str(arrotonda_intero(monete_residue)) + "  |  Paga equipaggio: -" + str(arrotonda_intero(paga_equipaggio)))
    )
    if saldo_finale >= 0:
        testo_segno_saldo = "+" + str(saldo_finale)
    else:
        testo_segno_saldo = str(saldo_finale)
    mostra_messaggio_evento(
        titolo="SALDO FINALE: " + testo_segno_saldo + " monete",
        domanda=testo_saldo(saldo_finale),
        motivo=("Carico: " + str(carico_nave["perle"]) + " perle | " + str(carico_nave["manufatti"]) + " manufatti | " + str(carico_nave["spezie"]) + " spezie.")
    )
    if saldo_finale < 0:
        ricavato_asta = fase_asta(monete_residue, profitto_merci, paga_equipaggio)
        saldo_finale = monete_residue + profitto_merci + ricavato_asta - paga_equipaggio
    if saldo_finale > 0:
        mostra_messaggio_evento(
            titolo="VIAGGIO PROFITTEVOLE!",
            domanda="Complimenti capitano! Guadagno netto: +" + str(saldo_finale) + " monete.",
            motivo="Avete arricchito la ciurma e riportato merci rare in patria.",
            scelte=["Fine avventura!"]
        )
        return "positivo"
    elif saldo_finale == 0:
        mostra_messaggio_evento(
            titolo="VIAGGIO NULLO",
            domanda="Siete riusciti a pagare tutti, ma non vi resta nulla.",
            motivo="Tanta fatica per niente...",
            scelte=["Fine avventura!"]
        )
        return "nullo"
    else:
        mostra_messaggio_evento(
            titolo="VIAGGIO IN PERDITA",
            domanda="Non siete riusciti a pagare l'equipaggio.",
            motivo=("Debito residuo: " + str(valore_assoluto(saldo_finale)) + " monete. Il vostro onore e' in gioco."),
            scelte=["Fine avventura!"]
        )
        return "negativo"

def baratto(personaggi_scelti, lista_equip, monete_residue, settimane_viaggio_fin_qui, albatro_avvistato, albatro_ucciso):
    personaggi_ingaggiati = []
    for personaggio in personaggi_scelti:
        if personaggio["stats"]["cost"] > 0:
            personaggi_ingaggiati.append(personaggio)
    gioco_continua = arrivo_nuovo_mondo(lista_equip)
    if not gioco_continua:
        return False, None
    carico_nave = fase_baratto(lista_equip)
    carico_nave, gioco_continua = fase_tradimento(
        lista_equip, carico_nave, albatro_avvistato, albatro_ucciso
    )
    if not gioco_continua:
        return False, None
    settimane_totali_con_ritorno = fase_epilogo(
        personaggi_scelti, settimane_viaggio_fin_qui, albatro_avvistato, albatro_ucciso
    )
    esito = fase_profitti(
        carico_nave, monete_residue, personaggi_ingaggiati, settimane_totali_con_ritorno
    )
    return False, esito