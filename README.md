# TL-R470T+ prometheus exporter

Utility to scrape some useful metrics from the admin interface for the TL-R470T+ router. May work for other tp-link routers, not sure. 

Outputs scraped stuff to a prometheus server.


## Get started

To run simply go to your admin interface and find your password by running

```javascript
obj = document.getElementById("login-password");  $.su.encrypt("yourpassword", [obj.n, obj.e])
```

in the console. Setting ENCRYPTED_PW=what you got above,

run 

```bash
docker run --env-file=.env -p 8000:8000 restd/tl-r470t-prometheus-export
```

Then go to http://localhost:8000

## Example output

```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 296.0
python_gc_objects_collected_total{generation="1"} 323.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 52.0
python_gc_collections_total{generation="1"} 4.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="11",patchlevel="0",version="3.11.0"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 1.84963072e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 2.7746304e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.66778799302e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 0.11
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 6.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP pings_sent_total The total number of pings sent to google.com
# TYPE pings_sent_total counter
pings_sent_total{interface="WAN1",network_name="broadband"} 4.0
pings_sent_total{interface="WAN2",network_name="starlink"} 4.0
pings_sent_total{interface="WAN3",network_name="mobile"} 4.0
# HELP pings_sent_created The total number of pings sent to google.com
# TYPE pings_sent_created gauge
pings_sent_created{interface="WAN1",network_name="broadband"} 1.667787995317165e+09
pings_sent_created{interface="WAN2",network_name="starlink"} 1.667787996581742e+09
pings_sent_created{interface="WAN3",network_name="mobile"} 1.6677879980366561e+09
# HELP pings_lost_total The total number of pings missed
# TYPE pings_lost_total counter
pings_lost_total{interface="WAN1",network_name="broadband"} 0.0
pings_lost_total{interface="WAN2",network_name="starlink"} 0.0
pings_lost_total{interface="WAN3",network_name="mobile"} 0.0
# HELP pings_lost_created The total number of pings missed
# TYPE pings_lost_created gauge
pings_lost_created{interface="WAN1",network_name="broadband"} 1.667787995317189e+09
pings_lost_created{interface="WAN2",network_name="starlink"} 1.6677879965817566e+09
pings_lost_created{interface="WAN3",network_name="mobile"} 1.667787998036677e+09
# HELP ping_roundtrip The roundtrip length of a ping in ms
# TYPE ping_roundtrip gauge
ping_roundtrip{interface="WAN1",network_name="broadband"} 13.767
ping_roundtrip{interface="WAN2",network_name="starlink"} 33.363
ping_roundtrip{interface="WAN3",network_name="mobile"} 54.395
# HELP bytes_received_total The total number of bytes received
# TYPE bytes_received_total counter
bytes_received_total{interface="None",ip_addr="192.168.0.192",network_name="None"} 7.36268914e+08
bytes_received_total{interface="None",ip_addr="192.168.0.103",network_name="None"} 3.423907024e+09
bytes_received_total{interface="None",ip_addr="192.168.0.154",network_name="None"} 8.670311858e+09
bytes_received_total{interface="LAN",ip_addr="None",network_name="None"} 1.043797579e+09
bytes_received_total{interface="WAN1",ip_addr="None",network_name="broadband"} 1.6066475e+07
bytes_received_total{interface="WAN2",ip_addr="None",network_name="starlink"} 8.073249934e+09
bytes_received_total{interface="WAN3",ip_addr="None",network_name="mobile"} 4.609010948e+09
# HELP bytes_received_created The total number of bytes received
# TYPE bytes_received_created gauge
bytes_received_created{interface="None",ip_addr="192.168.0.192",network_name="None"} 1.6677879984238236e+09
bytes_received_created{interface="None",ip_addr="192.168.0.103",network_name="None"} 1.6677879984238591e+09
bytes_received_created{interface="None",ip_addr="192.168.0.154",network_name="None"} 1.6677879984238825e+09
bytes_received_created{interface="LAN",ip_addr="None",network_name="None"} 1.6677879984239044e+09
bytes_received_created{interface="WAN1",ip_addr="None",network_name="broadband"} 1.6677879984239416e+09
bytes_received_created{interface="WAN2",ip_addr="None",network_name="starlink"} 1.6677879984239626e+09
bytes_received_created{interface="WAN3",ip_addr="None",network_name="mobile"} 1.667787998423982e+09
# HELP bytes_transmitted_total The total number of bytes transmitted
# TYPE bytes_transmitted_total counter
bytes_transmitted_total{interface="None",ip_addr="192.168.0.192",network_name="None"} 7.49764526e+08
bytes_transmitted_total{interface="None",ip_addr="192.168.0.103",network_name="None"} 1.6185511e+08
bytes_transmitted_total{interface="None",ip_addr="192.168.0.154",network_name="None"} 1.75716921e+08
bytes_transmitted_total{interface="LAN",ip_addr="None",network_name="None"} 1.2850817052e+010
bytes_transmitted_total{interface="WAN1",ip_addr="None",network_name="broadband"} 4.958982e+06
bytes_transmitted_total{interface="WAN2",ip_addr="None",network_name="starlink"} 2.0704887e+08
bytes_transmitted_total{interface="WAN3",ip_addr="None",network_name="mobile"} 8.83624796e+08
# HELP bytes_transmitted_created The total number of bytes transmitted
# TYPE bytes_transmitted_created gauge
bytes_transmitted_created{interface="None",ip_addr="192.168.0.192",network_name="None"} 1.6677879984238381e+09
bytes_transmitted_created{interface="None",ip_addr="192.168.0.103",network_name="None"} 1.6677879984238656e+09
bytes_transmitted_created{interface="None",ip_addr="192.168.0.154",network_name="None"} 1.6677879984238877e+09
bytes_transmitted_created{interface="LAN",ip_addr="None",network_name="None"} 1.6677879984239094e+09
bytes_transmitted_created{interface="WAN1",ip_addr="None",network_name="broadband"} 1.6677879984239473e+09
bytes_transmitted_created{interface="WAN2",ip_addr="None",network_name="starlink"} 1.6677879984239676e+09
bytes_transmitted_created{interface="WAN3",ip_addr="None",network_name="mobile"} 1.667787998423986e+09
# HELP packets_received_total The total number of packets received
# TYPE packets_received_total counter
packets_received_total{interface="None",ip_addr="192.168.0.192",network_name="None"} 1.109162e+06
packets_received_total{interface="None",ip_addr="192.168.0.103",network_name="None"} 2.633894e+06
packets_received_total{interface="None",ip_addr="192.168.0.154",network_name="None"} 6.293963e+06
packets_received_total{interface="LAN",ip_addr="None",network_name="None"} 4.680273e+06
packets_received_total{interface="WAN1",ip_addr="None",network_name="broadband"} 41032.0
packets_received_total{interface="WAN2",ip_addr="None",network_name="starlink"} 5.966206e+06
packets_received_total{interface="WAN3",ip_addr="None",network_name="mobile"} 4.084141e+06
# HELP packets_received_created The total number of packets received
# TYPE packets_received_created gauge
packets_received_created{interface="None",ip_addr="192.168.0.192",network_name="None"} 1.6677879984238462e+09
packets_received_created{interface="None",ip_addr="192.168.0.103",network_name="None"} 1.6677879984238715e+09
packets_received_created{interface="None",ip_addr="192.168.0.154",network_name="None"} 1.6677879984238923e+09
packets_received_created{interface="LAN",ip_addr="None",network_name="None"} 1.6677879984239225e+09
packets_received_created{interface="WAN1",ip_addr="None",network_name="broadband"} 1.6677879984239523e+09
packets_received_created{interface="WAN2",ip_addr="None",network_name="starlink"} 1.6677879984239726e+09
packets_received_created{interface="WAN3",ip_addr="None",network_name="mobile"} 1.6677879984239902e+09
# HELP packets_transmitted_total The total number of packets transmitted
# TYPE packets_transmitted_total counter
packets_transmitted_total{interface="None",ip_addr="192.168.0.192",network_name="None"} 814065.0
packets_transmitted_total{interface="None",ip_addr="192.168.0.103",network_name="None"} 1.447813e+06
packets_transmitted_total{interface="None",ip_addr="192.168.0.154",network_name="None"} 2.314948e+06
packets_transmitted_total{interface="LAN",ip_addr="None",network_name="None"} 1.0123691e+07
packets_transmitted_total{interface="WAN1",ip_addr="None",network_name="broadband"} 47582.0
packets_transmitted_total{interface="WAN2",ip_addr="None",network_name="starlink"} 2.504958e+06
packets_transmitted_total{interface="WAN3",ip_addr="None",network_name="mobile"} 2.080332e+06
# HELP packets_transmitted_created The total number of packets transmitted
# TYPE packets_transmitted_created gauge
packets_transmitted_created{interface="None",ip_addr="192.168.0.192",network_name="None"} 1.6677879984238532e+09
packets_transmitted_created{interface="None",ip_addr="192.168.0.103",network_name="None"} 1.6677879984238765e+09
packets_transmitted_created{interface="None",ip_addr="192.168.0.154",network_name="None"} 1.6677879984238968e+09
packets_transmitted_created{interface="LAN",ip_addr="None",network_name="None"} 1.667787998423931e+09
packets_transmitted_created{interface="WAN1",ip_addr="None",network_name="broadband"} 1.6677879984239566e+09
packets_transmitted_created{interface="WAN2",ip_addr="None",network_name="starlink"} 1.667787998423977e+09
packets_transmitted_created{interface="WAN3",ip_addr="None",network_name="mobile"} 1.6677879984239943e+09
# HELP memory_usage Current memory usaeg (%) for router
# TYPE memory_usage gauge
memory_usage 15.0
# HELP cpu_usage Current CPU usage (%) for router
# TYPE cpu_usage gauge
cpu_usage 100.0
```