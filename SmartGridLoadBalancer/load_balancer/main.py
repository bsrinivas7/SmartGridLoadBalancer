from flask import Flask, jsonify
import requests
import os
import threading
import time

app = Flask(__name__)
substation_hosts = os.getenv('SUBSTATION_HOSTS', '').split(',')
load_data = {host: 0 for host in substation_hosts}
lock = threading.Lock()

def poll_substations():
    while True:
        for host in substation_hosts:
            try:
                response = requests.get(f'http://{host}/metrics')
                # Parse current_load metric
                for line in response.text.split('\n'):
                    if line.startswith('current_load '):
                        with lock:
                            load_data[host] = float(line.split()[1])
            except:
                with lock:
                    load_data[host] = float('inf')
        time.sleep(5)

@app.route('/get_substation', methods=['GET'])
def get_substation():
    with lock:
        min_host = min(load_data, key=load_data.get)
    return jsonify({
        "substation_url": f"http://{min_host}/charge",
        "current_load": load_data[min_host]
    })

if __name__ == '__main__':
    threading.Thread(target=poll_substations, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
