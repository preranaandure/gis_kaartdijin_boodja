from django.core.management.base import BaseCommand
from django.contrib import auth
from django.conf import settings
from datetime import datetime
import requests
import json
import codecs
import decouple
import logging
from govapp.apps.accounts import utils, emails
from govapp.apps.publisher.models.geoserver_roles_groups import GeoServerGroup, GeoServerGroupUser


logger = logging.getLogger(__name__)
UserModel = auth.get_user_model()

class Command(BaseCommand):
    """
    Ref: https://github.com/dbca-wa/ledger/blob/master/ledger/accounts/management/commands/sync_itassets_users.py
    """
    help = 'Sync Itassets Users.'

    def _sync_users(self, itassets_data):
        """
        Handles the core logic of creating and updating users in bulk.
        """
        target_domain = settings.DEPT_DOMAINS
        if not target_domain:
            logger.warning("DEPT_DOMAINS setting is empty. No users will be synced.")
            return 0, 0

        # --- Step 1: Fetch all existing users from the database ONCE. ---
        # This dictionary provides instant lookup by email.
        existing_users_map = {
            user.email: user
            for user in UserModel.objects.filter(email__endswith=f"@{target_domain}")
        }
        logger.info(f"Fetched {len(existing_users_map)} existing users from the database for domain [{target_domain}].")

        users_to_create = []
        users_to_update = []
        
        # --- Step 2: Process Itassets data in memory, without touching the DB. ---
        for user_data in itassets_data:
            email = user_data.get("email", "").lower()
            # Correctly check if the email ends with the target domain.
            if not email.endswith(f"@{target_domain}"):
                continue  # Skip users with a non-department domain.

            first_name = user_data.get("given_name") or "No First Name"
            last_name = user_data.get("surname") or "No Last Name"
            
            if email in existing_users_map:
                # --- UPDATE path ---
                user = existing_users_map[email]
                if (user.first_name != first_name or user.last_name != last_name or not user.is_staff):
                    user.first_name = first_name
                    user.last_name = last_name
                    user.is_staff = True
                    users_to_update.append(user)
            else:
                # --- CREATE path ---
                users_to_create.append(
                    UserModel(
                        username=email,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        is_staff=True,
                    )
                )

        # --- Step 3: Perform bulk database operations ONCE. ---
        if users_to_create:
            UserModel.objects.bulk_create(users_to_create)
            logger.info(f"Created {len(users_to_create)} new users.")

        if users_to_update:
            UserModel.objects.bulk_update(users_to_update, ["first_name", "last_name", "is_staff"])
            logger.info(f"Updated {len(users_to_update)} existing users.")

        return len(users_to_create), len(users_to_update)

    def _associate_users_with_group(self):
        """Handles associating users with the default group."""
        default_group_name = settings.GEOSERVER_GROUP_DBCA_USERS
        target_domain_suffix = f"@{settings.DEPT_DOMAINS}"

        try:
            target_group = GeoServerGroup.objects.get(name=default_group_name)
            users_to_link = UserModel.objects.filter(is_active=True, email__endswith=target_domain_suffix)

            if users_to_link.exists():
                linked_count = GeoServerGroupUser.objects.link_users_to_group(users_to_link, target_group)
                logger.info(
                    f"Successfully processed {users_to_link.count()} users for the [{default_group_name}] group. "
                    f"({linked_count} links were created or confirmed)."
                )
            else:
                logger.info(f"No active users found with the domain suffix [{target_domain_suffix}].  No associations made.")

        except GeoServerGroup.DoesNotExist:
            logger.error(f"Required group [{default_group_name}] not found.  Skipping association.")

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            logger.info("Starting Itassets Users Sync command...")
            
            # Fetch data from Itassets
            ITASSETS_USER_JSON_URL = decouple.config("ITASSETS_USER_JSON_URL", default='')
            ITASSETS_USER_LOGIN = decouple.config("ITASSETS_USER_LOGIN", default='')
            ITASSETS_USER_TOKEN = decouple.config("ITASSETS_USER_TOKEN", default='')
            resp = requests.get(ITASSETS_USER_JSON_URL, auth=(ITASSETS_USER_LOGIN, ITASSETS_USER_TOKEN))
            resp.raise_for_status()
            data = json.loads(codecs.decode(resp.content, "utf-8-sig"))

            # --- Part 1: Sync users ---
            created_count, updated_count = self._sync_users(data)
            logger.info(f"User sync complete. Created: {created_count}, Updated: {updated_count}.")

            # --- Part 2: Associate users with group ---
            self._associate_users_with_group()

            logger.info("Itassets Users Sync command finished successfully.")

        except Exception as e:
            time_error = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            logger.error(f"An error occurred during Itassets Users Sync: {e}", exc_info=True)
            emails.SyncItassetsUsersEmail().send_to(
                *utils.all_administrators(),
                context={"ad_error": e, "time_error": time_error},
            )
