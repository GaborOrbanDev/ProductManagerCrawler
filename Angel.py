import requests
from bs4 import BeautifulSoup
import re
import creds


class Angel:
    """
    `Angel` is a scraper, that scrapes angel.co
    methods: 
    - `RunScraper` calls `Scrape` function, and returns a `list[requests.Respons]`
    - `Scrape` scrapes website and returns a `requests.Response` type object
    - `RunParser` runs `Parser` function and returns `None`
    - `Parse` a `requests.Response` type object and append the found urls in the `list[str]` type `self.urls` variable
    """

    def Parse(self, response : requests.Response)->None:
        """
        Parse function searches for addvertisement and extract their url
        return: `None`
        """
        doc = BeautifulSoup(response.text, 'html.parser')
        advertisements : list[BeautifulSoup] = doc.find_all(class_="styles_jobListing__PLqQ_")
        
        for ad in advertisements:
            try:
                re.search(r"Product Manager", ad.a.get_text(), re.IGNORECASE).group()
                self.urls.append(f"https://angel.co{ad.a.get('href')}")
            except:
                continue

    def RunParser(self, responses : list[requests.Response]) -> None:
        """`RunParser` runs `Parser` function and returns `None`"""
        for response in responses:
            self.Parse(response)

    def Scrape(self, index : int) -> requests.Response:
        """
        Scrape angel.co
        return: `request.Response` object
        """
        proxies = creds.proxies
        url = "https://angel.co/role/r/product-manager"
        querystring = {"page": f"{index}"}
        payload = ""
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
            "cache-control": "max-age=0",
            "cookie": 'ajs_anonymous_id=90ffa68e-a096-4712-a869-9f2c33c749dc; _angellist=a331fc18998ce575befa68672e7ad975; _gcl_au=1.1.119084880.1667908491; ln_or=d; _ga=GA1.1.1714932784.1667908491; __stripe_mid=5a2073d6-a605-4a10-b2fb-c83d4e1116451af506; __cf_bm=w3FQxFXZowN4dVgkrlrrYU0w4aas5YPo1I7.9AxJIuk-1667920398-0-AYhG9xq1WJSo3nS5ObP5fDUFaLn8zJPAVvGA/D1/6NxGZ717fBQFrJNbkZk0pYXVEKfS0jWVUHkqCgMI4iw5L7Q=; _hjSessionUser_1444722=eyJpZCI6ImEwYWY3YzAzLTMzZWYtNThkOC05YTg3LTQwYjFmNjY4ZWIzZSIsImNyZWF0ZWQiOjE2Njc5MDg0OTEzNDMsImV4aXN0aW5nIjp0cnVlfQ==; _hjIncludedInSessionSample=0; _hjSession_1444722=eyJpZCI6Ijc3MmI0MzdiLTU4NDItNDQ1MC05NmY0LWQ2MzA1ZjBkMzVlMiIsImNyZWF0ZWQiOjE2Njc5MjA0MDQ2MjQsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; g_state={"i_p":1668006809568,"i_l":2}; __stripe_sid=7690b9d5-9d8d-4fa5-91e2-6957099896be23a528; _ga_705F94181H=GS1.1.1667920404.2.1.1667920554.53.0.0; datadome=b600kNctMx-rsDAOvrP-UsxZr6G_U-gm5VRHKHoSblQ2DJtzE10Iv38JrJ3oAJh3M~IDAUt1ZFxmcc.idmLbta49WVUzKGqJrFZTZSQ4pTg7xcsUzlbnz5DVbmB2PZB',
            "sec-ch-device-memory": "8",
            "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            "sec-ch-ua-arch": '"x86"',
            "sec-ch-ua-full-version-list": '"Chromium";v="106.0.5249.119", "Google Chrome";v="106.0.5249.119", "Not;A=Brand";v="99.0.0.0"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring, proxies=proxies)

        return response

    def RunScraper(self) -> list[requests.Response]:
        """
        This function handle pagination. It calls the `self.Scrape` function by `i` times
        returns: `list[requests.Response]`
        """

        list_of_responses : list[requests.Response] = []
        for i in range(1,11):
            list_of_responses.append(self.Scrape(i))

        return list_of_responses

    def __init__(self) -> None:
        self.domain = "https://angel.co/"
        self.urls : list[str] = []
        responses : list[requests.Response] = self.RunScraper()    
        #print([(i.url, i.status_code) for i in responses])
        self.RunParser(responses)
        

if __name__ == '__main__':
    print(Angel().urls)