from django.utils import timezone

from django.db import models


def delay_since_last_run(etl_name):
    '''Return time duration since the ETL etl_name was run for the last time
    '''
    log = EtlLog.objects.filter(etl_name=etl_name).first()
    if not log:
        return None
    return timezone.now() - log.last_run_at

def mark_as_run(etl_name):
    '''Mark the ETL etl_name as run just now'''
    log = EtlLog.objects.filter(etl_name=etl_name).first()
    if log:
        log.last_run_at = timezone.now()
        log.save()
    else:
        EtlLog.objects.create(
            etl_name=etl_name,
            last_run_at=timezone.now(),
        )


class EtlLog(models.Model):
    etl_name = models.TextField(unique=True)
    last_run_at = models.DateTimeField()
