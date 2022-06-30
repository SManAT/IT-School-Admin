import logging
import re
import sys
import time
import psutil
from libs.MySQL import MySQL
from libs.Tools import Tools


class Worker:
    """ Class to do all the Stuff """
    debug = True
    debugHostname = "DummyHostname"

    def __init__(self, config, rootDir, cryptor):
        self.logger = logging.getLogger('Worker')
        self.config = config
        self.rootDir = rootDir
        self.cryptor = cryptor
        
        self.mysql = {}
        
        self.mysql['server'] = self.config["config"]["mysql"]["server"]
        self.mysql['user'] = self.config["config"]["mysql"]["user"]
        # decrypt password
        pwd = self.cryptor.decrypt(self.config["config"]["mysql"]["password"])
        self.mysql['password'] = pwd


    def decrypt(self, encMessage):
        """ decrypt a String """
        return self.fernet.decrypt(str.encode(encMessage)).decode()
    
    def doTheJob(self):
        self.mac = self.getMAC()
        if self.mac is None:
            self.logger.error("No active Interface found -abort-")
            sys.exit()
        else:
            msg = "Detected MAC: %s" % self.mac
            self.logger.info(msg)
          
          
        if self.debug is True:
            self.logger.info("=== DEBUGGING ===")
            self.hostname = self.debugHostname
            msg = "Using MAC: %s, Hostname: %s" % ("-keine-", self.hostname)
            self.logger.info(msg)           
        else: 
            # get Hostname from MySQL DB
            self.hostname = self.getHostname()
            msg = "MAC: %s, Hostname: %s gefunden!" % (self.mac, self.hostname)
            self.logger.info(msg)

        # Delay, gib Windows Zeit to complete StartUp
        if self.debug is False:
            time.sleep(10000) 

        self.doTheRealJobNow()
       

    def doTheRealJobNow(self):
        """ Main Method """
        tools = Tools(self.config, self.hostname, self.debug)
        # LockFile Status erfragen, falls es noch nicht existiert - 1
        lock_status = tools.getLockFilestatus()
        
        if self.debug:
            lock_status = 4

        # kein Lock File > Rename Computer and Reboot
        if lock_status == -1: 
            tools.Rename(self.hostname)
            tools.setLockFileStatus(1, "Host Renamed")
            tools.RestartHost()

        if lock_status == 1:
            tools.JoinDomain()
            if self.config["config"]["kms"] is False:
                tools.appendLockFileStatus(2, "Joined Domain")
            else:
                # index muss auf 4 gesetzt werden
                tools.appendLockFileStatus(4, "Joined Domain")
            tools.RestartHost()
        
        
        if lock_status == 2:
            if self.config["config"]["kms"] is True:
                tools.KMSRearm()
                tools.appendLockFileStatus(3, "KMS Client rearmed")
                tools.RestartHost()       
        
        if lock_status == 3:
            if self.config["config"]["kms"] is True:
                tools.KMSAto()
                tools.appendLockFileStatus(4, "KMS Client ato")
                tools.RestartHost()

        
        if lock_status == 4:
            tools.appendLockFileStatus(-2, "All done")
            self.logger.info("")
            self.logger.info("############################################################")
            self.logger.info("       we are finished, hostname, joined, rearmed, ato")
            self.logger.info("############################################################")
            self.logger.info("")

            # shutdown Host
            tools.Shutdown()

        # nichts zu tun
        if lock_status == -2:
            self.logger.info("Host %s:%s bereits fertig bearbeitet!" % (self.hostname, self.mac))
 
    def getMAC(self):
        """ get MAC Adress from active interface """
        eth_list = []
        ipv4_list = []
        ipv6_list = []
        eth_id_list = []
        mac_list = []

        eth_dict = psutil.net_if_addrs()
        # get active interfaces
        stats = psutil.net_if_stats()
        available_networks = []
        for intface, addr_list in eth_dict.items():
            if any(getattr(addr, 'address').startswith("169.254") for addr in addr_list):
                continue
            elif intface in stats and getattr(stats[intface], "isup"):
                available_networks.append(intface)
        # -----------------------

        # collect informations
        for eth in eth_dict:
            eth_list.append(eth)
            eth_id_list.append(eth)
            snic_list = eth_dict[eth]
            for snic in snic_list:
                if snic.family == psutil.AF_LINK:
                    mac_list.append(snic.address)
                elif snic.family.name == 'AF_INET':
                    ipv4_list.append(snic.address)
                elif snic.family.name == 'AF_INET6':
                    ipv6_list.append(re.sub('%.*$', '', snic.address))

        # build it together
        result = {}
        for i, k in enumerate(eth_list):  # noqa
            try:
                data = {}
                data['name'] = eth_list[i]
                data['id'] = eth_id_list[i]
                data['ip4'] = ipv4_list[i]
                data['ip6'] = ipv6_list[i]
                data['mac'] = mac_list[i]

                result[i] = data
            except Exception:
                pass

        filteredResult = {}
        # filter out inactive Adresses
        for i, k in enumerate(result):  # noqa
            item = result[i]
            for i2, k2 in enumerate(available_networks):  # noqa
                item2 = available_networks[i2]
                if item['name'] in item2:
                    filteredResult[i] = item

        try:
            # Getting first key in dictionary
            index = list(filteredResult.keys())[0]
            mac = filteredResult[index]['mac']
        except Exception:
            mac = None
        return mac

    def getHostname(self):
        """ load the HostName via MAC Adress from MySQL Database """
        mysql = MySQL(self.mysql)
        sql = self.config["config"]["mysql"]["sql"]
        if self.debug is False:
            hostname = mysql.getHostName(sql, self.mac)
        else:
            hostname = self.debugHostname       
        
        if hostname is None:
            self.logger.error("Die MAC Adresse %s existiert nicht! -exit-" % self.mac)
            exit()
       
        return hostname
    
    
   
      
     
