from rest_framework.throttling import AnonRateThrottle


class RegistrationRateThrottle(AnonRateThrottle):
    scope = 'registration'


class EmailConfirmationRateThrottle(AnonRateThrottle):
    scope = 'email_confirmation'
