import csv
from datetime import datetime
#----------------------------------------------------------------------

def menu(nome_azienda,user):
    opzioni={
        1:"Cerca nel database",
        2:"Inserisci",
        3:"Modifica",
        4:"Elimina",
        5:"Genera DDT in CSV",
        6:"Esci dal programma",
    }
    print("\n------------------------------------------")
    print(f" Azienda: {nome_azienda} - Utente: {user}")
    print("------------------------------------------")
    print("\n\tMENU")
    for k,v in opzioni.items():
        print(f"{k}-{v}")
#----------------------------------------------------------------------
def intestazioneClienti():
    print("---------------------------------------------")
    print("| ID | Rag.Sociale | Indirizzo | P.IVA | SDI |")
    print("---------------------------------------------")

def intestazioneProdotti():
    print("-----------------------------------------")
    print("| ID | Nome | U.M. | Prezzo/um | IVA(%) |")
    print("-----------------------------------------")

def cerca():
    tabelle=["clienti","prodotti"]
    scelta=input("Vuoi cercare clienti o prodotti? ").lower()
    while scelta not in tabelle:
        print("Scelta errata!")
        scelta=input("Vuoi cercare clienti o prodotti? ").lower()

    print("\n\t"+scelta.upper())
    if scelta=="clienti":
        intestazioneClienti()
    elif scelta=="prodotti":
        intestazioneProdotti()

    return f"SELECT * FROM {scelta}"
#----------------------------------------------------------------------
def insert():
    while True:
        tabella = input("Inserisci il nome della tabella da utilizzare (clienti/prodotti): ").lower()
        if tabella in ["clienti", "prodotti"]:
            break
        print("Tabella non valida. Inserisci 'clienti' o 'prodotti'.")

    if tabella=="prodotti":
        nome=input("Inserisci nome prodotto: ")
        um=input("Inserisci unità di misura del prodotto: ")
        prezzo=input("Inserisci il prezzo/um del prodotto: ")
        iva=input("Inserisci il valore dell'iva per il prodotto: ")

        sql = f"INSERT INTO {tabella} (nome, um, prezzo, iva) VALUES (%s, %s, %s, %s)"
        values=(nome, um, prezzo, iva)
    elif tabella=="clienti":
        rag_sociale=input("Inserisci la ragione sociale del cliente: ")
        indirizzo=input("Inserisci l'indirizzo della sede: ")
        p_iva=input("Inserisci la p.iva del cliente: ")
        sdi=input("Inserisci il codice SDI del cliente: ")

        sql=f"INSERT INTO {tabella} (rag_sociale, indirizzo, p_iva,sdi) VALUES (%s, %s, %s, %s)"
        values=(rag_sociale, indirizzo, p_iva, sdi)
    else:
        print("Tabella non valida!")
        return None, None

    return sql, values
#----------------------------------------------------------------------
def modifica():
    while True:
        tabella = input("Inserisci il nome della tabella da utilizzare (clienti/prodotti): ").lower()
        if tabella in ["clienti", "prodotti"]:
            break
        print("Tabella non valida. Inserisci 'clienti' o 'prodotti'.")

    campo=input("Inserisci nome del campo da modificare: ")
    idn=input("Inserisci ID elemento da modificare: ")
    nuovo_val=input("Inserisci il nuovo valore: ")

    sql=f"UPDATE {tabella} SET {campo} = %s WHERE id = %s"
    values=(nuovo_val, idn)
    return sql, values
#---------------------------------------------------------------------
def elimina():
    while True:
        tabella = input("Inserisci il nome della tabella da utilizzare (clienti/prodotti): ").lower()
        if tabella in ["clienti", "prodotti"]:
            break
        print("Tabella non valida. Inserisci 'clienti' o 'prodotti'.")

    idn=input("Inserisci ID elemento da eliminare: ")

    sql=f"DELETE from {tabella} WHERE id = {idn}"
    return sql
#----------------------------------------------------------------------
#dati per generazione ddt
def get_cliente():
    cliente=input("Inserisci la P.IVA del cliente: ")
    while len(cliente) != 11 or not cliente.isdigit():
        print("P.IVA non valida!")
        cliente=input("Inserisci una P.IVA valida di 11 cifre: ")

    sql=f"SELECT * FROM `clienti` WHERE `p_iva` ={cliente}"
    return sql

def get_prodotto():
    prodotto=input("Inserisci l'ID del prodotto da inserire nel DDT: ")
    while not prodotto.isdigit():
        print("Inserito ID errato!")
        prodotto=input("Inserisci l'ID del prodotto da inserire nel DDT: ")

    sql=f"SELECT * FROM `prodotti` WHERE `id` ={prodotto}"
    return sql
#----------------------------------------------------------------------
#generazione ddt in formato csv
def genera_csv(righe,nome_azienda):
    ddt_name=input("Inserisci nome del documento: ").replace(" ", "_")
    while True: #ciclo di validazione della data che tenta di convertire la stringa inserita, nel formato richiesto dal programma, tramite il modulo datetime
        data=input("Inserisci la data del documento (gg/mm/aaaa): ")
        try: #va usato un try/except perche datetime restituisce "ValueError" in caso di mancato match con il formato indicato
            data_valida=datetime.strptime(data,"%d/%m/%Y") #verifica che la data rispetti il formato indicato; "%Y" verifica che l'anno sia di 4 cifre mentre "%y" ne accetta 2
            data_formattata=datetime.strftime(data_valida,"%d-%m-%Y") #cambia il formato per poterlo scrivere nel nome del file
            break #interrompe il ciclo se la data è verificata
        except ValueError:
            print("Data non valida! Inserisci una data valida nel formato gg/mm/aaaa")

    fileName=f"{ddt_name}_{data_formattata}.csv"
    with open(fileName,"w") as file: #apre file in scrittura
        contenuto=csv.writer(file) #il metodo csv.writer crea un oggetto sul quale scrivere le righe da convertire poi in file.csv
        contenuto.writerow([nome_azienda])
        contenuto.writerow([data]) #Per scrivere una singola stringa senza dividerla in caratteri separati da virgole, va passata la stringa come un elemento di una lista
        contenuto.writerow([])
        contenuto.writerows(righe) #scrive la lista di liste nell'oggetto

    with open(fileName,"r") as file: #apre file in lettura
        contenuto=file.read()

    print("\n", contenuto)
#----------------------------------------------------------------------
