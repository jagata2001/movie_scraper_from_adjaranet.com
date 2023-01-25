from tqdm import tqdm

class Data_processing:
    def __init__(self,data):
        self.data = data
    def collect_actors(self):
        actors = []
        for each in tqdm(self.data["films"],desc="Actors"):
            for actor in tqdm(each["actors"],desc="Second",leave=False):
                actors.append([actor["actor_id"],actor["name"],actor["image"]])

        return actors
        
    def collect_directors(self):
        directors = []
        for each in tqdm(self.data["films"],desc="Directors"):
            for director in tqdm(each["data"]["directors"],desc="Second",leave=False):
                directors.append([director["director_id"],director["name"],director["image"]])

        return directors

    def collect_genres(self):
        genres = []
        for each in tqdm(self.data["films"],desc="Genres"):
            for genre in tqdm(each["genres"],desc="Second",leave=False):
                genres.append([genre["genre_id"],genre["genre"]])

        return genres
