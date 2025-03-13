#!/bin/bash

RESOURCE_GROUP="MyResourceGroup"
APP_NAME="ai-trading-bot"
RUNTIME="PYTHON:3.9"

echo "Deploying AI Trading Bot to Azure..."
az webapp up --name $APP_NAME --resource-group $RESOURCE_GROUP --runtime $RUNTIME

echo "✅ Deployment complete!"
