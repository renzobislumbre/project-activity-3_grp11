import requests
import tkinter as tk
from tkinter import messagebox

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

# Initialize the main window
root = tk.Tk()
root.title("IP Information App")
root.geometry("600x500")
root.configure(bg="#f5f5f5")

# Fonts and styles
header_font = ("Arial", 16, "bold")
info_font = ("Arial", 12)

# Create a header label
header_label = tk.Label(root, text="IP Address Information", font=header_font, bg="#f5f5f5", fg="#333333")
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

# Run the application
root.mainloop()
