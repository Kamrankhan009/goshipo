
import requests

# shippo_api_key = "shippo_live_d31bf486ebbff553e9d4b9dac8013b30c9bfc33a"
# shippo_api_key = 'shippo_test_0de636e44a648051475e1cfe3cbd039e0419bacd'
shippo_api_key = 'shippo_live_fc161f2fafa5b6b1c181ef4ca9ee861cf2b73f31'

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
        print(valid_carrier_account_id)


import shippo

shippo_api_key = 'shippo_live_fc161f2fafa5b6b1c181ef4ca9ee861cf2b73f31'
shippo.config.api_key = shippo_api_key

sender_address = {
    "name": "xyz",
    "street1": "71 ST. NICHOLAS DRIVE",
    "city": "NORTH POLE",
    "state": "AK",
    "zip": "99705",
    "country": "US",
    "phone": "", 
    "email": ""
}

recipient_address = {
    "name": "john",
    "street1": "2417 TONGASS AVE",
    "city": "KETCHIKAN",
    "state": "AK",
    "zip": "99901",
    "country": "US",
    "phone": "",
    "email": ""
}

parcel = {
    "length": "3",
    "width": "3",
    "height": "3",
    "weight": "3",
    "distance_unit": "cm",
    "mass_unit": "kg"
}

shipment = shippo.Shipment.create(
    address_from=sender_address,
    address_to=recipient_address,
    parcels=[parcel],
    carrier_accounts=[valid_carrier_account_id]
)

new_data = shippo.Shipment.get_rates(shipment.object_id, sync=True)

print(new_data)
# for rate in rates:
#     if rate["provider"] == "fedex":
#         print("FedEx Rate:", rate["amount"])
