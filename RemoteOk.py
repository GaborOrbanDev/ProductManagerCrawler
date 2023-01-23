import requests
from bs4 import BeautifulSoup
import creds

class RemoteOk:
    """
    `RemoteOk` is a scraper, that scrapes remoteok.com
    methods: 
    - `Scrape` scrapes website and returns a `requests.Response` type object
    - `Parse` a `requests.Response` type object and appends found urls in `self.urls`
    """
    def Scrape(self)->requests.Response:
        """
        Scrape remoteok.com
        return: `request.Response` object
        """
        url = "https://remoteok.com/"

        proxies = creds.proxies

        querystring = {"tags":"product-manager","order_by":"date","action":"get_jobs"}

        payload = ""
        headers = {
            "cookie": "ref=https%3A%2F%2Fremoteok.com%2Fremote-product-management-jobs; new_user=false; hidden_subscribe_to_newsletter_Product Management=true; visits=12; visit_count=12; adShuffler=0",
            "authority": "remoteok.com",
            "accept": "*/*",
            "accept-language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
            "referer": "https://remoteok.com/remote-product-manager-jobs?order_by=date",
            "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring, proxies=proxies)
        return response

    def Parse(self, response : requests.Response)->None:
        """
        Parse function searches for addvertisement and extract their url
        return: `None`
        """
        doc = BeautifulSoup(response.text, 'html.parser')
        advertisements : list[BeautifulSoup] = doc.find_all(class_="job")
        for ad in advertisements:
            self.urls.append(f"https://remoteok.com{ad.a.get('href')}")

    def __init__(self) -> None:
        self.domain = "https://remoteok.com/"
        self.urls : list[str] = []
        response : requests.Response = self.Scrape()
        self.Parse(response)

if __name__ == '__main__':
    print(RemoteOk().urls)