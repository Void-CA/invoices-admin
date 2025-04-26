from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/printing', methods=['POST'])
def printing():
    if request.is_json:
        data = request.get_json()
        documento = data.get('documento')
        print(f"Recibido para imprimir: {documento}")
    else:
        print("No se recibió JSON")
        documento = None

    return jsonify({"message": "Documento recibido para impresión", "documento": documento}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
