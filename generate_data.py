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

# Utility functions
def generate_uuid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

def fraud_not():
    is_fraud = random.choices([True, False], weights=[5, 95])[0]
    fraud_type = None
    if is_fraud:
        fraud_type = random.choice(['UA', 'PF', 'CC'])
    return pd.Series([is_fraud, fraud_type])

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
us_fraction = random.uniform(0.6, 0.75)
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
users_df[['is_fraud', 'fraud_type']] = users_df.apply(lambda _: fraud_not(), axis=1)

# find PF users
pf_users_idx = users_df[users_df['fraud_type'] == 'PF'].index.tolist()
normal_users_idx = users_df[users_df['fraud_type'] != 'PF'].index.tolist()

# prepare a Series to hold account numbers
account_numbers = pd.Series(index=users_df.index, dtype=object)

# Assign to normal users → unique accounts
for idx in normal_users_idx:
    account_numbers[idx] = faker.credit_card_number()

# Assign to PF users → batch 2–4 users per fraudulent account
i = 0
while i < len(pf_users_idx):
    group_size = random.randint(2, 4)
    group = pf_users_idx[i:i+group_size]
    fraud_account = faker.credit_card_number()
    for idx in group:
        account_numbers[idx] = fraud_account
    i += group_size

# attach to dataframe
users_df['account_number'] = account_numbers


print(users_df['locale'].value_counts())
print(f"Unique UUIDs: {users_df['uuid'].nunique()}")

users_df['shipFrom_address'] = users_df['locale'].apply(
    lambda loc: generate_address(country_code=loc)
)

# Generate Shipments
shipment_rows = []

for _, user in users_df.iterrows():
    num_shipments = random.randint(1, 7)
    fraud_type = user['fraud_type']
    is_fraud = user['is_fraud']

    if fraud_type == 'UA':
        base_time = datetime.now() - timedelta(days=random.randint(0, 30))

    for i in range(num_shipments):
        ship_date, ship_time = random_datetime()

        if fraud_type == 'UA':
            dt = base_time + timedelta(minutes=random.randint(0, 5))
            ship_date = dt.strftime('%Y-%m-%d')
            ship_time = dt.strftime('%H:%M:%S')

        if fraud_type == 'CC':
            # CC fraud → still randomly choose wrong locale or force international
            cc_behavior = random.choice(['wrong_locale', 'international'])
            if cc_behavior == 'wrong_locale':
                fake_locale = random.choice([loc for loc in locales if loc != user['locale']])
                ship_from = generate_address(country_code=fake_locale)
                is_domestic = random.choices([True, False], weights=[95, 5])[0]
                ship_to_country = ship_from['countryCode'] if is_domestic else random.choice([loc for loc in locales if loc != ship_from['countryCode']])
            elif cc_behavior == 'international':
                ship_from = generate_address(country_code=user['locale'])
                ship_to_country = random.choice([loc for loc in locales if loc != ship_from['countryCode']])
        else:
            # Non-CC users → always use their fixed ship_from
            ship_from = user['shipFrom_address']
            is_domestic = random.choices([True, False], weights=[95, 5])[0]
            ship_to_country = ship_from['countryCode'] if is_domestic else random.choice([loc for loc in locales if loc != ship_from['countryCode']])

        ship_to = generate_address(country_code=ship_to_country)

        row = {
            "uuid": user['uuid'],
            "username": user['username'],
            "email": user['email'],
            "locale": user['locale'],
            "is_fraud": is_fraud,
            "fraud_type": fraud_type,
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

            # Payment Info
            "payment_accountNumber": user['account_number'],
            "payment_addressLine": ship_from['addressLine']
        }

        shipment_rows.append(row)

shipments_df = pd.DataFrame(shipment_rows)
print(shipments_df.head())

shipments_df.to_csv("users_with_shipments.csv", index=False)

print(f"✅ Created shipments table with {len(shipment_rows)} rows in users_with_shipments.csv")
