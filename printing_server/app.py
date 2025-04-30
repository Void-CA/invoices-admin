from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/printing', methods=['POST'])
def printing():
    if 'file' not in request.files or 'printer_name' not in request.form:
        return jsonify({"error": "Faltan datos: archivo o nombre de impresora"}), 400

    file = request.files['file']
    printer_name = request.form['printer_name']
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    print(f"Imprimiendo {filename} en {printer_name}...")

    gs_command = [
        "gswin64c",
        "-dNOPAUSE",
        "-dBATCH",
        "-dPrinted",
        "-sDEVICE=mswinpr2",
        f"-sOutputFile=\\\\spool\\{printer_name}",  # Ruta correcta para impresoras en Windows
        filepath
    ]

    try:
        subprocess.run(gs_command, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Error al imprimir", "detalle": str(e)}), 500

    return jsonify({"message": f"{filename} enviado a imprimir en {printer_name}"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
