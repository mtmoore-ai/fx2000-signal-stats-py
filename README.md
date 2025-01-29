# fx2000-py-signalstats
Python script to report the signal stats of an Inseego FX2000 web interface

```
$ ./fx2000-signal-stats.py -h
usage: fx2000-signal-stats [-h] [-d DELAY] [-f LOG] [-i IP] [-l] [-r RETRIES]

Report the signal stats from an Inseego FX2000 Wavemaker

options:
  -h, --help            show this help message and exit
  -d, --delay DELAY     Delay between queries when looping
  -f, --log LOG         Output status to log instead of stdout, append if file exists
  -i, --ip IP           IP address of the FX2000 HTTP interface
  -l, --loop            Loop over status checks, otherwise one-shot
  -r, --retries RETRIES
                        Number of retries if GET or POST errors
```

## Authentication
The password to access admin pages is retrieved from the environment variable PASS to avoid hard-coding the password in the script.

## FX2000 IP
The default IP is 192.168.1.1, a different IP can be specified via the ``--ip`` argument

## Output
Currently, output is in CSV format with retrieved fields prefixed by the current epoch.
```
time,internetStatus4G,internetStatusTech,band,bandwidth,internetStatusNetworkOperator4G,internetStatus4gRSSI,internetStatusSNR
```
