from flask import Flask, jsonify, render_template_string
import requests
import speedtest
from datetime import datetime

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Utility Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #121212;
            color: #f8f9fa;
        }
        .navbar {
            background-color: #1f1f1f;
            border-bottom: 1px solid #444;
        }
        .navbar-brand {
            font-size: 1.5rem;
            color: #f8f9fa;
        }
        .container {
            margin-top: 30px;
        }
        .card {
            background-color: #1f1f1f;
            color: #f8f9fa;
            border: none;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        .card-title {
            color: #0d6efd;
            font-size: 1.5rem;
            font-weight: bold;
        }
        .btn {
            margin-top: 15px;
            font-size: 1rem;
            padding: 10px 20px;
        }
        .btn-primary {
            background-color: #0d6efd;
            border-color: #0d6efd;
        }
        .btn-success {
            background-color: #198754;
            border-color: #198754;
        }
        .btn-info {
            background-color: #0dcaf0;
            border-color: #0dcaf0;
            color: #121212;
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg">
        <div class="container">
            <a class="navbar-brand" href="#">Utility Dashboard</a>
        </div>
    </nav>

    <!-- Content -->
    <div class="container">
        <div class="row">
            <!-- IP Information Card -->
            <div class="col-md-4">
                <div class="card text-center p-3">
                    <div class="card-body">
                        <h5 class="card-title">IP Information</h5>
                        <p class="card-text" id="ip_info">Public IPv4 Address: N/A</p>
                        <p class="card-text" id="location_info">Location: N/A</p>
                        <p class="card-text" id="isp_info">ASN and ISP: N/A</p>
                        <button class="btn btn-primary w-100" onclick="getIPInfo()">Get IP Information</button>
                    </div>
                </div>
            </div>

            <!-- Speed Test Card -->
            <div class="col-md-4">
                <div class="card text-center p-3">
                    <div class="card-body">
                        <h5 class="card-title">Speed Test</h5>
                        <p class="card-text" id="speed_info">Download Speed: N/A</p>
                        <p class="card-text" id="animal_info">Animal Comparison: N/A</p>
                        <button class="btn btn-success w-100" onclick="checkSpeed()">Check Internet Speed</button>
                    </div>
                </div>
            </div>

            <!-- Date & Time Card -->
            <div class="col-md-4">
                <div class="card text-center p-3">
                    <div class="card-body">
                        <h5 class="card-title">Current Date & Time</h5>
                        <p class="card-text" id="datetime_info">Date & Time: N/A</p>
                        <button class="btn btn-info w-100" onclick="getDateTime()">Refresh Date & Time</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function getIPInfo() {
            fetch('/get_ip_info')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('ip_info').innerText = 'Public IPv4 Address: ' + data.ipv4;
                    document.getElementById('location_info').innerText = 'Location: ' + data.city + ', ' + data.region + ', ' + data.country;
                    document.getElementById('isp_info').innerText = 'ISP: ' + data.isp;
                });
        }

        function checkSpeed() {
            fetch('/check_speed')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('speed_info').innerText = 'Download Speed: ' + data.download_speed;
                    document.getElementById('animal_info').innerText = 'Animal Comparison: ' + data.animal;
                });
        }

        function getDateTime() {
            fetch('/get_datetime')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('datetime_info').innerText = 'Date & Time: ' + data.datetime;
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/get_ip_info')
def get_ip_info():
    try:
        response = requests.get('https://ipinfo.io/json')
        if response.status_code == 200:
            ip_data = response.json()
            return jsonify({
                "ipv4": ip_data.get("ip", "N/A"),
                "city": ip_data.get("city", "N/A"),
                "region": ip_data.get("region", "N/A"),
                "country": ip_data.get("country", "N/A"),
                "isp": ip_data.get("org", "N/A")
            })
        else:
            return jsonify({"error": "Failed to retrieve IP information"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/check_speed')
def check_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000

        if download_speed > 100:
            animal = "cheetah (super fast!)"
        elif download_speed > 50:
            animal = "horse (fast!)"
        elif download_speed > 10:
            animal = "cat (moderate speed)"
        elif download_speed > 1:
            animal = "turtle (slow)"
        else:
            animal = "snail (very slow)"

        return jsonify({
            "download_speed": f"{download_speed:.2f} Mbps",
            "animal": animal
        })
    except Exception as e:
        return jsonify({"error": f"Failed to check speed: {e}"}), 500

@app.route('/get_datetime')
def get_datetime():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"datetime": current_time})

if __name__ == '__main__':
    app.run(debug=True)
