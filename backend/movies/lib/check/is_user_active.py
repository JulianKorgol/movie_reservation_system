from movies.models import Account


def check_if_user_is_active(account: Account | None) -> bool:
  if account is None:
    return False

  if account.status == 1 and account.user.is_active:
    return True
  elif account.status == 0:
    return False

  return False
