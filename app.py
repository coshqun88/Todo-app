from flask import Flask, request, jsonify
from anthropic import Anthropic
import os

app = Flask(__name__)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Biznes məlumatları - bunu müştəriyə görə dəyişirsiniz
BIZNES_MELUMATI = """
Ad: Leyla Restoran
Ünvan: Neftçilər prospekti 45, Bakı
Telefon: +994 12 555 01 23
WhatsApp: +994 50 555 01 23
İş saatları: Hər gün 10:00 - 23:00 (bayram günlərində də açıq)

MENYU VƏ QİYMƏTLƏR:
- Xəngəl: 8 AZN
- Piti: 12 AZN (ən populyar!)
- Qutab ətli: 4 AZN
- Qutab göyərtili: 4 AZN
- Şişlik: 18 AZN
- Küftəbozbaş: 10 AZN
- Dövlətabadı: 14 AZN
- Şəkər çörəyi: 3 AZN
- Çay dəsti: 5 AZN
- Müxtəlif salatlar: 5-8 AZN

ÇATDIRILMA:
- Bakı daxilində çatdırılma var
- Minimum sifariş: 15 AZN
- Çatdırılma haqqı: 3 AZN
- Müddət: 30-45 dəqiqə
- Sifariş üçün: +994 12 555 01 23

REZERVASIYA:
- Masa rezervasiyası üçün zəng edin: +994 12 555 01 23
- Ən azı 2 saat əvvəl bildirin
- Böyük qrup üçün (10+ nəfər) 1 gün əvvəl bildirin

ƏLAVƏ MƏLUMAT:
- Pulsuz WiFi var
- Pulsuz parkinq var
- Vegetarian seçimlər mövcuddur
- Uşaq menyu var
- Korporativ sifarişlər qəbul edilir
"""

SISTEM_PROMPTU = f"""Sən "Leyla Restoran"ın mehriban və peşəkar müştəri xidməti assistentisən.

QAYDALAR:
1. HƏMİŞƏ Azərbaycan dilində cavab ver
2. Qısa və aydın ol (maksimum 3-4 cümlə)
3. Emoji istifadə et - mehriban görünüş üçün
4. Yalnız aşağıdakı məlumatlar əsasında cavab ver
5. Bilmədiyini soruşsalar telefon nömrəsini ver
6. Rezervasiya və ya sifariş üçün həmişə telefona yönləndir

RESTORAN HAQQINDA MƏLUMAT:
{BIZNES_MELUMATI}
"""

@app.route("/", methods=["GET"])
def home():
    return "Leyla Restoran Bot işləyir! ✅"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Mesaj boşdur"}), 400

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=SISTEM_PROMPTU,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.content[0].text

        return jsonify({
            "reply": bot_reply,
            "status": "ok"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# WhatsApp inteqrasiyası üçün (Twilio)
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    try:
        incoming_msg = request.form.get("Body", "")
        sender = request.form.get("From", "")

        if not incoming_msg:
            return "", 200

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=SISTEM_PROMPTU,
            messages=[
                {"role": "user", "content": incoming_msg}
            ]
        )

        bot_reply = response.content[0].text

        # Twilio XML cavabı
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{bot_reply}</Message>
</Response>"""

        return twiml, 200, {"Content-Type": "text/xml"}

    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
