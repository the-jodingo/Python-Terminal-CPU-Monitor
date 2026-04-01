# Python-Terminal-CPU-Monitor

# This version uses psutil for precise, cross-core monitoring and adds colors + history graphs in the terminal.
First, install the dependency:

sudo apt update && sudo apt install python3-pip -y

pip3 install psutil rich

After depencies you will run this code :

python3 cpu_monitor.py

Want email alerts on high CPU? Extend the Python script with smtplib or use monit / Prometheus + Grafana for advanced setups.
