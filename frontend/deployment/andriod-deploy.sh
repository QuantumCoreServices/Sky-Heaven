#!/bin/bash

echo "🔹 Building Android app..."
cd /home/seano/ai-crypto-trader/frontend
npx react-native run-android
echo "✅ Android deployment complete!"
