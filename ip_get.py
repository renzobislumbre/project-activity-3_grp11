import requests
import tkinter as tk
from tkinter import messagebox
import speedtest

# Function to get IP information using ipapi
def get_ip_info():
    try:
        response = requests.get('https://ipapi.co/json/')
        if response.status_code == 200:
            ip_data = response.json()
            ipv4 = ip_data.get("ip", "N/A")
            city = ip_data.get("city", "N/A")
            region = ip_data.get("region", "N/A")
            country = ip_data.get("country_name", "N/A")
            isp = ip_data.get("org", "N/A")
            asn = ip_data.get("asn", "N/A")
            
            # Update the UI labels with the fetched data
            ip_label.config(text=f"Public IPv4 Address: {ipv4}")
            location_label.config(text=f"Location: {city}, {region}, {country}")
            isp_label.config(text=f"ISP: {isp}")
            asn_label.config(text=f"ASN: {asn}")
        else:
            messagebox.showerror("Error", "Failed to retrieve IP information.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to check internet speed and give an animal comparison
def check_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        # Animal comparison based on download speed
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
        
        # Update the UI labels with the speed and animal comparison
        speed_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
        animal_label.config(text=f"Animal Comparison: {animal}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check speed: {e}")

# Initialize the main window
root = tk.Tk()
root.title("IP Information and Speed Test App")
root.geometry("600x500")
root.configure(bg="#f5f5f5")

# Fonts and styles
header_font = ("Arial", 16, "bold")
info_font = ("Arial", 12)

# Create a header label
header_label = tk.Label(root, text="IP Address and Internet Speed Information", font=header_font, bg="#f5f5f5", fg="#333333")
header_label.pack(pady=10)

# Create a button to trigger the IP lookup
fetch_button = tk.Button(root, text="Get IP Information", command=get_ip_info, font=info_font, bg="#4CAF50", fg="white", padx=10, pady=5)
fetch_button.pack(pady=10)

# Labels to display IP and other information
ip_label = tk.Label(root, text="Public IPv4 Address: N/A", font=info_font, bg="#f5f5f5", fg="#333333")
ip_label.pack(pady=5)

location_label = tk.Label(root, text="Location: N/A", font=info_font, bg="#f5f5f5", fg="#333333")
location_label.pack(pady=5)

isp_label = tk.Label(root, text="ISP: N/A", font=info_font, bg="#f5f5f5", fg="#333333")
isp_label.pack(pady=5)

asn_label = tk.Label(root, text="ASN: N/A", font=info_font, bg="#f5f5f5", fg="#333333")
asn_label.pack(pady=5)

# Create a button to check internet speed
speed_button = tk.Button(root, text="Check Internet Speed", command=check_speed, font=info_font, bg="#2196F3", fg="white", padx=10, pady=5)
speed_button.pack(pady=20)

# Labels to display internet speed and animal comparison
speed_label = tk.Label(root, text="Download Speed: N/A", font=info_font, bg="#f5f5f5", fg="#333333")
speed_label.pack(pady=5)

animal_label = tk.Label(root, text="Animal Comparison: N/A", font=info_font, bg="#f5f5f5", fg="#333333")
animal_label.pack(pady=5)

# Run the application
root.mainloop()
