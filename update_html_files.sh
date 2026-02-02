#!/bin/bash
# Script to add legal disclaimer and AdSense to all HTML files

echo "Adding legal disclaimer and AdSense to HTML files..."

# List of files to update
files=(
    "list.html"
    "calculator.html"
    "calendar.html"
    "fortune.html"
)

echo "Files to update: ${files[@]}"
echo "Please manually update these files with:"
echo "1. Google AdSense script in <head>"
echo "2. AdSense ad units in appropriate locations"
echo "3. Legal disclaimer in footer"
