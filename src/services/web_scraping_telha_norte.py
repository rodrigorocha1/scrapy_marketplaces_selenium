from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    InvalidElementStateException
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from src.services.webscarpingbase import WebScrapingBase
from src.pacote_log.config__log import logger
from typing import (Generator, Dict, Optional)
import re
from enums.enum_empresa import Empresa


class WebScrapingTelhaNorte(WebScrapingBase):

    def __init__(self) -> None:

        self.__empresa = Empresa.TELHA_NORTE
        super().__init__(url='https://www.telhanorte.com.br/')

    def fazer_pesquisa_produto(self, termo_busca: str) -> None:
        """Método para fazer pesquisa do produto

        Args:
            termo_busca (str): termo de busca Ex: Churrasqueira
        """
        try:
            busca_produto = self.navegador.find_element(
                By.CLASS_NAME, 'vtex-styleguide-9-x-input')

            busca_produto.send_keys(termo_busca, Keys.ENTER)

        except NoSuchElementException as msg:
            logger.error(f'Não encontrou elemento: {msg} ')
        except ElementNotInteractableException:
            logger.error('Elemento não pode ser interagido')
        except InvalidElementStateException:
            logger.error('Falha na operação de enviar teclas')
        except Exception:
            logger.error('Falha Geral')

    def executar_paginacao(self) -> Optional[bool]:
        """Método para executar páginação

        Returns:
            Optional[bool]: none ou false
        """
        while True:
            try:
                self.navegador.find_element(
                    By.XPATH, '/html/body/div[2]/div/div[1]/div/div[1]/div/div[4]/section/div[2]/div/div[3]/div/a/div'
                ).click()
            except Exception as E:
                break

    def coletar_dados_produtos(self) -> Generator[Dict[str, str | int | float], None, None]:
        """Método para recuperar os dados de produtos

        Yields:
            Generator[Dict[str, str | int | float], None, None]: dados dos produtos
        """
        try:
            self.executar_paginacao()
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
                    'PRECO': float(
                        re.sub(r'[^\d.,]', '', preco.text.replace(
                            '.', '').replace(',', '.').replace('R$', '').strip())

                    ),
                    'URL_IMG':  url_imagem.get_attribute('src'),
                    'URL_PRODUTO': url_produto.get_attribute('href'),
                    'DATA_EXTRACAO':  self._data_atual()

                }
        except NoSuchElementException as msg:
            logger.error(f'Não encontrou id: {msg} ')
        except Exception:
            logger.error('Falha Geral')
