from abc import abstractmethod, ABC
from typing import (
    Generator,
    Dict
)


class IWebScraping(ABC):
    @abstractmethod
    def abrir_navegador(self, url: str):
        """Método para abrir o navegador e conectar na url

        Args:
            url (str): url do site

        """

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
            Generator[Tuple[str, str, str, str, str], None, None]: Um gerador de produtos
        """
        pass

    @abstractmethod
    def executar_paginacao(self) -> bool | None:
        """Execcuta a páginação

        Returns:
            bool: Verdadeiro caso a páginação seja feita com sucesso, falso caso contrário
        """
        pass

    @abstractmethod
    def fechar_nagegador(self):
        pass
