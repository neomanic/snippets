20231008_19 ->
20231026_10

17.6 days

heater on for 16% of the time


sqlite-utils insert plants.db plants plants.csv --csv --multi --convert '

https://www.soliscloud.com/#/exportRecords

SELECT * from logpoints WHERE strftime('%H', datetime(timestamp, 'unixepoch')) BETWEEN '07' AND '17' AND meter == 2 AND power > 2000

SELECT * from logpoints WHERE strftime('%H', datetime(timestamp, 'unixepoch')) BETWEEN '07' AND '17'

SELECT * from logpoints WHERE power > 3000

SELECT datetime(timestamp, 'unixepoch','localtime') from logpoints WHERE strftime('%H', datetime(timestamp, 'unixepoch', 'localtime')) BETWEEN '07' AND '17' AND meter == 2

SELECT AVG(power) as avg_power from logpoints WHERE meter == 2 AND CAST(strftime('%H', datetime(timestamp, 'unixepoch', 'localtime')) AS INTEGER) NOT BETWEEN 7 AND 17 AND power < 3000

AVG, where power > 3000 = 3745.1533050223497 (20369 count) -> -545.5863748047503 (128040)
> 2000 = 3581.8260996380764 (23485) < -> -621.9064207838438 ()


aircon throws it off, boo...
need to get inverter values in there

SELECT
  ROUND(power / 100) as bucket,
  COUNT(*) AS frequency
from
  logpoints
WHERE
  meter == 2
  AND CAST(
    strftime(
      '%H',
      datetime(timestamp, 'unixepoch', 'localtime')
    ) AS INTEGER
  ) NOT BETWEEN 5 AND 17
GROUP BY
  bucket
ORDER BY
  bucket


import inverter and then we can create 



I want the usage areas when there is no solar... and why?
hot water:  meter 2 
histogram it, both daylight hours 
7-5 then

usage vs returned... max and min
get meter 2, all data 

1C: oven, lighting 1
2A: hot water, power 1 (lower usage of house), light 2
3B: power 2 (heavy usage kitchen + pool pump), stove

light 1
Front room x3
Entry
Garage, subfloor
Media
Back room
Back yard
Bathroom, toilet
Bed main1, 2, bathroom
Kitchen x2

light 2
Top security
Bed 3,4
Laundry


sqlite-utils insert shelly3em.db report $FILE -- --multi --convert '
return {
    "time": int(row["unixtime"]),

    "name": row["name"].upper(),
    "latitude": float(row["latitude"]),
    "longitude": float(row["longitude"]),
}'




  "emeters": [
    {
      "power": -2355.07,
      "pf": -0.98,
      "current": 9.68,
      "voltage": 247.36,
      "is_valid": true,
      "total": 74460.7,
      "total_returned": 264737.9
    },
    {
      "power": -2401.95,
      "pf": -0.96,
      "current": 10.17,
      "voltage": 244.81,
      "is_valid": true,
      "total": 224588.2,
      "total_returned": 261406.0
    },
    {
      "power": -1405.09,
      "pf": -0.84,
      "current": 6.81,
      "voltage": 246.57,
      "is_valid": true,
      "total": 134701.6,
      "total_returned": 163459.4
    }
  ],
  "total_power": -6162.11,
  "emeter_n": {
    "current": 0.00,
    "ixsum": 3.62,
    "mismatch": false,
    "is_valid": false
  },

```
{
  "wifi_sta": {
    "connected": true,
    "ssid": "Office",
    "ip": "192.168.1.101",
    "rssi": -82
  },
  "cloud": {
    "enabled": true,
    "connected": true
  },
  "mqtt": {
    "connected": false
  },
  "time": "10:01",
  "unixtime": 1696978860,
  "serial": 1928,
  "has_update": false,
  "mac": "C45BBE798699",
  "cfg_changed_cnt": 1,
  "actions_stats": {
    "skipped": 0
  },
  "relays": [
    {
      "ison": false,
      "has_timer": false,
      "timer_started": 0,
      "timer_duration": 0,
      "timer_remaining": 0,
      "overpower": false,
      "is_valid": true,
      "source": "input"
    }
  ],
  "emeters": [
    {
      "power": -2355.07,
      "pf": -0.98,
      "current": 9.68,
      "voltage": 247.36,
      "is_valid": true,
      "total": 74460.7,
      "total_returned": 264737.9
    },
    {
      "power": -2401.95,
      "pf": -0.96,
      "current": 10.17,
      "voltage": 244.81,
      "is_valid": true,
      "total": 224588.2,
      "total_returned": 261406.0
    },
    {
      "power": -1405.09,
      "pf": -0.84,
      "current": 6.81,
      "voltage": 246.57,
      "is_valid": true,
      "total": 134701.6,
      "total_returned": 163459.4
    }
  ],
  "total_power": -6162.11,
  "emeter_n": {
    "current": 0.00,
    "ixsum": 3.62,
    "mismatch": false,
    "is_valid": false
  },
  "fs_mounted": true,
  "v_data": 1,
  "ct_calst": 0,
  "update": {
    "status": "idle",
    "has_update": false,
    "new_version": "20230913-114244/v1.14.0-gcb84623",
    "old_version": "20230913-114244/v1.14.0-gcb84623"
  },
  "ram_total": 49920,
  "ram_free": 31652,
  "fs_size": 233681,
  "fs_free": 155369,
  "uptime": 1527291
}
```