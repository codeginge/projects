import ntplib
from time import ctime
from datetime import datetime

def get_time_offset(ntp_server='pool.ntp.org'):
    try:
        client = ntplib.NTPClient()
        response = client.request(ntp_server)
        offset = response.offset  # seconds, can be positive or negative
        print(f"\n🕒 Local Time:  {ctime()}")
        print(f"🌐 NTP Time:    {ctime(response.tx_time)}")
        print(f"📏 Time Offset: {offset:.6f} seconds ({'ahead' if offset > 0 else 'behind'})")
    except Exception as e:
        print(f"❌ Failed to get NTP time: {e}")

    return offset

if __name__ == "__main__":
    get_time_offset()
