# mytop2csv
Output mytop -b to a file in semicolon-seperated lines


# Usage:
```mytop2csv.py -o <file> -r <refresh_rate>```

  

---

Output of mytop -b is assumed to in format for regex to work:
```
MariaDB 10.5.15 on 127.0.0.1      load (0.00 0.23 0.50) up 0+02:15:09 [00:56:52]
 Queries: 1.6M     qps:  212 Slow:     0.0         Se/In/Up/De(%):    93/00/00/00


 MyISAM Key Cache Efficiency: 100.0%  Bps in/out: 123.8k/349.4k
```
