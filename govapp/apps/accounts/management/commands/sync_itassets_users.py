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


class Command(BaseCommand):
    """
    Ref: https://github.com/dbca-wa/ledger/blob/master/ledger/accounts/management/commands/sync_itassets_users.py
    """
    help = 'Sync Itassets Users.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            # --- START: Sync itassets users (email with @dbca.wa.gov.au) with UserModel --- #
            logger.info("Syncing Itassets Users ...")
            ITASSETS_USER_JSON_URL = decouple.config('ITASSETS_USER_JSON_URL', default=[])
            ITASSETS_USER_LOGIN = decouple.config('ITASSETS_USER_LOGIN', default='')
            ITASSETS_USER_TOKEN = decouple.config('ITASSETS_USER_TOKEN', default='')
            url = ITASSETS_USER_JSON_URL
            resp = requests.get(url, data ={}, auth=(ITASSETS_USER_LOGIN, ITASSETS_USER_TOKEN))
            data = json.loads(codecs.decode(resp.text.encode(), 'utf-8-sig'))
            row = 0
            noaccount = 0
            updatedaccount = 0
            for user in data:
                ed = str(user["email"]).split("@")
                email_domain = ed[1]
                if email_domain in settings.DEPT_DOMAINS:
                    email = user['email'].lower()
                    first_name = user['given_name']
                    last_name = user['surname']
                    if first_name is None or first_name == '':
                        first_name = "No First Name"
                    if last_name is None or last_name == '':
                        last_name = "No Last Name"

                    UserModel = auth.get_user_model()
                    user_objects = UserModel.objects.filter(email=email)
                    if user_objects.count() > 0:
                        existing_user = user_objects[0]
                        existing_user.first_name = first_name
                        existing_user.last_name = last_name
                        existing_user.is_staff = True
                        existing_user.save()
                        logger.info(f"User: [{existing_user}] has been updated.")
                        updatedaccount = updatedaccount + 1
                    else:
                        new_user = UserModel.objects.create_user(
                            username=email,
                            email=email,
                            first_name=first_name,
                            last_name=last_name,
                            is_staff=True,
                        )
                        logger.info(f"User: [{new_user}] has been created.")
                        noaccount = noaccount + 1
                    row = row + 1
            logger.info(f"Successfully Completed Itassets Users Import.  Created Users: {str(noaccount)}.  Updated Users: {str(updatedaccount)}")
            # --- END --- #

            # --- START: Add users (email with @dbca.wa.gov.au) to the 'DBCA_Users' Group --- #
            logger.info("Starting batch process to associate DBCA users with the 'DBCA_Users' GeoServer group...")
            default_group_name = settings.GEOSERVER_GROUP_DBCA_USERS
            target_domain = f"@{settings.DEPT_DOMAINS}"

            try:
                # Step 1: Get the target GeoServerGroup object.
                # Using get() will raise a DoesNotExist exception if not found, which is handled below.
                target_group = GeoServerGroup.objects.get(name=default_group_name)

                # Step 2: Get a queryset of all active users with the specified email domain.
                users_to_link = UserModel.objects.filter(
                    is_active=True,
                    email__endswith=target_domain
                )

                # Step 3: Call the manager method to perform the bulk link.
                if users_to_link.exists():
                    # This single line handles the creation of all necessary links.
                    linked_count = GeoServerGroupUser.objects.link_users_to_group(users_to_link, target_group)
                    logger.info(
                        f"Successfully processed {users_to_link.count()} users for the [{default_group_name}] group. "
                        f"({linked_count} links were created or confirmed to exist)."
                    )
                else:
                    logger.info(f"No active users found with the domain [{target_domain}]. No group associations were made.")

            except GeoServerGroup.DoesNotExist:
                logger.error(
                    f"The required GeoServer group [{default_group_name}] was not found in the database. "
                    "Skipping user-group association. Please ensure the group exists."
                )
            # --- END --- #

        except Exception as e:
            time_error = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            logger.error(f"Itassets Users Sync Error: {e}")
            emails.SyncItassetsUsersEmail().send_to(
                *utils.all_administrators(),  # All administrators
                context = {
                    "ad_error": e,
                    "time_error": time_error,
                },
            )
