from flask import Flask, request, jsonify, send_from_directory
import os
import random

app = Flask(__name__)

IMAGES_DIR = "images"
SOLUTIONS_DIR = "solutions"

os.makedirs(SOLUTIONS_DIR, exist_ok=True)


@app.route("/api/get_image", methods=["GET"])
def get_image():
    # Filtra le immagini che non hanno già una soluzione salvata
    candidates = []
    for f in os.listdir(IMAGES_DIR):
        if f.endswith(".jpeg"):
            txt_path = os.path.join(SOLUTIONS_DIR, f + ".txt")
            if not os.path.exists(txt_path):
                candidates.append(f)

    if not candidates:
        return jsonify({"error": "Nessuna immagine disponibile"}), 404

    # Scegli immagine casuale
    chosen = random.choice(candidates)
    return jsonify({"filename": chosen})


@app.route("/api/get_image_file/<filename>", methods=["GET"])
def get_image_file(filename):
    return send_from_directory(IMAGES_DIR, filename)


@app.route("/api/submit", methods=["POST"])
def submit_solution():
    data = request.json
    filename = data.get("filename")
    text = data.get("text")

    if not filename or not text:
        return jsonify({"error": "Missing fields"}), 400

    txt_path = os.path.join(SOLUTIONS_DIR, filename + ".txt")
    if os.path.exists(txt_path):
        return jsonify({"error": "Solution already exists"}), 400

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text.strip())

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10202, debug=True)
