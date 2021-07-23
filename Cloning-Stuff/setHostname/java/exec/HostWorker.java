package exec;

import SH.Bibliothek.Runtime.aRuntime;
import SH.FileTools.FileTools;
import crypt.CryptClass;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import main.AdminObject;
import main.HostObject;
import org.slf4j.LoggerFactory;

/**
 * Setzt Shares in WIndows
 *
 * @author Mag. Stefan Hagmann
 */
public class HostWorker {

  private static final org.slf4j.Logger logger = LoggerFactory.getLogger(HostWorker.class);
  private static final String LOCKFILE = ".lock";
  private final String TMP_Dir = "tmp/";
  private final String SCRIPT_Dir = "scripts/";

  private final HostObject host;
  private final AdminObject adminObject;
  private final Path lockfile;
  private final AdminObject localAdminObject;
  private final boolean kmsON;
  private final boolean debug;

  /**
   * Do some Work
   * @param host
   * @param adminObject
   * @param localAdminObject
   * @param kmsON 
   * @param debug 
   */
  public HostWorker(HostObject host, 
          AdminObject adminObject, 
          AdminObject localAdminObject, 
          boolean kmsON,
          boolean debug) {
    this.host = host;
    this.adminObject = adminObject;
    this.localAdminObject = localAdminObject;
    this.kmsON = kmsON;
    this.debug = debug;
    lockfile = Paths.get(LOCKFILE);
  }

  /**
   * Erstellt ein Script im angegeben Path
   *
   * @param cmds Alle Befehle
   * @param filename Name der Datei
   */
  public void createScript(String[] cmds, String filename) {
    FileTools.createDirectory(Paths.get(TMP_Dir));
    Path filepath = Paths.get(TMP_Dir + filename);
    FileTools.Delete(filepath);
    FileTools.createFile(filepath);

    try {
      //Zeilenweise in Date schreiben
      for (String cmd : cmds) {
        Files.write(filepath,
                (cmd + "\n").getBytes("utf-8"),
                StandardOpenOption.APPEND
        );
      }
    } catch (UnsupportedEncodingException ex) {
      Logger.getLogger(HostWorker.class.getName()).log(Level.SEVERE, null, ex);
    } catch (IOException ex) {
      Logger.getLogger(HostWorker.class.getName()).log(Level.SEVERE, null, ex);
    }
  }

  /**
   * Hostname
   *
   * @return Hostname oder Null
   */
  public String getHostName() {
    try {
      return InetAddress.getLocalHost().getHostName();
    } catch (UnknownHostException ex) {
      logger.error("Kann Hostname nicht bestimmen!");
      return null;
    }
  }

  /**
   * Get the Domain Name from Hostname
   *
   * @return
   */
  public String getDomainName() {
    String strDomainName;
    String hostnameCanonical;
    hostnameCanonical = this.getHostName();
    strDomainName = hostnameCanonical.substring(hostnameCanonical.indexOf(".") + 1);
    return strDomainName;
  }


  /**
   * Create User without asking for password
   * https://msdn.microsoft.com/powershell/reference/5.1/microsoft.powershell.security/Get-Credential
   * $User = "Domain01\User01" $PWord = ConvertTo-SecureString -String
   * "P@sSwOrd" -AsPlainText -Force $Credential = New-Object -TypeName
   * "System.Management.Automation.PSCredential" -ArgumentList $User, $PWord
   *
   * @param filename
   */
  public void JoinDomain(String filename) {
    String[] cmdarray = this.loadScript(filename);
    this.modifyScript(cmdarray);
    this.createScript(cmdarray, filename);
    Path filepath = Paths.get(TMP_Dir + filename);
    
    if(FileTools.Exists(filepath) == false){
      logger.error("Script not found: " + filename);
      this.triggerCloseEvent();
    }
    
    
    logger.info("Joining Domain " + host.getDomainname());
    //Do the JOB
    if(this.debug == false){
      aRuntime shell = new aRuntime();
      shell.executePSScript(filepath, true);
      //Delete tmp Script with passwords
      FileTools.Delete(Paths.get(TMP_Dir + "joinDomain.ps1"));
    }
    logger.info("Joined Domain--------------------------------------------");
  }

