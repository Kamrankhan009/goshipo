import shippo
# from flask_ngrok import run_with_ngrok
# api_key= "shippo_live_d31bf486ebbff553e9d4b9dac8013b30c9bfc33a"

# mine api key
# api_key = "shippo_live_fc161f2fafa5b6b1c181ef4ca9ee861cf2b73f31"

# #client api key
# # api_key = "shippo_live_05c8397eb96c1618c677ea52c74cd3f15eafadbf"
# # shippo.api_key = api_key
# shippo.config.api_key = api_key

def API1(address_from, address_to, parcel):
             
    shipment = shippo.Shipment.create(
    address_from = address_from,
    address_to = address_to,
    parcels = [parcel]
    )
        
    new_data = shippo.Shipment.get_rates(shipment.object_id, sync=True)
            
    specified_carrier_account = "609d43244bfe4f90a7021a1945e9a00a"

    fedex_rates = []
    other_fedex_rates = []

    result_data = new_data
    count = 0
    for result in result_data["results"]:

        other_fedex_rates.append(result)
        if result["provider"] == "FedEx" and result["carrier_account"] == specified_carrier_account:
            fedex_rates.append(result)

            # Sort the rates by amount in ascending order
    fedex_rates.sort(key=lambda x: float(x["amount"]))
    other_fedex_rates.sort(key=lambda x: float(x["amount"]))            
    rate_data = new_data['results']

    # print("_______________________________________________________________________")
    # print(other_fedex_rates)

    return fedex_rates, other_fedex_rates, rate_data