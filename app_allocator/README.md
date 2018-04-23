# app-allocator-scripts
Scripts for prototyping application allocators

Two common commands are:

1) `python3 generate.py 110 1000 | python3 allocate.py > tmp.out`

This will generate a random set of 110 judges and 1000 applications
to be judged.  It will then allocate them and report the results
in tmp.out.  tmp.out will contain a history of the actions taken by
the various judges.  The end of tmp.out will include a summary of
which queues were successfully empties and which ones failed.

2) `python3 allocate.py example.csv > tmp.out`

Ths runs the allocator against some example data anonymized from an
actually judging round.
