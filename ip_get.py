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
            font-family: 'Roboto', sans-serif;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
        }
        canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }
        .navbar {
            background-color: #1f1f1f;
            border-bottom: 2px solid #444;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .navbar-brand {
            font-size: 2rem;
            color: #f8f9fa;
            text-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .container {
            margin-top: 50px;
        }
        .card {
            background-color: #1e1e1e;
            color: #f8f9fa;
            border: none;
            border-radius: 15px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.5);
            height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.7);
        }
        .card-title {
            color: #00b4d8;
            font-size: 1.8rem;
            font-weight: bold;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
        }
        .btn {
            font-size: 1rem;
            padding: 10px 20px;
            border-radius: 30px;
            transition: background-color 0.3s, transform 0.2s;
        }
        .btn-primary {
            background-color: #0077b6;
            border: none;
        }
        .btn-primary:hover {
            background-color: #00b4d8;
            transform: scale(1.05);
        }
        .btn-success {
            background-color: #52b788;
            border: none;
        }
        .btn-success:hover {
            background-color: #70e000;
            transform: scale(1.05);
        }
        .btn-info {
            background-color: #4361ee;
            border: none;
        }
        .btn-info:hover {
            background-color: #3a86ff;
            transform: scale(1.05);
        }
        .card-body {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
    </style>
</head>
<body>
    <canvas id="particleCanvas"></canvas>

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
            <div class="col-md-4 mb-4">
                <div class="card text-center">
                    <div class="card-body">
                        <div>
                            <h5 class="card-title">IP Information</h5>
                            <p id="ip_info">Public IPv4 Address: N/A</p>
                            <p id="location_info">Location: N/A</p>
                            <p id="isp_info">ASN and ISP: N/A</p>
                        </div>
                        <button class="btn btn-primary w-100" onclick="getIPInfo()">Get IP Information</button>
                    </div>
                </div>
            </div>

            <!-- Speed Test Card -->
            <div class="col-md-4 mb-4">
                <div class="card text-center">
                    <div class="card-body">
                        <div>
                            <h5 class="card-title">Speed Test</h5>
                            <p id="speed_info">Download Speed: N/A</p>
                            <p id="animal_info">Animal Comparison: N/A</p>
                        </div>
                        <button class="btn btn-success w-100" onclick="checkSpeed()">Check Internet Speed</button>
                    </div>
                </div>
            </div>

            <!-- Date & Time Card -->
            <div class="col-md-4 mb-4">
                <div class="card text-center">
                    <div class="card-body">
                        <div>
                            <h5 class="card-title">Current Date & Time</h5>
                            <p id="datetime_info">Date & Time: N/A</p>
                        </div>
                        <button class="btn btn-info w-100" onclick="getDateTime()">Refresh Date & Time</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Particle Animation
        const canvas = document.getElementById('particleCanvas');
        const ctx = canvas.getContext('2d');
        let particlesArray = [];
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        class Particle {
            constructor(x, y, directionX, directionY, size, color) {
                this.x = x;
                this.y = y;
                this.directionX = directionX;
                this.directionY = directionY;
                this.size = size;
                this.color = color;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
                ctx.fillStyle = this.color;
                ctx.fill();
            }
            update() {
                if (this.x + this.size > canvas.width || this.x - this.size < 0) {
                    this.directionX = -this.directionX;
                }
                if (this.y + this.size > canvas.height || this.y - this.size < 0) {
                    this.directionY = -this.directionY;
                }
                this.x += this.directionX;
                this.y += this.directionY;
                this.draw();
            }
        }

        function initParticles() {
            particlesArray = [];
            let numberOfParticles = (canvas.width * canvas.height) / 9000;
            for (let i = 0; i < numberOfParticles; i++) {
                let size = Math.random() * 3 + 1;
                let x = Math.random() * (canvas.width - size * 2) + size;
                let y = Math.random() * (canvas.height - size * 2) + size;
                let directionX = (Math.random() * 0.6) - 0.3;
                let directionY = (Math.random() * 0.6) - 0.3;
                let color = 'rgba(0, 180, 216, 0.8)';
                particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
            }
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particlesArray.length; i++) {
                particlesArray[i].update();
            }
            requestAnimationFrame(animateParticles);
        }

        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            initParticles();
        });

        initParticles();
        animateParticles();

        // API Calls (Your existing functions)
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
            const rawDatetime = new Date(data.datetime);
            const options = {
                month: 'long',
                day: 'numeric',
                year: 'numeric',
                hour: 'numeric',
                minute: 'numeric',
                hour12: true
            };
            const formattedDatetime = rawDatetime.toLocaleString('en-US', options);
            document.getElementById('datetime_info').innerText = `Date & Time: ${formattedDatetime}`;
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
        print(f"Error in /check_speed: {e}")
        return jsonify({"error": f"Failed to check speed: {e}"}), 500

@app.route('/get_datetime')
def get_datetime():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"datetime": current_time})

if __name__ == '__main__':
    app.run(debug=True)
