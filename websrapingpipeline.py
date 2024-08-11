from src.services.iwebscraping import IWebScraping


class WebScrapingPipeline:
    def __init__(self, web_scraping_service: IWebScraping) -> None:
        self.__web_scraping_service = web_scraping_service

    def rodar_web_scraping(self):
        paginacao = True
        while paginacao:
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
            self.__web_scraping_service.coletar_dados_produtos()
            paginacao = self.__web_scraping_service.executar_paginacao()
