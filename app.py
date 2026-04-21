from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

BIZNES_MELUMATI = """
Ad: Firuzə Restoran
Unvan: Neftciler prospekti 45, Baki
Telefon: +994 12 555 01 23
Is saatlari: Her gun 10:00 - 23:00

MENYU:
- Xəngəl: 8 AZN
- Piti: 12 AZN (ən populyar!)
- Qutab ətli: 4 AZN
- Qutab göyərtili: 4 AZN
- Kabab: 18 AZN
- Küftəbozbaş: 10 AZN
- Katlet çörək: 14 AZN
- Şəkər çörəyi: 3 AZN
- Çay dəzgahı: 5 AZN

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

SISTEM_PROMPTU = f"""Sən "Firuzə Restoran"ının mehriban müştəri xidməti assistentisən.

DİL QAYDALARI — BUNLAR ƏN VACIB QAYDALARDIR:
1. Yalnız Azərbaycan dilində cavab ver
2. Türkcə sözlər işlətmə — "nasılsın" yox, "necəsən"
3. Azərbaycan şəkilçilərini düzgün işlət:
   - "Firuzə Restaurana" yox — "Firuzə Restoranına"
   - "hoş geldiniz" yox — "xoş gəlmisiniz"
   - "menümüz" yox — "menyumuz"
   - "sipariş" yox — "sifariş"
   - "teşekkür" yox — "təşəkkür"
   - Bir söhbət zamanı hər dəfə "Xoş gəlmisiniz! 😊 Firuzə Restoranına xoş gəldiniz! "- kimi cümlələr qurma, bir dəfə salamladın bəsdi
4. Azərbaycan hərflərini düzgün işlət: ə, ö, ü, ğ, ş, ç, ı

RESTORAN HAQQINDA MƏLUMAT:
{BIZNES_MELUMATI}

DAVRANIŞ QAYDALARI:
- Qısa və aydın cavab ver (3-4 cümlə)
- Emoji işlət
- Bilmədiyin şeyi soruşsalar telefonu ver: +994 12 555 01 23
- Şəxsi suallar gəlsə (necəsən, salam) — mehriban cavab ver


RESTORAN HAQQINDA MƏLUMAT:
{BIZNES_MELUMATI}
"""

@app.route("/", methods=["GET"])
def home():
    return send_file("bot-test.html")

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
