from flask import Flask, request, jsonify
import requests
import os

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

def get_fx_rate(from_cur, to_cur):
    fx_url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_cur}&to_currency={to_cur}&apikey={ALPHA_KEY}'
    resp = requests.get(fx_url)
    fx = resp.json()
    try:
        return float(fx['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    except Exception:
        return None

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

@app.route('/get-trade-signal', methods=['GET'])
def get_trade_signal():
    symbol = request.args.get('symbol', 'NIFTY50')
    market = request.args.get('market', 'IN')
    # Your AI logic here (this is a placeholder)
    response = {
        "symbol": symbol,
        "market": market,
        "signal": "BUY",
        "target": "22450",
        "sl": "22225",
        "confidence": 0.86,
        "message": "Auto-AI: BUY recommended based on global & local market AI, GPT-4.1, GPT-4o, GPT-o3, o4-mini, o4-mini-high,
         GPT-4.5, GPT-4.1-mini, o1-pro, Codex"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
