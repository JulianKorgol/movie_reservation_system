from rest_framework.permissions import BasePermission

from movies.models import Account


def is_admin(account: Account) -> bool:
  return account.role.id == 2 and account.role.name == "Admin"


class IsAdminBasePermission(BasePermission):
  def has_permission(self, request, view) -> bool:
    account = Account.objects.filter(user=request.user).first()
    return account is not None and is_admin(account)
