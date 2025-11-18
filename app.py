from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    items = data.get("items", [])
    parameters = data.get("parameters", [])

    subtotal = sum(item.get("quantity", 0) * item.get("unit_price", 0) for item in items)

    tax_amount = 0
    discount_amount = 0

    for param in parameters:

        type_ = param.get("param_type")
        percent = param.get("value_percent")
        amount = param.get("value_amount")
        min_purchase = param.get("min_purchase")

        # ------- Impuestos -------
        if type_ == "TAX":
            if percent:
                tax_amount += subtotal * (percent / 100)

        # ------- Descuentos -------
        if type_ == "DISCOUNT":
            # fijo
            if amount:
                discount_amount += amount

            # porcentaje directo
            elif percent and not min_purchase:
                discount_amount += subtotal * (percent / 100)

            # porcentaje con rango
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
