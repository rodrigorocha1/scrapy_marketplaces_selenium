from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    InvalidElementStateException
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from src.services.webscarpingbase import WebScrapingBase
from src.pacote_log.config__log import logger
from typing import (Generator, Dict, Optional)
from enums.enum_empresa import Empresa
from time import sleep


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
            logger.error(f'Não encontrou elemento: {msg} ')
        except ElementNotInteractableException:
            logger.error('Elemento não pode ser interagido')
        except InvalidElementStateException:
            logger.error('Falha na operação de enviar teclas')
        except Exception:
            logger.error('Falha Geral')

    def clicar_cookie(self):
        try:
            WebDriverWait(self.navegador, 20).until(
                EC.presence_of_element_located(
                    (By.ID,
                     'onetrust-accept-btn-handler'))).click()
        except NoSuchElementException as msg:
            logger.error(f'Não encontrou elemento: {msg} ')
        except TimeoutException as msg:
            logger.error('Tempo esgotado')
        except ElementNotInteractableException:
            logger.error('Elemento não pode ser interagido')
        except ElementClickInterceptedException:
            logger.error('Falha de clique')
        except Exception:
            logger.error('Falha Geral')

    def __esperar_elemento(self):
        """Espera a tag do css antes de fazer as pesquisas
        """

        try:
            WebDriverWait(self.navegador, 20).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '#mobile-filter-content > div > div > div:nth-child(6) > div.flex-1.px-4.py-4 > div > div:nth-child(1) > div > input'
                    )
                )
            )

        except TimeoutException:
            logger.error('Tempo Esgotado')
        except Exception:
            logger.error('Falha Geral')

    def __selecionar_faixa_preco(self):
        """Método para selecionar a faixa de preço


        """
        try:
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
            preco_maximo.send_keys(self.__preco_maior, Keys.ENTER)
        except NoSuchElementException as msg:
            logger.error(f'Não encontrou elemento: {msg} ')
            exit()
        except ElementNotInteractableException:
            logger.error('Elemento não pode ser interagido')
            exit()
        except InvalidElementStateException:
            logger.error('Falha na operação de enviar teclas')
            exit()
        except Exception:
            logger.error('Falha Geral')
            exit()

    def __executar_rolagem(self):
        """Executa a barra de rolagem


        """
        for i in range(1, 60):
            self.navegador.execute_script(f'window.scroll(1, {i * 60})')

    def __aguardar_listagem_produtos(self):
        try:
            WebDriverWait(self.navegador, 30).until(
                EC.presence_of_element_located(
                    (
                        By.CLASS_NAME,
                        'new-product-thumb'
                    )
                )
            )
            sleep(3)
        except TimeoutException:
            logger.error('Tempo Esgotado')
            exit()
        except Exception:
            logger.error('Falha Geral')
            exit()

    def coletar_dados_produtos(self) -> Generator[Dict[str, str | int | float], None, None]:
        """Método para retornar os dados de cada produto por vez

        Yields:
            Generator[Dict[str, str | int | float], None, None]: Um gerador de produtos
        """
        # self.clicar_cookie()
        self.__selecionar_faixa_preco()
        paginacao = True
        while paginacao:
            try:

                self.__aguardar_listagem_produtos()
                self.__executar_rolagem()
                nome_produtos = self.navegador.find_elements(
                    By.CLASS_NAME,
                    'css-1eaoahv-ellipsis'
                )
                codigos_produtos = self.navegador.find_elements(
                    By.CLASS_NAME,
                    'css-19qfvzb-new-product-thumb__product-code'
                )
                precos_produto = self.navegador.find_elements(
                    By.CLASS_NAME,
                    'css-m39r81-price-tag__price'
                )
                url_imagens = self.navegador.find_elements(
                    By.CLASS_NAME,
                    'css-1n5vdld-product-thumbnail__image'
                )
                url_produtos = self.navegador.find_elements(
                    By.CLASS_NAME, 'css-1c4absn-new-product-thumb__title')

                for nome_produto, codigo_produto, preco_produto, url_imagem, url_produto in zip(nome_produtos, codigos_produtos, precos_produto, url_imagens, url_produtos):

                    yield {
                        'EMPRESA': self.__empresa.name,
                        'CODIGO_EMPRESA':  self.__empresa.value,
                        'NOME_PRODUTO': nome_produto.text,
                        'CODIGO': int(codigo_produto.text.replace('Cód. ', '')
                                      ),
                        'PRECO': float(preco_produto.text.replace('R$ ', '').replace('.', '').replace(',', '.').strip()),
                        'URL_IMG':  url_imagem.get_attribute('src'),
                        'URL_PRODUTO': url_produto.get_attribute('href'),
                        'DATA_EXTRACAO':  self._data_atual()

                    }
                paginacao = self.executar_paginacao()

            except NoSuchElementException as msg:
                logger.error(f'Não encontrou id: {msg} ')
                exit()
            except Exception:
                logger.error('Falha Geral')
                exit()

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
