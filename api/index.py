import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Ensure Python can import the Django project + ml package.
# Repo layout contains the runnable Django project under:
#   fake_news_project/backend/fake_news_project/backend/
BASE_DIR = Path(__file__).resolve().parents[1]  # .../backend
NESTED_DJANGO_ROOT = BASE_DIR / "fake_news_project" / "backend"
if NESTED_DJANGO_ROOT.exists():
    sys.path.insert(0, str(NESTED_DJANGO_ROOT))
else:
    # Fallback to repo backend root
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = get_wsgi_application()

