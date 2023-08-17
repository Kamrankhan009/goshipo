
data={
  "address_from": {
    "city": "",
    "company": "",
    "country": "US",
    "email": "",
    "is_complete": False,
    "is_residential": None,
    "name": "",
    "object_id": "b0468cdc499049e899ea70fe8fd3f12e",
    "phone": "",
    "state": "VA",
    "street1": "",
    "street2": "",
    "street3": "",
    "street_no": "",
    "test": True,
    "validation_results": {},
    "zip": "24550"
  },
  "address_return": {
    "city": "",
    "company": "",
    "country": "US",
    "email": "",
    "is_complete": False,
    "is_residential": None,
    "name": "",
    "object_id": "b0468cdc499049e899ea70fe8fd3f12e",
    "phone": "",
    "state": "VA",
    "street1": "",
    "street2": "",
    "street3": "",
    "street_no": "",
    "test": True,
    "validation_results": {},
    "zip": "24550"
  },
  "address_to": {
    "city": "",
    "company": "",
    "country": "US",
    "email": "",
    "is_complete": False,
    "is_residential": None,
    "name": "",
    "object_id": "803a46e74cc9413fad08328b0d2c8830",
    "phone": "",
    "state": "AL",
    "street1": "",
    "street2": "",
    "street3": "",
    "street_no": "",
    "test": True,
    "validation_results": {},
    "zip": "35004"
  },
  "alternate_address_to": None,
  "carrier_accounts": [],
  "customs_declaration": None,
  "extra": {},
  "messages": [
    {
      "code": "",
      "source": "ShippoCommon",
      "text": "Attribute \"address_from.name\" must not be empty."
    },
    {
      "code": "",
      "source": "DHLExpress",
      "text": "Shippo's DHL Express master account doesn't support shipments to inside of the US"
    }
  ],
  "metadata": "",
  "object_created": "2023-08-12T04:05:30.224Z",
  "object_id": "cfddab64dc104a70afc11032a323e5df",
  "object_owner": "kamrankhan567855@gmail.com",
  "object_updated": "2023-08-12T04:05:30.436Z",
  "order": None,
  "parcels": [
    {
      "distance_unit": "cm",
      "extra": {},
      "height": "0.1000",
      "length": "2.0000",
      "line_items": [],
      "mass_unit": "lb",
      "metadata": "",
      "object_created": "2023-08-12T04:05:30.192Z",
      "object_id": "b73d33c015b14650b6653b7f4a8eaf90",
      "object_owner": "kamrankhan567855@gmail.com",
      "object_state": "VALID",
      "object_updated": "2023-08-12T04:05:30.238Z",
      "template": None,
      "test": True,
      "value_amount": None,
      "value_currency": None,
      "weight": "1.0000",
      "width": "1.0000"
    }
  ],
  "rates": [
    {
      "amount": "31.25",
      "amount_local": "31.25",
      "arrives_by": None,
      "attributes": [
        "FASTEST"
      ],
      "carrier_account": "0e35d892fbe24d7a8864d9590adcd04a",
      "currency": "USD",
      "currency_local": "USD",
      "duration_terms": "Overnight delivery to most U.S. locations.",
      "estimated_days": 2,
      "included_insurance_price": None,
      "messages": [],
      "object_created": "2023-08-12T04:05:30.667Z",
      "object_id": "bc84fd5a6ded4388aecc669801211472",
      "object_owner": "kamrankhan567855@gmail.com",
      "provider": "USPS",
      "provider_image_200": "https://shippo-static-v2.s3.amazonaws.com/providers/200/USPS.png",
      "provider_image_75": "https://shippo-static-v2.s3.amazonaws.com/providers/75/USPS.png",
      "servicelevel": {
        "extended_token": "usps_priority_express",
        "name": "Priority Mail Express",
        "parent_servicelevel": None,
        "terms": "",
        "token": "usps_priority_express"
      },
      "shipment": "cfddab64dc104a70afc11032a323e5df",
      "test": True,
      "zone": "4"
    },
    {
      "amount": "6.59",
      "amount_local": "6.59",
      "arrives_by": None,
      "attributes": [
        "BESTVALUE",
        "CHEAPEST"
      ],
      "carrier_account": "0e35d892fbe24d7a8864d9590adcd04a",
      "currency": "USD",
      "currency_local": "USD",
      "duration_terms": "Delivery in 2 to 5 days.",
      "estimated_days": 5,
      "included_insurance_price": None,
      "messages": [],
      "object_created": "2023-08-12T04:05:30.667Z",
      "object_id": "4319222b95bb4a59811f7edea11e8c4c",
      "object_owner": "kamrankhan567855@gmail.com",
      "provider": "USPS",
      "provider_image_200": "https://shippo-static-v2.s3.amazonaws.com/providers/200/USPS.png",
      "provider_image_75": "https://shippo-static-v2.s3.amazonaws.com/providers/75/USPS.png",
      "servicelevel": {
        "extended_token": "usps_ground_advantage",
        "name": "Ground Advantage",
        "parent_servicelevel": None,
        "terms": "",
        "token": "usps_ground_advantage"
      },
      "shipment": "cfddab64dc104a70afc11032a323e5df",
      "test": True,
      "zone": "4"
    }
  ],
  "shipment_date": "2023-08-12T04:05:30.436Z",
  "status": "QUEUED",
  "test": True
}



rate_data = data['rates']
for rate in rate_data:
    amount = rate["amount"]
    currency = rate["currency_local"]
    provider = rate["provider"]
    image = rate['provider_image_200']
    print(f"Rate: {amount} {currency} from {provider} {image}")
# Replace rates_data with the actual variable name holding your JSON data. This code will iterate through each rate in the "rates" list and print the amount, currency, and provider information for each rate. You can modify the code to store or process the extracted data as required.





