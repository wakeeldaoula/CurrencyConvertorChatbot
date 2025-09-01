# Backend for our currency convertor chatbot using flask
# First we deploy this code on ngrok. Because it is necessary for our backend to be online for connecting with 
# dialogflow chatbot. And for testing this is the best free software to deploy the model for limited time.
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    print(data)

    sourceCurrency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    targetCurrency = data['queryResult']['parameters']['currency-name']

    url = f"https://api.currencyapi.com/v3/latest?apikey=cur_live_yE5VgkxHKnqgx8JSiAHdH7PlmZUI0JHId7TG3dwg&base_currency={sourceCurrency}&currencies={targetCurrency}"
    response = requests.get(url)   # ✅ ye correct hai
    output = response.json()       # ✅ response ko json mein convert karo

    # Conversion factor nikalna
    CF = output["data"][targetCurrency]["value"]

    # Final target value
    targetValue = amount * CF
    targetValue = round(targetValue, 2)

    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount,sourceCurrency,targetValue,targetCurrency)
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
