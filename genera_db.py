import mysql.connector
from mysql.connector import cursor

def inizializza_db():
    try:
        while True:
            #inserimento dati del db da utilizzare
            print("\n-----VERIFICA/CREAZIONE DB-----\n")
            host_db=input("Inserisci l'host del database da utilizzare: ")
            user_db=input("Inserisci l'user con il quale accedere al database: ")
            psw_db=input("Inserisci la password per accedere al database: ")
            nome_db=input("Inserisci il nome del database da utilizzare: ")
            print(f"\nI dati inseriti sono:\nhost={host_db}\nuser={user_db}\npassword={psw_db}\nnome database={nome_db}")
            scelta=input("\nI dati sono stati inseriti correttamente? (y/n): ").lower()
            if scelta == "y":
                break
            else:
                print("Inserire i dati corretti.")

        #creazione variabile della connessione
        connection = mysql.connector.connect(
            host=host_db,
            user=user_db,
            password=psw_db
            )
        #creazione del cursore ed assegnazione alla variabile relativa alla connessione creata
        cursore = connection.cursor()

        #creazione database se non esiste
        cursore.execute(f"CREATE DATABASE IF NOT EXISTS {nome_db}")
        print("Database verificato/creato correttamente.")

        #selezione db
        connection.database=nome_db

        #CREAZIONE TABELLE
        #creazione tabella clienti
        cursore.execute("""
            CREATE TABLE IF NOT EXISTS `clienti` (
            `id` int NOT NULL AUTO_INCREMENT,
            `rag_sociale` varchar(25) DEFAULT NULL,
            `indirizzo` varchar(30) DEFAULT NULL,
            `p_iva` varchar(11) NOT NULL,
            `sdi` varchar(7) DEFAULT NULL,
            PRIMARY KEY (`p_iva`),
            UNIQUE KEY `id` (`id`))
        """)

        #creazione tabella prodotti
        cursore.execute("""
            CREATE TABLE IF NOT EXISTS `prodotti` (
            `id` int NOT NULL AUTO_INCREMENT,
            `nome` varchar(20) DEFAULT NULL,
            `um` varchar(5) DEFAULT NULL,
            `prezzo_x_um` float DEFAULT NULL,
            `iva` int DEFAULT NULL,
            PRIMARY KEY (`id`))
        """)
        print("Tabelle create/verificate con successo")

        return host_db, user_db, psw_db, nome_db

    except:
        print("Si è verificato un errore.")
