from db_class import *
from adjaranet_class import *
from data_processing_class import *

import time

if __name__ == "__main__":
    adj = Adjaranet()
    db = Database(dbfile)
    adj.parse_films_ids()




    rowcount = db.insert_films(adj.film_ids)
    print(f"Inserted {rowcount} rows")


    film_ids_to_parse = db.films_to_parse()
    parse_films_queue = Queue()
    print("size of films:",len(film_ids_to_parse))
    for each in film_ids_to_parse:
        parse_films_queue.put(list(each))
    adj.parse_films_queue = parse_films_queue
    for _ in range(4):
        threading.Thread(target=adj.parse_films_data,args=()).start()
    while True:
        print(len(adj.main_data["films"]),adj.parse_films_queue.qsize())
        time.sleep(0.5)
        if adj.parse_films_queue.qsize() == 0:
            time.sleep(5)
            dp = Data_processing(adj.main_data)
            actors = dp.collect_actors()
            actor_rowcount = db.insert_actor(actors)

            directors = dp.collect_directors()
            directors_rowcount = db.insert_director(directors)

            genres = dp.collect_genres()
            genres_rowcount = db.insert_genres(genres)

            print(f"{actor_rowcount} new actors inserted")
            print(f"{directors_rowcount} new directors inserted")
            print(f"{genres_rowcount} new genres inserted")
            break
