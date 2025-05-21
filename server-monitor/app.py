from flask import Flask, render_template, jsonify
import psutil

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/cpu')
def cpu_api():
    # overall CPU and per-core usage
    data = {
        'percent': psutil.cpu_percent(interval=0.5),
        'per_core': psutil.cpu_percent(percpu=True),
        'count': psutil.cpu_count(logical=False),  # physical cores
        'threads': psutil.cpu_count(logical=True)  # logical (threads)
    }
    # temperature sensors, if available
    temps = psutil.sensors_temperatures().get('coretemp', [])
    data['temps'] = [{t.label or f"Sensor{i}": t.current} for i, t in enumerate(temps)]
    return jsonify(data)

@app.route('/api/memory')
def mem_api():
    vm = psutil.virtual_memory()
    data = {
        'total': vm.total,
        'available': vm.available,
        'used': vm.used,
        'percent': vm.percent
    }
    return jsonify(data)

@app.route('/api/processes')
def procs_api():
    procs = []
    for p in psutil.process_iter(['pid','name','cpu_percent','memory_percent','num_threads']):
        procs.append(p.info)
    # sort by CPU desc and take top 20
    procs = sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)[:20]
    return jsonify(procs)

if __name__ == '__main__':
    # matches your docker-compose expose
    app.run(host='0.0.0.0', port=5004)
