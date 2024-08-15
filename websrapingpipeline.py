from src.services.iwebscraping import IWebScraping
from src.services.webscrapingleroymerlin import WebScrapingLeroyMerling
from src.services.web_scraping_telha_norte import WebScrapingTelhaNorte
from src.pacote_log.config__log import logger
from time import sleep
from src.infra.interface.iconexaodatabase import IconexaoDatabase
from src.infra.conexao_banco_sqlite import ConexaoBancoSQLITE


class WebScrapingPipeline:
    def __init__(self, web_scraping_service: IWebScraping, operacoes_banco: IconexaoDatabase) -> None:
        self.__web_scraping_service = web_scraping_service
        self.__operacoes_banco = operacoes_banco

    def rodar_web_scraping(self):

        self.__web_scraping_service.abrir_navegador()
        self.__web_scraping_service.fazer_pesquisa_produto(
            termo_busca='Telha'
        )
        sleep(3)
        for produto in self.__web_scraping_service.coletar_dados_produtos():
            self.__operacoes_banco.inserir_produtos(dados=produto)
        self.__web_scraping_service.fechar_nagegador()


logger.info('Iniciando web Scraping')
ws = WebScrapingPipeline(
    web_scraping_service=WebScrapingTelhaNorte(),
    operacoes_banco=ConexaoBancoSQLITE()
)
ws.rodar_web_scraping()
logger.info('Fim web Scraping')
