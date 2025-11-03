import sys
import logging
from django.core.checks import register, Error, Warning
from django.conf import settings
# from ledger_api_client.managed_models import SystemGroup

logger = logging.getLogger(__name__)


@register()
def geoserver_group_check(app_configs, **kwargs):
    errors = []

    def perform_geoserver_group_check():
        logger.debug('aho')
        # for group_name in settings.GROUP_NAME_CHOICES:
        #     try:
        #         group, created = SystemGroup.objects.get_or_create(name=group_name)
        #         if created:
        #             logger.info(f"SystemGroup: [{group}] has been created.")
        #         else:
        #             logger.debug(f"SystemGroup: [{group}] already exists.")
        #     except Exception as e:
        #         msg = f"{e}, SystemGroup: [{group_name}]"
        #         errors.append(Error(msg))
        #         logger.error(msg)

    if sys.argv and ('migrate' in sys.argv or 'makemigrations' in sys.argv or 'showmigrations' in sys.argv or 'sqlmigrate' in sys.argv):
        pass
    else:
        perform_geoserver_group_check()

    return errors