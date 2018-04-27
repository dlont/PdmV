# Short excercise how to migrate one chain

## Problem statement: PPD wants to migrate NanoAODv1 to NanoAODv2 using existing MiniAODv2 datasets as input for NanoAODv2 samples.
You will use chained campaign with small number of requests to perform migration using semi-automatic script.

Small chain for migration (ochain)
https://cms-pdmv-dev.cern.ch/mcm/chained_campaigns?prepid=chain_RunIIFall17GS_flowRunIIFall17DRNoPU_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAOD&page=0&shown=15

### Tasks:

1. Create new NanoAODv2 campaign in McM (call it RunIIFall17NanoAODv2)
use https://cms-pdmv-dev.cern.ch/mcm/campaigns?prepid=RunIIFall17NanoAOD&page=0&shown=63 as example
2. Create new MiniAODv2 -> NanoAODv2 flow (call it flowRunIIFall17NanoAODv2)
use https://cms-pdmv-dev.cern.ch/mcm/flows?prepid=flowRunIIFall17NanoAOD&page=0&shown=31 as example
3. Create new GS->NanoAODv2 chained campaign 
 - find chain_RunIIFall17GS_flowRunIIFall17DRNoPU_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv2 in the list of allowed chained campaigns
4. Login to lxplus
5. Dowload somewhere **ticket-miniaodv2-nanoaod.py** from github and fetch cookie file to the same directory
 - $ cern-get-sso-cookie -u https://cms-pdmv-dev.cern.ch/mcm/ -o dev-cookie.txt --krb
6. change the names of origin (ochain) and destination (dchain) chains in **ticket-miniaodv2-nanoaod.py** to
 chain_RunIIFall17GS_flowRunIIFall17DRNoPU_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAOD
 and
 chain_RunIIFall17GS_flowRunIIFall17DRNoPU_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv2, respectively
 
7. Launch the script in dry_run mode
 - `$ python -u ticket-miniaodv2-nanoaod.py`
8. if CMS does not explode flip safety flag (`dry_run=False`) and create tickets in McM
 - `$ python -u ticket-miniaodv2-nanoaod.py|tee out.log`
9. Find new tickets created by the script in McM 
10. Find created chained requests

-----------------------------------

## Additioanl info

### list of root requests that have to be migrated
https://cms-pdmv-dev.cern.ch/mcm/chained_requests?member_of_campaign=chain_RunIIFall17GS_flowRunIIFall17DRNoPU_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAOD*&page=0&shown=15

These requests should have two NanoAOD chains after the exercise: NanoAOD and NanoAODv2 respectively
