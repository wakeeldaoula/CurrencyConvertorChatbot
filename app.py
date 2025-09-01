from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Currency Converter Bot Backend is Live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    print(data)

    sourceCurrency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    targetCurrency = data['queryResult']['parameters']['currency-name']

    url = f"https://api.currencyapi.com/v3/latest?apikey=YOUR_API_KEY&base_currency={sourceCurrency}&currencies={targetCurrency}"
    response = requests.get(url)
    output = response.json()

    CF = output["data"][targetCurrency]["value"]
    targetValue = round(amount * CF, 2)

    return jsonify({
        'fulfillmentText': f"{amount} {sourceCurrency} is {targetValue} {targetCurrency}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
