from flask import Flask, request
import africastalking
import os
import requests

AFRICASTALKING_API_KEY = "f9adeb64e252e6ab6ad32cfb36d68e924d6174baada05e58e37ce79aa7ac68d5"
app = Flask(__name__)
username = "sandbox"
api_key = AFRICASTALKING_API_KEY
africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_SMS(sms_phone_number):
    sms_response = sms.send(
        "Hello, I am your personal assistant. How may I help you?",
        sms_phone_number)

    print(sms_response)
    

send_SMS(+255689737839)               
                
            

