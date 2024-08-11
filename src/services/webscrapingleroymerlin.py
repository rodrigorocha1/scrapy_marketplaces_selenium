from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.services.webscarpingbase import WebScrapingBase


class WebScrapingLeroyMerling(WebScrapingBase):

    def __init__(self) -> None:
        super().__init__()

    def fazer_pesquisa_produto(self, termo_busca: str) -> None:
        busca_produto = self.navegador.find_element(
            By.ID, '@autocomplete-quicksearch-input')
        busca_produto.send_keys(termo_busca)

    def __esperar_elemento(self):
        WebDriverWait(self.navegador, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 '#mobile-filter-content > div > div > div:nth-child(6) > div.flex-1.px-4.py-4 > div > div:nth-child(1) > div > input')))

    def clicar_botao_pesquisa(self) -> None:
        self.navegador.find_element(
            By.XPATH,
            '/html/body/header/div[2]/div/div[1]/form/div/div[1]/div/div/button'
        ).click()

    def selecionar_faixa_preco(self, preco_menor: float, preco_maior: float):
        self.__esperar_elemento()
        preco_minimo = self.navegador.find_element(
            By.CSS_SELECTOR,
            '#mobile-filter-content > div > div > div:nth-child(6) > div.flex-1.px-4.py-4 > div > div:nth-child(1) > div > input')
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

    def coletar_dados_produtos(self):
        lista_produtos = self.navegador.find_elements(
            By.CLASS_NAME,  'new-product-thumb')
        for chave, produto in enumerate(lista_produtos):
            nome = produto.find_element(
                By.CLASS_NAME, 'css-1eaoahv-ellipsis').text
            codigo = produto.find_element(
                By.CLASS_NAME, 'css-19qfvzb-new-product-thumb__product-code').text
            preco = produto.find_element(
                By.CLASS_NAME, 'css-m39r81-price-tag__price').text
            url_imagem = produto.find_element(
                By.CLASS_NAME, 'css-1n5vdld-product-thumbnail__image').get_attribute('src')
            url_produto = produto.find_element(
                By.TAG_NAME, 'a').get_attribute('href')
            self.navegador.execute_script(f'window.scroll(0, {chave * 80})')

    def executar_paginacao(self) -> bool:
        try:
            self.navegador.find_element(
                By.CLASS_NAME, 'glyph-arrow-right').click()
            return True
        except:
            return False
