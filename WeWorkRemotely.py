import requests
from bs4 import BeautifulSoup
import creds

class WeWorkRemotely:
    """
    `WeWorkRemotely` is a scraper, that scrapes https://weworkremotely.com/
    methods: 
    - `Scrape` scrapes website and returns a `requests.Response` type object
    - `Parse` a `requests.Response` type object and append the found urls in the `list[str]` type `self.urls` variable
    """

    def Parse(self, response : requests.Response)->None:
        """
        Parse function searches for addvertisement and extract their url
        return: `None`
        """
        doc = BeautifulSoup(response.text, 'html.parser')
        advertisements : list[BeautifulSoup] = doc.find(class_="jobs").find_all("li")[:-1]

        for ad in advertisements:
            title = str(ad.find(class_="title")).lower()
            if "product" in title and "manager" in title:
                #print(title)
                self.urls.append(f'https://weworkremotely.com{ad.select_one(".title").parent.get("href")}')
            else:
                continue  

    def Scrape(self) -> requests.Response:
        """
        Scrape https://weworkremotely.com/
        return: `request.Response` object
        """
        proxies = creds.proxies
        url = "https://weworkremotely.com/categories/remote-product-jobs"
        payload = ""
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "__adroll_fpc=1f45a6941a7689fb3d63ce7fdbd65c10-1667922627216; _hjSessionUser_2385808=eyJpZCI6IjUwZGE1M2I0LWZmYWQtNWQyZS04YWZiLTEzZDQ0YWViZWJmNCIsImNyZWF0ZWQiOjE2Njc5MjI2MTM5NTYsImV4aXN0aW5nIjp0cnVlfQ==; __adroll_consent=CPiKMt9PiKMt9AAACBENAJCv_____3___wQAAQv____-AEL_____gAA%23ACJ6YJHXKNBNJBSFTNFVOF; ln_or=d; _hjIncludedInSessionSample=0; _hjSession_2385808=eyJpZCI6IjFkOGJiYjMwLTQxNDQtNDgyYS04OTNlLTJhNDRiODU5NzA5NiIsImNyZWF0ZWQiOjE2NjgxMTMyNzkyODgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _jobs_session=TS1%2B%2BgDD%2FECmHwV73HStieuzhQ%2BAF96jKtpAq6nxvBq%2Bvd3vSfUckzDzG%2B%2F5IZjWOU%2BocPzRhUaXqXNDpgSRa5ID71%2BYIYGUTHhlFDwIHaszAZP26OS%2B5VQ42Meat2o3X2csINDQW14HNQz%2BlU7zTW32pBFi2iATVM1uWpCS8NkzpftCPXcji5oHzQMG1NiZ0btztllll7KHxSB9u7XoZfqytQAnxrZrG36kNt4siQNyEZZajUbyLLye3zn%2FkIDv%2Fb%2Bh00BZiHduin5T6MUrL3Shg%2FAS--zCupK1quaDHi%2Fp2P--AmNyFi0QKx3Ed2zuEcts%2Fg%3D%3D; __ar_v4=ACJ6YJHXKNBNJBSFTNFVOF%3A20221108%3A9%7CW4DPE7ODW5E3BKBBL3VPMG%3A20221108%3A9%7CWRYKO24VNNGITFKBAXEEY3%3A20221108%3A9",
            "If-None-Match": 'W/"0410cec6df56d8306133aaf028fbc2fa"',
            "Referer": "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term=product+manager",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }

        response = requests.request("GET", url, data=payload, headers=headers, proxies=proxies)

        return response

    def __init__(self) -> None:
        self.domain = "https://weworkremotely.com/"
        response : requests.Response = self.Scrape()   
        #print([(i.url, i.status_code) for i in responses])
        self.urls : list[str] = []
        self.Parse(response)
        

if __name__ == '__main__':
    print(WeWorkRemotely().urls)
    