from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

BIZNES_MELUMATI = """
Ad: Leyla Restoran
Unvan: Neftciler prospekti 45, Baki
Telefon: +994 12 555 01 23
Is saatlari: Her gun 10:00 - 23:00

MENYU:
- Xengel: 8 AZN
- Piti: 12 AZN (en populyar!)
- Qutab etli: 4 AZN
- Qutab goyertili: 4 AZN
- Sislik: 18 AZN
- Kuftebozbas: 10 AZN
- Dovletabadi: 14 AZN
- Seker coreyti: 3 AZN
- Cay desti: 5 AZN

CATDIRILMA:
- Baki daxilinde catdirilma var
- Minimum sifaris: 15 AZN
- Catdirilma haggi: 3 AZN
- Muddet: 30-45 deqiqe

REZERVASIYA:
- Telefon: +994 12 555 01 23
- En azi 2 saat evvel bildirin

ELAVE:
- Pulsuz WiFi var
- Pulsuz parkinq var
"""

SISTEM_PROMPTU = f"""Sen "Leyla Restoran"in mehriban musteri xidmeti assistentisen.

QAYDALAR:
1. HEMISE Azerbaycan dilinde cavab ver
2. Qisa ve aydin ol (maksimum 3-4 cumle)
3. Emoji istifade et
4. Yalniz asagidaki melumatlar esasinda cavab ver
5. Bilmediyini sorusarlarsa telefon nomresini ver
6. Əgər şəxsi sual gəlirsə (necəsən, nə var, salam kimi) — mehribancasına cavab ver

RESTORAN HAQQINDA MELUMAT:
{BIZNES_MELUMATI}
"""

@app.route("/", methods=["GET"])
def home():
    return send_file("test.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Mesaj boshdur"}), 400

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-haiku-4-5",
                "max_tokens": 300,
                "messages": [
                    {"role": "system", "content": SISTEM_PROMPTU},
                    {"role": "user", "content": user_message}
                ]
            }
        )

        result = response.json()
        bot_reply = result.get("choices", [{}])[0].get("message", {}).get("content", str(result))

        return jsonify({"reply": bot_reply, "status": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
