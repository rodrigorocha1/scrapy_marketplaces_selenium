from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.services.iwebscraping import IWebScraping
from abc import abstractmethod
from typing import (
    Generator,
    Dict
)


class WebScrapingBase(IWebScraping):
    def __init__(self) -> None:
        self.__servico = Service(ChromeDriverManager().install())
        self.navegador = webdriver.Chrome(service=self.__servico)
        self.navegador.maximize_window()

    @abstractmethod
    def abrir_navegador(self, url: str):
        """Método para abrir o navegador e conectar na url

        Args:
            url (str): url do site

        """
        pass

    @abstractmethod
    def fazer_pesquisa_produto(self, termo_busca: str) -> None:
        """Método para fazer a pesquisa de um produto

        Args:
            termo_busca (str): Nome do produto: Ex: Churrasqueira
        """
        pass

    @abstractmethod
    def clicar_botao_pesquisa(self) -> None:
        """Método para fazer a pesquisa
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
    def executar_paginacao(self) -> bool:
        """Execcuta a páginação

        Returns:
            bool: Verdadeiro caso a páginação seja feita com sucesso, falso caso contrário
        """
        pass

    def fechar_nagegador(self):
        """Método para fechar o navegador
        """
        pass
