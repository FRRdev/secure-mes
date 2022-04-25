import random

from src.neuro_base.neuro_config import ConfigNNT
from typing import List, Optional


class Perceptron:
    """ Model of single Perceptron for implementation TMP
    """

    def __init__(self):
        self.__weights: List = [0 for _ in range(ConfigNNT.N)]
        self.__output: Optional[int] = None
        self.__inputs: List = [0 for _ in range(ConfigNNT.N)]
        self.generate_random_weights()

    def get_output(self, a_inputs: List) -> int:
        self.__inputs = a_inputs
        self.__output = 0
        for i in range(ConfigNNT.N):
            self.__output += self.__inputs[i] * self.__weights[i]
        self.__output = 1 if self.__output >= 0 else -1
        return self.__output

    def generate_random_weights(self) -> None:
        for i in range(ConfigNNT.N):
            self.__weights[i] = ConfigNNT.L - random.randint(1, 2 * ConfigNNT.L)

    def actualize_weight(self, output_tpm: int) -> None:
        if output_tpm == self.__output:
            for i in range(ConfigNNT.N):
                self.__weights[i] += self.__output * self.__inputs[i]
                if abs(self.__weights[i]) > ConfigNNT.L:
                    self.__weights[i] = ConfigNNT.L
                elif self.__weights[i] < -ConfigNNT.L:
                    self.__weights[i] = -ConfigNNT.L

    def get_weights_of_perceptron(self):
        return self.__weights


class TPM:
    """ Model of TPM consists of several Perceptron
    """
    __output: int

    def __init__(self, name: str, list_perceptron: List[Perceptron]):
        self.__name = name
        self.__perceptron = list_perceptron

    def get_output(self, a_inputs: List[List]) -> int:
        self.__output = 1
        for i in range(ConfigNNT.K):
            self.__output *= self.__perceptron[i].get_output(a_inputs[i])
        return self.__output

    def synchronize(self, output_other_tpm) -> None:
        if self.__output != output_other_tpm:
            return
        for i in range(ConfigNNT.K):
            self.__perceptron[i].actualize_weight(self.__output)

    @property
    def weights(self):
        return [p.get_weights_of_perceptron() for p in self.__perceptron]

    def print_tmp_weights(self) -> None:
        list_of_tmp_weights = [p.get_weights_of_perceptron() for p in self.__perceptron]
        print(f'Сеть {self.__name} имеет веса => {list_of_tmp_weights}\n')
