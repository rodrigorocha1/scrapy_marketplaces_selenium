from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from src.services.webscarpingbase import WebScrapingBase
from src.pacote_log.config__log import logger
from typing import (Generator, Dict, Optional)
from enums.enum_empresa import Empresa


class WebScrapingLeroyMerling(WebScrapingBase):

    def __init__(self,  preco_menor: float, preco_maior: float) -> None:
        self.__empresa = Empresa.LEROY_MERLIN
        self.__preco_menor = preco_menor
        self.__preco_maior = preco_maior
        super().__init__(url='https://www.leroymerlin.com.br/')

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
            busca_produto.send_keys(termo_busca, Keys.ENTER)
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

    def __selecionar_faixa_preco(self):
        """Método para selecionar a faixa de preço


        """
        self.__esperar_elemento()
        preco_minimo = self.navegador.find_element(
            By.CSS_SELECTOR,
            '#mobile-filter-content > div > div > div:nth-child(6) > div.flex-1.px-4.py-4 > div > div:nth-child(1) > div > input'
        )
        preco_minimo.send_keys(self.__preco_menor)
        preco_maximo = self.navegador.find_element(
            By.XPATH,
            '//*[@id="mobile-filter-content"]/div/div/div[6]/div[2]/div/div[2]/div/input'
        )
        preco_maximo.send_keys(self.__preco_maior)
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

    def coletar_dados_produtos(self) -> Generator[Dict[str, str | int | float], None, None]:
        """Método para retornar os dados de cada produto por vez

        Yields:
            Generator[Dict[str, str | int | float], None, None]: Um gerador de produtos
        """
        try:
            self.__selecionar_faixa_preco()
            lista_produtos = self.navegador.find_elements(
                By.CLASS_NAME,
                'new-product-thumb'
            )
            for chave, produto in enumerate(lista_produtos):

                yield {
                    'EMPRESA': self.__empresa.name,
                    'CODIGO_EMPRESA':  self.__empresa.value,
                    'NOME_PRODUTO': produto.find_element(
                        By.CLASS_NAME,
                        'css-1eaoahv-ellipsis'
                    ).text,
                    'CODIGO': int(produto.find_element(
                        By.CLASS_NAME,
                        'css-19qfvzb-new-product-thumb__product-code'
                    ).text.replace('Cód. ', '')
                    ),
                    'PRECO': float(produto.find_element(
                        By.CLASS_NAME,
                        'css-m39r81-price-tag__price'
                    ).text.replace('R$ ', '').replace(',', '.').strip()),
                    'URL_IMG':  produto.find_element(
                        By.CLASS_NAME,
                        'css-1n5vdld-product-thumbnail__image'
                    ).get_attribute('src'),
                    'URL_PRODUTO': produto.find_element(
                        By.TAG_NAME,
                        'a'
                    ).get_attribute('href'),
                    'DATA_EXTRACAO':  self._data_atual()

                }
                self.__executar_rolagem(chave=chave)
                if not self.executar_paginacao():
                    break
        except NoSuchElementException as msg:
            logger.error(f'Não encontrou id: {msg} ')

    def executar_paginacao(self) -> Optional[bool]:
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
