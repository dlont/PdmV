import sys
import time
from collections import defaultdict
import pprint
import copy
import json

today = time.mktime( time.localtime() )
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import restful

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

# Global settings defining access to McM
cookie_file = ''
is_dev_instance = False
is_dry_run = False

if is_dry_run:
        print 'This is DRYRUN!'
else:
        print 'WARNING!'*10
        print 'REAL QUERIES WILL BE MADE!!!'
        print 'WARNING!'*10

if is_dev_instance:
        cookie_file = 'dev-cookie.txt'  #dev
        print 'Running on dev instance!'
else:
        cookie_file = 'cookie.txt'      #prod
        print 'WARNING!'*10
        print 'Running on prod instance!!!'
        print 'WARNING!'*10

mcm=restful(dev=is_dev_instance, cookie=cookie_file, debug=True)

pwgs=mcm.get('restapi/users/get_pwg')['results']
# submit only these groups
#pwgs=['B2G','BPH','BTV','EXO']
print pwgs

ochain = ''
dchain = ''


#[1] Use False first to check
#Remember to use False first, to make sure that all tickets are creatable.
#createTicket = True
createTicket = False

N_REQUESTS_PER_TICKET = 30

#[2] Choose one campaign types
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPUMoriond2017NanoAODGS'
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80PremixPUMoriond17Nooutput_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPUMoriond2017NooutputNanoAODGS'
#ochain = 'chain_RunIIWinter15pLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPUMoriond2017NanoAODpLHE'
#ochain = 'chain_RunIIWinter15wmLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPUMoriond2017NanoAODwmLHE'
#ochain = 'chain_RunIISummer15wmLHEGS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPUMoriond2017NanoAODwmLHEGS'
#ochain = 'chain_RunIISummer15wmLHEGS_flowRunIISummer16DR80PremixPUMoriond17Nooutput_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPUMoriond2017NooutputNanoAODwmLHEGS'
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80BSandPU2016_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80BSandPU2016PremixPUMoriond2017NanoAODGS'

#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80FlatPU0to75TuneCP2RECO_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80CP2PremixPUMoriond2017NooutputNanoAODwmLHEGS'

#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80FlatPU0to75TuneCP0RECO_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80CP0PremixPUMoriond2017NanoAODGS'


#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80FlatPU0to75TuneCP5RECO_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80CP5PremixPUMoriond2017NanoAODGS'

#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80FlatPU0to75TuneCUETP8M1_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80FlatPU0to75TuneCUETP8M1NanoAODGS'
#
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80FlatPU0to75TuneCUETP8M2_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80FlatPU0to75TuneCUETP8M2NanoAODGS'
#
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80FlatPU0to75TuneCUETP8M3_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80FlatPU0to75TuneCUETP8M3NanoAODGS'
#
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80FlatPU0to75TuneCUETP8M4_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80FlatPU0to75TuneCUETP8M4NanoAODGS'
#
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80NoPUHcalNZSRAW_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80NoPUHcalNZSRAWNanoAODGS'
#
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80PUFlat0to50_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80PUFlat0to50NanoAODGS'
#
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80PUFlat0to70_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80PUFlat0to70NanoAODGS'
#
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80PUMoriond17_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80PUMoriond2017NanoAODGS'
#
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80PremixPUMoriond17EGM0_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPUMoriond17EGM0NanoAODGS'
#
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80PremixPUMoriond17RAW_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PUMoriond17RAWNanoAODGS'
#
#ochain = 'chain_RunIISummer15GS_flowRunIISummer16DR80PremixPilot_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPilotNanoAODGS'
#
#ochain = 'chain_RunIISummer15wmLHEGS_flowLHE2Summer15GS_flowRunIISummer16DR80FlatPU28to62HcalNZSRAW_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80FlatPU28to62HcalNZSRAWNanoAODwmLHEGS'
#
#ochain = 'chain_RunIISummer15wmLHEGS_flowLHE2Summer15GS_flowRunIISummer16DR80PUFlat0to50_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80PUFlat0to50NanoAODwmLHEGS'
#
#ochain = 'chain_RunIISummer15wmLHEGS_flowLHE2Summer15GS_flowRunIISummer16DR80PUMoriond17_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80PUMoriond17NanoAODwmLHEGS'
#
#ochain = 'chain_RunIISummer15wmLHEGS_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPUMoriond17NanoAODwmLHEGSreGS'
#
#ochain = 'chain_RunIISummer15wmLHEGS_flowRunIISummer16DR80BSandPU2016_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80BSandPU2016NanoAODwmLHEGS'
#
#ochain = 'chain_RunIISummer15wmLHEGS_flowRunIISummer16DR80FlatPU0to75TuneCUETP8M1_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80PUFlat0to75TuneCUETP8M1NanoAODwmLHEGS'
#
#ochain = 'chain_RunIISummer15wmLHEGS_flowRunIISummer16DR80FlatPU0to75TuneCUETP8M2_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80PUFlat0to75TuneCUETP8M2NanoAODwmLHEGS'
#
#ochain = 'chain_RunIISummer15wmLHEGS_flowRunIISummer16DR80FlatPU0to75TuneCUETP8M3_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80PUFlat0to75TuneCUETP8M3NanoAODwmLHEGS'
#
#ochain = 'chain_RunIISummer15wmLHEGS_flowRunIISummer16DR80FlatPU0to75TuneCUETP8M4_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80PUFlat0to75TuneCUETP8M4NanoAODwmLHEGS'
#
#ochain = 'chain_RunIISummer15wmLHEGS_flowRunIISummer16DR80PUMoriond17_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80PUMoriond17NanoAODwmLHEGS'
#
#ochain = 'chain_RunIISummer16FSPremix_flowRunIISummer16MiniAODFast'
#dchain = 'RunIISummer16FSPreMixNanoAOD'
#
#ochain = 'chain_RunIIWinter15pLHE_flowLHE2Summer15GSNooutput_flowRunIISummer16DR80PremixPUMoriond17Nooutput_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPUMoriond2017NooutputNanoAODpLHE'
#
#ochain = 'chain_RunIIWinter15wmLHE_flowLHE2Summer15GSBS2016_flowRunIISummer16DR80BSandPU2016_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80BSandPU2016NanoAODwmLHE'
#
#ochain = 'chain_RunIIWinter15wmLHE_flowLHE2Summer15GS_flowRunIISummer16DR80FlatPU28to62HcalNZSRAWAODSIM_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80FlatPU28to62HcalNZSRAWAODSIMNanoAODwmLHE'
#
#ochain = 'chain_RunIIWinter15wmLHE_flowLHE2Summer15GS_flowRunIISummer16DR80FlatPU28to62HcalNZSRAW_flowRunIISummer16MiniAODv2'
#dchain = 'RunIISummer16DR80FlatPU28to62HcalNZSRAWNanoAODwmLHE'
#
#ochain = 'chain_RunIIWinter15wmLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17EGM0_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPUMoriond17EGM0NanoAODwmLHE'
#
#ochain = 'chain_RunIIWinter15wmLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17Nooutput_flowRunIISummer16PremixMiniAODv2'
#dchain = 'RunIISummer16DR80PremixPUMoriond17NooutputNanoAODwmLHE'
#
ochain = 'chain_RunIIWinter15wmLHE_flowLHE2Summer15GS_flowRunIISummer16DR80PremixPUMoriond17NooutputpfMETcut_flowRunIISummer16PremixMiniAODv2'
dchain = 'RunIISummer16DR80PremixPUMoriond17NooutputpfMETcutNanoAODwmLHE'







