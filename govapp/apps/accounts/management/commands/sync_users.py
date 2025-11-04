from django.core.management.base import BaseCommand
from govapp.apps.publisher.models.geoserver_pools import GeoServerPool


class Command(BaseCommand):
    help = 'Synchronize users, roles, and groups with GeoServer.'

    def handle(self, *args, **options):
        geoservers = GeoServerPool.objects.filter(enabled=True)
        for geoserver in geoservers:
            # Sync relations between users and groups, and users and roles
            geoserver.sync_users_groups_users_roles()

            # Sync relations between roles with grous ###
            geoserver.sync_groups_roles()

            # Cleanup users
            geoserver.cleanup_users()
