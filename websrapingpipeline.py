from src.services.webscarpingbase import WebScrapingBase


class WebScrapingPipeline:
    def __init__(self, web_scraping_service: WebScrapingBase) -> None:
        self.__web_scraping_service = web_scraping_service

    def rodar_web_scraping(self):
        pass
