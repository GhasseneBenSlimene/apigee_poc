from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 1000},
    {"id": 2, "name": "Phone", "price": 500},
]

class Product(BaseModel):
    name: str
    price: float

@app.get("/products", response_model=List[dict])
def get_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)
    return product if product else {"error": "Product not found"}

@app.post("/products")
def create_product(product: Product):
    new_id = max(p["id"] for p in products) + 1
    new_product = {"id": new_id, **product.dict()}
    products.append(new_product)
    return new_product

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    for p in products:
        if p["id"] == product_id:
            p.update(product.dict())
            return p
    return {"error": "Product not found"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    global products
    products = [p for p in products if p["id"] != product_id]
    return {"message": "Deleted"}
