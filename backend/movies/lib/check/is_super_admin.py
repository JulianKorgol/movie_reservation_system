from rest_framework.permissions import BasePermission

from movies.models import Account


def is_super_admin(account: Account) -> bool:
  return account.role.id == 1 and account.role.name == "Super Admin"


class IsSuperAdminBasePermission(BasePermission):
  def has_permission(self, request, view) -> bool:
    account = Account.objects.filter(user=request.user).first()
    return account is not None and is_super_admin(account)
