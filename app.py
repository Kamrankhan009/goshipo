from flask import Flask, render_template, request, jsonify, flash, session, redirect, url_for
from flask_mail import Mail, Message

import requests
import stripe

test_key = "pk_test_51NfLmnGZINefu7hyxFBdpdsLsaahaPR039XnKIXL4sL59kXytlfUgzQqtAcpYd19dTpyhcLiUVSlQfRt1gfA7R5a00hScRaAMp"
secret_key = "sk_test_51NfLmnGZINefu7hysYG9JeNmUN5vev5LnrXyg9OVHXWVOMTldFfhyKd2jK5tPufzwVzjq0oAOF8tQVk4oZ9dxT4z00PXYR5jgT"

stripe.api_key = secret_key
import shippo
payments = False
# from flask_ngrok import run_with_ngrok
# api_key= "shippo_live_d31bf486ebbff553e9d4b9dac8013b30c9bfc33a"

# mine api key
# api_key = "shippo_live_fc161f2fafa5b6b1c181ef4ca9ee861cf2b73f31"

#client api key
# api_key = "shippo_live_fdd23133f0d8522faf7cf1a37defa110528f8ddb"

#ladha
# api_key = "shippo_live_05c8397eb96c1618c677ea52c74cd3f15eafadbf" 
#ladha test
api_key = "shippo_test_effec733b0707aa4561e174fa72fda07e8c39fd6"

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
app.secret_key = "Youwillneverquess"
# run_with_ngrok(app)


app_password = "rdixjldwxbgkidhz"
email = "kamrankhan567855@gmail.com"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = email
app.config['MAIL_PASSWORD'] = app_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



payment_info = {}


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

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

@app.route('/')
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
            "country":"USA", #"US",
            "phone": "",
            "email": "",
            }
            address_to={
                "name": nameto,#"Alice Johnson",
                "street1":addressto, #"5678 Elm Street",
                "city": cityto,#"Los Angeles",
                "state": stateto,#"CA",
                "zip": zipto,#"90001",
                "country": "USA", #"US",
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
            # print(other_fedex_rates)
            # shippo.config.api_key = "shippo_live_05c8397eb96c1618c677ea52c74cd3f15eafadbf"
            shippo.config.api_key = "shippo_test_effec733b0707aa4561e174fa72fda07e8c39fd6"
            fedex_rates2, other_fedex_rates2,rate_data2 = API2(address_from, address_to, parcel)

            # print(other_fedex_rates2)
            data2 = compare_and_choose(other_fedex_rates, other_fedex_rates2)
         
            return render_template("result.html", rate = rate_data, best_rate = fedex_rates, other_rate =data2)
        except Exception as e:
            pass
        
    return render_template("rates.html")




@app.route("/payment/<object_id>/<owner>/<amount>")
def payment(object_id, owner, amount):
    return render_template("payment.html", object_id = object_id, owner=owner, amount = amount)


@app.route('/charge', methods=['POST'])
def charge():
    if request.method == 'POST':
        # amount = 1000  # Replace with the desired amount in cents

        amount = request.form.get('amount')
        amount = int(float(amount) * 100)
        object_id = request.form.get('object_id')
        owner = request.form.get('owner')
        email = request.form.get('email')
   
        try:
            # Create a payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card']
            )

         

            # session['Label']
            payment_info['payment_intent_id'] = payment_intent.id
            payment_info['payment_amount'] = amount
            payment_info['payment_status'] = payment_intent.status
            payment_info['object_id'] = object_id
            payment_info['owner'] = owner
            payment_info['email'] = email
            session['Label'] = payment_info

            return payment_intent.client_secret
            
        except Exception as e:
        
            return jsonify(error=str(e)), 500
        



@app.route("/success")
def buy_label():
    try:
        if not session['Label']:
            return redirect("/")
        
        data = session['Label']

        if data['owner'] == "tahirladha03@gmail.com":
            # shippo.config.api_key = "shippo_live_05c8397eb96c1618c677ea52c74cd3f15eafadbf"
            shippo.config.api_key = "shippo_test_effec733b0707aa4561e174fa72fda07e8c39fd6"

        # Purchase the desired rate.
        transaction = shippo.Transaction.create(
            rate=data['object_id'],
            label_file_type="PDF",
            sync=True)
        
        print("________________________________transaction_______________")
        print(transaction)
        print("__________________________________end___________________________")
        if transaction.status == "SUCCESS" or transaction.object_state== "VALID":
            new_data = shippo.Transaction.retrieve(transaction.object_id)
            print("________________________llllllllllllllllllllll")
            print(new_data.label_url)
            # print(shippo.orders(transaction.object_id))

            # download_pdf(new_data.label_url)
            send_mail(data['email'],new_data.label_url)
            session['pdf_link'] = new_data.label_url
            # return redirect(f"/download/{new_data.label_url}")
            return redirect(url_for('download'))

        else:
            
            return transaction.messages
    except Exception as e:
         
         return e

@app.route("/order")
def order1():

    return shippo.Transaction.retrieve("afe952f1cc9e4ee28ba35c1a7bc837ac")


@app.route("/download")
def download():
    # session['pdf_link'] = pdf_link
    pdf_link = session['pdf_link']
    return render_template('download.html', link = pdf_link)


@app.route("/pdf_download")
def download_pdf():

    pdf_link = session['pdf_link']
    import os
    import requests
    from flask import Flask, request, send_file
    # Replace 'your_pdf_link' with the actual link to the PDF file
    # pdf_link = 'https://deliver.goshippo.com/afe952f1cc9e4ee28ba35c1a7bc837ac.pdf?Expires=1725826386&Signature=jQrcfOLDwBsYkdw-NVbN~ppCUIqIx~qm-QjnUnQo1OIqdasLtSf~YklE~tRKsH~lVJ7JIBohaP6k-g99aHY1JszmJMzP1sRa7F4a1GVtk5pDwXc41ecCkLnf1xIG0~7eMDQw98AXbcaemjSJidRT6SpZwnPcnu8HWqhnkgIGJpa45H9rCr4NhFPAbhgUTLBQ~yBfflRF3BYvvwffPmMjgqHwXssfWZbz2MwSQTeAYKDKNaFXVtQAZcmHY1IHoqcvDalygH7UOH1oGazy~wno77YWfbzqOilWmY5LHXdFxXEObqg~NV~RZjZpOMpzetbBsOwKXre0StylLeI~V4c8Cw__&Key-Pair-Id=APKAJRICFXQ2S4YUQRSQ'

    # Use the requests library to fetch the PDF file
    response = requests.get(pdf_link)

    if response.status_code == 200:
        # Define the filename for the downloaded PDF
        filename = 'downloaded_file.pdf'

        # Save the PDF locally
        with open(filename, 'wb') as pdf_file:
            pdf_file.write(response.content)

        # Serve the downloaded PDF as a downloadable file
        return send_file(filename, as_attachment=True)
    else:
        return 'Failed to download the PDF', 404



def send_mail(recipients, pdf_link):
    print(recipients)
    msg = Message('Hello from the other side!',
                   sender = 'kamrankhan567855@gmail.com', recipients = [recipients])
    message_body = f"""
        <html>
        <body>
            <h1>Label</h1>
            <p>This is the email content.</p>
            <p><a href="{pdf_link}">Click here to download</a></p>
        </body>
        </html>
        """
    msg.html = message_body
    mail.send(msg)
    return "Message sent!"
 

if __name__ == "__main__":
    app.run(debug=True)