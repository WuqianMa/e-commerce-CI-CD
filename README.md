# Django E-commerce Demo — Docker & CI/CD

An educational course project demonstrating a small Django storefront and containerized testing/deployment workflows. This is a portfolio code sample, **not a production e-commerce application**.

## What is included

- Django models and pages for products, carts, orders, posts and an affiliate-link view.
- SQLite for local development, Django unit/integration tests, and Docker Compose.
- GitHub Actions workflow: build a container, run Django tests, then (only on a successful push to main) publish a container image to GitHub Container Registry.
- Frontend: HTML, CSS and JavaScript. Backend: Python and Django.

## Run locally (Docker)

    docker compose up --build

Visit http://localhost:8000/. This binds to localhost only. The demo container runs Django's development server; do **not** expose it on the public internet.

To run tests without starting the server:

    docker compose build
    docker compose run --rm web python manage.py test

For local Python development (Python 3.11+), create a virtual environment, install requirements, then set DJANGO_DEBUG=true before running migrations/tests. For any non-development environment set DJANGO_SECRET_KEY to a strong unique secret and configure DJANGO_ALLOWED_HOSTS.

## CI and image publishing

The workflow in .github/workflows/django.yml runs the Django test suite for pull requests and pushes to main. Container images are published **only after the test job succeeds on main**. Image tags are latest and the commit SHA under ghcr.io/<lowercase-owner>/<repo>. Publishing uses the built-in GITHUB_TOKEN (no personal-access-token secret needed).

## Limitations / security notes

- This is a **course demo, not a finished paid checkout**. The legacy PayPal client-side integration lacked secure backend verification. Real payments and the process_order endpoint are deliberately disabled pending server-side verification, order locking, amount verification and webhook handling.
- No production-grade deployment, database migrations strategy, authentication/onboarding flow, payments, or concurrency testing is claimed.
- The repository previously tracked a full venv, local db.sqlite3, chromedriver.exe and Python cache files. These are excluded from the new branch and ignored going forward. Removing files from a branch does **not** erase them from older Git history. If the old SQLite database contained personal information, review it and consider a separate history-rewrite and credential rotation.
- Keep secrets and private database records out of Git. Existing development credentials in Git history should never be reused.
- The CI workflow has been updated, but its success should be confirmed via the GitHub Actions run after opening/merging this pull request.

## Provenance

Originally developed as an Efrei "Machine Learning in Production" course exercise. Updated to make the engineering workflow reproducible and more appropriately scoped for a public portfolio. The original course attribution remains.

