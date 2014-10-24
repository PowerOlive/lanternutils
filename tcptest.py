#!/usr/bin/python

import sys
import socket
import string
import time

def main(argv=None):
    if argv is None:
        argv = sys.argv
    (host, port) = string.split(sys.argv[1], ":")
    iters = int(sys.argv[2])

    dnssuccess = 0
    dnstotal = 0
    dnsmin = 0
    dnsmax = 0
    
    connsuccess = 0
    conntotal = 0
    connmin = 0
    connmax = 0

    for i in range(iters):
        start = time.time()
        try:
            ip = socket.gethostbyname(host)
            dnstime = (time.time() - start) * 1000
            dnssuccess += 1
            if dnsmin == 0 or dnstime < dnsmin:
                dnsmin = dnstime
            if dnstime > dnsmax:
                dnsmax = dnstime
            dnstotal += dnstime
            
            start = time.time()
            s = socket.socket()
            s.settimeout(30)
            s.connect((ip, int(port)))
            conntime = (time.time() - start) * 1000
            connsuccess += 1
            if connmin == 0 or conntime < dnsmin:
                connmin = conntime
            if conntime > connmax:
                connmax = conntime
            conntotal += conntime
        except:
            pass
        sys.stdout.write('.')
        sys.stdout.flush()

    print """
------------------- %s -------------------
DNS Success:     %d / %d
DNS Min:         %d ms
DNS Max:         %d ms
DNS Avg:         %d ms

Connect Success: %d / %d
Connect Min:     %d ms
Connect Max:     %d ms
Connect Avg:     %d ms
--------------------------------------------------------------------------------
""" % (sys.argv[1], \
       dnssuccess, iters, dnsmin, dnsmax, dnstotal / dnssuccess, \
       connsuccess, iters, connmin, connmax, conntotal / connsuccess)

if __name__ == "__main__":
    main()
