import json
import time
import requests
import re
from prometheus_client import start_http_server, Counter, Gauge
import os


class OtherLoginError(Exception):
    """logged in elsewhere"""


WAIT_IF_LOGGED_IN_ELSEWHERE_FOR = int(
    os.environ.get("WAIT_IF_LOGGED_IN_ELSEWHERE_FOR", "300")
)
BASE_URL = os.environ.get("BASE_URL", "http://192.168.0.1")

DATA_RETRIEVAL_FREQUENCY = int(os.environ.get("DATA_RETRIEVAL_FREQUENCY", "30"))  # secs
TIME_BETWEEN_ACTIONS = float(
    os.environ.get(
        "TIME_BETWEEN_ACTIONS", "0.05"
    )  # secs - give time for the router to do otherstuff and not hog cpu
)

# get this from going to router login and in devtools running
# obj = document.getElementById("login-password");  $.su.encrypt("yourpassword", [obj.n, obj.e])
ENCRYPTED_PW = os.environ["ENCRYPTED_PW"]

# e.g. WAN1:broadband,WAN2:starlink
if wns := os.environ.get("WAN_NAMES"):
    pairs = wns.split(",")
    WAN_NAMES = {interface: name for interface, name in [p.split(":") for p in pairs]}
else:
    WAN_NAMES = {"WAN1": "broadband", "WAN2": "starlink", "WAN3": "mobile"}


headers = {
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en;q=0.5",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": BASE_URL.replace("http://", ""),
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/webpages/login.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "X-Requested-With": "XMLHttpRequest",
}

logged_in_headers = {
    **headers,
    "Referer": f"{BASE_URL}/webpages/index.html",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-orgin",
}

session = requests.Session()


stok = None


def login():
    global stok
    resp = session.post(
        BASE_URL + "/cgi-bin/luci/;stok=/login?form=login",
        data={
            "data": json.dumps(
                {
                    "method": "login",
                    "params": {
                        "username": "admin",
                        "password": ENCRYPTED_PW,
                    },
                }
            )
        },
        headers=headers,
    )
    stok = resp.json()["result"]["stok"]


def extract_result(resp) -> dict:
    try:
        return resp.json()["result"]
    except KeyError:
        if resp.json()["error_code"] == 704:
            raise OtherLoginError
        raise


def get_sys_status():
    resp = session.post(
        f"{BASE_URL}/cgi-bin/luci/;stok={stok}/admin/sys_status?form=all_usage",
        headers=logged_in_headers,
        data={
            "data": json.dumps(
                {
                    "method": "get",
                }
            )
        },
    )
    result = extract_result(resp)
    return {
        **result["mem_usage"],
        **result["cpu_usage"],
    }


def get_ifstats():
    resp = session.post(
        f"{BASE_URL}/cgi-bin/luci/;stok={stok}/admin/ifstat?form=list",
        headers=logged_in_headers,
        data={
            "data": json.dumps(
                {
                    "method": "get",
                }
            )
        },
    )
    return extract_result(resp)


def get_ipstats():
    resp = session.post(
        f"{BASE_URL}/cgi-bin/luci/;stok={stok}/admin/ipstats?form=list",
        headers=logged_in_headers,
        data={
            "data": json.dumps(
                {
                    "method": "get",
                }
            )
        },
    )
    return extract_result(resp)


def ping_interface(
    interface: str, method: str = "start", my_result: str = "The+Router+is+ready."
):
    resp = session.post(
        f"{BASE_URL}/cgi-bin/luci/;stok={stok}/admin/diagnostic?form=diag",
        headers=logged_in_headers,
        data={
            "data": json.dumps(
                {
                    "method": method,
                    "params": {
                        "type": "0",
                        "type_hidden": "0",
                        "ipaddr_ping": "google.com",
                        "iface_ping": interface,
                        "iface_trace": interface,
                        "ipaddr": "google.com",
                        "iface": interface,
                        "count": "4",
                        "pktsize": "64",
                        "my_result": my_result,
                    },
                }
            )
        },
    )
    result = extract_result(resp)
    if int(result["finish"]) == 1:
        return _parse_ping_response(result["my_result"])
    return ping_interface(interface, method="continue", my_result=result["my_result"])


