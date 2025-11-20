from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json

    # --- DEBUG: mostrar lo que llega ---
    print("\n📌 JSON recibido en Python:")
    print(data)

    items = data.get("items", [])
    parameters = data.get("parameters", [])

    subtotal = sum(item.get("quantity", 0) * item.get("unitPrice", 0) for item in items)

    tax_amount = 0
    discount_amount = 0

    for param in parameters:

        type_ = param.get("paramType") or param.get("param_type")
        percent = param.get("valuePercent") or param.get("value_percent")
        amount = param.get("valueAmount") or param.get("value_amount")
        min_purchase = param.get("minPurchase") or param.get("min_purchase")

        if type_ == "TAX" and percent:
            tax_amount += subtotal * (percent / 100)

        if type_ == "DISCOUNT":
            if amount:
                discount_amount += amount
            elif percent and not min_purchase:
                discount_amount += subtotal * (percent / 100)
            elif percent and min_purchase and subtotal >= min_purchase:
                discount_amount += subtotal * (percent / 100)

    total = subtotal + tax_amount - discount_amount

    return jsonify({
        "subtotal": round(subtotal, 2),
        "tax": round(tax_amount, 2),
        "discount": round(discount_amount, 2),
        "total": round(total, 2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
