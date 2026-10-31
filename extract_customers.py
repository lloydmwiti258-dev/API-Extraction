"""
Day 1 - API Data Extraction and Transformation
Squad Python Specialization - Data Engineering

Fill in every function. Keep the signatures; you may add helpers of your own.
"""
import os
import sys
import requests
import pandas as pd

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_PATH = os.path.join("output", "customers_clean.csv")
DEFAULT = "Unknown"   # default for missing text fields (document in README)

# Set this to match the header in expected_customers_clean.csv
COLUMN_ORDER = [
    "customer_id", "name", "username", "email", "phone", "website",
    "address_street", "address_suite", "address_city", "address_zipcode",
    "address_geo_lat", "address_geo_lng",
    "company_name", "company_catchPhrase", "company_bs",
]


# Task 1
def fetch_users(url=API_URL, timeout=10):
    response = requests.get(url, timeout=timeout)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(
            f"API returned status {response.status_code}")
    return response.json()


# Task 2
def describe_structure(payload):
    print("Top-level type:", type(payload).__name__)
    record = payload[0]
    print("One record type:", type(record).__name__)

    def walk(d, prefix=""):
        for key, value in d.items():
            print(f"  {prefix}{key}: {type(value).__name__}")
            if isinstance(value, dict):
                walk(value, prefix + key + ".")
    walk(record)


# Task 3
def extract_core_fields(users):
    return [
        {
            "id": u.get("id"),
            "name": u.get("name", DEFAULT),
            "email": u.get("email", DEFAULT),
            "city": (u.get("address") or {}).get("city", DEFAULT),
            "company": (u.get("company") or {}).get("name", DEFAULT),
        }
        for u in users
    ]


# Task 4
def build_structures(users):
    names = [u.get("name", DEFAULT) for u in users]                 # list comprehension
    id_city = {u.get("id"): (u.get("address") or {}).get("city", DEFAULT)
               for u in users}                                       # dict comprehension
    id_email = []
    for u in users:                                                  # plain for loop
        id_email.append((u.get("id"), u.get("email", DEFAULT)))
    return names, id_email, id_city


# Task 5
def flatten_user(user, parent_key="", sep="_"):
    flat = {}
    for key, value in user.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            flat.update(flatten_user(value, new_key, sep))           # recursion = any depth
        else:
            flat[new_key] = value
    return flat


# Task 6
def to_dataframe(flat_users):
    df = pd.DataFrame(flat_users).rename(columns={"id": "customer_id"})
    for col in ["address_geo_lat", "address_geo_lng"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    ordered = [c for c in COLUMN_ORDER if c in df.columns]
    extras = [c for c in df.columns if c not in ordered]
    df = df[ordered + extras]
    print("Shape:", df.shape)
    print(df.dtypes)
    return df


# Task 7
def export_csv(df, path=OUTPUT_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)        # mode 'w' -> overwrites on re-run
    print(f"Saved {len(df)} rows to {path}")


# Task 8
def main():
    url = sys.argv[1] if len(sys.argv) > 1 else API_URL
    timeout = float(sys.argv[2]) if len(sys.argv) > 2 else 10
    try:
        users = fetch_users(url, timeout)
    except requests.exceptions.Timeout:
        print(f"Error: request timed out after {timeout}s.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"Error: could not connect to {url}. Check the URL.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError:
        print("Error: the response was not valid JSON.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: request failed ({e}).")
        sys.exit(1)

    if not isinstance(users, list) or not users:
        print("Error: expected a non-empty list of users.")
        sys.exit(1)

    describe_structure(users)
    print(extract_core_fields(users)[:2])
    names, id_email, id_city = build_structures(users)
    print(names, id_email[:2], id_city, sep="\n")

    flat = [flatten_user(u) for u in users]
    df = to_dataframe(flat)
    export_csv(df)


if __name__ == "__main__":
    main()





















