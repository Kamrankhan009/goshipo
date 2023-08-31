from flask import Flask, render_template, request
import requests


import shippo
# from flask_ngrok import run_with_ngrok
# api_key= "shippo_live_d31bf486ebbff553e9d4b9dac8013b30c9bfc33a"

# mine api key
api_key = "shippo_live_fc161f2fafa5b6b1c181ef4ca9ee861cf2b73f31"

#client api key
# api_key = "shippo_live_05c8397eb96c1618c677ea52c74cd3f15eafadbf"
# shippo.api_key = api_key
shippo.config.api_key = api_key
# # shippo_live_d31bf486ebbff553e9d4b9dac8013b30c9bfc33a
# # api_key= "shippo_live_d31bf486ebbff553e9d4b9dac8013b30c9bfc33a"
# # api_key = "shippo_test_4be9534dc1f3440b8d3943690c81882757e696b8"
# api_key = "shippo_live_fc161f2fafa5b6b1c181ef4ca9ee861cf2b73f31"

from api1 import API1
from api2 import API2
from comparing_result import compare_and_choose


app = Flask(__name__)
# run_with_ngrok(app)



def get_carrier_object_id():
    headers = {
    "Authorization": f"ShippoToken {shippo_api_key}",
    "Content-Type": "application/json"
    }

    response = requests.get("https://api.goshippo.com/v1/carrier_accounts/", headers=headers)
    if response.status_code == 200:
        carrier_accounts = response.json()["results"]
        if carrier_accounts:

            valid_carrier_account_id = ""
            for value in carrier_accounts:
                if value['carrier'] == "fedex" and value['account_id'] == "279007477":
                    valid_carrier_account_id = value['object_id']
    
    return valid_carrier_account_id


@app.route("/calculate", methods = ['POST','GET'])
def calculate():
    if request.method == "POST":

        addressFrom = request.form.get('address')
        namefrom = request.form.get('name')
        zipfrom = request.form.get('addressToZip')
        cityfrom = request.form.get('city')
        statefrom = request.form.get('state')
        countryfrom = request.form.get('country')


        addressto = request.form.get('address2')
        nameto = request.form.get('name2')
        zipto = request.form.get('addressToZip2')
        cityto = request.form.get('city2')
        stateto = request.form.get('state2')
        countryto = request.form.get('country2')


        packageType = request.form.get('packageType')
        lenght = request.form.get('length')
        width = request.form.get('width')
        height = request.form.get('height')
        if not height:
            height = 0.1
        unit = request.form.get('unit')
        weight = request.form.get('weight')
        weight_unit = request.form.get('weight-unit')
        

        
        try:
            address_from={
            "name": namefrom, #"John Smith",
            "street1": addressFrom,#"1234 Main Street",
            "city": cityfrom,#"San Francisco",
            "state": statefrom,#"CA",
            "zip":  zipfrom,#"94111",
            "country":countryfrom, #"US",
            "phone": "",
            "email": "",
            }
            address_to={
                "name": nameto,#"Alice Johnson",
                "street1":addressto, #"5678 Elm Street",
                "city": cityto,#"Los Angeles",
                "state": stateto,#"CA",
                "zip": zipto,#"90001",
                "country": countryto, #"US",
                "phone": "",
                "email": "",
            }
            parcel={
                "length": lenght,
                "width": width,
                "height": height,
                "distance_unit": unit,
                "weight": weight,
                "mass_unit": weight_unit,
            }



            headers = {
                "Authorization": f"ShippoToken ",
                "Content-Type": "application/json"
            }

            data = {
                "address_from": address_from,
                "address_to": address_to, 
                "parcels":[parcel]
            }
      

            fedex_rates, other_fedex_rates,rate_data = API1(address_from, address_to, parcel)
            shippo.config.api_key = "shippo_live_05c8397eb96c1618c677ea52c74cd3f15eafadbf"
            fedex_rates2, other_fedex_rates2,rate_data2 = API2(address_from, address_to, parcel)

            data2 = compare_and_choose(other_fedex_rates, other_fedex_rates2)

            # print("____________________________________________")
            # print(data2)

            return render_template("results.html", rate = rate_data, best_rate = fedex_rates, other_rate =data2)
        except Exception as e:
            print("hello world")
            print(e)
        
    return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)