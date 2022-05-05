from django.db.models import Count

from config.celery import app

from src.mes_app.models import CurrentKey, Key
from src.neuro_base.service import get_secret_key_for_message



@app.task
def refresh_all_current_key():
    for ck in CurrentKey.objects.all():
        neuro_key = get_secret_key_for_message('TMP_A', 'TPM_B', trace=False)
        key = Key.objects.create(value=neuro_key)
        ck.key = key
        ck.save()

@app.task
def delete_unused_keys():
    queryset = Key.objects.annotate(cnt=Count('key_messages')). \
        filter(current_data__isnull=True, cnt=0)
    queryset.delete()
