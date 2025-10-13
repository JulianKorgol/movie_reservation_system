from rest_framework.permissions import BasePermission

from movies.models import Account


def is_super_admin(account: Account) -> bool:
  if account.role.id == 1 and account.role.name == "Super Admin":
    return True
  return False


class IsSuperAdminBasePermission(BasePermission):
  def has_permission(self, request, view):
    if is_super_admin(request.account):
      return True
    return False
