"""Kaartdijin Boodja Publisher Django Application Notification Utilities."""


# Local
from govapp.apps.accounts import utils
from govapp.apps.publisher import emails

# Typing
from typing import TYPE_CHECKING

# Type Checking
if TYPE_CHECKING:
    from govapp.apps.publisher.models import publish_entries


def publish_entry_lock(entry: "publish_entries.PublishEntry") -> None:
    """Sends notifications for a Publish Entry lock.

    Args:
        entry (publish_entries.PublishEntry): Publish Entry to notify for
    """

    editors = entry.editors.all()
    editors_list = []
    for ed in editors:
        editors_list.append(ed.user)

    # Send Emails
    emails.PublishEntryLockedEmail().send_to(
        # *utils.all_administrators(),  # All administrators
        *editors_list,  # All editors
        *entry.email_notifications(manager="on_lock").filter(active=True).all(),  # type: ignore[operator]
        *entry.email_notifications(manager="both").filter(active=True).all(),  # type: ignore[operator]
        context={"name": entry.name},
    )


def publish_entry_publish_success(entry: "publish_entries.PublishEntry") -> None:
    """Sends notifications for a Publish Entry publish success.

    Args:
        entry (publish_entries.PublishEntry): Publish Entry to notify for
    """
    editors = entry.editors.all()
    editors_list = []
    for ed in editors:
        editors_list.append(ed.user)

    # Send Emails
    emails.PublishEntryPublishSuccessEmail().send_to(
        # *utils.all_administrators(),  # All administrators
        *editors_list,  # All editors
        *entry.email_notifications(manager="on_publish").filter(active=True).all(),  # type: ignore[operator]
        *entry.email_notifications(manager="both").filter(active=True).all(),  # type: ignore[operator]
        context={"name": entry.name},
    )


def publish_entry_publish_failure(entry: "publish_entries.PublishEntry") -> None:
    """Sends notifications for a Publish Entry publish failure.

    Args:
        entry (publish_entries.PublishEntry): Publish Entry to notify for
    """
    editors = entry.editors.all()
    editors_list = []
    for ed in editors:
        editors_list.append(ed.user)

    # Send Emails
    emails.PublishEntryPublishFailEmail().send_to(
        *utils.all_administrators(),  # All administrators
        *editors_list,  # All editors
        *entry.email_notifications(manager="on_publish").filter(active=True).all(),  # type: ignore[operator]
        *entry.email_notifications(manager="both").filter(active=True).all(),  # type: ignore[operator]
        context={"name": entry.name},
    )
