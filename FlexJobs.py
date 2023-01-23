import requests
from bs4 import BeautifulSoup
import re
import creds

class FlexJobs:
    """
    `FlexJobs` is a scraper, that scrapes flexjobs.com
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
        advertisements : list[BeautifulSoup] = doc.find_all("li", class_="job")
        for ad in advertisements:
            try:
                re.search(r"Product Manager", ad.a.get_text(), re.IGNORECASE).group()
                self.urls.append(f"https://www.flexjobs.com{ad.a.get('href')}")
            except:
                continue

    def RunParser(self, responses : list[requests.Response]) -> None:
        """`RunParser` runs `Parser` function and returns `None`"""
        for response in responses:
            self.Parse(response)

    def Scrape(self, index : int) -> requests.Response:
        """
        Scrape www.flexjobs.com
        return: `request.Response` object
        """
        proxies = creds.proxies
        url = "https://www.flexjobs.com/search"
        querystring = {"exact":"on","location":"","page":f"{index}","search":"&quot;product manager&quot;","srt":"date"}
        payload = ""
        headers = {
            "cookie": "_ga=GA1.1.155597045.1667908556; _gcl_au=1.1.1181553448.1667908556; _tt_enable_cookie=1; _ttp=0064d871-8206-4c96-917a-24fb26fc240a; _cb=_p-szQpJmbulqlh; _uetsid=2a050d50611b11edacf84550537b641a; _uetvid=4d6c62505f5c11ed81f96b7eb5d814b4; _cb_svref=null; _session_id=ddb16d01846032ecf837d74c14c17db1; AWSALB=h6+1t0WgsnLDSfZg2eHE3Tw7eARBEeG97+GbVjzPhsUbsbUlMRgjX/0ZH87yA41VT15xSC9QbDqifBPfDhkjtJCOdkgNs70202e9nA4hJyynKMCWWZ9ozA0cbNnV; AWSALBCORS=h6+1t0WgsnLDSfZg2eHE3Tw7eARBEeG97+GbVjzPhsUbsbUlMRgjX/0ZH87yA41VT15xSC9QbDqifBPfDhkjtJCOdkgNs70202e9nA4hJyynKMCWWZ9ozA0cbNnV; _chartbeat2=.1667908556600.1668100680192.101.D_Rfo-DNkDbPCX8i8UCzev50CpApiZ.6; _ga_WMVDBGWRKR=GS1.1.1668100481.3.1.1668100736.0.0.0; _chartbeat5=344|10856|%2Fsearch|https%3A%2F%2Fwww.flexjobs.com%2Fsearch%3Fexact%3Don%26location%3D%26page%3D2%26search%3D%2526quot%253Bproject%2Bmanager%2526quot%253B%26srt%3Ddate|DiCgCBrMiGrDLXp9xCSGHXXCCyt2q||c|D_iTryCcnc5cC5znhmBt7vKxC_488j|flexjobs.com|",
            "authority": "www.flexjobs.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
            "referer": "https://www.flexjobs.com/search?search=%22project+manager%22&location=&srt=date",
            "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring, proxies=proxies)

        return response

    def RunScraper(self) -> list[requests.Response]:
        """
        This function handle pagination. It calls the `self.Scrape` function by `i` times
        returns: `list[requests.Response]`
        """

        list_of_responses : list[requests.Response] = []
        for i in range(1,3):
            list_of_responses.append(self.Scrape(i))

        return list_of_responses

    def __init__(self) -> None:
        self.domain = "https://www.flexjobs.com/"
        self.urls : list[str] = []
        responses : list[requests.Response] = self.RunScraper()    
        #print([(i.url, i.status_code) for i in responses])
        self.RunParser(responses)
        

if __name__ == '__main__':
    print(FlexJobs().urls)