"""Kaartdijin Boodja Publisher Django Application Cron Jobs."""


# Standard
import logging

# Third-Party
from django import conf
from django.core import management
import django_cron

from govapp.apps.publisher.models.publish_channels import GeoServerPublishChannel


# Logging
log = logging.getLogger(__name__)

class GeoServerSyncUsersCronJob(django_cron.CronJobBase):
    schedule = django_cron.Schedule(run_every_mins=conf.settings.GEOSERVER_SYNC_USERS_PERIOD_MINS)
    code = "govapp.accounts.geoserver_sync_users_cron_job"

    def do(self) -> None:
        log.info("Sync geoserver users cron job triggered, running...")

        # Run Management Command
        management.call_command("sync_users")


class ItassetsUsersSyncCronJob(django_cron.CronJobBase):
    schedule = django_cron.Schedule(run_every_mins=conf.settings.SYNC_ITASSETS_USERS_PERIOD_MINS)
    code = "govapp.accounts.sync_itassets_users"

    def do(self) -> None:
        log.info("Sync itassets users cron job triggered, running...")

        # Run Management Command
        management.call_command("sync_itassets_users")