ticketfilename = dchain+'.json'

collector=defaultdict(lambda : defaultdict( lambda : defaultdict( int )))
#for cc in ccs:
print 50*"-"
#print cc['prepid']
#pwgs.remove('B2G')
#pwgs.remove('BPH')
#pwgs.remove('BTV')
#pwgs.remove('EXO')
#pwgs.remove('HIG')
#pwgs.remove('JME')
#pwgs.remove('SMP')
#pwgs.remove('SUS')
#pwgs.remove('TOP')
#pwgs.remove('TSG')
for pwg in pwgs:
    #if pwg != "TOP": continue
        ## get all chains from that pwg in that chained campaign
        #crs = mcm.getA('chained_requests', query='member_of_campaign=%s&pwg=%s'%(cc['prepid'],pwg))
    crs = mcm.getA('chained_requests', query='member_of_campaign=%s&pwg=%s'%(ochain,pwg))
    print "\t",pwg,":\t",len(crs)
    for cr in crs:
        root_id = cr['chain'][0]
        #print "\t\t",root_id
        #chainchecks = mcm.getA('chained_requests',query='contains=%s'%(root_id))
        #print chainchecks
        campaign = root_id.split('-')[1]
        collector[pwg][campaign][root_id]+=1

print "This is the list of %s requests that are deemed chainable: "%(pwgs)
#pprint.pprint( dict(collector) )
#print collector
all_ticket=[]
for pwg in pwgs:
    ## create a ticket for the correct chain
    #ccs = mcm.getA('chained_campaigns', query='contains=....')
    ccs = mcm.getA('chained_campaigns', query='alias=%s'%(dchain))
    for cc in ccs:
        alias = cc['alias']
        root_campaign = cc['campaigns'][0][0]
	# create tickets with different repetition numbers for root requests
        for repeat in range(10):
	    # list of root requests in cc['alias'] chained campaign with 'repeat' repetition number
            requests_for_that_repeat = map(lambda i : i[0], filter(lambda i : i[1]==repeat, collector[pwg][root_campaign].items()))
            if not requests_for_that_repeat: continue
            #print requests_for_that_repeat
            requests_for_that_repeat.sort()
            ## create a ticket with that content
	    for chunk in chunks(requests_for_that_repeat,N_REQUESTS_PER_TICKET):
            	mccm_ticket = { 'prepid' : pwg, ## this is how one passes it in the first place
                                'pwg' : pwg,
                                'requests'  : chunk,
                                'notes' : "Summer16MiniAODv2 to Summer16NanoAOD central migration",
                                'chains' : [ alias ],
                                'repetitions' : repeat,
                                'block' : 1
                              }
            	all_ticket.append( copy.deepcopy( mccm_ticket ) )
            	#print mccm_ticket
                            
## you'll be able to re-read all tickets from the created json
open(ticketfilename,'w').write(json.dumps( all_ticket ))

#all_ticket = json.loads(open('all_tickets_pythia_nooutput.json').read())
for ticket in all_ticket:
    ### flip the switch
    if createTicket:
        res = mcm.putA('mccms', ticket )
	print "Create ticket"
	print res
	ticket_prepid=res.get('prepid',None)
	print "Ticket prepid: ", ticket_prepid
	if ticket_prepid: mcm.get('restapi/mccms/generate/%s'%(ticket_prepid))
	else:
		print "Error: no ticket"
		print ticket
        time.sleep(60)
    pass
