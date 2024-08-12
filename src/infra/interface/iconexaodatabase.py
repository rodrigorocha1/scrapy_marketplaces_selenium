from abc import (
    ABC,
    abstractmethod
)
from typing import Dict


class IconexaoDatabase(ABC):

    @abstractmethod
    def conectar_banco(self) -> bool:
        pass

    def desconectar_banco(self):
        pass

    @abstractmethod
    def inserir_produtos(self, dados: Dict):
        pass
