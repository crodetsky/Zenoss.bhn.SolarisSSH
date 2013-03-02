#!/usr/local/bin/env python2.6

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin


class Processor:
    """
    Class to hold processor info
    """
    def __init__(self):
        self.socket = 0
        self.manufacturer = ''
        self.model = ''
        self.speed = 0
        self.cores = 0


class cpuinfo(CommandPlugin):
    """
    psrinfo -pv - get CPU information on Solaris machines
    """

    command = "/usr/sbin/psrinfo -pv"
    compname = "hw"
    relname = "cpus"
    modname = "Products.ZenModel.CPU"
    procs = []

    def process(self, device, results, log):
        log.info('Collecting CPU information for device %s' % device.id)
        rm = self.relMap()
        for line in results:
            if 'The' in line:
                proc = Processor()
                proc.cores = int(line.split()[4])
            if 'x86' in line:
                proc.socket = line.split()[2]
                proc.manufacturer = line.split()[3]
                proc.speed = line.split()[11]
            if 'Intel(r)' in line:
                proc.model = line.strip()
                self.procs.append(proc)
            if 'SPARC' in line:
                proc.manufacturer = 'Sun'
                proc.model = line.split()[0]
                proc.socket = line.split()[2]
                proc.speed = line.split()[8]
            self.procs.append(proc)

        for proc in self.procs:
            curCore = 1
            while curCore <= proc.cores:
                om = self.objectMap()
                om.id = proc.socket + '_' + curCore
                om.socket = proc.socket
                om.clockspeed = proc.speed
                om.ProductKey = proc.model
                rm.append(om)
        return [rm]
