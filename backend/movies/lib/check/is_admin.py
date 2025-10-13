from rest_framework.permissions import BasePermission

from movies.models import Account


def is_admin(account: Account) -> bool:
  if account.role.id == 2 and account.role.name == "Admin":
    return True
  return False


class IsAdminBasePermission(BasePermission):
  def has_permission(self, request, view):
    if is_admin(request.account):
      return True
    return False
