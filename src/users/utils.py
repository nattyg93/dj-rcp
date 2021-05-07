"""Utils for users app."""
from functools import reduce
from operator import or_

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models import Q


def populate_default_groups():
    """Ensure relevant Groups exist and have correct Permissions."""
    for group_info in settings.AUTH_GROUPS:
        group = Group.objects.get_or_create(name=group_info["name"])[0]
        perm_q_list = []
        for perm in group_info["permissions"]:
            app_label, codename = perm.split(".")
            perm_q_list.append(Q(content_type__app_label=app_label, codename=codename))
        if perm_q_list:
            perm_q = reduce(or_, (perm_q_list))
            group.permissions.set(Permission.objects.filter(perm_q))
