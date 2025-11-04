import sys
import logging
from django.contrib.auth.models import Group
from django.core.checks import register, Error
from django.conf import settings
from govapp.apps.publisher.models.geoserver_roles_groups import GeoServerGroup, GeoServerRole, GeoServerUserGroupService
from govapp.apps.publisher.models.publish_channels import GeoServerPublishChannel


logger = logging.getLogger(__name__)


@register()
def geoserver_group_check(app_configs, **kwargs):
    errors = []

    def are_migrations_running():
        '''
        Checks whether the app was launched with the migration-specific params
        '''
        # return sys.argv and ('migrate' in sys.argv or 'makemigrations' in sys.argv)
        return sys.argv and ('migrate' in sys.argv or 'makemigrations' in sys.argv or 'showmigrations' in sys.argv or 'sqlmigrate' in sys.argv)


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
    
    def perform_group_check():
        for group_name in settings.CUSTOM_GROUPS:
            try:
                group, created = Group.objects.get_or_create(name=group_name)
                if created:
                    logger.info(f"Group: [{group_name}] has been created.")
                else:
                    logger.info(f"Group: [{group_name}] already exists.")

            except Exception as e:
                msg = f'{e}, Group name: [{group_name}]'
                errors.append(Error(msg))
                logger.error(msg)

    def perform_geoserver_default_role_check():
        for role_name in settings.DEFAULT_ROLES_IN_GEOSERVER:
            try:
                role, created = GeoServerRole.objects.get_or_create(name=role_name)
                if created or not role.default:
                    role.default = True  # This role exists in the geoserver as a default role
                    role.save()
                    logger.info(f"GeoServerRole: [{role_name}] has been created or set default to True.")
                else:
                    logger.info(f"GeoServerRole: [{role_name}] already exists as a geoserver default role.")

            except Exception as e:
                msg = f'{e}, GeoServerRole name: [{role_name}]'
                errors.append(Error(msg))
                logger.error(msg)

    def perform_geoserver_usergroup_service_name_check():
        for ug_service_name in settings.GEOSERVER_USERGROUP_SERVICE_NAMES:
            try:
                service_name, created = GeoServerUserGroupService.objects.get_or_create(name=ug_service_name)
                if created:
                    logger.info(f"GeoServerUserGroupService: [{service_name}] has been created.")
                else:
                    logger.info(f"GeoServerUserGroupService: [{service_name}] already exists.")
            except Exception as e:
                msg = f'{e}, GeoServerUserGroupService: [{ug_service_name}]'
                errors.append(Error(msg))
                logger.error(msg)


    if are_migrations_running():
        pass
    else:
        perform_geoserver_group_check()
        perform_group_check()
        perform_geoserver_default_role_check()
        perform_geoserver_usergroup_service_name_check()

        # For bulk-updated data, if the 'active' field contains 'Null', set it to 'True'
        GeoServerPublishChannel.objects.filter(active__isnull=True).update(active=True)

    return errors
