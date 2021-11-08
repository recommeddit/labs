# labs/AnmolStuff
Anmol's experiments for Recommeddit Backend

## Notes:
 * gsearch has been completed [save for some additional testing needed]
 * currently has the label 'further I/O testing needed'
 * According to the Timed outputs below, it is significantly faster to use Google's Knowledge Graph API, however, using SERP API's Google Search API would allow us to get more accurate results

##Time Outputs:
 * Timelapse for checking using the `with_serp` command
```
$ time python3 gsearch.py
Query: syntax podcast

real    0m2.863s
user    0m0.143s
sys     0m0.000s
```

 * Timelapse for checking using the `gkg_query` command
```
$ time python3 gsearch.py
Query: syntax podcast

real    0m0.526s
user    0m0.106s
sys     0m0.029s
```