  /**
   * Ladet ein bestehendes Script in ein String[]
   * @param filename
   */
  private String[] loadScript(String filename) {
    Path filepath = Paths.get("scripts/" + filename);
    LinkedList<String> ReadFile = FileTools.ReadFile(filepath.toAbsolutePath().toString());
    String[] erg = ReadFile.toArray(new String[ReadFile.size()]);
    return erg;
  }

  /**
   * do it
   */
  public void doTheJob() {
    //LockFile gesetzt Status erfragen, falls es noch nicht existiert -1
    int status = this.getLockFilestatus();
    //Debug
    if(this.debug){
      status = 4;
    }

    //kein Lock File > Rename Computer and Reboot
    if (status == -1) {
      this.Rename("Rename.ps1");

      this.setLockFileStatus(1, "Host Renamed");
      //das Restart File kann man nicht löschen, da es während des Reboots aktiv sein muss!
      this.Restart();
    }
    if (status == 1) { 
      this.JoinDomain("joinDomain.ps1");
      this.appendLockFileStatus(2, "Joined Domain");
      this.Restart();
    }
    if (status == 2) {
      if (kmsON) {
        //KMS Rearm Thing
        this.KMS("KMSPart1.ps1");
        logger.info("KMS Client REARM-----------------------------------");
        this.appendLockFileStatus(3, "KMS Client rearmed");
        this.Restart();
      }
    }
    if (status == 3) {
      if (kmsON) {
        //KMS Rearm Thing
        this.KMS("KMSPart2.ps1");
        logger.info("KMS Client ATO-----------------------------------");
        this.appendLockFileStatus(4, "KMS Client ato");
        this.Restart();
      }
    }
    if (status == 4) {
      this.appendLockFileStatus(-2, "All done");
      logger.info("");
      logger.info("");
      logger.info("############################################################");
      logger.info("       we are finished, hostname, joined, rearm, ato");
      logger.info("############################################################");
      logger.info("");
      logger.info("");
      
      this.Shutdown();
    }
    
    //nichts zu tun
    if (status == -2) {
      logger.info("Host " + host.getName() + ":" + host.getMacListasString() + " bereits fertig bearbeitet!");
      this.triggerCloseEvent();
    }
    //try to delete tmp Folder
    if(this.debug == false){
      FileTools.deleteDir(Paths.get(TMP_Dir).toFile());
    }
  }
  
  /**
   * Close the Program
   */
  private void triggerCloseEvent(){
   //nothing to do
  }

  /**
   * Restart Host
   */
  private void Restart() {
    String filename = "Restart.ps1";
    String[] cmdarray = this.loadScript(filename);
    this.createScript(cmdarray, filename);
    Path filepath = Paths.get(SCRIPT_Dir + filename);
    
    if(FileTools.Exists(filepath) == false){
      logger.error("Script not found: " + filename);
      this.triggerCloseEvent();
    }

    //Do the JOB
    if(this.debug == false){
      logger.info("Restarting Host now ....");
      aRuntime shell = new aRuntime();
      shell.executePSScript(filepath, true);
    }
  }
  
  /**
   * Shutdown Host
   */
  private void Shutdown() {
    String filename = "Shutdown.ps1";
    String[] cmdarray = this.loadScript(filename);
    this.createScript(cmdarray, filename);
    Path filepath = Paths.get(SCRIPT_Dir + filename);

    //Do the JOB
    if(this.debug == false){
      logger.info("Shuting down Host now ....");
      aRuntime shell = new aRuntime();
      shell.executePSScript(filepath, true);
    }
  }

