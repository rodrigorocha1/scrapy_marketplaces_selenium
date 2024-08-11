from src.services.iwebscraping import IWebScraping
from src.services.webscrapingleroymerlin import WebScrapingLeroyMerling
from src.pacote_log.config__log import logger
from time import sleep


class WebScrapingPipeline:
    def __init__(self, web_scraping_service: IWebScraping) -> None:
        self.__web_scraping_service = web_scraping_service

    def rodar_web_scraping(self):
        logger.info('Iniciando web Scraping')
        paginacao = True

        self.__web_scraping_service.abrir_navegador(
            url='https://www.leroymerlin.com.br/'
        )
        self.__web_scraping_service.fazer_pesquisa_produto(
            termo_busca='Churrasqueira'
        )
        self.__web_scraping_service.clicar_botao_pesquisa()
        self.__web_scraping_service.selecionar_faixa_preco(
            preco_menor=100,
            preco_maior=150
        )
        while paginacao:

            sleep(3)
            for produto in self.__web_scraping_service.coletar_dados_produtos():
                print('Entrou no loop para obter os dados dos produtos')
                print(produto)
            paginacao = self.__web_scraping_service.executar_paginacao()
        self.__web_scraping_service.fechar_nagegador()


ws = WebScrapingPipeline(web_scraping_service=WebScrapingLeroyMerling())
ws.rodar_web_scraping()
