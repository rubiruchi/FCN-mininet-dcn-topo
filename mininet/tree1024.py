#!/usr/bin/python

"""
Create a 1024-host network, and run the CLI on it.
If this fails because of kernel limits, you may have
to adjust them, e.g. by adding entries to /etc/sysctl.conf
and running sysctl -p. Check util/sysctl_addon.
"""

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import OVSKernelSwitch
from mininet.topolib import TreeNet
from mininet.log import setLogLevel, info

def customParsePingFull( pingOutput ):
    "Parse ping output and return all data."
    errorTuple = (1, 0, 0, 0, 0, 0)
    # Check for downed link
    r = r'[uU]nreachable'
    m = re.search( r, pingOutput )
    if m is not None:
        return errorTuple
    r = r'(\d+) packets transmitted, (\d+) received'
    m = re.search( r, pingOutput )
    if m is None:
        error( '*** Error: could not parse ping output: %s\n' %
               pingOutput )
        return errorTuple
    sent, received = int( m.group( 1 ) ), int( m.group( 2 ) )
    r = r'rtt min/avg/max/mdev = '
    r += r'(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+) ms'
    m = re.search( r, pingOutput )
    if m is None:
        error( '*** Error: could not parse ping output: %s\n' %
               pingOutput )
        return errorTuple
    rttmin = float( m.group( 1 ) )
    rttavg = float( m.group( 2 ) )
    rttmax = float( m.group( 3 ) )
    rttdev = float( m.group( 4 ) )
    return sent, received, rttmin, rttavg, rttmax, rttdev

def customPingFull( hosts=None, timeout=None ):
    """Ping between all specified hosts and return all data.
       hosts: list of hosts
       timeout: time to wait for a response, as string
       returns: all ping data; see function body."""
    # should we check if running?
    # Each value is a tuple: (src, dsd, [all ping outputs])
    all_outputs = []
    if not hosts:
        hosts = self.hosts
        output( '*** Ping: testing ping reachability\n' )
    for node in hosts:
        output( '%s -> ' % node.name )
        for dest in hosts:
            if node != dest:
                opts = ''
                if timeout:
                    opts = '-W %s' % timeout
                result = node.cmd( 'ping -c1 %s %s' % (opts, dest.IP()) )
                outputs = customParsePingFull( result )
                sent, received, rttmin, rttavg, rttmax, rttdev = outputs
                all_outputs.append( (node, dest, outputs) )
                output( ( '%s ' % dest.name ) if received else 'X ' )
        output( '\n' )
    output( "*** Results: \n" )
    for outputs in all_outputs:
        src, dest, ping_outputs = outputs
        sent, received, rttmin, rttavg, rttmax, rttdev = ping_outputs
        output( " %s->%s: %s/%s, " % (src, dest, sent, received ) )
        output( "rtt min/avg/max/mdev %0.3f/%0.3f/%0.3f/%0.3f ms\n" %
                (rttmin, rttavg, rttmax, rttdev) )
    return all_outputs

if __name__ == '__main__':
    setLogLevel( 'info' )
    temp_list = [i for i in range(2, 10)]
    for i in temp_list:
        network = TreeNet( depth=i, fanout=2, switch=OVSKernelSwitch )
        info('** Dumping host processes\n')
#    for host in network.hosts:
#       host.cmdPrint("")
#    network.run( CLI, network )
        "Perform a complete start/test/stop cycle."
        network.start()
        info( '*** Running test\n' )
        network.iperf((network.hosts[0], network.hosts[-1]))
#        customPingFull(hosts=[network.hosts[0], network.hosts[-1]])
#    result = test( *args, **kwargs )
        CLI(network)
        network.stop()
