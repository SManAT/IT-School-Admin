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

    def __init__(self, config, rootDir):
        self.logger = logging.getLogger('Worker')
        self.config = config
        self.rootDir = rootDir

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
          
        if self.debug is True:
            self.hostname = self.debugHostname
            msg = "Using MAC: %s, Hostname: %s" % ("-keine-", self.hostname)
            self.logger.info(msg)
            
        else:
            # get Hostname from MySQL DB
            self.logger.info("ToDo: Code missing")
            # self.hostname = self.getHostname()
            self.hostname = "ToDo"
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

        lock_status = -1

        # kein Lock File > Rename Computer and Reboot
        if lock_status == -1:
            tools.Rename("Rename.ps1")

            # tools.setLockFileStatus(1, "Host Renamed")
            # das Restart File kann man nicht löschen, da es während des Reboots aktiv sein muss!
            # tools.Restart()

        """
        if (status == 1) {
            this.JoinDomain("joinDomain.ps1")
            this.appendLockFileStatus(2, "Joined Domain")
            this.Restart()
        }
        if (status == 2) {
            if (kmsON) {
                // KMS Rearm Thing
                this.KMS("KMSPart1.ps1")
                logger.info("KMS Client REARM-----------------------------------")
                this.appendLockFileStatus(3, "KMS Client rearmed")
                this.Restart()
            }
        }
        if (status == 3) {
            if (kmsON) {
                // KMS Rearm Thing
                this.KMS("KMSPart2.ps1")
                logger.info("KMS Client ATO-----------------------------------")
                this.appendLockFileStatus(4, "KMS Client ato")
                this.Restart()
            }
        }
        if (status == 4) {
            this.appendLockFileStatus(-2, "All done")
            logger.info("")
            logger.info("")
            logger.info("############################################################")
            logger.info("       we are finished, hostname, joined, rearm, ato")
            logger.info("############################################################")
            logger.info("")
            logger.info("")

            this.Shutdown()
        }

        //nichts zu tun
        if (status == -2) {
            logger.info("Host " + host.getName() + ":" + host.getMacListasString() + " bereits fertig bearbeitet!")
            this.triggerCloseEvent()
        }
        //try to delete tmp Folder
        if(this.debug == false){
            FileTools.deleteDir(Paths.get(TMP_Dir).toFile())
        }
        """

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
        for i, k in enumerate(eth_list):
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
        for i, k in enumerate(result):
            item = result[i]
            for i2, k2 in enumerate(available_networks):
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
        mysql = MySQL()

        server = self.config["config"]["mysql"]["server"]
        user: self.config["config"]["mysql"]["user"]
        password: self.config["config"]["mysql"]["password"]
        database: self.config["config"]["mysql"]["database"]
        mactable: self.config["config"]["mysql"]["mactable"]

        # Tests
        # print(self.config)
        # print(self.config["config"]["domain"])

        # Test
        mysql.getHostData()

        if self.debug is False:
            mysql.getHostData()

        """
            if (host.getId() == -1) {
                logger.error("Die MAC Adresse " +
                             host.getMacListasString() + " existiert nicht!")
                logger.error("Exit")
                System.exit(0)
            }
        }
        if (DEBUG == false) {
            host.setName(mysql.getHostname())
        } else {
            host.setName(debugHostname)
        }
        logger.info("Debug Informations:")
        String msg = String.format("MAC: %s, Hostname: %s gefunden!", host.getMacListasString(), host.getName())
        if (DEBUG) {
            msg = String.format("MAC: %s, Hostname: %s gefunden!",
                                "-keine-", host.getName())
        }
        logger.info(msg)
        // Host existiert umbenennen starten
        HostWorker work = new HostWorker(host, domainAdminObject, localAdminObject, kmsON, DEBUG)

        // Delay gib Windows etwas Zeit to complete StartUp
        if (DEBUG == false) {
            Wait(10000)
        }
        work.doTheJob()
        """
