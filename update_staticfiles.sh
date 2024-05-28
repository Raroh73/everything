#!/usr/bin/env bash

curl https://unpkg.com/htmx.org/dist/htmx.js --output staticfiles/js/htmx.js --location
curl https://unpkg.com/htmx.org/dist/ext/ws.js --output staticfiles/js/ws.js --location

tailwindcss --input tailwind.css --output staticfiles/css/styles.css
