from flask import Flask, render_template, request, jsonify, flash, session, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate

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
# api_key = "shippo_test_effec733b0707aa4561e174fa72fda07e8c39fd6"

#themaitham test
api_key = "shippo_test_cba653fa4b9033df466bccb48c9eadaf7966f85b"


# shippo.api_key = api_key
shippo.config.api_key = api_key
# # shippo_live_d31bf486ebbff553e9d4b9dac8013b30c9bfc33a
# # api_key= "shippo_live_d31bf486ebbff553e9d4b9dac8013b30c9bfc33a"
# # api_key = "shippo_test_4be9534dc1f3440b8d3943690c81882757e696b8"
# api_key = "shippo_live_fc161f2fafa5b6b1c181ef4ca9ee861cf2b73f31"

from api1 import API1
from api2 import API2
from comparing_result import compare_and_choose
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "youwillneverguesss"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.sqlite'  # SQLite for simplicity, use a proper DB in production
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# app.secret_key = "Youwillneverquess"
# run_with_ngrok(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    is_active = db.Column(db.Boolean, default = True)
    

class Address_book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255))
    address = db.Column(db.Text)
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(255))
    name2 = db.Column(db.String(255))
    address2 = db.Column(db.Text)
    city2 = db.Column(db.String(255))
    country2 = db.Column(db.String(255))
    state2 = db.Column(db.String(255))
    zip_code2 = db.Column(db.String(255))
    
    

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    download_link = db.Column(db.Text)
    payment_amount = db.Column(db.String)
    payment_status = db.Column(db.String)
    object_id = db.Column(db.Text)
    owner = db.Column(db.String)
    email = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)



@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

Migrate(app, db)
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



@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

# Create a route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(email=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('calculate'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html')



# Define a route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        user = User(name=name, email=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/')
@app.route("/calculate", methods = ['POST','GET'])
def calculate():
    if request.method == "POST":
        print(request.form)
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
        
        
        # name,address,city,country,state,zip_code
        if current_user.is_authenticated:
        # Check if a similar address entry already exists
            existing_entry = Address_book.query.filter(
            Address_book.name == namefrom,
            Address_book.address == addressFrom,
            Address_book.city == cityfrom,
            Address_book.country == countryfrom,
            Address_book.state == statefrom,
            Address_book.zip_code == zipfrom,
            Address_book.name2 == nameto,
            Address_book.address2 == addressto,
            Address_book.country2 == countryto,
            Address_book.city2 == cityto,
            Address_book.state2 == stateto,
            Address_book.zip_code2 == zipto,
            Address_book.user_id == current_user.id
            ).first()

            if existing_entry:
                print("done")
            else:
                # Create a new address entry
                address = Address_book(
                    name=namefrom,
                    address=addressFrom,
                    city=cityfrom,
                    country=countryfrom,
                    state=statefrom,
                    zip_code=zipfrom,
                    name2=nameto,
                    address2=addressto,
                    country2=countryto,
                    city2=cityto,
                    state2=stateto,
                    zip_code2=zipto,
                    user_id=current_user.id
                )
                db.session.add(address)
                db.session.commit()
        else:
            pass







        
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



            print(address_from)
            print(address_to)
            print(parcel)

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
            print(other_fedex_rates)
            # print(other_fedex_rates)
            # shippo.config.api_key = "shippo_live_05c8397eb96c1618c677ea52c74cd3f15eafadbf"
            shippo.config.api_key = "shippo_test_effec733b0707aa4561e174fa72fda07e8c39fd6"
            fedex_rates2, other_fedex_rates2,rate_data2 = API2(address_from, address_to, parcel)

            # print(other_fedex_rates2)
            data2 = compare_and_choose(other_fedex_rates, other_fedex_rates2)
            print("________________________________________")
            print(data2)         
            print("__________________________________________")
            return render_template("result.html", rate = rate_data, best_rate = fedex_rates, other_rate =data2)
        except Exception as e:
            pass
        
    return render_template("rates.html")



@app.route('/check-rates/<id>')
@login_required
def check_rates(id):
    address = Address_book.query.get(id)
    print(address.zip_code)
    return render_template('rates.html', address=address)
    


@app.route("/payment/<object_id>/<owner>/<amount>")
@login_required
def payment(object_id, owner, amount):
    return render_template("payment.html", object_id = object_id, owner=owner, amount = amount)


@app.route('/charge', methods=['POST'])
@login_required
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
            order = Orders(
                user_id = current_user.id,
                payment_amount = amount,
                payment_status = payment_intent.status,
                object_id = object_id,
                owner = owner,
                email = email
            )
            db.session.add(order)
            db.session.commit()
            payment_info['payment_intent_id'] = payment_intent.id
            payment_info['payment_amount'] = amount
            payment_info['payment_status'] = payment_intent.status
            payment_info['object_id'] = object_id
            payment_info['owner'] = owner
            payment_info['email'] = email
            session['Label'] = payment_info
            return payment_intent.client_secret
            
        except Exception as e:
            print(e)
            return jsonify(error=str(e)), 500
        

