import time
import csv
import concurrent.futures

MAX_THREADS = 5

# Lista com 15 filmes totalmente diferentes divididos em 3 blocos
FILMES_SINGLE = [
    {"title": "The Shawshank Redemption", "date": "1994", "rating": "9.3", "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."},
    {"title": "The Godfather", "date": "1972", "rating": "9.2", "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."},
    {"title": "The Dark Knight", "date": "2008", "rating": "9.0", "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."},
    {"title": "The Godfather Part II", "date": "1974", "rating": "9.0", "plot": "The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate."},
    {"title": "12 Angry Men", "date": "1957", "rating": "9.0", "plot": "The jury in a New York City murder trial is frustrated by a single member whose skeptical caution forces them to more carefully consider the evidence before jumping to a hasty verdict."}
]

FILMES_MULTIPROCESSING = [
    {"title": "Schindler's List", "date": "1993", "rating": "9.0", "plot": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis."},
    {"title": "The Lord of the Rings: The Return of the King", "date": "2003", "rating": "9.0", "plot": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring."},
    {"title": "Pulp Fiction", "date": "1994", "rating": "8.9", "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."},
    {"title": "The Lord of the Rings: The Fellowship of the Ring", "date": "2001", "rating": "8.9", "plot": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron."},
    {"title": "The Good, the Bad and the Ugly", "date": "1966", "rating": "8.8", "plot": "A bounty hunting scam joins two men in an uneasy alliance against a third in a race to find a fortune in gold buried in a remote cemetery."}
]

FILMES_MULTITHREADING = [
    {"title": "Forrest Gump", "date": "1994", "rating": "8.8", "plot": "The history of the United States from the 1950s to the 1970s unfolds from the perspective of an Alabama man with an IQ of 75, who yearns to be reunited with his childhood sweetheart."},
    {"title": "Fight Club", "date": "1999", "rating": "8.7", "plot": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more."},
    {"title": "Inception", "date": "2010", "rating": "8.7", "plot": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."},
    {"title": "The Lord of the Rings: The Two Towers", "date": "2002", "rating": "8.7", "plot": "While Frodo and Sam edge closer to Mordor with the help of the shifty Gollum, the divided fellowship makes a stand against Sauron's new ally, Saruman, and his hordes of Isengard."},
    {"title": "Star Wars: Episode V - The Empire Strikes Back", "date": "1980", "rating": "8.7", "plot": "After the Rebels are brutally overpowered by the Empire on the ice planet Hoth, Luke Skywalker begins Jedi training with Yoda, while his friends are pursued by Darth Vader."}
]

def extract_movie_details(movie_data):
    """Simula o processamento e escrita de um filme de forma segura."""
    time.sleep(0.2) # Delay para manter o cálculo de tempo de execução perceptível
    
    title = movie_data["title"]
    date = movie_data["date"]
    rating = movie_data["rating"]
    plot_text = movie_data["plot"]

    with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
        movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        movie_writer.writerow([title, date, rating, plot_text])

# --- FUNÇÕES DE TESTE DE PERFORMANCE ---

def run_single_thread(movies):
    print("-> Iniciando modo: Single-Thread (Filmes 1 a 5)...")
    start_time = time.time()
    for movie in movies:
        extract_movie_details(movie)
    duration = time.time() - start_time
    print(f"✓ Concluído Single-Thread em: {duration:.2f} segundos\n")
    return duration

def run_multi_processing(movies):
    print("-> Iniciando modo: Multi-Processing (Filmes 6 a 10)...")
    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(extract_movie_details, movies)
    duration = time.time() - start_time
    print(f"✓ Concluído Multi-Processing em: {duration:.2f} segundos\n")
    return duration

def run_multi_threading(movies):
    print("-> Iniciando modo: Multi-Threading (Filmes 11 a 15)...")
    start_time = time.time()
    threads = min(MAX_THREADS, len(movies))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movies)
    duration = time.time() - start_time
    print(f"✓ Concluído Multi-Threading em: {duration:.2f} segundos\n")
    return duration

def main():
    # Reinicia o arquivo gravando o cabeçalho limpo
    with open('movies.csv', mode='w', newline='', encoding='utf-8') as file:
        movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        movie_writer.writerow(['Title', 'Date', 'Rating', 'Plot'])

    print("Executando o comparativo de performance com 15 filmes exclusivos...\n")
    
    # 1. Execução Sequencial (Filmes bloco 1)
    tempo_single = run_single_thread(FILMES_SINGLE)
    print("-" * 50)
    
    # 2. Execução Paralela por Processos (Filmes bloco 2)
    tempo_multi = run_multi_processing(FILMES_MULTIPROCESSING)
    print("-" * 50)
    
    # 3. Execução Paralela por Threads (Filmes bloco 3)
    tempo_threads = run_multi_threading(FILMES_MULTITHREADING)
    print("=" * 50)
    
    # Relatório Final
    print("MÉTRICAS FINAIS COMPARATIVAS:")
    print(f"• O Multi-Threading foi {tempo_single / tempo_threads:.2f}x mais rápido que o Sequencial.")
    print(f"• O Multi-Processing foi {tempo_single / tempo_multi:.2f}x mais rápido que o Sequencial.")
    print("=" * 50)

    print("\nCONTEÚDO ATUALIZADO SALVO NO ARQUIVO MOVIES.CSV:")
    with open('movies.csv', mode='r', encoding='utf-8') as file:
        print(file.read())

if __name__ == '__main__':
    main()