from src.mes_app.models import Key, CurrentKey
from src.profiles.models import SecureUser

from src.neuro_base.service import get_secret_key_for_message


def generate_neuro_key(first_user: SecureUser, second_user: SecureUser) -> None:
    """ Generate secret key and save in DB
    """
    neuro_key = get_secret_key_for_message('TMP_A', 'TPM_B', trace=False)
    key = Key.objects.create(value=neuro_key)
    CurrentKey.objects.create(first_user=first_user, second_user=second_user, key=key)
