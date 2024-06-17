from fastapi import FastAPI
from models import engine, Base
from apis.products import router as product_routes
from apis.users import router as user_routes
from apis.orders import router as order_routes
from apis.posts import router as posts_routes

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the products router
app.include_router(product_routes)
app.include_router(user_routes)
app.include_router(order_routes)
app.include_router(posts_routes)