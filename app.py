from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Nifty Sniper 🔱 is LIVE!"

@app.route('/getTradeSignal', methods=['POST'])
def get_trade_signal():
    return jsonify({"signal": "BUY", "target": 100, "sl": 95})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
