# Migration script

In order to migrate requests from one campaign to another one can use provided script.

The script processes one chained campaign at time. It searches for root requests in origin chained campaign and creates new ticket with new destination chained campaign. Possible chain repetitions are taken into account.

Improtant flags are 

``` createTicket #determines whether or not real tickets will be created in mcm```

``` ochain #full name of the origin chained campaign```

``` dchain #alias of the destination chained campaign```

Script is launched using following command
``` 
cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o cookie.txt --krb

#use createTicket = False        in the script to check that they make sence
python -u ticket-miniaodv2-nanoaod.py
#use createTicket = True
python -u ticket-miniaodv2-nanoaod.py|tee out.log 
```

It is **strongly** advised to make tests in dev, before migration on production instance.
