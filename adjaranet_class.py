import threading
import requests as r
from bs4 import BeautifulSoup
import json,time
from queue import Queue

class Adjaranet:
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }
    film_ids = []
    def __init__(self):
        try:
            resp = r.get(f"https://api.adjaranet.com/api/v1/movies?page=1&per_page=50&filters%5Blanguage%5D=GEO&filters%5Byear_range%5D=1900%2C2021&filters%5Binit%5D=true&filters%5Bsort%5D=-upload_date&filters%5Btype%5D=movie&filters%5Bwith_actors%5D=3&filters%5Bwith_directors%5D=1&filters%5Bwith_files%5D=yes&sort=-upload_date&source=adjaranet", headers=self.headers,timeout=15)
            if resp.status_code == 200:
                try:
                    for_last_page = json.loads(resp.text)
                    self.pages_queue = Queue()
                    total_pages = for_last_page["meta"]["pagination"]["total_pages"]
                    for i in range(1,int(total_pages)+1-144):
                        self.pages_queue.put({"page":i,"Error_count":0})
                    print(f"total pages {total_pages}")
                except json.decoder.JSONDecodeError:
                    print("Incorrect returned data")
                    exit()
                except KeyError:
                    print("Incorrect Key for dict")
                    exit()
            else:
                print(f"Status code Error: {resp.status_code}")
                exit()
        except r.exceptions.ConnectTimeout:
            print("Connection timed out")
            exit()
        except:
            print("Something went wrong")
            exit()

    def parse_films_ids(self,max_error=3):
        i = 0
        while self.pages_queue.qsize() != 0:
            i+=1
            seg = self.pages_queue.get()
            page = seg["page"]
            url = f"https://api.adjaranet.com/api/v1/movies?page={page}&per_page=50&filters%5Blanguage%5D=GEO&filters%5Byear_range%5D=1900%2C2021&filters%5Binit%5D=true&filters%5Bsort%5D=-upload_date&filters%5Btype%5D=movie&filters%5Bwith_actors%5D=3&filters%5Bwith_directors%5D=1&filters%5Bwith_files%5D=yes&sort=-upload_date&source=adjaranet"

            try:
                resp = r.get(url,headers=self.headers,timeout=15)
                if resp.status_code == 200:
                    try:
                        for_film_ids = json.loads(resp.text)
                        for each in for_film_ids["data"]:
                            #print(each["id"])
                            if each["id"] != None and each["adjaraId"]:
                                self.film_ids.append([each["id"],each["adjaraId"]])
                        print(f"Current page: {page}")

                    except json.decoder.JSONDecodeError:
                        seg["Error_count"]+=1
                        if seg["Error_count"] < max_error:
                            self.pages_queue.put(seg)
                        else:
                            print("Maximum error exceeded")
                            continue
                        print("Incorrect returned data")

                    except KeyError:
                        seg["Error_count"]+=1
                        if seg["Error_count"] < max_error:
                            self.pages_queue.put(seg)
                        else:
                            print("Maximum error exceeded")
                            continue
                        print("Incorrect Key for dict")
                elif resp.status_code == 429:
                    seg["Error_count"]+=1
                    if seg["Error_count"] < max_error:
                        self.pages_queue.put(seg)
                    else:
                        print("Maximum error exceeded")
                        continue
                    print("Too many requests")
                else:
                    print(f"Status code Error: {resp.status_code}")
            except r.exceptions.Timeout:
                seg["Error_count"]+=1
                print(seg["Error_count"],i)
                if seg["Error_count"] < max_error:
                    print(seg)
                    self.pages_queue.put(seg)

                else:
                    print("Maximum error exceeded")
                print("Connection timed out")
            except KeyboardInterrupt:
                print("Exit with KeyboardInterrupt")
                exit()
            except:
                print("Something went wrong")
    main_data = {"films":[]}
    def parse_films_data(self,max_error=3):
        while self.parse_films_queue.qsize() != 0:
            film_ids = self.parse_films_queue.get()
            film_id = film_ids[1]# to load persons and vidoe urls
            film_adjaraid = film_ids[2] #to load film data
            try:
                for_video = r.get("https://api.adjaranet.com/api/v1/movies/"+str(film_id)+"/season-files/0?source=adjaranet",headers=self.headers,timeout=15)
                if for_video.status_code == 200:

                    try:

                        cont = True
                        video_dict = json.loads(for_video.text)
                        video_urls = []
                        for films in video_dict["data"][0]["files"]:
                            for link in films["files"]:
                                #print(films["lang"],link["quality"],":",link["src"])
                                if(films["lang"] == "GEO"):
                                    video_urls.append({link["quality"]:link["src"],"duration":link["duration"]})
                                    cont = False
                        if cont:
                            continue
                        for_actors = r.get("https://api.adjaranet.com/api/v1/movies/"+str(film_adjaraid)+"/persons?page=1&per_page=100&filters%5Brole%5D=cast&source=adjaranet",headers=self.headers,timeout=15)
                        actors = []
                        #print(for_actors,for_video)
                        if for_actors.status_code == 200:
                            actors_dict = json.loads(for_actors.text)
                            for each_actor in actors_dict["data"]:
                                actors.append({"actor_id":each_actor["id"],"name":each_actor["originalName"],"image":each_actor["poster"]})

                            for_data = r.get("https://api.adjaranet.com/api/v1/movies/"+str(film_adjaraid)+"?filters%5Bwith_directors%5D=3&filters%5Bcustom_vast_zone%5D=no&source=adjaranet",headers=self.headers,timeout=15)
                            data_dict = json.loads(for_data.text)
                            if for_data.status_code == 200:
                                genres = []
                                for genre in data_dict["data"]["genres"]["data"]:
                                    genres.append({"genre_id":genre["id"],"genre":genre["secondaryName"]+" / "+genre["primaryName"]})

                                main_title = data_dict["data"]["primaryName"] + " / " +data_dict["data"]["originalName"]
                                description = data_dict["data"]["plot"]["data"]["description"]

                                directors = []
                                for director in data_dict["data"]["directors"]["data"]:
                                        directors.append({"director_id":director["id"],"name":director["originalName"],"image":director["poster"]})

                                releaseDate = data_dict["data"]["releaseDate"]
                                poster = data_dict["data"]["posters"]["data"]["240"]
                                cover = data_dict["data"]["covers"]["data"]["1920"]
                                imdb_data = {"imdbUrl":data_dict["data"]["imdbUrl"],"data":data_dict["data"]["rating"]["imdb"]}

                                main_film_data = {
                                    "title":main_title,
                                    "description":description,
                                    "directors":directors,
                                    "releaseDate":releaseDate,
                                    "poster":poster,
                                    "cover":cover,
                                    "imgb_data":imdb_data

                                }
                                link = "https://www.adjaranet.com/movies/"+str(film_adjaraid)+"/"+data_dict["data"]["primaryName"].replace(" ","-")
                                #print(link)
                                self.main_data["films"].append({"data":main_film_data,"actors":actors,"genres":genres,"video_urls":video_urls,"link":link,"local_db_film_id":film_ids[0]})
                            elif for_data.status_code == 429:
                                film_ids[3]+=1
                                if film_ids[3] < max_error:
                                    self.parse_films_queue.put(film_ids)
                                    print("Too many requests")
                                    continue
                                else:
                                    print("Maximum error exceeded")
                                    continue
                            else:
                                continue
                        elif for_actors.status_code == 429:
                            film_ids[3]+=1
                            if film_ids[3] < max_error:
                                self.parse_films_queue.put(film_ids)
                                print("Too many requests")
                                continue
                            else:
                                print("Maximum error exceeded")
                                continue
                        else:
                            continue


                    except json.decoder.JSONDecodeError:
                        film_ids[3]+=1
                        if film_ids[3] < max_error:
                            self.parse_films_queue.put(film_ids)
                            print("Incorrect returned data")
                            continue
                        else:
                            print("Maximum error exceeded")
                            continue

                elif for_video.status_code ==  429:
                    film_ids[3]+=1
                    if film_ids[3] < max_error:
                        self.parse_films_queue.put(film_ids)
                        print("Too many requests")
                        continue
                    else:
                        print("Maximum error exceeded")
                        continue
                elif for_video.status_code ==  403:
                    print(for_video.text,film_ids)
                    continue
                else:
                    continue
            except r.exceptions.Timeout:
                film_ids[3]+=1
                if film_ids[3] < max_error:
                    self.parse_films_queue.put(film_ids)
                    print("Connection timed out")
                    continue
                else:
                    print("Maximum error exceeded")
                    continue

            except KeyboardInterrupt:
                print("Exit with KeyboardInterrupt")
                exit()
            except:
                print("Something went wrong")

if __name__ == "__main__":
    print("i am here")











#
#for video urls
#https://api.adjaranet.com/api/v1/movies/5431/season-files/0?source=adjaranet

#actors and actres
#https://api.adjaranet.com/api/v1/movies/450271709/persons?page=1&per_page=24&filters%5Brole%5D=cast&source=adjaranet


#for main data
#https://api.adjaranet.com/api/v1/movies/21023?filters%5Bwith_directors%5D=3&filters%5Bcustom_vast_zone%5D=no&source=adjaranet
