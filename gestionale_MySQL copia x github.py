import mysql.connector
from mysql.connector import cursor
import csv
from datetime import datetime

#----------------------------------------------------------------------
def menu():
    print()
    print("--------------------------------")
    print("Azienda: laMiaAzienda S.r.l")
    print()
    print("\tMENU")
    print("1-Cerca nel database")
    print("2-Inserisci")
    print("3-Modifica")
    print("4-Elimina")
    print("5-Genera DDT in CSV")
    print("6-Esci dal programma..")
    print()
#----------------------------------------------------------------------
def cerca():
    tabelle=["clienti","prodotti"]
    scelta=input("Vuoi cercare clienti o prodotti? ").lower()
    while scelta not in tabelle:
        print("Scelta errata!")
        scelta=input("Vuoi cercare clienti o prodotti? ").lower()
    print("\n\t"+scelta.upper())
    return f"SELECT * FROM {scelta}"

#----------------------------------------------------------------------
def insert():
    tabella=input("Inserisci il nome della tabella da utilizzare (clienti/prodotti): ").lower()
    if tabella=="prodotti":
        nome=input("Inserisci nome prodotto: ")
        um=input("Inserisci unità di misura del prodotto: ")
        prezzo_per_um=input("Inserisci il prezzo/um del prodotto: ")
        iva=input("Inserisci il valore dell'iva per il prodotto: ")

        sql = f"INSERT INTO {tabella} (nome, um, prezzo_x_um, iva) VALUES (%s, %s, %s, %s)"
        values=(nome, um, prezzo_per_um, iva)
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
    tabella=input("Inserisci il nome della tabella da utilizzare: ")
    campo=input("Inserisci nome del campo da modificare: ")
    idn=input("Inserisci id elemento da modificare: ")
    nuovo_val=input("Inserisci il nuovo valore: ")

    sql=f"UPDATE {tabella} SET {campo} = %s WHERE id = %s"
    values=(nuovo_val, idn)
    return sql, values
#---------------------------------------------------------------------
def elimina():
    tabella=input("Inserisci il nome della tabella da utilizzare: ")
    idn=input("Inserisci id elemento da eliminare: ")

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
def genera_csv(righe):
    ddt_name=input("Inserisci nome del documento: ").replace(" ", "_")
    while True: #ciclo di validazione della data che tenta di convertire la stringa inserita, nel formato richiesto dal programma, tramite il modulo datetime
        data=input("Inserisci la data del documento (gg/mm/aaaa): ")
        try:#va usato un try/except perche datetime restituisce "ValueError" in caso di mancato match con il formato indicato
            data_valida=datetime.strptime(data,"%d/%m/%Y") #verifica che la data rispetti il formato indicato; "%Y" verifica che l'anno sia di 4 cifre mentre "%y" ne accetta 2
            data_formattata=datetime.strftime(data_valida,"%d-%m-%Y") #cambia il formato per poterlo scrivere nel nome del file
            break #interrompe il ciclo se la data è verificata
        except ValueError:
            print("Data non valida! Inserisci una data valida nel formato gg/mm/aaaa")

    fileName=f"{ddt_name}_{data_formattata}.csv"
    with open(fileName,"w") as file: #apre file in scrittura
        contenuto=csv.writer(file) #il metodo csv.writer crea un oggetto sul quale scrivere le righe da convertire poi in file.csv
        contenuto.writerow(["laMiaAzienda S.r.l"])
        contenuto.writerow([data]) #Per scrivere una singola stringa senza dividerla in caratteri separati da virgole, va passata la stringa come un elemento di una lista
        contenuto.writerow([])
        contenuto.writerows(righe) #scrive la lista di liste nell'oggetto

    with open(fileName,"r") as file: #apre file in lettura
        contenuto=file.read()

    print("\n", contenuto)
#----------------------------------------------------------------------
#----------------------------------------------------------------------
def main():
    #creazione variabile della connessione
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="ilMioDatabase"
    )

    #creazione del cursore ed assegnazione alla variabile relativa alla connessione creata
    cursor = db.cursor()
#----------------------------------------------------------------------
    #ELABORAZIONE TABELLA
    #inizializzazione del ciclo
    while True:
        try:
            menu()
            scelta=int(input("Digita la scelta: "))

            if scelta==1:
                sql=cerca()
                cursor.execute(sql) #execute() esegue il comando SQL passatogli
                result=cursor.fetchall() #fetchall() restituisce tutte le tuple
                for riga in result:
                    print(riga)
            elif scelta==2:
                sql,values=insert()
                if sql:
                    cursor.execute(sql,values)
                    db.commit()
            elif scelta==3:
                sql,values=modifica()
                cursor.execute(sql,values)
                db.commit()
            elif scelta==4:
                sql=elimina()
                cursor.execute(sql)
                db.commit()
            elif scelta==5:
                #CREAZIONE DTT
                righe=[]
                intestazione_clienti=["ID Cliente","Ragione Sociale","Indirizzo","P.IVA","SDI"]
                intestazione_prodotti=["ID Prodotto","Nome Prodotto","U.M.","Quantità","IVA"]

                #dati cliente
                sql=get_cliente()
                cursor.execute(sql)
                dati_cliente=cursor.fetchall()
                righe.append(intestazione_clienti)
                righe.append(dati_cliente)

                #dati prodotti
                righe.append([])
                righe.append(intestazione_prodotti)
                while True:
                    sql=get_prodotto()
                    cursor.execute(sql)
                    dati_prodotto=cursor.fetchall()
                    righe.append(dati_prodotto)

                    scelta=input("Vuoi inserire altri prodotti? (y/n): ").lower()
                    if scelta=="n":
                        break

                genera_csv(righe)
            elif scelta==6:
                print("Esco dal programma..")
                break
        except ValueError:
            print("Inserito valore non valido, digitare scelta corretta (1-6)")
#----------------------------------------------------------------------
#----------------------------------------------------------------------
main()