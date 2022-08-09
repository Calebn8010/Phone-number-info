from flask import Flask, render_template, redirect, request, session
from flask_session import Session

import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from phonenumbers import timezone

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def get_phone_number():
    if request.method == "POST":
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
        country = geocoder.country_name_for_number(ch_number, "en")
        print(country)
        state = geocoder.description_for_number(ch_number, "en")
        print(state)
        #print(phonenumbers.parse(number, "CH"))
        if country == "" or country == None:
            country = "Unkown"

        if state == "" or state == None:
            state = "Unkown"
        
        service_number = phonenumbers.parse(number, "RO")
        print(carrier.name_for_number(service_number, "en"))
        carrierinfo = carrier.name_for_number(service_number, "en")
        #print(service_number)
        if carrierinfo == "" or carrierinfo == None:
            carrierinfo = "Unkown"

        
        gb_number = phonenumbers.parse(number, "GB")
        print(timezone.time_zones_for_number(gb_number))
        timezones = (timezone.time_zones_for_number(gb_number))
        if len(timezones) > 1 and len(timezones) < 5:
            timezones = timezones[0]
        if len(timezones) > 5:
            timezones = "Unknown"
        print(timezones)
        return render_template("indexfilled.html", country=country, state=state, carrier=carrierinfo, timezones=timezones)
    return render_template("index.html")