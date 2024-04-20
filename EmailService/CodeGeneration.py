import random
## A code generator for auth. 
def generate_random_5_digit_number():
    """Generate a random 5-digit number."""
    return ''.join(random.choice('0123456789') for _ in range(5))

# This function is helping the system to choose greeting words randomly
def shuffleTxtEntry():
    
  lst = ["Taylor. is listening..", "Taylor. is ON", "Taylor. is waiting.", "Taylor loves your voice. speak up!..."]

  random.shuffle(lst)
  x = lst[-1]
  return x
