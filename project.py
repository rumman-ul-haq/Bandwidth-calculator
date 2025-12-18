import psutil
import time
import streamlit as st
import matplotlib.pyplot as plt

# ---------------------- Streamlit Page Config ----------------------
st.set_page_config(page_title="Network Bandwidth Monitor", layout="wide")
st.title("📶 Network Bandwidth Monitor")

# ---------------------- Default Settings ----------------------
INTERVAL = 1.0  # float
MAX_POINTS = 60  # number of points to show on graph

# Initialize previous network stats
prev_stats = psutil.net_io_counters()

# Lists to store data for plotting
upload_speeds = []
download_speeds = []
timestamps = []

# ---------------------- Sidebar Settings ----------------------
st.sidebar.header("Settings")
interval_input = st.sidebar.number_input(
    "Update interval (seconds)",
    min_value=0.5,
    max_value=5.0,
    value=INTERVAL,
    step=0.5
)
max_points_input = st.sidebar.number_input(
    "Max data points on graph",
    min_value=10,
    max_value=200,
    value=MAX_POINTS,
    step=10
)

# ---------------------- Placeholders ----------------------
graph_placeholder = st.empty()
log_placeholder = st.empty()

# ---------------------- Functions ----------------------
def get_speed(prev, interval=1.0):
    """Calculate upload/download speed in KB/s."""
    new = psutil.net_io_counters()
    bytes_sent = new.bytes_sent - prev.bytes_sent
    bytes_recv = new.bytes_recv - prev.bytes_recv
    upload_speed = bytes_sent / interval / 1024  # KB/s
    download_speed = bytes_recv / interval / 1024  # KB/s
    return upload_speed, download_speed, new

def network_status(speed):
    """Return human-friendly status for layman."""
    if speed < 50:
        return "⚠️ Slow"
    elif speed < 200:
        return "✅ Good"
    else:
        return "🚀 Excellent"

# ---------------------- Monitoring Loop ----------------------
while True:
    time.sleep(interval_input)
    
    # Get current speed
    up, down, prev_stats = get_speed(prev_stats, interval_input)

    # Store data
    upload_speeds.append(up)
    download_speeds.append(down)
    timestamps.append(time.strftime("%H:%M:%S"))

    # Keep only last max_points_input points
    if len(upload_speeds) > max_points_input:
        upload_speeds.pop(0)
        download_speeds.pop(0)
        timestamps.pop(0)

    # ---------------------- Plot Graph ----------------------
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(timestamps, upload_speeds, label="Upload KB/s", color='red')
    ax.plot(timestamps, download_speeds, label="Download KB/s", color='green')
    ax.set_xlabel("Time")
    ax.set_ylabel("Speed (KB/s)")
    ax.set_title("Real-time Network Speed")
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    graph_placeholder.pyplot(fig)

    # ---------------------- Display Logs ----------------------
    log_placeholder.markdown(
        f"**Current Upload:** {up:.2f} KB/s ({network_status(up)})  |  "
        f"**Current Download:** {down:.2f} KB/s ({network_status(down)})"
    )
