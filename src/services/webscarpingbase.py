from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from abc import abstractmethod


class WebScrapingBase:
    def __init__(self) -> None:
        self.__servico = Service(ChromeDriverManager().install())
        self.navegador = webdriver.Chrome(service=self.__servico)
        self.navegador.maximize_window()

    @abstractmethod
    def abrir_navegador(self, url: str) -> WebDriver:
        pass

    @abstractmethod
    def fazer_pesquisa_produto(self, termo_busca: str) -> None:
        pass

    @abstractmethod
    def clicar_botao_pesquisa(self) -> None:
        pass

    @abstractmethod
    def selecionar_faixa_preco(self, preco_menor: float, preco_maior: float):
        pass

    @abstractmethod
    def coletar_dados_produtos(self):
        pass
