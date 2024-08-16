from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.services.iwebscraping import IWebScraping
from abc import abstractmethod
from datetime import datetime
from typing import (
    Generator,
    Dict,
    Optional
)


class WebScrapingBase(IWebScraping):
    def __init__(self, url: str) -> None:
        self.__url = url
        self.__sevico = Service(ChromeDriverManager().install())
        self.navegador = webdriver.Chrome(service=self.__sevico)

    def _data_atual(self) -> datetime:
        """Método para obter a data atual

        Returns:
            datetime: data_atual
        """
        data_atual = datetime.now()
        data_formatada = data_atual.strftime('%Y-%m-%d %H:%M:%S')

        return data_formatada

    def abrir_navegador(self):
        """Método para abrir o navegador e conectar na url

        """
        self.navegador.get(self.__url)

    @abstractmethod
    def fazer_pesquisa_produto(self, termo_busca: str) -> None:
        """Método para fazer a pesquisa de um produto

        Args:
            termo_busca (str): Nome do produto: Ex: Churrasqueira
        """
        pass

    @abstractmethod
    def coletar_dados_produtos(self) -> Generator[Dict[str, str | int | float], None, None]:
        """Método para retornar os dados de cada produto por vez

        Yields:
            Generator[Dict[str, str | int | float], None, None]: Um gerador de produtos
        """
        pass

    @abstractmethod
    def executar_paginacao(self) -> Optional[bool]:
        """Execcuta a páginação

        Returns:
            bool: Verdadeiro caso a páginação seja feita com sucesso, falso caso contrário
        """
        pass

    def fechar_nagegador(self):
        self.navegador.close()
