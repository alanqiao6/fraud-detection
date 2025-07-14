import random
import string
import pandas as pd
import numpy as np

def generate_uuid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

locales = ['KY', 'MY', 'US', 'CA', 'MX', 'FR', 'DE', 'SA', 'AU', 'KO']
non_us_locales = [loc for loc in locales if loc != 'US']

num_users = 20000

users = []

# Decide US proportion (random between 50%–75%)
us_fraction = random.uniform(0.5, 0.75)
num_us_users = int(us_fraction * num_users)
num_other_users = num_users - num_us_users

# Generate US users
for _ in range(num_us_users):
    user = {
        "uuid": generate_uuid(),
        "username": f"user_{_}",
        "locale": "US"
    }
    users.append(user)

# Evenly distribute remaining users among other locales
other_locales_cycle = np.tile(non_us_locales, int(np.ceil(num_other_users / len(non_us_locales))))
other_locales_cycle = other_locales_cycle[:num_other_users]

for idx in range(num_us_users, num_users):
    user = {
        "uuid": generate_uuid(),
        "username": f"user_{idx}",
        "locale": other_locales_cycle[idx - num_us_users]
    }
    users.append(user)

# Convert to DataFrame
users_df = pd.DataFrame(users)
print(users_df['locale'].value_counts())

# Optional: Save to CSV
users_df.to_csv("users_with_locales.csv", index=False)

print(users_df.head())