  private void Rename(String filename) {
    String[] cmdarray = this.loadScript(filename);
    this.modifyScript(cmdarray);
    this.createScript(cmdarray, filename);
    Path filepath = Paths.get(TMP_Dir + filename);
    
    if(FileTools.Exists(filepath) == false){
      logger.error("Script not found: " + filepath);
      this.triggerCloseEvent();
    }

    //Do the JOB
    logger.info("Renaming Host to " + host.getName());
    if(this.debug == false){
      aRuntime shell = new aRuntime();
      shell.executePSScript(filepath, true);
      //Delete tmp Script with passwords
      FileTools.Delete(Paths.get(TMP_Dir + "Rename.ps1"));
    }
    logger.info("Host Renamed---------------------------------------------");
  }

  /**
   * Replace placehoders
   * @param cmdarray
   * @param replaceMap
   */
  private void modifyScript(String[] cmdarray) {
    CryptClass crypt = new CryptClass();
    //get Admin Password
    String adminpasswd = crypt.decrypt(adminObject.getPasswd());
    String localadminpasswd = crypt.decrypt(localAdminObject.getPasswd());

    Map<String, String> replaceMap = new HashMap<>();
    replaceMap.put("\\{% username %\\}", adminObject.getUsername());
    replaceMap.put("\\{% password %\\}", adminpasswd);
    replaceMap.put("\\{% newhostname %\\}", host.getName());
    replaceMap.put("\\{% oldhostname %\\}", this.getHostName());
    replaceMap.put("\\{% domain %\\}", host.getDomainname());

    replaceMap.put("\\{% localadmin %\\}", localAdminObject.getUsername());
    replaceMap.put("\\{% localadminpasswd %\\}", localadminpasswd);

    replaceMap.entrySet().forEach((entry) -> {
      //System.out.println(entry.getKey() + "/" + entry.getValue());
      for (int i = 0; i < cmdarray.length; i++) {
        String line = cmdarray[i];
        cmdarray[i] = line.replaceAll(entry.getKey(), entry.getValue());
      }
    });
  }

  /**
   * Falls nicht existiert = 0 1... Renamed 2... Joined Domain
   *
   * @param status
   */
  private void setLockFileStatus(int status, String msg) {
    LinkedList<String> data = new LinkedList<>();
    //Lock File gibt es nicht
    if (FileTools.Exists(lockfile) == false) {
      FileTools.createFile(lockfile);
    }
    data.add(msg);
    data.add("" + status);

    FileTools.WritetoFile(lockfile, data);
    logger.info("Lock File gesetzt (" + status + ") ...");
  }

  /**
   * hängt Zeile dran
   *
   * @param status
   * @param msg
   */
  private void appendLockFileStatus(int status, String msg) {
    LinkedList<String> data = FileTools.ReadFile(lockfile.toFile());
    //Alte Datei löschen
    FileTools.Delete(lockfile);

    data.add(msg);
    data.add("" + status);

    FileTools.WritetoFile(lockfile, data);
    logger.info("Lock File gesetzt (" + status + ") ...");
  }

  private int getLockFilestatus() {
    try {
      LinkedList<String> lines = FileTools.ReadFile(lockfile.toFile());
      //letzter Eintrag ist letzte Aktion
      String line = lines.get(lines.size() - 1);
      return Integer.parseInt(line);
    } 
    catch (NumberFormatException | IndexOutOfBoundsException e) {
      return -1;
    }
  }

  /**
   * KMS Stuff /rearm > /ato
   *
   * @param filename
   */
  private void KMS(String filename) {
    String[] cmdarray = this.loadScript(filename);
    this.modifyScript(cmdarray);
    this.createScript(cmdarray, filename);
    Path filepath = Paths.get(SCRIPT_Dir + filename);
    
    if(FileTools.Exists(filepath) == false){
      logger.error("Script not found: " + filename);
      this.triggerCloseEvent();
    }
    
    logger.info("Activating KMS Client " + host.getDomainname());
    if(this.debug == false){
      //Do the JOB
      aRuntime shell = new aRuntime();
      shell.executePSScript(filepath, true);
    }
  }

}
