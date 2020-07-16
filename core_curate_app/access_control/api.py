""" Set of functions to define the common rules for access control across collections
"""
import logging
from django.contrib.auth.models import User
from core_curate_app.components.curate_data_structure.models import CurateDataStructure
from core_main_app.access_control.exceptions import AccessControlError

logger = logging.getLogger(__name__)


def can_read(func, *args, **kwargs):
    """ Can user read

        Args:
            func:
            *args:
            **kwargs:

        Returns:

        """
    # get the User in the args list
    user = next((arg for arg in args if isinstance(arg, User)), None)

    if user.is_superuser:
        return func(*args, **kwargs)

    document = func(*args, **kwargs)
    if type(document) is list:
        document_list = document
    else:
        document_list = [document]

    _check_can_read(document_list, user)

    return document


def _check_can_read(document_list, user):
    """ Can read from list id.

    Args:
        document_list:
        user:

    Returns:

    """
    # check access is correct
    for document in document_list:
        # user is document owner
        if document.user == str(user.id):
            continue
        # user is not owner or document
        raise AccessControlError("The user doesn't have enough rights.")


def can_write(func, *args, **kwargs):
    """ Can user write

    Args:
        func:
        *args:
        **kwargs:

    Returns:

    """
    user = next((arg for arg in args if isinstance(arg, User)), None)
    if user.is_superuser:
        return func(*args, **kwargs)

    document = next((arg for arg in args if isinstance(arg, CurateDataStructure)), None)
    if document.user != str(user.id):
        raise AccessControlError(
            "The user doesn't have enough rights to access this document."
        )

    return func(*args, **kwargs)