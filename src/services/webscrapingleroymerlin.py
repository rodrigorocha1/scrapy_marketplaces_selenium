from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.services.webscarpingbase import WebScrapingBase
from src.pacote_log.config__log import logger
from typing import (Generator, Tuple)
from datetime import datetime


class WebScrapingLeroyMerling(WebScrapingBase):

    def __init__(self) -> None:
        self.__data_extracao = self.__data_atual()
        super().__init__()

    def abrir_navegador(self, url: str):
        """Método para abrir o navegador e conectar na url

        Args:
            url (str): url do site

        """
        self.navegador.get(url)

    def __data_atual(self) -> datetime:
        """Método para obter a data atual

        Returns:
            datetime: data_atual
        """
        data_atual = datetime.now()
        data_formatada = data_atual.strftime('%Y-%m-%d %H:%M:%S')

        return data_formatada

    def fazer_pesquisa_produto(self, termo_busca: str) -> None:
        """Método para abrir o navegador e conectar na url

        Args:
            url (str): url do site

        """
        try:
            busca_produto = self.navegador.find_element(
                By.ID,
                '@autocomplete-quicksearch-input'
            )
            busca_produto.send_keys(termo_busca)
        except NoSuchElementException as msg:
            logger.error(f'Não encontrou id: {msg} ')

    def __esperar_elemento(self):
        """Espera a tag do css antes de fazer as pesquisas
        """
        WebDriverWait(self.navegador, 20).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '#mobile-filter-content > div > div > div:nth-child(6) > div.flex-1.px-4.py-4 > div > div:nth-child(1) > div > input'
                )
            )
        )

    def clicar_botao_pesquisa(self) -> None:
        """Método para fazer a pesquisa
        """
        self.navegador.find_element(
            By.XPATH,
            '/html/body/header/div[2]/div/div[1]/form/div/div[1]/div/div/button'
        ).click()

    def selecionar_faixa_preco(self, preco_menor: float, preco_maior: float):
        """Método para selecionar a faixa de preço

        Args:
            preco_menor (float): preço menor do produto
            preco_maior (float): preço maior do produto
        """
        self.__esperar_elemento()
        preco_minimo = self.navegador.find_element(
            By.CSS_SELECTOR,
            '#mobile-filter-content > div > div > div:nth-child(6) > div.flex-1.px-4.py-4 > div > div:nth-child(1) > div > input'
        )
        preco_minimo.send_keys(preco_menor)
        preco_maximo = self.navegador.find_element(
            By.XPATH,
            '//*[@id="mobile-filter-content"]/div/div/div[6]/div[2]/div/div[2]/div/input'
        )
        preco_maximo.send_keys(preco_maior)
        self.navegador.find_element(
            By.XPATH,
            '//*[@id="mobile-filter-content"]/div/div/div[6]/div[2]/div/button'
        ).click()

    def __executar_rolagem(self, chave: int):
        """Executa a barra de rolagem

        Args:
            chave (int): número do loop
        """
        self.navegador.execute_script(f'window.scroll(0, {chave * 90})')

    def coletar_dados_produtos(self) -> Generator[Tuple[str, int, float, str, str], None, None]:
        """Método para retornar os dados de cada produto por vez

        Yields:
            Generator[Tuple[str, str, str, str, str], None, None]: Um gerador de produtos
        """
        try:
            lista_produtos = self.navegador.find_elements(
                By.CLASS_NAME,
                'new-product-thumb'
            )
            for chave, produto in enumerate(lista_produtos):
                nome = produto.find_element(
                    By.CLASS_NAME,
                    'css-1eaoahv-ellipsis'
                ).text
                codigo = produto.find_element(
                    By.CLASS_NAME,
                    'css-19qfvzb-new-product-thumb__product-code'
                ).text
                preco = produto.find_element(
                    By.CLASS_NAME,
                    'css-m39r81-price-tag__price'
                ).text
                url_imagem = produto.find_element(
                    By.CLASS_NAME,
                    'css-1n5vdld-product-thumbnail__image'
                ).get_attribute('src')
                url_produto = produto.find_element(
                    By.TAG_NAME,
                    'a'
                ).get_attribute('href')
                yield nome, int(codigo.replace('Cód. ', '')), float(preco.replace('R$', '')), url_imagem, url_produto, self.__data_extracao
                self.__executar_rolagem(chave=chave)
        except NoSuchElementException as msg:
            logger.error(f'Não encontrou id: {msg} ')

    def executar_paginacao(self) -> bool:
        """Execcuta a páginação

        Returns:
            bool: Verdadeiro caso a páginação seja feita com sucesso, falso caso contrário
        """
        try:
            self.navegador.find_element(
                By.CLASS_NAME, 'glyph-arrow-right').click()
            return True
        except:
            return False

    def fechar_nagegador(self):
        self.navegador.close()
