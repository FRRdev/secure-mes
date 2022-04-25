import random

from src.neuro_base.neuro_config import ConfigNNT
from src.neuro_base.tpm import TPM, Perceptron


def synchronize_tmp(name_tmp1: str, name_tpm_2: str, trace: bool = True):
    list_perceptron_for_first_tpm = [Perceptron() for _ in range(ConfigNNT.K)]
    list_perceptron_for_second_tpm = [Perceptron() for _ in range(ConfigNNT.K)]
    tpm1 = TPM(name_tmp1, list_perceptron_for_first_tpm)
    tpm2 = TPM(name_tpm_2, list_perceptron_for_second_tpm)
    if trace:
        tpm1.print_tmp_weights()
        tpm2.print_tmp_weights()
    iter_count = 1

    while tpm1.weights != tpm2.weights:
        generate_input = [
            [random.choice([1, -1]) for _ in range(ConfigNNT.N)] for i in range(ConfigNNT.K)
        ]
        output_tpm_1 = tpm1.get_output(generate_input)
        output_tpm_2 = tpm2.get_output(generate_input)
        tpm1.synchronize(output_tpm_2)
        tpm2.synchronize(output_tpm_1)
        iter_count += 1

    if trace:
        print(f'Сети синхронизированы спустя {iter_count} итераций\n')
        tpm1.print_tmp_weights()
        tpm2.print_tmp_weights()

    return tpm1.weights
