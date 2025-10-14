from rest_framework.permissions import BasePermission

from movies.models import Account


def is_admin(account: Account) -> bool:
  return account.role.id == 2 and account.role.name == "Admin"


class IsAdminBasePermission(BasePermission):
  def has_permission(self, request, view):
    if is_admin(request.account):
      return True
    return False
