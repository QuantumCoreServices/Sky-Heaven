import json
from api.app import app
from mangum import Mangum

handler = Mangum(app)

def lambda_handler(event, context):
    return handler(event, context)
