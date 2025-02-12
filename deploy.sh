#!/bin/bash

echo "🔄 Starting deployment..."

cd /opt/booking_system

echo "📡 Pulling latest code from GitHub..."
git pull origin main

echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "⚙️ Installing dependencies..."
pip install -r requirements.txt

echo "🛠 Running database migrations..."
python manage.py migrate

echo "🔨 Building frontend..."
npm install --prefix frontend
npm run build --prefix frontend

echo "🚀 Restarting services..."
sudo systemctl restart gunicorn
sudo systemctl restart nginx

echo "✅ Deployment complete!"