@app.route("/success")
@login_required
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
            link = new_data.label_url
            # print(shippo.orders(transaction.object_id))

            # download_pdf(new_data.label_url)
            print("herrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
            try:
                order = Orders.query.filter_by(user_id=current_user.id).order_by(Orders.timestamp.desc()).first()

                order.download_link = link
                db.session.commit()
            except Exception as e:
                print(e)
            print("___________________________finished_______________--")
            try:
                send_mail(data['email'],new_data.label_url)
            except Exception as e:
                print(e)
            return redirect(url_for('download'))

        else:
            
            return transaction.messages
    except Exception as e:
         
         return e

@app.route("/order")
def order1():

    return shippo.Transaction.retrieve("afe952f1cc9e4ee28ba35c1a7bc837ac")


@app.route("/profile")
@login_required
def download():
    
    return render_template('profile.html')

@app.route('/address_book')
@login_required
def address_book():
    address = Address_book.query.filter_by(user_id = current_user.id).all()
    return render_template("address_book.html", address = address)

@app.route("/pdf_download/<id>")
@login_required
def download_pdf(id):
    # pdf_link = session['pdf_link']

    data = Orders.query.filter_by(id=id).first()
    pdf_link = data.download_link
    import os
    import requests
    from flask import send_file
    # Replace 'your_pdf_link' with the actual link to the PDF file
    # pdf_link = 'https://deliver.goshippo.com/afe952f1cc9e4ee28ba35c1a7bc837ac.pdf?Expires=1725826386&Signature=jQrcfOLDwBsYkdw-NVbN~ppCUIqIx~qm-QjnUnQo1OIqdasLtSf~YklE~tRKsH~lVJ7JIBohaP6k-g99aHY1JszmJMzP1sRa7F4a1GVtk5pDwXc41ecCkLnf1xIG0~7eMDQw98AXbcaemjSJidRT6SpZwnPcnu8HWqhnkgIGJpa45H9rCr4NhFPAbhgUTLBQ~yBfflRF3BYvvwffPmMjgqHwXssfWZbz2MwSQTeAYKDKNaFXVtQAZcmHY1IHoqcvDalygH7UOH1oGazy~wno77YWfbzqOilWmY5LHXdFxXEObqg~NV~RZjZpOMpzetbBsOwKXre0StylLeI~V4c8Cw__&Key-Pair-Id=APKAJRICFXQ2S4YUQRSQ'

    # Use the requests library to fetch the PDF file
    print(pdf_link)
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
 


@app.route('/process_csv', methods=['POST'])
def process_csv():
    # Check if a CSV file is uploaded
    if 'csv_file' not in request.files:
        return "No CSV file provided", 400
    
    csv_file = request.files['csv_file']
    
    # Check if the file has a CSV extension
    if not csv_file.filename.endswith('.csv'):
        return "File is not a CSV", 400

    # Parse the CSV file
    csv_data = []
    for line in csv_file.readlines():
        line = line.decode().strip()
        if line:  # Ignore empty lines
            row = line.split(',')
            csv_data.append(row)

    # Assuming that the CSV file has a specific structure (as mentioned in your example),
    # extract the relevant data.

    print(csv_data)
    address_from = csv_data[1][0]  # Change the row/column index as needed
    
    
    zip_from = csv_data[1][3]
    state_from = csv_data[1][2]
    address_to = csv_data[1][5]  # Change the row/column index as needed

    city_from = csv_data[1][1]
    city_to = csv_data[1][6]

    country_from = csv_data[1][4]
    country_to = csv_data[1][9]

    zip_to = csv_data[1][8]
    state_to = csv_data[1][7]

    # You can now use the extracted data as needed
    # For example, you can return it as a JSON response
    response_data = {
        "Address From": address_from,
        "ZIP From": zip_from,
        "State From": state_from,
        "Address To": address_to,
        "ZIP To": zip_to,
        "State To": state_to,
        "city from": city_from,
        "city to": city_to,
        "country from": country_from,
        "country to": country_to
    }

    return render_template('rates.html', address_from = address_from, address_to = address_to, zip_from=zip_from, zip_to=zip_to,
                           state_from = state_from, state_to= state_to,
                           city_from= city_from, city_to=city_to, country_from=country_from, country_to=country_to, 
                           name_from = "testing", name_to="testing2",
                           csv_data = True)
    


@app.route("/FAQ")
def FAQ():
    return render_template('faq.html')    


@app.route('/support')
def customer_support():
    return render_template("support.html")


@app.route('/order_label')
def order_label():
    order = Orders.query.filter_by(user_id = current_user.id).all()
    return render_template("download.html", order = order)

@app.route("/connection")
def connection():
    return render_template("connect_with.html")
if __name__ == "__main__":
    app.run(debug=True)