"""Kaartdijin Boodja Publisher Django Application Emails."""


# Local
from govapp.apps.emails import emails


class SyncItassetsUsersEmail(emails.TemplateEmailBase):
    subject = "[KB] Itassets Users Sync"
    html_template = "sync_itassets_users.html"
    txt_template = "sync_itassets_users.txt"
