import pandas as pd
import random
from faker import Faker
import numpy as np

# Initialize Faker
fake = Faker()

# Constants for the clothing and accessories e-shop
CATEGORIES = [
    "Tops", "Bottoms", "Dresses", "Outerwear", 
    "Shoes", "Accessories", "Sportswear"
]

BRANDS = [
    "Nike", "Adidas", "Puma", "Zara", "H&M", 
    "Gucci", "Prada", "Levi's", "Ralph Lauren", 
    "Under Armour", "Calvin Klein", "New Balance", 
    "Tommy Hilfiger", "Versace", "Burberry"
]

ADJECTIVES = ["Classic", "Modern", "Stylish", "Luxury", "Casual", "Comfortable", "Premium"]
COLORS = ["Red", "Blue", "Black", "White", "Green", "Beige", "Pink", "Grey"]

def generate_behavioral_data(num_customers=2000):
    """
    Generates a behavioral dataset with customer purchase information, including deliberate errors.
    Values are set to create clearly separated groups for clustering.
    Returns:
        pandas.DataFrame: Dataset with customer behavioral data
    """
    # Define clearly separated customer groups
    customer_types = np.random.choice(['low', 'medium', 'high', 'premium'], size=num_customers, p=[0.3, 0.4, 0.2, 0.1])
    
    # Initialize empty lists for data
    behavioral_data = {
        "customer_id": [i for i in range(1, num_customers + 1)],
        "email": [fake.email() for _ in range(num_customers)],
        "total_spent": [],
        "total_orders": [],
        "avg_order_value": [],
        "last_purchase_days_ago": [],
        "categories_bought": [],
        "brands_bought": []
    }

    # Generate data based on customer type with more distinct differences
    for ctype in customer_types:
        if ctype == 'low':
            behavioral_data["total_spent"].append(np.random.uniform(10, 100))
            behavioral_data["total_orders"].append(np.random.randint(1, 3))
            behavioral_data["last_purchase_days_ago"].append(np.random.randint(180, 365))
            behavioral_data["categories_bought"].append(np.random.randint(1, 2))
            behavioral_data["brands_bought"].append(np.random.randint(1, 2))
        elif ctype == 'medium':
            behavioral_data["total_spent"].append(np.random.uniform(200, 500))
            behavioral_data["total_orders"].append(np.random.randint(5, 10))
            behavioral_data["last_purchase_days_ago"].append(np.random.randint(60, 180))
            behavioral_data["categories_bought"].append(np.random.randint(2, 4))
            behavioral_data["brands_bought"].append(np.random.randint(2, 4))
        elif ctype == 'high':
            behavioral_data["total_spent"].append(np.random.uniform(800, 1500))
            behavioral_data["total_orders"].append(np.random.randint(15, 25))
            behavioral_data["last_purchase_days_ago"].append(np.random.randint(14, 60))
            behavioral_data["categories_bought"].append(np.random.randint(4, 6))
            behavioral_data["brands_bought"].append(np.random.randint(4, 7))
        else:  # premium
            behavioral_data["total_spent"].append(np.random.uniform(2000, 5000))
            behavioral_data["total_orders"].append(np.random.randint(30, 50))
            behavioral_data["last_purchase_days_ago"].append(np.random.randint(1, 14))
            behavioral_data["categories_bought"].append(np.random.randint(6, 8))
            behavioral_data["brands_bought"].append(np.random.randint(7, 10))

    # Calculate average order value
    behavioral_data["avg_order_value"] = [
        round(spent / orders if orders > 0 else 0, 2)
        for spent, orders in zip(behavioral_data["total_spent"], behavioral_data["total_orders"])
    ]

    # Generate invalid emails (10 random records)
    for _ in range(10):
        idx = random.randint(0, num_customers - 1)
        behavioral_data["email"][idx] = "invalid_email.com" if random.random() < 0.5 else "user@@example.com"

    # Missing average order values (5 random records)
    for _ in range(5):
        idx = random.randint(0, num_customers - 1)
        behavioral_data["avg_order_value"][idx] = None

    # Negative values (2 records)
    for _ in range(2):
        idx = random.randint(0, num_customers - 1)
        behavioral_data["total_spent"][idx] = -random.uniform(100, 500)
        behavioral_data["avg_order_value"][idx] = -random.uniform(50, 200)

    # Empty records (3 random records)
    for _ in range(3):
        idx = random.randint(0, num_customers - 1)
        behavioral_data["total_spent"][idx] = None
        behavioral_data["total_orders"][idx] = 0
        behavioral_data["avg_order_value"][idx] = None
        behavioral_data["categories_bought"][idx] = None
        behavioral_data["brands_bought"][idx] = None
        behavioral_data["last_purchase_days_ago"][idx] = None

    return pd.DataFrame(behavioral_data)

