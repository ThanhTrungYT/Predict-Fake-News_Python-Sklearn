#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def patch_django_settings():
    """
    Ép mở host + CORS ngay từ manage.py để khỏi phải sửa settings.py.
    """
    try:
        import importlib

        settings_module_name = os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "backend.settings"
        )
        settings_module = importlib.import_module(settings_module_name)

        # Mở host toàn bộ
        setattr(settings_module, "ALLOWED_HOSTS", ["*"])

        # Bật CORS nếu đã cài django-cors-headers
        try:
            import corsheaders  # noqa: F401

            installed_apps = list(getattr(settings_module, "INSTALLED_APPS", []))
            if "corsheaders" not in installed_apps:
                installed_apps.insert(0, "corsheaders")
            setattr(settings_module, "INSTALLED_APPS", installed_apps)

            middleware = list(getattr(settings_module, "MIDDLEWARE", []))
            cors_middleware = "corsheaders.middleware.CorsMiddleware"
            if cors_middleware not in middleware:
                middleware.insert(0, cors_middleware)
            setattr(settings_module, "MIDDLEWARE", middleware)

            # Mở toàn bộ CORS
            setattr(settings_module, "CORS_ALLOW_ALL_ORIGINS", True)
            setattr(settings_module, "CORS_ALLOW_CREDENTIALS", True)
            setattr(settings_module, "CORS_URLS_REGEX", r"^.*$")
            setattr(
                settings_module,
                "CSRF_TRUSTED_ORIGINS",
                [
                    "https://fake-new-fe-react-vite.vercel.app",
                    "http://fake-new-fe-react-vite.vercel.app",
                ],
            )
            # QUAN TRỌNG:
            # Không set CSRF_TRUSTED_ORIGINS = ["*"]
            # Django 4+ sẽ báo lỗi.
            # Nếu cần thì phải ghi rõ:
            # ["http://localhost:3000", "https://frontend-domain.com"]

        except ImportError:
            pass

    except Exception:
        # Không để patch lỗi làm chết app
        pass


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

    patch_django_settings()

    # Tự mở runserver ra toàn mạng
    # python manage.py runserver -> 0.0.0.0:8000
    if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
        has_addr = any(":" in arg or arg.count(".") >= 1 for arg in sys.argv[2:])
        if not has_addr:
            sys.argv.append("0.0.0.0:8000")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? "
            "Did you forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()