def _parse_ping_response(result):
    *_, packets, roundtrip, _ = result.split("\n")
    packet_matches = re.match(
        "Packets: Sent=([\d]+), Received=([\d]+), Lost=([\d]+)", packets
    )

    roundtrip_match = re.match(
        "Round-trip min/avg/max = ([\d.]+)/([\d.]+)/([\d.]+) ms", roundtrip
    )

    return {
        "packets": {
            "sent": int(packet_matches.group(1)),
            "received": int(packet_matches.group(2)),
            "lost": int(packet_matches.group(3)),
        },
        "round_trip": {
            "min": float(roundtrip_match.group(1)),
            "avg": float(roundtrip_match.group(2)),
            "max": float(roundtrip_match.group(3)),
        },
    }


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    # Generate some requests.
    pings_sent = Counter(
        "pings_sent_total",
        "The total number of pings sent to google.com",
        ["interface", "network_name"],
    )
    pings_lost = Counter(
        "pings_lost_total",
        "The total number of pings missed",
        ["interface", "network_name"],
    )
    ping_roundtrip = Gauge(
        "ping_roundtrip",
        "The roundtrip length of a ping in ms",
        ["interface", "network_name"],
    )

    bytes_received = Counter(
        "bytes_received_total",
        "The total number of bytes received",
        ["interface", "network_name", "ip_addr"],
    )
    bytes_transmitted = Counter(
        "bytes_transmitted_total",
        "The total number of bytes transmitted",
        ["interface", "network_name", "ip_addr"],
    )

    packets_received = Counter(
        "packets_received_total",
        "The total number of packets received",
        ["interface", "network_name", "ip_addr"],
    )
    packets_transmitted = Counter(
        "packets_transmitted_total",
        "The total number of packets transmitted",
        ["interface", "network_name", "ip_addr"],
    )

    memory_usage = Gauge("memory_usage", "Current memory usaeg (%) for router")
    cpu_usage = Gauge("cpu_usage", "Current CPU usage (%) for router")
    start_http_server(8000)

    login()

    while True:
        started_checking_at = time.time()
        try:
            for interface, name in WAN_NAMES.items():
                ping_resp = ping_interface(interface)
                time.sleep(TIME_BETWEEN_ACTIONS)
                pings_sent.labels(interface, name).inc(ping_resp["packets"]["sent"])
                pings_lost.labels(interface, name).inc(ping_resp["packets"]["lost"])
                ping_roundtrip.labels(interface, name).set(
                    ping_resp["round_trip"]["avg"]
                )

            ip_stats = get_ipstats()
            time.sleep(TIME_BETWEEN_ACTIONS)
            if_stats = get_ifstats()
            time.sleep(TIME_BETWEEN_ACTIONS)

            for stats in ip_stats:
                bytes_received.labels(None, None, stats["addr"])._value.set(
                    stats["rx_bytes"]
                )
                bytes_transmitted.labels(None, None, stats["addr"])._value.set(
                    stats["tx_bytes"]
                )

                packets_received.labels(None, None, stats["addr"])._value.set(
                    stats["rx_pkts"]
                )
                packets_transmitted.labels(None, None, stats["addr"])._value.set(
                    stats["tx_pkts"]
                )

            for stats in if_stats:
                interface = stats["interface"]
                name = WAN_NAMES.get(interface)
                bytes_received.labels(interface, name, None)._value.set(
                    stats["rx_bytes"]
                )
                bytes_transmitted.labels(interface, name, None)._value.set(
                    stats["tx_bytes"]
                )

                packets_received.labels(interface, name, None)._value.set(
                    stats["rx_pkts"]
                )
                packets_transmitted.labels(interface, name, None)._value.set(
                    stats["tx_pkts"]
                )

            sys_status = get_sys_status()
            time.sleep(TIME_BETWEEN_ACTIONS)

            memory_usage.set(sys_status["mem"])
            cpu_usage.set(sys_status["core1"])
            print("completed successful metrics fetch loop!")
        except OtherLoginError:
            print(
                f"seems to be logged in elsewhere... waiting for {WAIT_IF_LOGGED_IN_ELSEWHERE_FOR}"
            )
            time.sleep(WAIT_IF_LOGGED_IN_ELSEWHERE_FOR)
            login()
        except Exception as e:
            print(e)
            print("attempting to log back in...")
            login()
        time.sleep(
            max(0, DATA_RETRIEVAL_FREQUENCY - (time.time() - started_checking_at))
        )
