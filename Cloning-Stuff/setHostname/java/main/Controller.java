package main;

import SH.FileTools.FileTools;
import SH.Xml.XMLTool;
import exec.HostWorker;
import java.io.File;
import java.net.URL;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ResourceBundle;
import java.util.TimeZone;
import java.util.logging.Level;
import javafx.application.Platform;
import javafx.fxml.Initializable;
import javafx.stage.Stage;
import mysql.MySQL;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import xml.configHandler;

/**
 * FXML Controller class
 *
 * @author Stefan
 */
public class Controller{

  private final Logger logger = LoggerFactory.getLogger(SetHostname.class);

  // do nothing, just simulate
  public final boolean DEBUG = false;

  final String configFileName = "config.xml";
  final String debugHostname = "DummyHostname";

  // with Timezone Issue
  // private final String SQL_JDBC = "jdbc:mysql://%s:3306/%s?serverTimezone=" + TimeZone.getDefault().getID();
  private final String SQL_JDBC = "jdbc:mysql://%s:3306/%s";

  private MySQL mysql;
  private AdminObject domainAdminObject;
  private AdminObject localAdminObject;
  private HostObject host;
  private boolean kmsON = false;
  private Stage primaryStage;


  public void Close() {
    Platform.exit();
    System.exit(0);
  }

  public void StartWorking() {
    //Create Password Hash
    /*
    CryptClass crypt = new CryptClass();
    String encrypt = crypt.encrypt("HansMoser");
     */
    //schule = ENC(3sjSYbUGt14ubjbbl5Q/FQ==)
    //XYZ123=ENC(S/7MWIrdwxHhVNROABFNvQ==)
    if (DEBUG) {
      logger.info("=== DEBUGGING ===");
    }

    host = new HostObject();
    DeleteTMP();
    LoadConfig();

    //Daten laden
    if (DEBUG == false) {
      mysql.LoadData(host);
      if (host.getId() == -1) {
        logger.error("Die MAC Adresse " + host.getMacListasString() + " existiert nicht!");
        logger.error("Exit");
        System.exit(0);
      }
    }
    if (DEBUG == false) {
      host.setName(mysql.getHostname());
    } else {
      host.setName(debugHostname);
    }
    logger.info("Debug Informations:");
    String msg = String.format("MAC: %s, Hostname: %s gefunden!", host.getMacListasString(), host.getName());
    if (DEBUG) {
      msg = String.format("MAC: %s, Hostname: %s gefunden!", "-keine-", host.getName());
    }
    logger.info(msg);
    //Host existiert umbenennen starten
    HostWorker work = new HostWorker(host, domainAdminObject, localAdminObject, kmsON, DEBUG);

    //Delay gib Windows etwas Zeit to complete StartUp
    if (DEBUG == false) {
      Wait(10000);
    }
    work.doTheJob();

    //Clean Shutdown macht Hostworker
  }

  /**
   * Lädt aus einer XML Datei alle Config einstellungen
   */
  private void LoadConfig() {
    try {
      configHandler handle = new configHandler();
      File file = Paths.get(configFileName).toFile();

      XMLTool.LoadXMLFile(file, handle);
      host.setDomainname(handle.domainname);

      domainAdminObject = new AdminObject();
      domainAdminObject.setUsername(handle.admin);
      domainAdminObject.setPasswd(handle.adminpasswd);

      localAdminObject = new AdminObject();
      localAdminObject.setUsername(handle.localadmin);
      localAdminObject.setPasswd(handle.localadminpasswd);

      //Teste die Verbindung zu Mysql
      if (DEBUG == false) {
        String server = this.removeCIDR(handle.server);
        String url = String.format(SQL_JDBC, server, handle.db);
        //table , handle.mac
        mysql = new MySQL(url, handle.user, handle.password, handle.server);
        mysql.setDefaultTable(handle.mactable);
      }
      if (handle.kmsstr.compareToIgnoreCase("true") == 0) {
        kmsON = true;
      }
    } catch (Exception ex) {
      System.exit(1);
    }
  }

  /**
   * löscht das TMP Verzeichnis, da stehen Passwörter drinnen
   */
  private void DeleteTMP() {
    Path tmppath = Paths.get("tmp/");
    FileTools.deleteDir(tmppath.toFile());
  }

  private void Wait(int i) {
    try {
      Thread.sleep(i);
    } catch (InterruptedException ex) {
      java.util.logging.Logger.getLogger(SetHostname.class.getName()).log(Level.SEVERE, null, ex);
    }
  }

  /**
   * Entfernt von einer IP Adr/CIDR den CIDR Part
   *
   * @param hostname
   * @return
   */
  private String removeCIDR(String hostname) {
    //CIDR weg
    String[] st = hostname.split("/");
    if (st.length != 2) {
      logger.error("Invalid CIDR format '"
              + hostname + "', should be: xx.xx.xx.xx/xx");
    }
    //String cidr = st[1];
    return st[0];
  }          
}
