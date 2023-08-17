from flask import Flask, render_template, request
import requests
# api_key= "shippo_live_d31bf486ebbff553e9d4b9dac8013b30c9bfc33a"
# api_key = "shippo_test_4be9534dc1f3440b8d3943690c81882757e696b8"
api_key = "shippo_live_38282379a39fc7fc8128ab78e05b09afa9922cfd"
import shippo

# shippo.api_key = api_key
shippo.config.api_key = api_key


app = Flask(__name__)



@app.route("/calculate", methods = ['POST','GET'])
def calculate():
    if request.method == "POST":
        # [('addressToZip', '33234'), ('addressFrom', '12323'), ('packageType', 'polymailer'),
        # ('length', '1'), ('width', '2'), ('height', ''), ('unit', 'cm'), ('weight', '22'), ('weight-unit', 'lbs')]
        print(request.form)
        abc =[('address', 'Banna Road'), ('name', 'testing'),
           ('addressToZip', '14700'), ('city', 'Patiala'), ('state', 'abc'),
             ('country', 'Pakistan'),
              
               ('address2', 'Banna Road'), ('name2', ''),
               ('addressToZip2', '147003'), ('city2', 'Patiala'), ('state2', ''), 
               ('country2', 'Pakistan'), ('packageType', 'polymailer'), 
          ('length', '1'), ('width', '2'), ('height', ''), ('unit', 'cm'),
            ('weight', '1'), ('weight-unit', 'lb')]
        

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

            shipment = shippo.Shipment.create(
            address_from = address_from,
            address_to = address_to,
            parcels = [parcel]
            )

        

            new_data = shippo.Shipment.get_rates(shipment.object_id, sync=True)
            # currency_code = "USD"  # Set your desired currency code
            # base_url = f"https://api.goshippo.com/rates/{shipment.object_id}"
            # headers = {"Authorization": f"ShippoToken {api_key}"}
            # response = requests.get(base_url, headers=headers)
            print(new_data)
            
            rate_data = new_data['results']
            # for rate in rate_data:
            #     amount = rate["amount"]
            #     currency = rate["currency_local"]
            #     provider = rate["provider"]
            #     image = rate['provider_image_200']
            
            return render_template("results.html", rate = rate_data)
        except Exception as e:
            print("hello world")
            print(e)
        
    return render_template("index.html")



# shipment = shippo.Shipment.create(
#     address_from = address_from,
#     address_to = address_to,
#     parcels = [parcel]
#     )



if __name__ == "__main__":
    app.run(debug = True)