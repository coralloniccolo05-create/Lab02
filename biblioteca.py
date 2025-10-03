
def carica_da_file(file_path):
    """Carica i libri dal file"""
    # TODO
    try:
        with open(file_path, 'r', encoding='utf-8') as file_biblio:

            lista_biblioteca = []
            file_biblio.readline()
            for libro in file_biblio:
                libro= libro.strip().split(',')
                diz_libro = {libro[0]: libro[1:5]}          #libro[1], int(libro[2]), int(libro[3]), int(libro[4])
                lista_biblioteca.append(diz_libro)
            return lista_biblioteca
    except FileNotFoundError:
        print('File not found')
        return None

def aggiungi_libro(biblio, title, author, year, pages, section, file_path):
    """Aggiunge un libro nella biblioteca"""
    #TODO
    try:
        with open(file_path, 'a') as biblioteca_file:
            # Verifica se la sezione esiste
            esiste_sezione=False
            for book in biblio: #book sono i vari dizionari
                for info in book.values():   #info sono i values dei singoli dizionari
                    if str(section) in info:
                        esiste_sezione=True
                if esiste_sezione:
                    break
            if not esiste_sezione:
                raise KeyError("Sezione non esistente")

            # Verifica se il titolo è già presente
            esiste_titolo=False
            for book in biblio:
                if title in book.keys():
                    esiste_titolo=True
                    break
            if esiste_titolo:
                raise ValueError("Titolo già presente")

            # Crea il nuovo libro
            diz_new_book = {title: [author, year, pages, section]}
            biblio.append(diz_new_book)
            # Scrive su file
            for title, info in diz_new_book.items():
                riga = f"{title},{info[0]},{info[1]},{info[2]},{info[3]}\n" #scrivo la stringa da aggiungere in fondo al file
                biblioteca_file.write(riga)
        return diz_new_book

    except FileNotFoundError:
        print("Errore: file non trovato.")
        return None
    except KeyError:
        print("Errore: sezione non esistente.")
        return None
    except ValueError:
        print("Errore: titolo già presente.")
        return None



def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""
    # TODO
    for libro in biblioteca:
        if titolo in libro:
            info = libro[titolo]
            libro_cercato = f"{titolo},{info[0]},{info[1]},{info[2]},{info[3]}\n"  #creo la stringa da stampare per il libro cercato
            return libro_cercato
    return None


def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    # TODO
    lista_libri_ordinati = []
    trovata=False
    for libro in biblioteca:
        if int(sezione) == int(list(libro.values())[0][-1]):  # confronto la sezione da input con la sezione dei vari libri
            lista_libri_ordinati.append(list(libro.keys())[0]) # inserisco i titoli nella lista da stampare ordinata
            trovata=True
    if not trovata:
        return None

    return sorted(lista_libri_ordinati)


def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, 'biblioteca.csv')
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: \n {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print('La sezione non esiste')

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

