from flask import Flask, jsonify, request

app = Flask(__name__)

# Données simulées
products = [
    {"id": 1, "name": "Laptop", "price": 1000},
    {"id": 2, "name": "Phone", "price": 500}
]

# GET /products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# GET /products/<id>
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

# POST /products
@app.route('/products', methods=['POST'])
def create_product():
    new_product = request.get_json()
    new_product['id'] = max([p['id'] for p in products]) + 1 if products else 1
    products.append(new_product)
    return jsonify(new_product), 201

# PUT /products/<id>
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    updates = request.get_json()
    product.update(updates)
    return jsonify(product)

# DELETE /products/<id>
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify({"message": "Product deleted"})

# Lancement de l'app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
