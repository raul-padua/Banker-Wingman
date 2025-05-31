from mangum import Mangum
from app import app

# Wrap FastAPI app with Mangum for Lambda
handler = Mangum(app) 