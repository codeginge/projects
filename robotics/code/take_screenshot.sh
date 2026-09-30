#!/bin/bash

# Find the active user logged into the desktop
REAL_USER=$(who | grep -m 1 '(' | awk '{print $1}')
if [ -z "$REAL_USER" ]; then
    REAL_USER=$(loginctl list-users | awk 'NR==2 {print $2}')
fi

# Dynamically look up the user's ID
USER_ID=$(id -u "$REAL_USER")

# Set the environment variables pointing to the live desktop session
export XDG_RUNTIME_DIR="/run/user/$USER_ID"
export WAYLAND_DISPLAY=$(ls /run/user/$USER_ID/wayland-* 2>/dev/null | head -n 1 | xargs basename)

# Fallback defaults if the discovery fails
export WAYLAND_DISPLAY=${WAYLAND_DISPLAY:-wayland-1}

# Make sure the saving directory exists
mkdir -p /home/$REAL_USER/Pictures/screenshots

# Take the screenshot
/usr/bin/grim /home/$REAL_USER/Pictures/screenshots/${REAL_USER}_$(date +%Y-%m-%d_%H-%M-%S).png

# delete old screenshots that are older than 1 hour
find "$TARGET_DIR" -type f -name "*.png" -mmin +60 -delete
