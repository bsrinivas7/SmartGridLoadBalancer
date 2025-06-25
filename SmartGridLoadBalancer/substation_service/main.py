from flask import Flask, request, jsonify
from prometheus_client import generate_latest, Counter, Gauge, REGISTRY
import threading
import time

app = Flask(__name__)
current_load = Gauge('current_load', 'Current load of substation')
lock = threading.Lock()

@app.route('/charge', methods=['POST'])
def charge_ev():
    data = request.json
    amount = data.get('amount', 10)

    with lock:
        current_load.inc(amount)

    # Simulate charging process
    def decrease_load():
        time.sleep(60)  # Simulate 1 minute charging
        with lock:
            current_load.dec(amount)

    threading.Thread(target=decrease_load).start()
    return jsonify({"status": "charging_started", "substation": os.getenv('HOSTNAME')})

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
