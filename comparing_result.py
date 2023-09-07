def compare_and_choose(api1_rates, api2_rates):
    chosen_rates = []
    
    for rate1 in api1_rates:
        service_name1 = rate1['servicelevel']['extended_token'].strip()

        # Try to find a rate with the same service name in api2_rates
        rate2_with_same_name = None
        for rate2 in api2_rates:
            service_name2 = rate2['servicelevel']['extended_token'].strip()
            if service_name1 == service_name2:
                rate2_with_same_name = rate2
                break

        if rate2_with_same_name is not None:
            api1_price = float(rate1['amount'])
            api2_price = float(rate2_with_same_name['amount'])
            
            print(f"comparing api1 {service_name1} with api 2 {service_name2}")
            print(f"Api 1 price {api1_price} and api 2 price {api2_price}")
            # Apply your formula
            adjusted_api2_price = api2_price + 1
            comparison_value = (api1_price - adjusted_api2_price)
            percent_of_result = 0.5 * comparison_value
            adjusted_price = round(percent_of_result + adjusted_api2_price, 1)
            
            print(f"adjusted price {adjusted_price}")
            print(f"api 1 price {api1_price}")
            print(type(api1_price))
            if float(api1_price) < float(adjusted_price):
                chosen_rates.append(rate1)
            else:
                rate2_with_same_name['amount'] = adjusted_price
                rate2_with_same_name['amount_local'] = adjusted_price
                chosen_rates.append(rate2_with_same_name)
        else:
            chosen_rates.append(rate1)
    
    return chosen_rates