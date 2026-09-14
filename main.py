from collections.abc import Callable


users: list[dict[str, str]] = []


def password_checker(func: Callable) -> Callable:
    """Проверяет пароль по базовым правилам перед вызовом функции."""

    def wrapper(password: str) -> str:
        """Проверяет пароль и вызывает исходную функцию при успехе."""
        if len(password) < 8:
            return "Ошибка: пароль должен содержать не меньше 8 символов."

        if not any(char.isdigit() for char in password):
            return "Ошибка: пароль должен содержать хотя бы одну цифру."

        if not any(char.isupper() for char in password):
            return "Ошибка: пароль должен содержать хотя бы одну заглавную букву."

        if not any(char.islower() for char in password):
            return "Ошибка: пароль должен содержать хотя бы одну строчную букву."

        return func(password)

    return wrapper


@password_checker
def register_user(password: str) -> str:
    """Возвращает сообщение об успешной регистрации пользователя."""
    return "Пользователь успешно зарегистрирован."


def password_validator(
    min_length: int = 8,
    min_uppercase: int = 1,
    min_lowercase: int = 1,
    min_digits: int = 1,
    min_special_chars: int = 1,
) -> Callable:
    """Создаёт декоратор для проверки пароля по заданным правилам."""

    def decorator(func: Callable) -> Callable:
        """Оборачивает функцию проверкой пароля."""

        def wrapper(username: str, password: str) -> str:
            """Проверяет пароль и вызывает исходную функцию при успехе."""
            uppercase_count = sum(char.isupper() for char in password)
            lowercase_count = sum(char.islower() for char in password)
            digit_count = sum(char.isdigit() for char in password)
            special_count = sum(not char.isalnum() for char in password)

            if len(password) < min_length:
                raise ValueError(
                    f"Пароль должен содержать не меньше {min_length} символов."
                )

            if uppercase_count < min_uppercase:
                raise ValueError(
                    f"Пароль должен содержать минимум {min_uppercase} "
                    "заглавную букву."
                )

            if lowercase_count < min_lowercase:
                raise ValueError(
                    f"Пароль должен содержать минимум {min_lowercase} "
                    "строчную букву."
                )

            if digit_count < min_digits:
                raise ValueError(
                    f"Пароль должен содержать минимум {min_digits} цифру."
                )

            if special_count < min_special_chars:
                raise ValueError(
                    f"Пароль должен содержать минимум {min_special_chars} "
                    "специальный символ."
                )

            return func(username, password)

        return wrapper

    return decorator


def username_validator(func: Callable) -> Callable:
    """Проверяет имя пользователя перед вызовом функции."""

    def wrapper(username: str, password: str) -> str:
        """Проверяет имя пользователя и вызывает исходную функцию."""
        if not username:
            raise ValueError("Имя пользователя не должно быть пустым.")

        if any(char.isspace() for char in username):
            raise ValueError("Имя пользователя не должно содержать пробелы.")

        return func(username, password)

    return wrapper


@username_validator
@password_validator(
    min_length=8,
    min_uppercase=1,
    min_lowercase=1,
    min_digits=2,
    min_special_chars=1,
)
def register_account(username: str, password: str) -> str:
    """Добавляет пользователя в список после успешной проверки данных."""
    users.append({"username": username, "password": password})
    return "Пользователь зарегистрирован."


def run_tests() -> None:
    """Запускает тестовые сценарии регистрации и выводит результаты."""
    print("=== Проверка простого декоратора ===")
    print(register_user("short"))
    print(register_user("password"))
    print(register_user("Password"))
    print(register_user("Password1"))

    print("\n=== Проверка регистрации аккаунтов ===")

    test_data: list[tuple[str, str]] = [
        ("ivan", "Password12!"),
        ("ivan petrov", "Password12!"),
        ("anna", "Pass1!"),
        ("maria", "password12!"),
        ("alex", "Password!"),
        ("olga", "Password12"),
    ]

    for username, password in test_data:
        try:
            result = register_account(username, password)
            print(f"{username}: {result}")
        except ValueError as error:
            print(f"{username}: ошибка — {error}")

    print("\nЗарегистрированные пользователи:")
    print(users)


run_tests()
