from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Nifty Sniper 🔱 is LIVE!"

@app.route('/get-trade-signal', methods=['GET', 'POST'])
def get_trade_signal():
    # Accept capital param from GET or POST
    if request.method == 'POST':
        data = request.json or {}
        capital = int(data.get('capital', 500))
    else:
        capital = int(request.args.get('capital', 500))
    
    # Simple logic for now: (customize as per your real logic)
    entry = 100 + capital // 10
    target = entry + 20
    stoploss = entry - 10

    return jsonify({
        "signal": "BUY",
        "entry": entry,
        "target": target,
        "stoploss": stoploss
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

