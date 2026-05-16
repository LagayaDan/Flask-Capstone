"""Production WSGI entry point — imported by Gunicorn / uWSGI."""
from webapp import create_app  # noqa: E402

app = create_app()
