package mysql;

import SH.Bibliothek.NET.NETUtils;
import main.HostObject;
import crypt.CryptClass;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import org.slf4j.LoggerFactory;

/**
 * Alles zu MySQL
 *
 * @author Mag. Stefan Hagmann
 */
public class MySQL extends JDBC_MySQL{
  private static final org.slf4j.Logger logger = LoggerFactory.getLogger(MySQL.class);
  private final String ipwithCIDR;
  private String hostname;
  private boolean debug;
  private HostObject host;

  /**
   * MySQL Stuff
   * @param url like jdbc:mysql://localhost:3306/test";
   * @param user
   * @param pwd
   * @param ipwithCIDR Server Adr. in CIDR Schreibweise
   */
  public MySQL(String url, String user, String pwd, String ipwithCIDR) {
    super(url, user, pwd);
    this.ipwithCIDR = ipwithCIDR;
    this.startup();
  }
  
  private void startup(){
    String hostip = this.getHostnamefromUrl();
    // set clear text passwprd
    if (NETUtils.isIP(hostip)) {
      CryptClass crypt = new CryptClass();
      String plaintext = crypt.decrypt(pwd);
      this.pwd = plaintext;
    } else {
      logger.error(hostip + " ist keine gültige Adresse!");
    }
  }
  
  public void LoadData(HostObject host) {
    this.connect();
    this.host = host;
    String firstMac = host.getFirstMac();
    if("".equals(firstMac)){
      // MAC Adr ermitteln
      NETUtils net = new NETUtils();
      //parameter is a Inetadress to Test Connectivity in CIDR notation
      //here Server Adr.
      ArrayList<String> allMAC = net.getAllMAC(this.ipwithCIDR);
      host.setMacs(allMAC);
    }
    //SQL Stmt mit OR aller MAC's bauen
    String sql = host.getSQL();

    logger.info("SQL Query for: "+ host.getMacListasString());
    //Daten vom Server laden
    String stmt = "SELECT * FROM "+this.getDatabasefromUrl()+"."+this.default_table+" WHERE "+sql;
    ResultSet rst = this.query(stmt);

    this.handleResult(rst);
  }

  @Override
  protected void handleResult(ResultSet rs) {
    try {
      while (rs.next()) {
        this.host.setId(rs.getInt("id"));
        String hostname = rs.getString("host");
        this.host.setName(hostname);
        this.hostname = hostname;
      }
      rs.close();
    } catch (SQLException sqlEx) {
      sqlEx.printStackTrace();
    } 
    finally {
      try {
        //the actual Statement
        stmt.close();
        //close open Connection
        con.close();
      } catch (SQLException se) {}
    }
  }

  /**
   * The founded hostname
   * @return 
   */
  public String getHostname() {
    return hostname;
  }

  public void setDebug(boolean DEBUG) {
    this.debug = DEBUG;
  }

  public void setHostname(String name) {
    this.hostname = name;
  }
  
  

  

  
}
