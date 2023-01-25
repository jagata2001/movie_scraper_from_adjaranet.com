import requests as r
from bs4 import BeautifulSoup


class Wordpress:
    def __init__(self,domain,username,password):
        if ("https" not in domain) or ("http" not in domain):
            print("Please add http or https")
            exit()
        self.domain = domain
        self.__username = username
        self.__password = username
    def login(self):
        login_url = self.domain+"/wp-login.php"
        load_header = {
            "Host": self.domain.split("/")[2],
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "TE": "Trailers"
        }
        login_header = {
            "Host": self.domain.split("/")[2],
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": login_url,
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": self.domain,
            "Connection": "keep-alive",
            "Cookie": "",
            "Upgrade-Insecure-Requests": "1",
        }
        try:
            resp = r.get(login_url,headers=load_header,timeout=15)
            if resp.status_code == 200:

                starstruck = resp.headers["Set-Cookie"].split(";")[0]+";"
                wordpress_test_cookie = "wordpress_test_cookie"+resp.headers["Set-Cookie"].split("wordpress_test_cookie")[1].split(";")[0]+";"
                login_header["Cookie"] = f"{starstruck} {wordpress_test_cookie}"
                print(login_header["Cookie"])
                login_data = {
                    "log":self.__username,
                    "pwd":self.__password,
                    "wp-submit":"შესვლა",
                    "redirect_to":login_url,
                    "testcookie":"1"
                }
                try:
                    login_resp = r.post(login_url,data=login_data,headers=login_header,timeout=15,allow_redirects=False)
                    if login_resp.status_code == 302:
                        print("succesfully loged in")
                        wordpress_sec = "wordpress_sec"+login_resp.headers["Set-Cookie"].split("wordpress_sec")[1].split(";")[0]+";"
                        wordpress_logged_in = "wordpress_logged_in"+login_resp.headers["Set-Cookie"].split("wordpress_logged_in")[1].split(";")[0]+";"
                        self.__loged_cookie = f"{wordpress_test_cookie} {wordpress_sec} {wordpress_logged_in}"
                        return 1
                    else:
                        print("Incorrect username of password")
                        return 0
                except r.exceptions.Timeout:
                    print("Connection timed out")
                    return 0
                except:
                    print("Something went wrong")
                    return 0
            else:
                print(f"status code Error: {resp.status_code}")

        except r.exceptions.Timeout:
            print("Connection timed out")
            return 0
        except:
            print("Something went wrong")
            return 0

call = Wordpress("https://*.ga/","root","toor")
call.login()
