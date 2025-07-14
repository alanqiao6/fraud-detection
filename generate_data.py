import random
import string
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

faker = Faker()

# Configuration
locales = ['KY', 'MY', 'US', 'CA', 'MX', 'FR', 'DE', 'SA', 'AU', 'KO']
non_us_locales = [loc for loc in locales if loc != 'US']
num_users = 20000

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

def random_datetime():
    start = datetime.now() - timedelta(days=30)
    rand_dt = start + timedelta(seconds=random.randint(0, 30*24*60*60))
    return rand_dt.strftime('%Y-%m-%d'), rand_dt.strftime('%H:%M:%S')

# Generate Users
users = []
us_fraction = random.uniform(0.5, 0.75)
num_us_users = int(us_fraction * num_users)
num_other_users = num_users - num_us_users

for _ in range(num_us_users):
    users.append({"uuid": generate_uuid(), "username": f"user_{_}", "locale": "US"})

other_locales_cycle = np.tile(non_us_locales, int(np.ceil(num_other_users / len(non_us_locales))))
other_locales_cycle = other_locales_cycle[:num_other_users]

for idx in range(num_us_users, num_users):
    users.append({
        "uuid": generate_uuid(),
        "username": f"user_{idx}",
        "locale": other_locales_cycle[idx - num_us_users]
    })

users_df = pd.DataFrame(users)
users_df['email'] = users_df['username'].apply(lambda x: faker.email())

# Assign fixed ship-from address per user
users_df['shipFrom_address'] = users_df['locale'].apply(
    lambda loc: generate_address(country_code=loc)
)

# Prepare PF users: batch into groups of 2–4 per fraudulent account number
pf_users_idx = []
normal_users_idx = []
account_numbers = pd.Series(index=users_df.index, dtype=object)

for idx, user in users_df.iterrows():
    account_numbers[idx] = faker.credit_card_number()  # temp placeholder
    normal_users_idx.append(idx)

users_df['account_number'] = account_numbers

shipment_rows = []

for idx, user in users_df.iterrows():
    num_shipments = random.randint(1, 7)

    # Determine fraud type
    if num_shipments == 1:
        is_fraud = random.choices([True, False], weights=[5, 95])[0]
        fraud_type = 'PF' if is_fraud else 'No'
    else:
        is_fraud = random.choices([True, False], weights=[5, 95])[0]
        if is_fraud:
            fraud_type = random.choice(['UA', 'PF', 'CC'])
        else:
            fraud_type = 'No'

    # Assign PF fraudulent accounts in groups of 2–4
    if fraud_type == 'PF':
        pf_users_idx.append(idx)

    # Save fraud info
    user['is_fraud'] = int(is_fraud)
    user['fraud_type'] = fraud_type

    if fraud_type == 'UA':
        base_time = datetime.now() - timedelta(days=random.randint(0, 30))

    for i in range(num_shipments):
        ship_date, ship_time = random_datetime()

        if fraud_type == 'UA':
            dt = base_time + timedelta(minutes=random.randint(0, 5))
            ship_date = dt.strftime('%Y-%m-%d')
            ship_time = dt.strftime('%H:%M:%S')

        if fraud_type == 'CC':
            cc_behavior = random.choice(['wrong_locale', 'international'])
            if cc_behavior == 'wrong_locale':
                fake_locale = random.choice([loc for loc in locales if loc != user['locale']])
                ship_from = generate_address(country_code=fake_locale)
                is_domestic = random.choices([True, False], weights=[95, 5])[0]
                ship_to_country = ship_from['countryCode'] if is_domestic else random.choice(
                    [loc for loc in locales if loc != ship_from['countryCode']])
            elif cc_behavior == 'international':
                ship_from = generate_address(country_code=user['locale'])
                ship_to_country = random.choice([loc for loc in locales if loc != ship_from['countryCode']])
        else:
            ship_from = user['shipFrom_address']
            is_domestic = random.choices([True, False], weights=[95, 5])[0]
            ship_to_country = ship_from['countryCode'] if is_domestic else random.choice(
                [loc for loc in locales if loc != ship_from['countryCode']])

        ship_to = generate_address(country_code=ship_to_country)

        row = {
            "uuid": user['uuid'],
            "username": user['username'],
            "email": user['email'],
            "locale": user['locale'],
            "is_fraud": user['is_fraud'],
            "fraud_type": user['fraud_type'],
            "ship_date": ship_date,
            "ship_time": ship_time,

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

            # Payment
            "payment_accountNumber": user['account_number'],
            "payment_addressLine": ship_from['addressLine']
        }

        shipment_rows.append(row)

# After all users, reassign PF account numbers in batches of 2–4
i = 0
while i < len(pf_users_idx):
    group_size = random.randint(2, 4)
    group = pf_users_idx[i:i+group_size]
    fraud_account = faker.credit_card_number()
    for idx in group:
        users_df.at[idx, 'account_number'] = fraud_account
    i += group_size

# Update account numbers in shipment_rows
account_number_map = users_df.set_index('uuid')['account_number'].to_dict()
for row in shipment_rows:
    row['payment_accountNumber'] = account_number_map[row['uuid']]

shipments_df = pd.DataFrame(shipment_rows)
print(shipments_df.head())

shipments_df.to_csv("users_with_shipments.csv", index=False)
print(f"✅ Created shipments table with {len(shipments_df)} rows in users_with_shipments.csv")
