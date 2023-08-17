api_key= "shippo_live_d31bf486ebbff553e9d4b9dac8013b30c9bfc33a"
import shippo

# shippo.api_key = api_key
shippo.config.api_key = api_key

address_from = {
            "name": "",
            "street1": "588 Walnut St",
            "city": " Newton",
            "state": 'MA',
            "zip": '02460',
            "country": 'USA'
            }

address_to = {
                "name": "",
                "street1": "98 Raider Rd",
                "city": "North Brunswick Township",
                "state": 'NJ',
                "zip": '08902',
                "country": 'USA'
            }

parcel = {
                "length": 23,
                "width": 23,
                "height": 2,
                "distance_unit": 'in',
                "weight": '2',
                "mass_unit": 'lb'
            }
shipment = shippo.Shipment.create(
            address_from = address_from,
            address_to = address_to,
            parcels = [parcel]
            )


new_data = shippo.Shipment.get_rates(shipment.object_id, sync=True)

print(new_data)
