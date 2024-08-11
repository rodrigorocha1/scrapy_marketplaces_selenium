from abc import abstractmethod, ABC
from typing import (
    Generator,
    Tuple
)


class IWebScraping(ABC):
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
    def selecionar_faixa_preco(self, preco_menor: float, preco_maior: float):
        """Método para selecionar a faixa de preço

        Args:
            preco_menor (float): preço menor do produto
            preco_maior (float): preço maior do produto
        """
        pass

    @abstractmethod
    def coletar_dados_produtos(self) -> Generator[Tuple[str, str, str, str, str], None, None]:
        """Método para retornar os dados de cada produto por vez

        Yields:
            Generator[Tuple[str, str, str, str, str], None, None]: Um gerador de produtos
        """
        pass

    @abstractmethod
    def executar_paginacao(self) -> bool:
        """Execcuta a páginação

        Returns:
            bool: Verdadeiro caso a páginação seja feita com sucesso, falso caso contrário
        """
        pass
