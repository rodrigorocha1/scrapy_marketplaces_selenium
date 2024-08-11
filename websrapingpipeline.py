from src.services.iwebscraping import IWebScraping


class WebScrapingPipeline:
    def __init__(self, web_scraping_service: IWebScraping) -> None:
        self.__web_scraping_service = web_scraping_service

    def rodar_web_scraping(self):
        pass
