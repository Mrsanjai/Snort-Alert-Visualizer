 🛡️ Snort Alert Visualizer

A lightweight real-time alert dashboard for Snort IDS.  
This tool automatically copies Snort log files, parses alerts, and displays them on a clean web dashboard.

---

 🔍 Features

- 📂 Monitors Snort's `C:\Snort\log\` folder in real time
- 🔄 Automatically copies `.log`, `.ids`, and subfolders to `/uploads`
- 🧠 Parses alert messages from `alert.ids` files
- 📊 Displays alerts clearly in a web dashboard
- ⚡ Built with Python (Flask), HTML/CSS, and JS

---

 📸 Screenshot

<img width="1920" height="896" alt="4" src="https://github.com/user-attachments/assets/ba3dd591-ea6c-494c-926c-5fa8c61364c1" />
<img width="1920" height="769" alt="3" src="https://github.com/user-attachments/assets/b3694223-6b0e-4145-a2a1-2d97d34c16d0" />
<img width="1919" height="963" alt="2" src="https://github.com/user-attachments/assets/1a3a062a-8314-4926-ad8f-c6b233593654" />
<img width="1920" height="1018" alt="1" src="https://github.com/user-attachments/assets/23e813e1-f5e8-4ec5-a33c-c8f4755422b8" />


---

 🚀 How It Works

1.Run Snort in IDS mode using your custom rules
2.Snort generates logs and alerts in `C:\Snort\log\`
3. This app:
   - Copies all logs into `/uploads`
   - Parses readable files (like `alert.ids`)
   - Displays `[DEMO]` alerts on the dashboard

---

 🧾 Sample Snort Rules

```snort
alert icmp any any -> any any (msg:"[DEMO] ICMP Packet Detected"; sid:1000001; rev:1;)
alert tcp any any -> any 80 (msg:"[DEMO] HTTP Request Detected"; sid:1000002; rev:1;)


🛠️ Technologies Used
Python 3 (Flask)

Snort IDS

Watchdog (for file monitoring)

HTML + Bootstrap (Dashboard UI)


# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Run the Flask app
python run.py

# Step 3: Open in browser
http://localhost:5000


📈 Demo Use
Trigger alerts by:

Running ping commands

Visiting websites (for HTTP rule)

Snort will generate alerts, and they’ll appear in your dashboard automatically!


DONE BY :
https://github.com/Amirtha-Varshini-04
https://github.com/Teju0216
https://github.com/sanket7107
https://github.com/Mrsanjai

