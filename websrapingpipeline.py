from src.services.iwebscraping import IWebScraping
from src.services.webscrapingleroymerlin import WebScrapingLeroyMerling
from src.services.web_scraping_telha_norte import WebScrapingTelhaNorte
from src.pacote_log.config__log import logger
from src.infra.interface.iconexaodatabase import IconexaoDatabase
from src.infra.conexao_banco_sqlite import ConexaoBancoSQLITE
from src.enums.enum_empresa import Empresa


class WebScrapingPipeline:
    def __init__(
            self,
            operacoes_banco: IconexaoDatabase,
            opcao: Empresa,
            preco_maior: float = None,
            preco_menor: float = None
    ) -> None:
        """Init da classe WebScrapingPipeline

        Args:
            operacoes_banco (IconexaoDatabase): Recebe um objeto banco
            opcao (int): opção de seleção web scraping
            preco_maior (float, optional): Preço maior para alguns serviços web scraping. Defaults to None.
            preco_menor (float, optional): Preço menor para alguns serviços. Defaults to None.
        """

        self.__operacoes_banco = operacoes_banco
        self.__preco_maior = preco_maior
        self.__preco_menor = preco_menor
        self.__opcao = opcao
        self.__web_scraping_service = self.selecionar_servico_web_scraping()

    def selecionar_servico_web_scraping(self) -> IWebScraping:
        """Seleciona a ordem de execução web scrapinf

        Returns:
            IWebScraping: Serviço web scraping
        """
        match self.__opcao:
            case Empresa.LEROY_MERLIN:

                return WebScrapingLeroyMerling(
                    preco_menor=self.__preco_menor,
                    preco_maior=self.__preco_maior
                )
            case Empresa.TELHA_NORTE:

                return WebScrapingTelhaNorte()

    def rodar_web_scraping(self):
        """Método para rodar o serviço web scraping
        """

        self.__web_scraping_service.abrir_navegador()
        self.__web_scraping_service.fazer_pesquisa_produto(
            termo_busca='Churrasqueira'
        )

        logger.info('Inserindo produtos no banco')
        for produto in self.__web_scraping_service.coletar_dados_produtos():
            self.__operacoes_banco.inserir_produtos(dados=produto)

        self.__web_scraping_service.fechar_nagegador()


if __name__ == '__main__':
    logger.info('Iniciando web Scraping')
    for servico_web_scraping in [Empresa.LEROY_MERLIN, Empresa.TELHA_NORTE]:
        print(servico_web_scraping)
        ws = WebScrapingPipeline(
            operacoes_banco=ConexaoBancoSQLITE(),
            preco_menor=100,
            preco_maior=120,
            opcao=servico_web_scraping
        )
        ws.rodar_web_scraping()
    logger.info('Fim web Scraping')
