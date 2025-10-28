from .exceptions import PermissionDeniedError


def check_permissions(required_role: str):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            user_role = getattr(self, "user_role", "student")
            if user_role != required_role:
                raise PermissionDeniedError(
                    f"Недостаточно прав: требуется роль '{required_role}'."
                )
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
