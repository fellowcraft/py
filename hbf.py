#!/usr/bin/python
import random
import datetime
import os

scriptname = os.path.basename(__file__)

""" 
Copyright (c) 1987-2014 by Frank Holger Rothkamm. Forth/Coldfusion/Python
psychostochastics - Classic Csound - humanized random distributions 
------------------------------------------------------------------------------
"""
orchestra = '''

sr = 44100
kr =  4410
ksmps = 10
nchnls = 2
galeft  init 0
garight init 0

instr 1
idur            = p3
iamp            = ampdb(p4)
ifreq           = p5   ;  1x - negative backwards 
iat             = p6
irel            = p7
ipanStart       = p8
ipanEnd         = p9
iskiptime       = p10
irevSend        = p11

kpan    linseg  ipanStart, idur, ipanEnd
aAmpEnv linseg  0, iat,  iamp, irel, 0

a1,a2  diskin2 "../WAV/hbf.wav", ifreq, iskiptime, 1

i1 = birnd(1)
if (i1 > 0) then
outs a2*aAmpEnv, a1*aAmpEnv
else
outs a1*aAmpEnv, a2*aAmpEnv
endif

galeft    =         galeft  +  a1 * irevSend
garight   =         garight +  a2 * irevSend
endin

instr 99                           ; global reverb ----------------------------
irvbtime    =        p4
aleft,  aright  reverbsc  galeft,  garight, irvbtime, 18000, sr, 0.8, 1 
outs   aright,   aleft              
galeft    =    0
garight   =    0 
endin 

'''         

# now = datetime.datetime.now()
  
# score 
# name 		= scriptname # + now.strftime("%Y%m%d")
start      	= 0
duration   	= 0
events		= 1600
minfreq 	= 1
devfreq 	= 0.2	
attack  	= 50
maxdb	 	= 0
mindb	 	= -60
panStart	= 1
panEnd		= 1
total      	= 900*4
revSend 	= 0.001
skiptime	= 2160
revTime 	= 0.94


def RndFreq(): return round(random.gauss(minfreq,devfreq), 3)

def RndEnvelope():
	global start
	start = random.uniform(0,total)
	#start = abs(random.gauss(total/2,total/5))
	global duration
	#duration = max(random.gammavariate(120,60),0.01)
	duration = max(random.uniform(0,120),0.01)
        global at
	global attack
	at  =  random.uniform(0,attack*duration/100)
	global release
	release = duration - at
	if release < 0.01:
		duration = duration + 0.01
		release =  0.01

def GenerateEnvelope():
    RndEnvelope()     
    while start + duration > total: 
        RndEnvelope()

def RndDb():          return random.uniform(mindb,maxdb)

def RndpanStart():    return random.uniform(0,panStart)

def RndpanEnd():      return random.uniform(0,panEnd)

def RndrevSend():     return random.uniform(0,revSend)

def Rndskiptime():    return random.uniform(0.4,skiptime)


scoreHeader = ""

scoreHeader +=  ("; Reverb , LFO \n"
"i99     0 " + `total+revTime*3` + "   " + `revTime`    + " \n"
"\n \n")


scoreData = ""

for i in range(events):
	GenerateEnvelope()
	scoreData += "i1 " + \
	" %4.3f" % start + \
	" %4.3f" % duration + \
	" %4.3f" % RndDb() + \
	" %4.3f" % RndFreq() + \
	" %4.3f" % at + \
	" %4.3f" % release + \
	" %4.3f" % RndpanStart() + \
	" %4.3f" % RndpanEnd() + \
	" %4.3f" % Rndskiptime() + \
	" %4.3f" % RndrevSend() + "\n"


csd = ""

csd += ("<CsoundSynthesizer> \n" 
"<CsOptions> \n"
"</CsOptions> \n"
"<CsInstruments> \n" 
+ orchestra +
"</CsInstruments> \n"
"<CsScore> \n" 
+ scoreHeader
+ scoreData +
"e \n"
"</CsScore> \n"
"</CsoundSynthesizer>")

scorename = scriptname + ".csd"
i = 0
while os.path.isfile(scorename):
	i = i + 1
	scorename = "CSD/" + scriptname + "." + `i` + ".csd"

f = open(scorename, 'w')
f.write(csd)
print scorename
