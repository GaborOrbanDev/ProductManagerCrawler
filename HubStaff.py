import requests
from bs4 import BeautifulSoup
import re
import creds

class HubStaff:
    """
    `HubStaff` is a scraper, that scrapes https://talent.hubstaff.com/
    methods: 
    - `RunScraper` calls `Scrape` function, and returns a `list[requests.Respons]`
    - `Scrape` scrapes website and returns a `requests.Response` type object
    - `RunParser` runs `Parser` function and returns `None`
    - `Parse` a `requests.Response` type object and append the found urls in the `list[str]` type `self.urls` variable
    """

    def Parse(self, response : requests.Response)->None:
        """
        Parse function searches for addvertisement and extracts their url
        return: `None`
        """
        try:
            raw_doc = re.search(r'.html\(.*?\);', response.text).group()
        except:
            return
        clean_raw_doc = re.sub(r'\\"', r'"', raw_doc)
        doc = BeautifulSoup(clean_raw_doc, "html.parser")
        advertisements : list[BeautifulSoup] = doc.find_all(class_='main-details')
        for ad in advertisements:
            try:
                title = re.search(r'^.*?<\\/a>', ad.a.get_text()).group()
                if re.search(r"Product Manager", title, re.IGNORECASE) != None:
                    self.urls.append(f'https://talent.hubstaff.com{ad.a.get("href")}')
                else:
                    #print("Nem talált:", title)
                    pass
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
        url = "https://talent.hubstaff.com/search/jobs"

        querystring = {"utf8":"✓","search[keywords]":"product manager","page":f"{index}","search[type]":"","search[last_slider]":"","search[newer_than]":["",""],"search[payrate_start]":"1","search[payrate_end]":"100+","search[payrate_null]":["0","1"],"search[budget_start]":"1","search[budget_end]":"100000+","search[budget_null]":["0","1"],"search[experience_level]":"-1","search[countries][]":"","search[languages][]":"","search[sort_by]":"date_added"}

        payload = ""
        headers = {
            "cookie": "ahoy_visitor=60c780b5-24ea-42dd-9ea4-6b957d6db5e1; ajs_anonymous_id=78d17f69-2eff-4e9f-b5eb-fe32645a20bc; wooTracker=PlwAZmeN7gWF; hubspotutk=e7400dcc08784e76c324770ba5a6f3cd; _gcl_au=1.1.408722305.1667921401; ahoy_visit=403b925c-299f-4991-8296-0a9d49a80e0a; __cflb=0H28vJNXHmvLZh4zYzEMp9a8sNN2fnhBq7Q8Sn7VgXf; __hstc=16287913.e7400dcc08784e76c324770ba5a6f3cd.1667921399421.1667921399421.1668102247923.2; __hssrc=1; ln_or=d; _hubstaff-talent_session=d3M5Mmo1Q0NtUlprOFQzUHhXbWJVN0MzL2M0RUs0WUxIeW1qc1RFVnVjZVV5K2JqcEtuNE5OaVhRSWt4VUNLby0taUdnYW9YazFLZWU3eXFKU1NqWVVBdz09--91c5542d808971de02de5c2616563300ae66d29c; __hssc=16287913.8.1668102247923",
            "authority": "talent.hubstaff.com",
            "accept": "*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript",
            "accept-language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
            "if-none-match": 'W/"7ae24d2840509f616e4d68a1fcf9ee4a"',
            "referer": "https://talent.hubstaff.com/search/jobs?search%5Bkeywords%5D=product+manager&page=1&search%5Btype%5D=&search%5Blast_slider%5D=&search%5Bnewer_than%5D=&search%5Bnewer_than%5D=&search%5Bpayrate_start%5D=1&search%5Bpayrate_end%5D=100%2B&search%5Bpayrate_null%5D=0&search%5Bpayrate_null%5D=1&search%5Bbudget_start%5D=1&search%5Bbudget_end%5D=100000%2B&search%5Bbudget_null%5D=0&search%5Bbudget_null%5D=1&search%5Bexperience_level%5D=-1&search%5Bcountries%5D%5B%5D=&search%5Blanguages%5D%5B%5D=&search%5Bsort_by%5D=date_added",
            "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "x-csrf-token": "5PuSdImBGn8hH0sEL2T/3RUKuWcrmvyyp5eAv+Z1jVcDGs2Q8S2JyGOfy50dDDQLZ/SQa3S8eOl3QLOOAJ6r8Q==",
            "x-requested-with": "XMLHttpRequest"
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
        self.domain = "https://talent.hubstaff.com/"
        self.urls : list[str] = []
        responses : list[requests.Response] = self.RunScraper()    
        self.RunParser(responses)
        

if __name__ == '__main__':
    print(HubStaff().urls)