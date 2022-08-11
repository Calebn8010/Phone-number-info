from flask import Flask, render_template, redirect, request, session
from flask_session import Session

# libphone number setup
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from phonenumbers import timezone

# import gotenv library for environment variables
from dotenv import load_dotenv
import os

# email function setup
import smtplib, ssl
from email.message import EmailMessage

def configure():
    load_dotenv()

app = Flask(__name__)

currphoneinfo = {"number":"Unknown","country":"Unknown", "state":"Unknown", "carrier":"Unknown", "timezone":"Unknown"}

@app.route('/', methods=["GET", "POST"])
def get_phone_number():
    print(os.environ.get('password'))
    if request.method == "POST":

        # check if user submitted phone number
        if request.form.getlist("phonenumber") != None and request.form.getlist("phonenumber") != []:
            # get user input
            input = request.form.get("phonenumber")
            # add + in front of areacode
            input = f"+{input}"
            # check if user input is valid phone number
            try:
                possiblephonenum = phonenumbers.parse(input, None)
                print(phonenumbers.is_valid_number(possiblephonenum))
                # if phone number is not valid return invalid html page
                if phonenumbers.is_valid_number(possiblephonenum) == False:
                    return render_template("invalidnumber.html")
            # if phonenumber is valid function is not able to complete with user input, return invalid html page    
            except:
                return render_template("invalidnumber.html")
            
            # after user input makes it through phone number checks, create number string variable
            number = input
            ch_number = phonenumbers.parse(number, "CH")
            print(ch_number)
            # update global dictionary
            currphoneinfo["number"] = ch_number
            country = geocoder.country_name_for_number(ch_number, "en")
            print(country)
            state = geocoder.description_for_number(ch_number, "en")
            print(state)
            # update global dictionary
            currphoneinfo["state"] = state
            #print(phonenumbers.parse(number, "CH"))
            if country == "" or country == None:
                country = "Unknown"
            # update global dictionary
            currphoneinfo["country"] = country
            if state == "" or state == None:
                state = "Unknown"
            # update global dictionary
            currphoneinfo["state"] = state
            
            service_number = phonenumbers.parse(number, "RO")
            print(carrier.name_for_number(service_number, "en"))
            carrierinfo = carrier.name_for_number(service_number, "en")
            #print(service_number)
            if carrierinfo == "" or carrierinfo == None:
                carrierinfo = "Unknown"
            # update global dictionary
            currphoneinfo["carrier"] = carrierinfo

            
            gb_number = phonenumbers.parse(number, "GB")
            print(timezone.time_zones_for_number(gb_number))
            timezones = (timezone.time_zones_for_number(gb_number))
            if len(timezones) > 1 and len(timezones) < 5:
                timezones = timezones[0]
            if len(timezones) > 5:
                timezones = "Unknown"
            if len(timezones) == 1:
                timezones = timezones[0]
            # update global dictionary
            currphoneinfo["timezone"] = timezones
            return render_template("indexfilled.html", country=country, state=state, carrier=carrierinfo, timezones=timezones)

        # else user submitted email form
        else:
            print(request.form.get("email"))
            # get personal email address from user form input
            sendto = request.form.get("email")
            print(currphoneinfo["carrier"])

            # configure emailmessage
            msg = EmailMessage()
            msg['Subject'] = 'Phone Number Check Report'
            msg['From'] = os.environ.get('gmail')
            msg['To'] = sendto 
            content = f'Thanks for using check-international-number! Here is your phone check information. \n \n {currphoneinfo["number"]} \n Country: {currphoneinfo["country"]}\n State / Local area: {currphoneinfo["state"]}\n Carrier: {currphoneinfo["carrier"]}\n Timezone: {currphoneinfo["timezone"]}'
            msg.set_content(content)
            # send email with phone information 
            try:

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(os.environ.get('gmail'), os.environ.get('password')) 
                    smtp.send_message(msg)
            except:
                return render_template("invalidemail.html", country=currphoneinfo["country"], state=currphoneinfo["state"], carrier=currphoneinfo["carrier"], timezones=currphoneinfo["timezone"])
                

    return render_template("index.html")