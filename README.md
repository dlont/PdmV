# Migration script

In order to migrate requests from one campaign to another, one can use provided script.

The script processes one chained campaign at time. It searches for root requests in origin chained campaign and creates new ticket with new destination chained campaign. Possible chain repetitions are taken into account.

Improtant flags are 

``` createTicket #determines whether or not real tickets will be created in mcm```

``` ochain #full name of the origin chained campaign```

``` dchain #alias of the destination chained campaign```

Script is launched using following command
``` 
cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o cookie.txt --krb
#or if you work on dev
cern-get-sso-cookie -u https://cms-pdmv-dev.cern.ch/mcm/ -o dev-cookie.txt --krb

#use createTicket = False        in the script to check that they make sence
python -u ticket-miniaodv2-nanoaod.py
#use createTicket = True
python -u ticket-miniaodv2-nanoaod.py|tee out.log 
```

It is **strongly** advised to make tests in dev, before launching the script on prod.


# How to create new campaign
1. Chose name. Disscuss it with other request managers, PPD conveners. It should be similar to existing campaigns 
e.g. RunIIFall17MiniAOD, RunIIFall17MiniAODv2, RunIIFall17NanoAOD etc.
2. Collect feedback on cmsDriver on prep-ops HN. Improtant ingredients are
 - cmssw release
 - GT
 - era
 - HLT menu (if this is DR campaign)
 - beamspot (if this is GS campaign)
 - possible customizations
 - Clarify the size of the minbias and premix libraries with PPD L1 conveners (if this is Premix or Stdmix DR campaign)
3. Announce the campaign to Data-ops
4. Create JIRA ticket for comp-ops
  - Subject of the ticket: **name of the campaign**
  - Assignee: **Allison Corry**
  - Label: **Unified officer**
  - example JIRA ticket can be found at https://its.cern.ch/jira/browse/CMSCOMPPR-2691
5. Create new campaign in McM with correct cmsDriver sequence. Enable and start it ('next step' and 'toggle' icons)
6. Prepare pilot request
 - clone request from other campaign (if this is GS or wmLHEGS campaign)
 - use process string '**pilot**' in request configuration (process string is very important for fast feedback from comp-ops)
 - validate/define/approve it (if this is GS or wmLHEGS campaign)
 - create new chained campaign that will connect root campaign with the campaign that will be probed by the pilot
 - create new ticket with relevant root request (**block 1**)
 - approve ticket and generete chained request
 - submit pilot request
 - announce batch (https://cms-pdmv.cern.ch/mcm/batches?page=0&shown=29&status=new)
7. Notify comp-ops via JIRA (see item 4.) about the pilot
 - always provide the link to **cmsprodmon** page of the pilot workflow (can be obtained by clicking on 'camera' at the pilot request page)

