#!/bin/sh
set -e

echo "Starting Nginx with BACKEND_URL=${BACKEND_URL}"

# Substitute environment variables in the template
envsubst '$$BACKEND_URL' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Verify the configuration was created
if [ -f /etc/nginx/conf.d/default.conf ]; then
    echo "Nginx configuration created successfully"
else
    echo "ERROR: Failed to create nginx configuration"
    exit 1
fi

# Test nginx configuration
nginx -t

# Start nginx
exec nginx -g 'daemon off;'
