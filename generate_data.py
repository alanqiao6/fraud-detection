import random
import string
import pandas as pd
import numpy as np
from faker import Faker

faker = Faker()

def generate_uuid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

def generate_address(country_code=None):
    if country_code is None:
        country_code = random.choice(locales)
    return {
        "addressLine": faker.street_address(),
        "city": faker.city(),
        "stateCode": faker.state_abbr(),
        "postalCode": faker.postcode(),
        "countryCode": country_code
    }

# 📋 Generate Users
locales = ['KY', 'MY', 'US', 'CA', 'MX', 'FR', 'DE', 'SA', 'AU', 'KO']
non_us_locales = [loc for loc in locales if loc != 'US']
num_users = 20000

users = []

# US proportion
us_fraction = random.uniform(0.5, 0.75)
num_us_users = int(us_fraction * num_users)
num_other_users = num_users - num_us_users

# US users
for _ in range(num_us_users):
    user = {
        "uuid": generate_uuid(),
        "username": f"user_{_}",
        "locale": "US"
    }
    users.append(user)

# Other locales evenly
other_locales_cycle = np.tile(non_us_locales, int(np.ceil(num_other_users / len(non_us_locales))))
other_locales_cycle = other_locales_cycle[:num_other_users]

for idx in range(num_us_users, num_users):
    user = {
        "uuid": generate_uuid(),
        "username": f"user_{idx}",
        "locale": other_locales_cycle[idx - num_us_users]
    }
    users.append(user)

users_df = pd.DataFrame(users)
users_df['email'] = users_df['username'].apply(lambda x: faker.email())

print(users_df['locale'].value_counts())
print(f"Unique UUIDs: {users_df['uuid'].nunique()}")

# 📋 Generate Shipments per User
shipment_rows = []

for _, user in users_df.iterrows():
    num_shipments = random.randint(1, 7)
    for _ in range(num_shipments):
        ship_from = generate_address(country_code=user['locale'])
        is_domestic = random.choices([True, False], weights=[95, 5])[0]
        if is_domestic:
            ship_to_country = ship_from['countryCode']  # same country
        else:
            # pick a different country than ship_from but from allowed locales
            other_locales = [loc for loc in locales if loc != ship_from['countryCode']]
            ship_to_country = random.choice(other_locales)
        ship_to = generate_address(country_code=ship_to_country)
        account_number = faker.credit_card_number()

        row = {
            "uuid": user['uuid'],
            "username": user['username'],
            "email": user['email'],
            "locale": user['locale'],

            # Ship From
            "shipFrom_addressLine": ship_from['addressLine'],
            "shipFrom_city": ship_from['city'],
            "shipFrom_stateCode": ship_from['stateCode'],
            "shipFrom_postalCode": ship_from['postalCode'],
            "shipFrom_countryCode": ship_from['countryCode'],

            # Ship To
            "shipTo_addressLine": ship_to['addressLine'],
            "shipTo_city": ship_to['city'],
            "shipTo_stateCode": ship_to['stateCode'],
            "shipTo_postalCode": ship_to['postalCode'],
            "shipTo_countryCode": ship_to['countryCode'],

            # Payment Info
            "payment_accountNumber": account_number,
            "payment_addressLine": ship_from['addressLine']  # same as shipFrom
        }
        shipment_rows.append(row)

# 📋 Save Shipments Table
shipments_df = pd.DataFrame(shipment_rows)
print(shipments_df.head())

shipments_df.to_csv("users_with_shipments.csv", index=False)

print(f"✅ Created shipments table with {len(shipments_df)} rows in users_with_shipments.csv")
