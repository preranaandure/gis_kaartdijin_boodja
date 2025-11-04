import json
import logging
from django.forms import ValidationError
import reversion

from django.db import models
from django.contrib import auth

from govapp import settings
from govapp.apps.publisher.models.workspaces import Workspace
from govapp.common import mixins


# Logging
log = logging.getLogger(__name__)


@reversion.register()
class GeoServerUserGroupService(mixins.RevisionedMixin):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


@reversion.register()
class GeoServerRole(mixins.RevisionedMixin):
    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_role = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_roles')
    default = models.BooleanField(default=False, verbose_name='Default at geoserver')

    class Meta:
        verbose_name = "GeoServer Role"
        verbose_name_plural = "GeoServer Roles"

    def clean(self):
        """Ensure parent_role does not refer to itself."""
        if self.parent_role == self:
            raise ValidationError("Parent role cannot be self.")

    def save(self, *args, **kwargs):
        """Override save method to enforce clean validation."""
        self.full_clean()  # Validate the object
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class GeoServerGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('geoserver_roles')


def get_custom_usergroup_service():
    return GeoServerUserGroupService.objects.get(name=settings.GEOSERVER_USERGROUP_SERVICE_NAME_CUSTOM)


@reversion.register()
class GeoServerGroup(mixins.RevisionedMixin):
    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    geoserver_roles = models.ManyToManyField(GeoServerRole, through='GeoServerGroupRole', related_name='geoserver_groups')
    geoserver_usergroup_service = models.ForeignKey(GeoServerUserGroupService, null=True, blank=True, on_delete=models.CASCADE, default=get_custom_usergroup_service)
    objects = GeoServerGroupManager()

    class Meta:
        verbose_name = "GeoServer Group"
        verbose_name_plural = "GeoServer Groups"

    def __str__(self) -> str:
        return self.name

    @property
    def users(self):
        geoserver_group_users = GeoServerGroupUser.objects.filter(geoserver_group=self)
        users = [geoserver_group_user.user for geoserver_group_user in geoserver_group_users]
        return users


@reversion.register()
class GeoServerGroupRole(mixins.RevisionedMixin):
    geoserver_group = models.ForeignKey(GeoServerGroup, null=True, blank=True, on_delete=models.CASCADE)
    geoserver_role = models.ForeignKey(GeoServerRole, null=True, blank=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "GeoServer GroupRole"
        verbose_name_plural = "GeoServer GroupRoles"
    

@reversion.register()
class GeoServerRolePermission(mixins.RevisionedMixin):
    geoserver_role = models.ForeignKey(GeoServerRole, null=True, blank=True, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, null=True, blank=True, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "GeoServer RolePermission"
        verbose_name_plural = "GeoServer RolePermissions"
    
    def __str__(self) -> str:
        return f'{self.workspace},{self.geoserver_role}, r:{self.read}, w:{self.write}, a:{self.admin}'

    @staticmethod
    def _add_or_update_rule(rules, key, value):
        """
        Add a new key-value pair to the dictionary. If the key already exists,
        append the new value to the existing value, separated by a comma.

        :param rules: Dictionary to update
        :param key: Key to add or update
        :param value: Value to add or append
        """
        if key in rules:
            # Append the new value to the existing value, separated by a comma
            rules[key] = f"{rules[key]},{value}"
        else:
            # Add the new key-value pair to the dictionary
            rules[key] = value
        
        return rules

    @staticmethod
    def get_rules():
        from django.db.models import Prefetch
        CREATE_PERMISSION_FOR_LAYER = False  # Considering the relationship from the current GeoServerRole model to other models, it seems that layer permission is not being taken into account.

        # Prefetch related data to minimize database hits
        permissions = GeoServerRolePermission.objects.filter(active=True).select_related(
            'geoserver_role',
            'workspace'
        ).prefetch_related(
            Prefetch('workspace__publish_channels__publish_entry__catalogue_entry')
        )
        
        rules = {}
        log.info(f'Permissions in the database: [{permissions}]')
        for perm in permissions:
            if perm.workspace:
                # Rules for workspaces
                if perm.read:
                    rules = GeoServerRolePermission._add_or_update_rule(rules, f"{perm.workspace.name}.*.r", perm.geoserver_role.name)
                if perm.write:
                    rules = GeoServerRolePermission._add_or_update_rule(rules, f"{perm.workspace.name}.*.w", perm.geoserver_role.name)
                if perm.admin:
                    rules = GeoServerRolePermission._add_or_update_rule(rules, f"{perm.workspace.name}.*.a", perm.geoserver_role.name)

                if CREATE_PERMISSION_FOR_LAYER:
                    # Rules for layers
                    for geoserver_publish_channel in perm.workspace.publish_channels.all():
                        catalogue_entry = geoserver_publish_channel.publish_entry.catalogue_entry if geoserver_publish_channel.publish_entry and geoserver_publish_channel.publish_entry.catalogue_entry else None
                        if catalogue_entry:
                            log.info(f'Catalogue entry (layer): [{catalogue_entry}] found for the publish_channel: [{geoserver_publish_channel}] under the workspace: [{perm.workspace}].')
                            if perm.read:
                                rules = GeoServerRolePermission._add_or_update_rule(rules, f"{perm.workspace.name}.{catalogue_entry.name}.r", perm.geoserver_role.name)
                            if perm.write:
                                rules = GeoServerRolePermission._add_or_update_rule(rules, f"{perm.workspace.name}.{catalogue_entry.name}.w", perm.geoserver_role.name)
                            # if perm.admin:  # <== No admin type for the layer acl
                            #     rules = GeoServerRolePermission._add_or_update_rule(rules, f"{perm.workspace.name}.{catalogue_entry.name}.a", perm.geoserver_role.name)

        log.info(f'Rules in the database: {json.dumps(rules, indent=4)}')
        return rules


UserModel = auth.get_user_model()


class GeoServerGroupUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user', 'geoserver_group',)
    
    def link_users_to_group(self, user_queryset, group_instance):
        """
        Links a queryset of users to a single group instance using a single bulk_create query.

        Args:
            user_queryset (QuerySet): A queryset of UserModel objects to be linked.
            group_instance (GeoServerGroup): The single GeoServerGroup object.

        Returns:
            int: The number of new links that were created or attempted.
        """
        # Build a list of the intermediate model instances to be created in memory.
        links_to_create = [
            self.model(user=user, geoserver_group=group_instance)
            for user in user_queryset
        ]

        # Use bulk_create for maximum efficiency if there are objects to create.
        if links_to_create:
            self.bulk_create(links_to_create, ignore_conflicts=True)
            
        return len(links_to_create)


class GeoServerGroupUser(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    geoserver_group = models.ForeignKey(GeoServerGroup, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GeoServerGroupUserManager()

    def __str__(self):
        return f"{self.user} - {self.geoserver_group}"

    class Meta:
        # This constraint is crucial for data integrity and for the
        # 'ignore_conflicts=True' flag in bulk_create to work correctly.
        unique_together = ('user', 'geoserver_group')


class GeoServerRoleUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user', 'geoserver_role',)

class GeoServerRoleUser(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    geoserver_role = models.ForeignKey(GeoServerRole, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GeoServerRoleUserManager()

    def __str__(self):
        return f"{self.user} - {self.geoserver_role}"