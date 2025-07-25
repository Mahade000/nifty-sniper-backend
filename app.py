from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Safely load your API key from Fly.io secrets or Render environment
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

@app.route('/')
def home():
    return "Nifty Sniper 🔱 is LIVE!"

@app.route('/get-live-price', methods=['GET'])
def get_live_price():
    symbol = request.args.get('symbol', 'AAPL')      # Example: AAPL, RELIANCE.BSE, BTCUSD
    market = request.args.get('market', 'US')        # Example: US, IN, CRYPTO

    if not ALPHA_VANTAGE_API_KEY:
        return jsonify({"error": "API key not set on server"}), 500

    # Pick API endpoint based on market type
    if market == 'US' or market == 'IN':
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
        resp = requests.get(url)
        data = resp.json()
        price = data.get('Global Quote', {}).get('05. price')
    elif market == 'CRYPTO':
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency=USD&apikey={ALPHA_VANTAGE_API_KEY}'
        resp = requests.get(url)
        data = resp.json()
        price = data.get('Realtime Currency Exchange Rate', {}).get('5. Exchange Rate')
    else:
        return jsonify({"error": "Unsupported market"}), 400

    if price:
        return jsonify({"symbol": symbol, "market": market, "price": price})
    else:
        return jsonify({"error": "Could not fetch price"}), 400

@app.after_request
def add_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache"
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
