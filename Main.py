from Angel import Angel
from FlexJobs import FlexJobs
from HubStaff import HubStaff
from RemoteOk import RemoteOk
from WeWorkRemotely import WeWorkRemotely
import creds
import concurrent.futures
import pandas as pd
import datetime
from email.message import EmailMessage
import ssl, smtplib
import time


class Main:
    def Log(self, start : float, end : float, event : str):
        """
        Log method appends log informations into `self.loggedDatas`
        input arguments: 
        - `start : float` start time
        - `end : float` end time
        - `event : str` event description
        
        return: `None`
        """
        self.loggedDatas.append(f'{event} in {end-start:.4f}s')

    def InitializeMemory(self):
        """This method calls and parses crawler_memory.csv"""
        _start = time.perf_counter()

        df = pd.read_csv("crawler_memory.csv", sep=";")
        #df.sort_values(by = ["dateid"], ascending=[False])

        _end = time.perf_counter()
        self.Log(_start, _end, "Memory is initialized")
        return df

    def ExecuteScrapers(self):
        """
        - This method calls the Scrapers from `self.scrapers` list and execute them with `concrurrent.fututres.ThreadPoolExecutor`.
        - The executed scrapers are appended to `self.executed_scrapers` list.
        - return: `None`
        """
        _start = time.perf_counter()

        with concurrent.futures.ThreadPoolExecutor() as exec:
            for result in exec.map(lambda s: s(), self.scrapers):
                self.executed_scrapers.append(result)

        _end = time.perf_counter()
        self.Log(_start,_end,"Sites are scrapped")
    
    def ValidateUrl(self, url : str):
        """
        - This method checks whether a url was previously scraped in the past or it a new one
        - return: `True` if memory contains url, `False` if memory does not contain url
        """
        if self.memory["url"].str.contains(url, regex=False).any():
            return True
        else:
            return False

    def RunValidation(self):
        """
        - This method calls `ValidateUrl` with `concurrent.futures.ThreadPoolExecutor` and appends valid urls into `self.urls`
        - return: `None`
        """
        self.loggedDatas.append("Start validating found urls")

        with concurrent.futures.ThreadPoolExecutor() as exec:
            for scraper in self.executed_scrapers:
                _start = time.perf_counter()
                
                for url in scraper.urls:
                    future = exec.submit(self.ValidateUrl, url)
                    if future.result() == False:
                        self.urls.append(url)
                
                self.Log(_start,time.perf_counter(),f"The urls from {scraper.domain} are validated")
        
        self.loggedDatas.append("Validation of found urls is ended")

    def FormatEmailBody(self):
        """
        This method is called by `self.SendEmail()` method and creats the html body of the email.
        returns: `LiteralString` of `html` variable
        """
        bodyContent = []
        for scraper in self.executed_scrapers:
            domain = scraper.domain.replace("https://", "").replace("www.", "")[:-1]
            relevant_urls = [i for i in self.urls if domain in i]
            if relevant_urls == []:
                output = "<i>No new advertisment was found with the keyword of \"product manager\".</i>"
            else:
                lis = [f'<li>{i}</li>' for i in relevant_urls]
                joined_lis = "\n".join(lis)
                output = f'<ul>{joined_lis}</ul>'
            bodyContent.append(f"<p><b>Found advertisements on {domain}:</b></p>{output}")
        body = "\n".join(bodyContent)
        html = f"""<html>
            <body>
                {body}
                <p>The content of this email was auto-crawled and auto-generated. In case of any question, problem please send your feedback via email to orban.gabor.mail@gmail.com or via fiverr to gabor_orban.</p>
            </body>
        </html>
        """
        return html

    def SendEmail(self):
        """
        This method sends `self.urls` content (if not empty) with `smptlib`
        Used modules: 
        - `creds`: contains password
        - `EmailMessage`: contains subject and body of email
        - `ssl`: provides secure connection
        - `smptlib`: handles connection with email server
        return: `None`
        """
        _start = time.perf_counter()

        email_sender = creds.email_sender
        email_password = creds.password16
        email_receiver = creds.toAddress
        subject = f'Found advertisements [keyword: Product Manager] - Date: {datetime.datetime.now().strftime("%d/%m/%Y")}'
        html = self.FormatEmailBody()

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em['Bcc'] = creds.bccAddress
        em.set_content("Found urls:")
        em.add_alternative(html, subtype='html')

        logMail = EmailMessage()
        logMail['From'] = email_sender
        logMail['To'] = creds.bccAddress
        logMail['Subject'] = f'Log output from crawler - Date: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}'

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

            _end = time.perf_counter()
            self.Log(_start,_end,"Email output is created, formated and sent")

            logMail.set_content("\n".join(self.loggedDatas))

            smtp.sendmail(email_sender, creds.bccAddress, logMail.as_string())

    def SaveUrlsIntoMemory(self):
        """
        This method saves `self.url` with dateid (format=yyyymmdd) into crawler_memory.csv
        return: `None`
        """

        format_output = {
            "url": self.urls,
            "dateid": [f"{datetime.datetime.now().strftime('%Y%m%d')}" for _ in self.urls]
        }
        df = pd.DataFrame(format_output)
        self.memory = pd.concat([df, self.memory])
        self.memory.to_csv("crawler_memory.csv", sep=";", index=False)

    def __init__(self):
        #region: assigning variables
        self.loggedDatas = []
        self.scrapers = [Angel, FlexJobs, HubStaff, RemoteOk, WeWorkRemotely]
        self.executed_scrapers = []
        self.urls = []
        self.memory : pd.DataFrame = self.InitializeMemory()
        #endregion

        #region: calling methods
        self.ExecuteScrapers()
        self.RunValidation()
        self.SendEmail()
        self.SaveUrlsIntoMemory()
        #endregion
          

if __name__ == "__main__":
    Main()