from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.services.webscarpingbase import WebScrapingBase
from src.pacote_log.config__log import logger
from typing import (Generator, Dict, Optional)
from datetime import datetime
from enums.enum_empresa import Empresa


class WebScrapingTelhaNorte(WebScrapingBase):

    def __init__(self) -> None:
        self.__empresa = Empresa.TELHA_NORTE
        super().__init__(url='https://www.telhanorte.com.br/')

    def fazer_pesquisa_produto(self, termo_busca: str) -> None:
        busca_produto = self.navegador.find_element(
            By.CLASS_NAME, 'vtex-styleguide-9-x-input')

        busca_produto.send_keys(termo_busca, Keys.ENTER)

    def executar_paginacao(self) -> Optional[bool]:
        while True:
            try:
                self.navegador.find_element(
                    By.XPATH, '/html/body/div[2]/div/div[1]/div/div[1]/div/div[4]/section/div[2]/div/div[3]/div/a/div'
                ).click()
            except Exception as E:
                break

    def coletar_dados_produtos(self) -> Generator[Dict[str, str | int | float], None, None]:
        nome_produtos = self.navegador.find_elements(
            By.CLASS_NAME, 'vtex-product-summary-2-x-productBrand')
        precos = self.navegador.find_elements(
            By.CLASS_NAME, 'telhanorte-telha-store-app-1-x-best-price-price-vitrini')
        url_produtos = self.navegador.find_elements(
            By.CLASS_NAME, 'vtex-product-summary-2-x-clearLink'
        )
        url_imagens = self.navegador.find_elements(
            By.XPATH, '//section/a/article/div[2]/img')

        for produto, preco, url_produto, url_imagem in zip(nome_produtos, precos, url_produtos, url_imagens):
            yield {
                'EMPRESA': self.__empresa.name,
                'CODIGO_EMPRESA':  self.__empresa.value,
                'NOME_PRODUTO': produto.text,
                'CODIGO': int(url_produto.get_attribute('href').split('-')[-1].replace('/p', '')),
                'PRECO': float(preco.text.replace(',', '.').strip()),
                'URL_IMG':  url_imagem.get_attribute('src'),
                'URL_PRODUTO': url_produto.get_attribute('href'),
                'DATA_EXTRACAO':  self._data_atual()

            }
