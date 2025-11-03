import sys
import logging
from django.core.checks import register, Error
from django.conf import settings
from govapp.apps.publisher.models.geoserver_roles_groups import GeoServerGroup


logger = logging.getLogger(__name__)


@register()
def geoserver_group_check(app_configs, **kwargs):
    errors = []

    def perform_geoserver_group_check():
        for group_name in settings.CUSTOM_GEOSERVER_GROUPS:
            try:
                group, created = GeoServerGroup.objects.get_or_create(name=group_name)
                if created:
                    logger.info(f"GeoServerGroup: [{group}] has been created.")
                else:
                    logger.debug(f"GeoServerGroup: [{group}] already exists.")
            except Exception as e:
                msg = f"{e}, GeoServerGroup: [{group_name}]"
                errors.append(Error(msg))
                logger.error(msg)

    if sys.argv and ('migrate' in sys.argv or 'makemigrations' in sys.argv or 'showmigrations' in sys.argv or 'sqlmigrate' in sys.argv):
        pass
    else:
        perform_geoserver_group_check()

    return errors