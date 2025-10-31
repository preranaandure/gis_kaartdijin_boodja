"""Kaartdijin Boodja Catalogue Django Application Notification Utilities."""


# Standard
import shutil

# Local
from govapp import gis, settings
from govapp.common import sharepoint
from govapp.apps.accounts import utils
from govapp.apps.catalogue import emails
from govapp.apps.catalogue import webhooks

# Typing
from typing import TYPE_CHECKING

# Type Checking
if TYPE_CHECKING:
    from govapp.apps.catalogue.models import catalogue_entries


def file_absorb_failure(file: str) -> None:
    """Sends notifications for a file absorption failure.

    Args:
        file (str): File that failed to absorb.
    """
    # Send Emails!
    emails.FileAbsorbFailEmail().send_to(
        *utils.all_administrators(),  # Send to all administrators
        context={"name": file},
    )


def catalogue_entry_creation(entry: "catalogue_entries.CatalogueEntry") -> None:
    """Sends notifications for a Catalogue Entry creation.

    Args:
        entry (catalogue_entries.CatalogueEntry): Catalogue Entry to notify for
    """
    # Send Emails
    emails.CatalogueEntryCreatedEmail().send_to(
        *utils.all_administrators(),  # All administrators
        context={"name": entry.name},
    )


def catalogue_entry_update_success(entry: "catalogue_entries.CatalogueEntry") -> None:
    """Sends notifications for a Catalogue Entry update success.

    Args:
        entry (catalogue_entries.CatalogueEntry): Catalogue Entry to notify for
    """

    editors = entry.editors.all()
    editors_list = []
    for ed in editors:
        editors_list.append(ed.user)
    # Send Emails
    emails.CatalogueEntryUpdateSuccessEmail().send_to(
        # *utils.all_administrators(),  # All administrators
        *editors_list,  # All editors
        *entry.email_notifications(manager="on_new_data").filter(active=True).all(),  # type: ignore[operator]
        *entry.email_notifications(manager="both").filter(active=True).all(),  # type: ignore[operator]
        context={"name": entry.name},
    )

    # Retrieve the File from Storage
    filepath = sharepoint.sharepoint_input().get_from_url(url=entry.active_layer.file)
    extension = filepath.suffix.lower()
    if extension not in ['.tif', '.tiff']:
        # Convert Layer to GeoJSON
        geojson = gis.conversions.to_geojson(
            filepath=filepath,
            layer=entry.metadata.name
        )

        if settings.WEBHOOK_ENABLED:
            # Send Webhook Posts
            webhooks.post_geojson(
                *entry.webhook_notifications(manager="on_new_data").all(),  # type: ignore[operator]
                geojson=geojson['full_filepath'],
            )

        # Delete local temporary copy of file if we can
        shutil.rmtree(filepath.parent, ignore_errors=True)


def catalogue_entry_update_failure(entry: "catalogue_entries.CatalogueEntry") -> None:
    """Sends notifications for a Catalogue Entry update failure.

    Args:
        entry (catalogue_entries.CatalogueEntry): Catalogue Entry to notify for
    """

    editors = entry.editors.all()
    editors_list = []
    for ed in editors:
        editors_list.append(ed.user)

    # Send Emails
    emails.CatalogueEntryUpdateFailEmail().send_to(
        *utils.all_administrators(),  # All administrators
        *editors_list,  # All editors
        context={"name": entry.name},
    )


def catalogue_entry_lock(entry: "catalogue_entries.CatalogueEntry") -> None:
    """Sends notifications for a Catalogue Entry lock.

    Args:
        entry (catalogue_entries.CatalogueEntry): Catalogue Entry to notify for
    """

    editors = entry.editors.all()
    editors_list = []
    for ed in editors:
        editors_list.append(ed.user)

    # Send Emails
    emails.CatalogueEntryLockedEmail().send_to(
        # *utils.all_administrators(),  # All administrators
        *editors_list,  # All editors
        *entry.email_notifications(manager="on_lock").filter(active=True).all(),  # type: ignore[operator]
        *entry.email_notifications(manager="both").filter(active=True).all(),  # type: ignore[operator]
        context={"name": entry.name},
    )
