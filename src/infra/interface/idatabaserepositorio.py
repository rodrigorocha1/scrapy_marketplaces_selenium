from abc import (
    ABC,
    abstractmethod
)
from typing import Dict


class IDatabaseRepositorio(ABC):
    @abstractmethod
    def inserir_produtos(self, dados: Dict):
        pass
