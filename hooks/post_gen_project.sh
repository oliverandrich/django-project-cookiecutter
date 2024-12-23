#!/bin/sh

echo "\033[32m✓\033[0m Downloaded htmx 2.x.x."
curl -s -L https://unpkg.com/htmx.org@2.x.x >assets/js/htmx.min.js

echo "\033[32m✓\033[0m Downloaded alpinejs 3.x.x."
curl -s -L https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js >assets/js/alpinejs.min.js

echo "\033[32m✓\033[0m Created .env file."
echo "# Activate debug mode for Django framework." >>.env
echo "DEBUG=true" >>.env

echo "\033[32m✓\033[0m Installed dependencies."
uv sync --quiet --all-extras

echo "\033[32m✓\033[0m Created default tailwind.config.js."
uv run python manage.py tailwind build 2>&1 >/dev/null

{% if cookiecutter.use_pycharm %}
echo "\033[32m✓\033[0m Configured PyCharm integration for Tailwind CSS and htmx."
uv run python manage.py tailwind install_pycharm_workaround 2>&1 >/dev/null
curl -s -L -O https://raw.githubusercontent.com/bigskysoftware/htmx/refs/heads/master/editors/jetbrains/htmx.web-types.json
echo '{ "devDependencies": {"tailwindcss": "latest"}, "web-types": "./htmx.web-types.json" }' >package.json
{% endif %}

{% if cookiecutter.license == "EUPL-1.2" %}
echo "\033[32m✓\033[0m Created EUPL-1.2 license file."
curl -s -L https://interoperable-europe.ec.europa.eu/sites/default/files/custom-page/attachment/2020-03/EUPL-1.2%20EN.txt >LICENSE.txt
{% endif %}

echo "\033[32m✓\033[0m Cleaned up new project."
rm assets/css/.gitkeep
rm assets/js/.gitkeep

echo "\033[32m✓\033[0m Initialized git repository."
git init -q

echo "\033[32m✓\033[0m Initial commit."
git add -A . 2>&1 >/dev/null
git commit -q -m "Initial commit"

echo "\033[32m✓\033[0m Installed pre-commit hook."
uv tool run pre-commit install

echo
echo "\033[32mHappy coding!\033[0m"
