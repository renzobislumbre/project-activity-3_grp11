from flask import Flask, jsonify, render_template_string
import requests
import speedtest

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IP and Speed Test App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #e3f2fd;
            color: #212529;
            padding: 40px;
        }
        .card {
            margin: 20px auto;
            padding: 30px;
            max-width: 600px;
            background-color: #ffffff;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }
        h1 {
            font-size: 2rem;
            margin-bottom: 25px;
            color: #0d6efd;
            text-align: center;
        }
        p {
            margin-top: 20px;
            font-size: 1.1rem;
        }
        button {
            margin-top: 30px;
            padding: 10px 20px;
        }
    </style>
</head>
<body>
<h1> Project Activty 3 - Group 11 </h1> 
    <div class="card text-center">
        <h1>IP Information</h1>
        <button class="btn btn-primary" onclick="getIPInfo()">Get IP Information</button>
        <p id="ip_info">Public IPv4 Address: N/A</p>
        <p id="location_info">Location: N/A</p>
        <p id="isp_info">ISP: N/A</p>
        <p id="asn_info">ASN: N/A</p>
    </div>

    <div class="card text-center">
        <h1>Speed Test</h1>
        <button class="btn btn-success" id="speed_btn" onclick="checkSpeed()">Check Internet Speed</button>
        <p id="speed_info">Download Speed: N/A</p>
        <p id="animal_info">Animal Comparison: N/A</p>
    </div>

    <script>
        function getIPInfo() {
            fetch('/get_ip_info')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('ip_info').innerText = 'Public IPv4 Address: ' + data.ipv4;
                    document.getElementById('location_info').innerText = 'Location: ' + data.city + ', ' + data.region + ', ' + data.country;
                    document.getElementById('isp_info').innerText = 'ISP: ' + data.isp;
                    document.getElementById('asn_info').innerText = 'ASN: ' + data.asn;
                });
        }

        function checkSpeed() {
            let speedBtn = document.getElementById('speed_btn');
            speedBtn.classList.add('fade-out');
            
            fetch('/check_speed')
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        document.getElementById('speed_info').innerText = 'Download Speed: ' + data.download_speed;
                        document.getElementById('animal_info').innerText = 'Animal Comparison: ' + data.animal;
                        speedBtn.classList.remove('fade-out');
                        speedBtn.classList.add('fade-in');
                    }, 1000);
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
        response = requests.get('https://ipapi.co/json/')
        if response.status_code == 200:
            ip_data = response.json()
            return jsonify({
                "ipv4": ip_data.get("ip", "N/A"),
                "city": ip_data.get("city", "N/A"),
                "region": ip_data.get("region", "N/A"),
                "country": ip_data.get("country_name", "N/A"),
                "isp": ip_data.get("org", "N/A"),
                "asn": ip_data.get("asn", "N/A")
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

if __name__ == '__main__':
    app.run(debug=True)
