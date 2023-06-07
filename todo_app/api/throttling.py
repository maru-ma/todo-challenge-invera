from rest_framework.throttling import UserRateThrottle


class MinuteRateThrottle(UserRateThrottle):
    """
    Throttling class for rate limiting API requests within a minute.

    This throttle restricts the number of requests that can be made by a user within a minute.

    Throttle Scope:
    - user_minute: Restricts the number of requests per minute for each user.
    """

    scope = "user_minute"


class DailyRateThrottle(UserRateThrottle):
    """
    Throttling class for rate limiting API requests within a day.

    This throttle restricts the number of requests that can be made by a user within a day.

    Throttle Scope:
    - user_day: Restricts the number of requests per day for each user.
    """

    scope = "user_day"
