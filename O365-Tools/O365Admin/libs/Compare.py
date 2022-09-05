#!!!!!!!!!!!! ó = o
from libs.UserObj import UserObj
from libs.UserSokrates import UserSokrates
import threading
from multiprocessing import Lock
import time
import sys
import re
from pickle import TRUE

    # VIPS fehlen# H.Dietl-L  Johannes  STANDARDWOFFPACK_IW_FACULTY
    # Odegaard      Doppelnamen
    # Paulina Lara  Doppelnamen
    # Zalan > Zalán

class Compare():
  # needed for printing
    lock = Lock()
    
    def __init__(self, azure, sokrates):
      self.azure = azure
      self.sokrates = sokrates
      self.delete = []
      
      self.thread = threading.Thread(target=self.run, args=())
      self.thread.daemon = True
      
    def start(self):
      self.thread.start()
      
    def getThread(self):
      return self.thread
      
    def setAzureUser(self, obj : UserObj):
      self.aUser = obj
      
    def setSokratesUser(self, obj : UserSokrates):
      self.sUser = obj
      
    def getDelete(self):
      """ all User which can be deleted """
      return self.delete
    
    def normalize(self, thestr):
      patterns = {
        'ä': 'ae',
        'ö': 'oe',
        'ü': 'ue',
        'ß': 'ss',
        'é': 'e',
        'è': 'e',
        'ê': 'e',
        'ë': 'e',
        'á': 'a',
        'à': 'a',
        'â': 'a', 
        'î': 'i',
        'ï': 'i',
        'ç': 'c',
        'ú': 'u',
        'ù': 'u',
        'û': 'u',
        'ò': 'o',
        'ó': 'o',
        'ô': 'o',
      }
      thestr = str(thestr)
      for key, val in patterns.items():
        thestr = thestr.replace(key, val)
      return thestr
        
    def compareNames(self, avorname, anachname, svorname, snachname):
      """ vergl, Vor und Nachnamen und auch mit tauschen """
      if avorname.lower() == svorname.lower() and anachname.lower() == snachname.lower():
        return True
      # Vor-Nachname tauschen
      if avorname.lower() == snachname.lower() and anachname.lower() == svorname.lower():
        return True
      return False
    
    def compareDoubleNames(self, avorname, anachname, svorname, snachname):
      """ vergl, Vor und Nachnamen auf Doppelname und auch mit tauschen 
      # Nachname Doppelname
        Steiner Pérez
        Schönfelder-Kickinger
      """
      if "diego" == avorname.lower():
        if "diego" == svorname.lower():
          k = 0
          STICHTAG nach ENtscheidungsprüfungen ....?
          
          
          
      if avorname.lower() in svorname.lower() and anachname.lower() in snachname.lower():
        return True 
      if avorname.lower() in snachname.lower() and anachname.lower() in svorname.lower():
        return True
      # split Doppelname
      nachnamepart = False
      parts = re.split(' |-', anachname)
      if len(parts) > 1:
        for p in parts:
          # check in Nachname Sokrates
          if p.lower() in snachname.lower():
            nachnamepart = True
            break
      # Vorname -----
      parts = re.split(' |-', avorname)
      vornameepart = False
      if len(parts) > 1:
        for p in parts:
          # check in Nachname Sokrates
          if p.lower() in svorname.lower():
            vornameepart = True
            break
          
      # Falls Vor und Nachname passen dann treffer
      if vornameepart is True and nachnamepart is True:
        return True
          
      
      
      return False
      
      
    
    

    def run(self):
      """ compare Azure User against Sokrates User """
      
      for aUser in self.azure:
        print(".", end="")
        sys.stdout.flush()
        
        found = False

        # keine Lehrer keine Vips
        if aUser.licenses == 'L' or aUser.licenses == 'V':
          found = True
        else:
          for sUser in self.sokrates:
            
            avorname = aUser.vorname
            anachname = aUser.nachname
            svorname = sUser.vorname
            snachname = sUser.nachname
            if self.compareNames(avorname, anachname, svorname, snachname):
              found = True
              break
            
            # Sonderzeichen herausnehmen ....
            avorname = self.normalize(aUser.vorname)
            anachname = self.normalize(aUser.nachname)
            svorname = self.normalize(sUser.vorname)
            snachname = self.normalize(sUser.nachname)
            if self.compareDoubleNames(avorname, anachname, svorname, snachname):
              found = True
              break
            
            
        


        if found is False:
          # gibt es nicht mehr
          self.delete.append(aUser)
      
      
     
     
      
      
      
      
      
      
      
      
      return False
        