from flask import Flask, request
import requests

app = Flask(__name__)


@app.route('/')
def smart_shamba():
    return 'Lima Kijanja'


word_responses = {
    "habari": "Salama, KARIBU SMART SHAMBA Karibu Tukuhudumie",
    "mnatoa huduma gani": "Tunatoa huduma za kukujulisha juu ya hali ya hewa, wadudu wa mazao na pia kukupatia soko la kuuza mazao yako.",
    "mnapatikana wapi": "Tunapatikana Dar Es Salaam jengo la Sky City floor ya 12.",
    "naweza pata maswasiliano yenu": "Unaweza ukapiga namba ya ofisi ambayo ni 0687887685. \n email: smartshambainfo.com \n ",

}


@app.route('/sms_callback', methods=['POST'])
def sms_callback():
    print(request.method)
    print(request.form)
    user_message = request.form["text"]
    sender = request.form["from"]

    response_message = get_response(user_message)
    response_to_sms(sender, response_message)

    return "Success", 201


def get_response(message):
    # Check if the user's message matches any of the word responses in the dictionary
    for word, response in word_responses.items():
        if word in message.lower():
            return response


SANDBOX_API_KEY = "API KEY"


def response_to_sms(recipient_phone_number, message):
    url = "https://api.sandbox.africastalking.com/version1/messaging"
    data = {
        "username": "sandbox",
        "to": recipient_phone_number,
        "message": message,
        "from": "3601"
    }
    headers = {
        "apikey": SANDBOX_API_KEY,
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        response_data = response.json()

        if response_data.get('SMSMessageData') and response_data['SMSMessageData'].get('Recipients'):
            recipients = response_data['SMSMessageData']['Recipients']
            for recipient in recipients:
                if recipient.get('status') != 'Success':
                    raise Exception(
                        f"Failed to send SMS to {recipient.get('number')}: {recipient.get('status')}")
        else:
            raise Exception(
                f"Unexpected response from Africa's Talking API: {response_data}")

    except Exception as e:
        raise Exception(f"Failed to send SMS: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)
