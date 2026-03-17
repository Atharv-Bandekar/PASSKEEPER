import re
import string
import random
import uuid
import time

# Function to validate email format
def is_valid_email(email):
    # Simple regex pattern for email validation
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


# Function to generate a highly randomized password
def generate_random_password(nr_letters=10, nr_symbols=4, nr_numbers=4):
    # Combine device-specific and time-based seeds for better randomness
    device_seed = uuid.getnode()
    current_time_seed = time.time()

    combined_seed = device_seed + int(current_time_seed)
    random.seed(combined_seed)

    # Generate password components
    letters = string.ascii_letters
    numbers = string.digits
    symbols = '!#$%&()*+'

    # Create the password lists based on requested lengths
    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    # Combine and shuffle
    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    return "".join(password_list)