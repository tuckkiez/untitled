#!/bin/bash

# 🚀 Push to GitHub
# สคริปต์สำหรับ push ขึ้น GitHub

echo "🚀 Pushing to GitHub"
echo "===================="

# Set current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Add all files
echo "📦 Adding all files..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Update football predictions for July 19, 2025"

# Push to GitHub
echo "🌐 Pushing to GitHub..."
git push

echo "✅ Successfully pushed to GitHub!"
echo "⏰ Completed at: $(date)"
