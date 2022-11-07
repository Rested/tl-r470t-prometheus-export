from router import _parse_ping_response


def test_parse_ping_result():
    result = 'PING google.com (142.250.179.238): 64 data bytes\nReply from 142.250.179.238:  bytes=64  ttl=118  seq=1  time=14.517 ms\nRequest timed out!\nReply from 142.250.179.238:  bytes=64  ttl=118  seq=3  time=14.453 ms\nReply from 142.250.179.238:  bytes=64  ttl=118  seq=4  time=13.826 ms\n\n--- Ping Statistic "google.com" ---\nPackets: Sent=4, Received=3, Lost=1 (25.00% loss)\nRound-trip min/avg/max = 13.826/14.265/14.517 ms\n'
    assert _parse_ping_response(result) == {
        "packets": {
            "sent": 4,
            "received": 3,
            "lost": 1,
        },
        "round_trip": {
            "min": 13.826,
            "avg": 14.265,
            "max": 14.517,
        },
    }
