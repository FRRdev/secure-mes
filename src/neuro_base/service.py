import random

from src.neuro_base.neuro_config import ConfigNNT
from src.neuro_base.tpm import TPM, Perceptron
from Crypto.Cipher import Blowfish


def get_secret_key_for_message(name_tmp1: str, name_tpm_2: str, trace: bool = True) -> str:
    """ Function for generating a secret key
    """
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

    weight_to_str = ''.join([str(elem) for item in tpm1.weights for elem in item])
    weight_to_str_correct = weight_to_str if len(weight_to_str) <= 56 else weight_to_str[:56]
    return weight_to_str_correct


def text_mod_8(text: bytes) -> bytes:
    """ Message length change function
    """
    while len(text) % 8 != 0:
        text += b' '
    return text


def encode_message(text: str, key: str) -> bytes:
    """ Encoding of the message using the algorithm Blowfish
    """
    key_to_bytes = bytes(key, encoding='utf-8')
    blow = Blowfish.new(key_to_bytes, Blowfish.MODE_ECB)
    text_to_bytes = bytes(text, encoding='utf-8')
    padded_text = text_mod_8(text_to_bytes)
    encrypted_text = blow.encrypt(padded_text)
    return encrypted_text

# secret = get_secret_key_for_message('Misha', 'Maks', False)
# print(secret)
# secret_to_str = ''.join([str(elem) for item in secret for elem in item])
# key = bytes('4524152532-124-543554245-4445-2-355-243-424535355-334514', encoding='utf-8')
#
#
#
#
# des = Blowfish.new(key, Blowfish.MODE_ECB)
# text = 'Hello'
# text = bytes(text, encoding='utf-8')
# padded_text = text_mod_8(text)
# print(padded_text)
# #
# encrypted_text = des.encrypt(padded_text)
# print(encrypted_text)
#
# data = des.decrypt(encrypted_text)
# print(data.decode('utf-8'))