def generate_preference_data(num_customers=2000):
    """
    Generates a preference dataset for customers with well-defined segments.
    Returns:
        pandas.DataFrame: Dataset with customer preferences
    """
    # Define customer types for better segmentation
    customer_types = np.random.choice(['budget', 'casual', 'fashion', 'luxury'], size=num_customers, p=[0.3, 0.4, 0.2, 0.1])
    
    preference_data = {
        "customer_id": [i for i in range(1, num_customers + 1)],
        "top_category": [],
        "top_brand": [],
        "price_preference_range": [],
        "discount_sensitivity": [],
        "luxury_preference_score": []
    }
    
    # Generate data based on customer type
    for ctype in customer_types:
        if ctype == 'budget':
            # Price-sensitive customers
            preference_data["top_category"].append(random.choice(["Tops", "Bottoms", "Sportswear"]))  # basic categories
            preference_data["top_brand"].append(random.choice(["H&M", "Zara", "Puma"]))  # affordable brands
            preference_data["price_preference_range"].append(1)  # low price preference
            preference_data["discount_sensitivity"].append(round(random.uniform(0.8, 1.0), 2))  # high discount sensitivity
            preference_data["luxury_preference_score"].append(random.randint(1, 2))  # low luxury preference
            
        elif ctype == 'casual':
            # Regular customers
            preference_data["top_category"].append(random.choice(["Tops", "Bottoms", "Dresses", "Shoes"]))
            preference_data["top_brand"].append(random.choice(["Nike", "Adidas", "Levi's", "Calvin Klein"]))
            preference_data["price_preference_range"].append(2)
            preference_data["discount_sensitivity"].append(round(random.uniform(0.4, 0.7), 2))
            preference_data["luxury_preference_score"].append(random.randint(2, 3))
            
        elif ctype == 'fashion':
            # Fashion enthusiasts
            preference_data["top_category"].append(random.choice(["Dresses", "Outerwear", "Accessories"]))
            preference_data["top_brand"].append(random.choice(["Ralph Lauren", "Tommy Hilfiger", "Versace"]))
            preference_data["price_preference_range"].append(2)
            preference_data["discount_sensitivity"].append(round(random.uniform(0.2, 0.5), 2))
            preference_data["luxury_preference_score"].append(random.randint(3, 4))
            
        else:  # luxury
            # Luxury customers
            preference_data["top_category"].append(random.choice(["Outerwear", "Accessories", "Shoes"]))
            preference_data["top_brand"].append(random.choice(["Gucci", "Prada", "Burberry"]))
            preference_data["price_preference_range"].append(3)
            preference_data["discount_sensitivity"].append(round(random.uniform(0.0, 0.3), 2))
            preference_data["luxury_preference_score"].append(5)

    return pd.DataFrame(preference_data)

def check_data_consistency(df):
    """
    Checks data consistency and returns a list of found problems.
    Args:
        df (pandas.DataFrame): Input dataset to check
    Returns:
        tuple: (list of problems, list of problem indices)
    """
    problems = []
    problem_indices = set()

    # Check emails
    invalid_emails = df[~df['email'].str.contains(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', regex=True)]
    if not invalid_emails.empty:
        problems.append(f"Found {len(invalid_emails)} invalid email addresses")
        problem_indices.update(invalid_emails.index)

    # Check null values
    null_records = df[df.isnull().any(axis=1)]
    if not null_records.empty:
        problems.append(f"Found {len(null_records)} records with missing values")
        problem_indices.update(null_records.index)

    # Check negative values
    negative_values = df[
        (df['total_spent'] < 0) |
        (df['total_orders'] < 0) |
        (df['avg_order_value'] < 0) |
        (df['last_purchase_days_ago'] < 0)
    ]
    if not negative_values.empty:
        problems.append(f"Found {len(negative_values)} records with negative values")
        problem_indices.update(negative_values.index)

    # Check average order value consistency
    mask = (df['total_orders'] > 0) & (df['total_spent'].notna()) & (df['avg_order_value'].notna())
    inconsistent_avg = df[mask].apply(
        lambda row: abs(row['total_spent'] / row['total_orders'] - row['avg_order_value']) > 0.01,
        axis=1
    )
    inconsistent_records = df[mask & inconsistent_avg]
    if not inconsistent_records.empty:
        problems.append(f"Found {len(inconsistent_records)} records with inconsistent average order value")
        problem_indices.update(inconsistent_records.index)

    return problems, list(problem_indices)

def generate_unique_product_name(unique_product_names):
    """Generates a unique product name."""
    while True:
        brand = random.choice(BRANDS)
        category = random.choice(CATEGORIES)
        adjective = random.choice(ADJECTIVES)
        color = random.choice(COLORS)
        product_name = f"{brand} {color} {adjective} {category}"
        if product_name not in unique_product_names:
            unique_product_names.add(product_name)
            return product_name

def generate_inventory_data(num_products=1000):
    """
    Generates an inventory dataset.
    Returns:
        pandas.DataFrame: Dataset with product inventory data
    """
    unique_product_names = set()
    
    inventory_data = {
        "product_id": [i for i in range(1, num_products + 1)],
        "product_name": [generate_unique_product_name(unique_product_names) for _ in range(num_products)],
        "category": [],
        "brand": [],
        "stock_quantity": [random.randint(0, 100) for _ in range(num_products)],
        "retail_price": [round(random.uniform(300, 5000), 2) for _ in range(num_products)],
        "cost_price": [],
        "profit_margin": []
    }

    # Populate category and brand based on product_name
    for product_name in inventory_data["product_name"]:
        split_name = product_name.split(" ")
        inventory_data["brand"].append(split_name[0])
        inventory_data["category"].append(split_name[-1])

    # Calculate cost_price and profit_margin
    for i in range(num_products):
        retail_price = inventory_data["retail_price"][i]
        profit_margin = round(random.uniform(50, 100), 2) / 100
        cost_price = round(retail_price * (1 - profit_margin), 2)
        inventory_data["cost_price"].append(cost_price)
        inventory_data["profit_margin"].append(round(profit_margin * 100, 2))

    return pd.DataFrame(inventory_data)
    