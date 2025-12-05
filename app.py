from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/price')
def get_price():
    symbol = request.args.get('symbol', '').upper().strip()
    if not symbol:
        return jsonify({'error': 'Invalid symbol'}), 400

    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        if data.empty:
            raise ValueError("No data found")
        price = round(data['Close'].iloc[-1], 2)
        return jsonify({'symbol': symbol, 'price': price})
    except Exception:
        return jsonify({'error': 'Invalid symbol'}), 400

@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    import os
    print("Static folder:", app.static_folder)
    print("Expected path:", os.path.join(app.static_folder, 'index.html'))
    app.run(debug=True)