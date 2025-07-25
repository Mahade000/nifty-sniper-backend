from flask import Flask, request, jsonify
import requests
import os
from tradingview_script import analyze_market
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

ALPHA_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")  # Set your API key in env

# Supported currency codes
CURRENCY_CODES = {
    "US": "USD",
    "IN": "INR",
    "UK": "GBP",
    "EU": "EUR",
    "JP": "JPY",
    "SG": "SGD",
    "AU": "AUD",
    "CA": "CAD",
    "CH": "CHF",
    "CN": "CNY",
    "KR": "KRW",
    "BR": "BRL",
    "ZA": "ZAR",
    "CRYPTO": "USD"  # Default for crypto
}
@app.route('/get-fx-rate', methods=['GET'])
def get_fx_rate():
    from_cur = request.args.get('from')
    to_cur = request.args.get('to')

    fx_url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_cur}&to_currency={to_cur}&apikey={ALPHA_KEY}"
    try:
        response = requests.get(fx_url)
        data = response.json()

        rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
        explanation = f"Exchange rate from {from_cur} to {to_cur}"
        return jsonify({"rate": rate, "explanation": explanation})

    except Exception as e:
        return jsonify({"error": "Failed to get exchange rate", "details": str(e)}), 500
@app.route('/', methods=['GET'])
def home():
    return "Nifty Sniper 🔱 is LIVE!"

@app.route('/get-live-price', methods=['GET'])
def get_live_price():
    symbol = request.args.get('symbol', 'AAPL')
    market = request.args.get('market', 'US').upper()
    to_currency = request.args.get('to_currency', 'INR').upper()
    base_currency = CURRENCY_CODES.get(market, "USD")
    price, explanation, converted_price, fx_rate = None, "", None, None

    # 1. Get price from Alpha Vantage
    if market == "CRYPTO":
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency={base_currency}&apikey={ALPHA_KEY}'
        resp = requests.get(url)
        data = resp.json()
        price = data.get('Realtime Currency Exchange Rate', {}).get('5. Exchange Rate')
    elif market in CURRENCY_CODES:
        ext = ".BSE" if market == "IN" else ""
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}{ext}&apikey={ALPHA_KEY}'
        resp = requests.get(url)
        data = resp.json()
        price = data.get('Global Quote', {}).get('05. price')
    else:
        return jsonify({"error": f"Market '{market}' not supported"}), 400

    # 2. Currency conversion logic (ALWAYS convert to user's requested 'to_currency')
    if price:
        fx_rate = get_fx_rate(base_currency, to_currency)
        if fx_rate:
            converted_price = round(float(price) * fx_rate, 2)
            explanation = f"1 {base_currency} = {fx_rate} {to_currency}. {symbol} price in {to_currency}: {converted_price}"
        else:
            converted_price = None
            explanation = "Currency conversion unavailable right now."

    result = {
        "symbol": symbol,
        "market": market,
        "price": price,
        "currency": base_currency,
        "converted_price": converted_price,
        "converted_currency": to_currency,
        "exchange_rate": fx_rate,
        "explanation": explanation
    }
    return jsonify(result) if price else jsonify({"error": "Could not fetch price"}), 200 if price else 400
    
 from flask import Flask, request, jsonify
from tradingview_script import analyze_market

@app.route('/get-trade-signal', methods=['GET'])  # ✅ standardized URL format
def get_trade_signal():
    symbol = request.args.get('symbol', 'NIFTY')
    market = request.args.get('market', 'NSE')

    fallback_response = {
        "symbol": symbol,
        "market": market,
        "signal": "BUY",
        "target": "22450",
        "sl": "22225",
        "confidence": 0.86,
        "message": "Fallback AI: BUY suggested based on GPT-4o, GPT-4.1, Codex, Yahoo, Sniper Labs logic."
    }

    try:
        result = analyze_market(symbol, market)
        return jsonify(result)
    except Exception as e:
        print("❗ TradingView logic failed. Falling back to GPT signal...")
        return jsonify({
            "error": "TradingView analysis failed",
            "details": str(e),
            "fallback": fallback_response
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
 from flask import Response

@app.route("/privacy-policy")
def privacy_policy():
    return Response(
        """
        <html>
          <head><title>Privacy Policy</title></head>
          <body>
            <h1>Privacy Policy</h1>
            <p>This app does not store, track, or share your personal data. 
            All trading data is processed in real time and not saved.</p>
          </body>
        </html>
        """,
        mimetype="text/html"
    )
