import requests
import random
import sys

CHARGE_URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000/charge'

def simulate_ev():
    requests.post(CHARGE_URL, json={
        "vehicle_id": f"EV-{random.randint(1000,9999)}",
        "amount": random.randint(5, 20)
    })

# Simulating the rush hour (100 requests)
for _ in range(100):
    simulate_ev()
