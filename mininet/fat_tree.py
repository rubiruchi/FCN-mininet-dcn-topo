import os
import sys
from mininet.topo import Topo
from mininet.node import OVSSwitch
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
 
class OVSBridgeSTP( OVSSwitch ):
    prio = 1000
    def start( self, *args, **kwargs ):
        OVSSwitch.start( self, *args, **kwargs )
        OVSBridgeSTP.prio += 1
        self.cmd( 'ovs-vsctl set Bridge', self,
                  'stp_enable=true',
                  'other_config:stp-priority=%d' % OVSBridgeSTP.prio )
 

class FatTree( Topo ):

    def __init__( self, K ):

        # Topology settings
        podNum = K                      # Pod number in FatTree
        coreSwitchNum = pow((K/2),2)    # Core switches 
        hostNum       = (K*pow((K/2),2))# Hosts in K-ary FatTree

        # Initialize topology
        Topo.__init__( self )

        coreSwitches = []
        aggrSwitches = []
        edgeSwitches = []

        # Core
        for core in range(0, coreSwitchNum):
            switch = self.addSwitch("cs_"+str(core))
            coreSwitches.append(switch)

        # Pod
        # For each pod lets add the switches 
        for pod in range(0, podNum):
            aggrSwitches += self.addAggrSwitch(pod, coreSwitches, K)
            edgeSwitches += self.addEdgeSwitch(pod, aggrSwitches, K)

        self.addHostEdgeLink(edgeSwitches, hostNum, K)    

    def addHostEdgeLink(self, edgeSwitches, hostNum, K):
        curHostNum = 0
        for x in range(0, (hostNum)):
            curHostNum+=1
            self.addLink(edgeSwitches[x/(K/2)], self.addHost("h"+str(curHostNum)))

    def addAggrSwitch(self, pod, coreSwitches, K):
        aggrSwitches = []
        for aggr in range(0, ((K*(K/2)))/K):         # aggrSwitch number = ((K/2)*K), number of pods = K
            aggrThis = self.addSwitch("as_"+str(pod)+"_"+str(aggr))
            aggrSwitches.append(aggrThis)
            for x in range((K/2)*aggr, (K/2)*(aggr+1)):
                self.addLink(aggrThis, coreSwitches[x])
        return aggrSwitches

    def addEdgeSwitch(self, pod, aggrSwitches, K):
        edgeSwitches = []
        for edge in range(0, ((K*(K/2))/K)):        # edgerSwitch number = ((K/2)*K), number of pods = K
            edgeThis = self.addSwitch("es_"+str(pod)+"_"+str(edge))
            edgeSwitches.append(edgeThis)
            for x in range(((K*(K/2))/K)*pod, (((K*(K/2))/K)*(pod+1))):
                print("len = %d"%len(aggrSwitches))
                print("x =%d"%x)
                self.addLink(edgeThis, aggrSwitches[x])
        return edgeSwitches


def createTopo(argv):
    setLogLevel('info')
    if (len(argv)<2):
        print("usage: python fat_tree.py <k> <controller>\nWhere,\nController = POX\tfor pox,\nController = OVS\tfor OVS controller")
        exit()

    K = int(argv[1])
    con = argv[2]
    topo = FatTree(K)
    print("Start Mininet")

    if con == "POX":
        net = Mininet(topo=topo, switch=OVSBridgeSTP, controller=None)
        CONTROLLER_IP = "0.0.0.0"
        CONTROLLER_PORT = 6633
        net.addController( 'controller',controller=RemoteController,ip=CONTROLLER_IP,port=CONTROLLER_PORT)
    elif con == "OVS":
        net = Mininet(topo=topo, switch=OVSBridgeSTP)
    else:
        print("Wrong controller option given\n")
        print("usage: python fat_tree.py <k> <controller>\nWhere,\nController = POX\tfor pox,\nController = OVS\tfor OVS controller")
        exit()

    net.start()
    os.system("time bash -c 'while ! ovs-ofctl show es_0_0 | grep FORWARD; do sleep 1; done'")

    print("iperf and ping between %s and %s\n\n"%(net.hosts[0], net.hosts[-1]))
    os.system("sleep 10")
#    net.iperf((net.hosts[0], net.hosts[-1]))
#    net.pingFull((net.hosts[0], net.hosts[-1]))
    CLI(net)
    net.stop()

if __name__ == '__main__':
    createTopo(sys.argv)


