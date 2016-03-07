from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod
from django.conf import settings
from pydoc import locate


_ACTIVE_BACKEND = None


def get_backend():
    """
    Gets the active backend for this casepro instance
    """
    global _ACTIVE_BACKEND
    if not _ACTIVE_BACKEND:
        _ACTIVE_BACKEND = locate(settings.SITE_BACKEND)()
    return _ACTIVE_BACKEND


class BaseBackend(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def pull_contacts(self, org, modified_after, modified_before, progress_callback=None):
        """
        Pulls contacts modified in the given time window

        :param org: the org
        :param datetime modified_after: pull contacts modified after this
        :param datetime modified_before: pull contacts modified before this
        :param progress_callback: callable that will be called from time to time with number of contacts pulled
        :return: tuple of the number of contacts created, updated, deleted and ignored
        """
        pass

    @abstractmethod
    def pull_fields(self, org):
        """
        Pulls all contact fields

        :param org: the org
        :return: tuple of the number of fields created, updated, deleted and ignored
        """
        pass

    @abstractmethod
    def pull_groups(self, org):
        """
        Pulls all contact groups

        :param org: the org
        :return: tuple of the number of groups created, updated, deleted and ignored
        """
        pass

    @abstractmethod
    def pull_labels(self, org):
        """
        Pulls all message labels

        :param org: the org
        :return: tuple of the number of labels created, updated, deleted and ignored
        """
        pass

    @abstractmethod
    def pull_messages(self, org, modified_after, modified_before, as_handled=False, progress_callback=None):
        """
        Pulls messages modified in the given time window

        :param org: the org
        :param datetime modified_after: pull messages modified after this
        :param datetime modified_before: pull messages modified before this
        :param bool as_handled: whether messages should be saved as already handled
        :param progress_callback: callable that will be called from time to time with number of messages pulled
        :return: tuple of the number of messages created, updated, deleted and ignored
        """
        pass

    @abstractmethod
    def create_label(self, org, name):
        """
        Creates a label (or returns an existing label) with the given name

        :param org: the org
        :param name: the name, e.g. "Spam"
        :return: the backend label UUID
        """
        pass

    @abstractmethod
    def create_outgoing(self, org, text, contacts, urns):
        """
        Creates an outgoing broadcast message

        :param org: the org
        :param text: the message text
        :param contacts: the contact recipients
        :param urns: the raw URN recipients
        :return: tuple of the broadcast id and it's timestamp
        """
        pass

    @abstractmethod
    def add_to_group(self, org, contact, group):
        """
        Adds the given contact to a group

        :param org: the org
        :param contact: the contact
        :param group: the group
        """
        pass

    @abstractmethod
    def remove_from_group(self, org, contact, group):
        """
        Removes the given contact from a group

        :param org: the org
        :param contact: the contact
        :param group: the group
        """
        pass

    @abstractmethod
    def stop_runs(self, org, contact):
        """
        Stops any ongoing flow runs for the given contact

        :param org: the org
        :param contact: the contact
        """
        pass

    @abstractmethod
    def label_messages(self, org, messages, label):
        """
        Adds a label to the given messages

        :param org: the org
        :param messages: the messages
        :param label: the label
        """
        pass

    @abstractmethod
    def unlabel_messages(self, org, messages, label):
        """
        Removes a label from the given messages

        :param org: the org
        :param messages: the messages
        :param label: the label
        """
        pass

    @abstractmethod
    def archive_messages(self, org, messages):
        """
        Archives the given messages

        :param org: the org
        :param messages: the messages
        """
        pass

    @abstractmethod
    def archive_contact_messages(self, org, contact):
        """
        Archives all messages for the given contact

        :param org: the org
        :param contact: the contact
        """
        pass

    @abstractmethod
    def restore_messages(self, org, messages):
        """
        Restores (un-archives) the given messages

        :param org: the org
        :param messages: the messages
        """
        pass

    @abstractmethod
    def flag_messages(self, org, messages):
        """
        Flags the given messages

        :param org: the org
        :param messages: the messages
        """
        pass

    @abstractmethod
    def unflag_messages(self, org, messages):
        """
        Un-flags the given messages

        :param org: the org
        :param messages: the messages
        """
        pass

    @abstractmethod
    def fetch_contact_messages(self, org, contact, created_after, created_before):
        """
        Fetches a contact's incoming and outgoing messages to display on a case timeline

        :param org: the org
        :param contact: the contact
        :param created_after: include messages created after this time
        :param created_before: include messages created before this time
        :return: the messages as JSON objects in reverse chronological order
        """
        pass