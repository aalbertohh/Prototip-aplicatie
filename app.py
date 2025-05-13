from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # permite accesul frontendului local

API_TOKEN = "a123c5bc60882b291cf7bfd5669f723eae74023b"

@app.route("/recognize", methods=["POST"])
def recognize_food():
    image = request.files.get("image")
    if not image:
        return jsonify({"error": "Nicio imagine primită"}), 400

    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    files = {"image": image.stream}

    url = "https://api.logmeal.es/v2/image/recognition/complete"

    try:
        response = requests.post(url, headers=headers, files=files)
        result = response.json()
        print("🔍 Răspuns LogMeal:", result)

        # Extrage primul aliment detectat (dishes[0].name)
        food = result.get("dishes", [{}])[0].get("name", "necunoscut")

        return jsonify({
            "foodType": food
        })

    except Exception as e:
        print("❌ Eroare:", str(e))
        return jsonify({"error": "Eroare internă"}), 500

if __name__ == "__main__":
    app.run(debug=True)
