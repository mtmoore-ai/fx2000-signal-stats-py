# fx2000-py-signalstats
Python script to report the signal stats of an Inseego FX2000 web interface

```
$ ./fx2000-signal-stats.py -h
usage: fx2000-signal-stats [-h] [-l] [-d DELAY] [-f LOG] [-r RETRIES]

Report the signal stats from an Inseego FX2000 Wavemaker

options:
  -h, --help            show this help message and exit
  -l, --loop            Loop over status checks, otherwise one-shot
  -d, --delay DELAY     Delay between queries when looping
  -f, --log LOG         Output status to log instead of stdout, append if file exists
  -r, --retries RETRIES
                        Number of retries if GET or POST errors
```
