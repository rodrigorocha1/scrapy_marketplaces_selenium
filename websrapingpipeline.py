from src.services.iwebscraping import IWebScraping
from src.services.webscrapingleroymerlin import WebScrapingLeroyMerling
from src.services.web_scraping_telha_norte import WebScrapingTelhaNorte
from src.pacote_log.config__log import logger
from time import sleep
from src.infra.interface.iconexaodatabase import IconexaoDatabase
from src.infra.conexao_banco_sqlite import ConexaoBancoSQLITE


class WebScrapingPipeline:
    def __init__(
            self,
            operacoes_banco: IconexaoDatabase,
            opcao: int,
            preco_maior: float = None,
            preco_menor: float = None
    ) -> None:
        self.__opcao = opcao
        self.__operacoes_banco = operacoes_banco
        self.__preco_maior = preco_maior
        self.__preco_menor = preco_menor
        self.__web_scraping_service = self.selecionar_servico_web_scraping()

    def selecionar_servico_web_scraping(self) -> IWebScraping:
        match self.__opcao:
            case 1:

                return WebScrapingLeroyMerling(
                    preco_menor=self.__preco_menor,
                    preco_maior=self.__preco_maior
                )
            case 2:

                return WebScrapingTelhaNorte()

    def rodar_web_scraping(self):

        self.__web_scraping_service.abrir_navegador()
        self.__web_scraping_service.fazer_pesquisa_produto(
            termo_busca='Churrasqueira'
        )
        sleep(3)
        logger.info('Inserindo produtos no banco')
        for produto in self.__web_scraping_service.coletar_dados_produtos():
            self.__operacoes_banco.inserir_produtos(dados=produto)
        self.__web_scraping_service.fechar_nagegador()


logger.info('Iniciando web Scraping')
for servico_web_scraping in [1, 2]:
    print(servico_web_scraping)
    ws = WebScrapingPipeline(
        operacoes_banco=ConexaoBancoSQLITE(),
        preco_menor=100,
        preco_maior=150,
        opcao=servico_web_scraping
    )
    ws.rodar_web_scraping()
logger.info('Fim web Scraping')
