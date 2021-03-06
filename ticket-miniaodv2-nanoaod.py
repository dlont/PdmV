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

def dr_output_not_saved(list_of_root_request,ochain):
    """Verify that all requests have AODSIM output"""
    set_of_root_request_prepid_without_aodsim = set()
    for root_request_prepid in list_of_root_request:
	crs = mcm.getA('chained_requests', query='contains=%s&prepid=%s'%(root_request_prepid,ochain))
	for cr in crs:
		list_of_dr_request_prepid = [dr for dr in cr['chain'] if 'DR' in dr]
		if len(list_of_dr_request_prepid)==1:
			dr_request = mcm.getA('requests', query='prepid=%s'%(dr_request_prepid[0]))[0]
			# last step of the request must be saved
			if dr_request['keep_output'][-1]: continue
			else: set_of_root_request_prepid_without_aodsim.add(root_request_prepid)
		else: set_of_root_request_prepid_without_aodsim.add(root_request_prepid)
    #remove not chainable requests from the original list
    list_of_root_request = [r for r in list_of_root_request if r not in set_of_root_request_prepid_without_aodsim]
    return set_of_root_request_prepid_without_aodsim

# Global settings defining access to McM
cookie_file = ''
is_dev_instance = True


#[1] Use False first to check
#Remember to use False first, to make sure that all tickets are creatable.
is_dry_run = True

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

N_REQUESTS_PER_TICKET = 30
PRIORITY_BLOCK = 1
TICKET_NOTE = "Fall17MiniAOD to Fall17MiniAODv2+NanoAOD central migration" 

#[2] Choose one campaign types
ochain = 'chain_RunIIFall17wmLHEGS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAOD'
dchain = 'chain_RunIIFall17wmLHEGS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAOD'

ticketfilename = dchain+'.json'

collector=defaultdict(lambda : defaultdict( lambda : defaultdict( int )))
#for cc in ccs:
print 50*"-"

for pwg in pwgs:
    #if pwg != "TOP": continue
        ## get all chains from that pwg in that chained campaign
        #crs = mcm.getA('chained_requests', query='member_of_campaign=%s&pwg=%s'%(cc['prepid'],pwg))
    crs = mcm.getA('chained_requests', query='member_of_campaign=%s&pwg=%s'%(ochain,pwg))
    print "\t",pwg,":\t",len(crs)
    for cr in crs:
        #print "\t\t",cr['prepid'], cr['chain']
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
#ccs = mcm.getA('chained_campaigns', query='contains=....')
ccs = mcm.getA('chained_campaigns', query='prepid=%s'%(dchain))
for pwg in pwgs:
    ## create a ticket for the correct chain
    for cc in ccs:
        chain_prepid = cc['prepid']
        root_campaign = cc['campaigns'][0][0]
	# create tickets with different repetition numbers for root requests
        for repeat in range(10):
	    # list of root requests in cc['prepid'] chained campaign with 'repeat' repetition number
            requests_for_that_repeat = map(lambda i : i[0], filter(lambda i : i[1]==repeat, collector[pwg][root_campaign].items()))
            if not requests_for_that_repeat: continue
            #print requests_for_that_repeat
            requests_for_that_repeat.sort()
	    set_of_invalid_requests = dr_output_not_saved(requests_for_that_repeat,ochain)
	    if len(set_of_invalid_requests) > 0: print 'NOT CHAINED: ', set_of_invalid_requests
            ## create a ticket with that content
	    for chunk in chunks(requests_for_that_repeat,N_REQUESTS_PER_TICKET):
            	mccm_ticket = { 'prepid' : pwg, ## this is how one passes it in the first place
                                'pwg' : pwg,
                                'requests'  : chunk,
                                'notes' : TICKET_NOTE,
                                'chains' : [ chain_prepid ],
                                'repetitions' : repeat,
                                'block' : PRIORITY_BLOCK
                              }
            	all_ticket.append( copy.deepcopy( mccm_ticket ) )
            	#print mccm_ticket
                            
## you'll be able to re-read all tickets from the created json
open(ticketfilename,'w').write(json.dumps( all_ticket ))

#all_ticket = json.loads(open('all_tickets_pythia_nooutput.json').read())
for ticket in all_ticket:
    ### flip the switch
    if not is_dry_run:
        res = mcm.putA('mccms', ticket )
	print "Create ticket"
	print res
	ticket_prepid=res.get('prepid',None)
	print "Ticket prepid: ", ticket_prepid
	if ticket_prepid: mcm.get('restapi/mccms/generate/%s/reserve'%(ticket_prepid))
	else:
		print "Error: no ticket"
		print ticket
        time.sleep(60)
    pass
