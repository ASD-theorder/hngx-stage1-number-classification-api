from fastapi import FastAPI, Query # type: ignore
import requests
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect (sum of divisors equals number)."""
    if n < 1: return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    n_str = str(n)

    if n_str[0] == '-':
        n_str = n_str[1:]
    digits = [int(d) for d in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="Number to classify")):
    """API endpoint to classify a number."""

    if not number.lstrip('-').isdigit():
     return {"number": number, "error": True, "message": "Input should be a valid integer"}

    number = int(number)  
    
    
    properties = ["odd" if number % 2 else "even"]
    if is_armstrong(number):
        properties.insert(0, "armstrong")
    
    
    try:
        response = requests.get(f"http://numbersapi.com/{abs(number)}/math?json")
        fun_fact = response.json().get("text", "No fun fact available.")
    except:
        fun_fact = "Fun fact not available."

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(number))),
        "fun_fact": fun_fact
} 
