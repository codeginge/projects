#!/bin/bash
# Define the Wayland display environment variable (required for automated tasks)
export WAYLAND_DISPLAY=wayland-1
export XDG_RUNTIME_DIR=/run/user/$(id -u)

# Ensure the output directory exists
mkdir -p /home/pi/Pictures/screenshots

# Take the full-screen capture using grim
grim /home/pi/Pictures/screenshots/$(date +%Y-%m-%d_%H-%M-%S).png

