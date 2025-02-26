import mysql.connector
import genera_db
import funzioni

#----------------------------------------------------------------------
#----------------------------------------------------------------------
def main():
    host,user,psw,nome=genera_db.inizializza_db()
    try:
        while True:
            #creazione variabile della connessione
            db = mysql.connector.connect(
                host=host,
                user=user,
                password=psw,
                database=nome
            )
            print("\n-----LOGIN-----\n")
            nome_azienda=input("Inserisci il nome dell'Azienda: ")

            #creazione del cursore ed assegnazione alla variabile relativa alla connessione creata
            cursore = db.cursor()
            break #esce dal ciclo se i dati sono corretti
    except:
        print("Errore nella connessione al database.")
#----------------------------------------------------------------------
    #INTERAZIONE CON DATABASE
    #inizializzazione del ciclo
    try:
        while True:
            funzioni.menu(nome_azienda,user)
            scelta=int(input("\nDigita la scelta: "))
            while scelta<1 or scelta>6:
                print("Inserito valore non valido, digitare scelta corretta (1-6)")
                scelta=int(input("\nDigita la scelta: "))

            if scelta==1:
                sql=funzioni.cerca()
                cursore.execute(sql) #execute() esegue il comando SQL passatogli
                result=cursore.fetchall() #fetchall() restituisce tutte le tuple
                for riga in result:
                    print("|",str(riga).strip().replace("(","").replace(")","").replace("'","").replace(","," | "),"|")
            elif scelta==2:
                sql,values=funzioni.insert()
                if sql:
                    cursore.execute(sql,values)
                    db.commit()
            elif scelta==3:
                sql,values=funzioni.modifica()
                cursore.execute(sql,values)
                db.commit()
            elif scelta==4:
                sql=funzioni.elimina()
                cursore.execute(sql)
                db.commit()
            elif scelta==5:
                #CREAZIONE DTT
                righe=[]
                intestazione_clienti=["ID Cliente","Ragione Sociale","Indirizzo","P.IVA","SDI"]
                intestazione_prodotti=["ID Prodotto","Nome Prodotto","U.M.","Quantità","IVA"]

                #dati cliente
                sql=funzioni.get_cliente()
                cursore.execute(sql)
                dati_cliente=cursore.fetchall()
                righe.append(intestazione_clienti)
                righe.append(dati_cliente)

                #dati prodotti
                righe.append([])
                righe.append(intestazione_prodotti)
                while True:
                    sql=funzioni.get_prodotto()
                    cursore.execute(sql)
                    dati_prodotto=cursore.fetchall()
                    righe.append(dati_prodotto)

                    scelta=input("Vuoi inserire altri prodotti? (y/n): ").lower()
                    if scelta=="n":
                        break

                #generazione file csv
                funzioni.genera_csv(righe,nome_azienda)
            elif scelta==6:
                print("Esco dal programma..")
                db.close()
                break
    except ValueError:
        print("Inserito valore non valido.")
    except Exception:
        print("Si è verificato un errore inatteso.")
    finally:
        db.close()
        print("Connessione al database chiusa.")
#----------------------------------------------------------------------
#----------------------------------------------------------------------
main()
