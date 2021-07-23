package mysql;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.slf4j.LoggerFactory;

public abstract class JDBC_MySQL {
  private static final org.slf4j.Logger logger = LoggerFactory.getLogger(JDBC_MySQL.class);

  // JDBC variables for opening and managing connection
  protected Connection con;
  protected ResultSet rs;
  
  protected String url;
  protected String user;
  protected String pwd;
  protected String default_table;
  protected Statement stmt;

  //https://javarevisited.blogspot.com/2015/06/how-to-connect-to-mysql-database-in-java-jdbc-example.html
  /**
   * @param url like jdbc:mysql://localhost:3306/test";
   * @param user Username
   * @param pwd Password
   */
  public JDBC_MySQL(String url, String user, String pwd) {
    this.url = url;
    this.user = user;
    this.pwd = pwd;
    try {
        Class.forName("com.mysql.cj.jdbc.Driver").getDeclaredConstructor();
    } catch (ClassNotFoundException | NoSuchMethodException | SecurityException ex) {
        logger.error("Error: mysql-connector-java ( MySQL Connector/J ) not found");
    }
  }

  public void setUrl(String url) {
    this.url = url;
  }

  public void setUser(String user) {
    this.user = user;
  }

  public void setPwd(String pwd) {
    this.pwd = pwd;
  }

  public Connection getCon() {
    return con;
  }

  public ResultSet getRs() {
    return rs;
  }
  
  /**
   * Stelle Verbindung her
   */
  public void connect(){
    try {
      if(this.con != null){
        //Connection is open
        return;
      }
      // opening database connection to MySQL server
      this.con = DriverManager.getConnection(this.url, this.user, this.pwd);
    } catch (SQLException ex) {
      logger.error("Error: connecting to MySQL Server with "+this.url);
      logger.error("SQLException: " + ex.getMessage());
      logger.error("SQLState: " + ex.getSQLState());
      logger.error("VendorError: " + ex.getErrorCode());
    }
    catch (Exception ex){
      ex.printStackTrace(System.out);
    }
  }

  /**
   * Query MySQL an get Result
   * @param query like select count(*) from books
   * @return Resultset
   */
  public ResultSet query(String query) {
    try {
      this.connect();
      // getting Statement object to execute query
      this.stmt = this.con.createStatement(); 
      // executing SELECT query
      ResultSet data = stmt.executeQuery(query);
      
      return data;
    } catch (SQLException ex) {
      logger.error("Error: connecting to MySQL Server with "+this.url);
      logger.error("SQLException: " + ex.getMessage());
      logger.error("SQLState: " + ex.getSQLState());
      logger.error("VendorError: " + ex.getErrorCode()); 
    }
    catch (Exception ex){
      ex.printStackTrace(System.out);
    }
    return null;
  }
  
  /**
   * get the IP Part from JDBC String
   * jdbc:mysql://localhost:3306/test"
   * @return localhost
   */
  protected String getHostnamefromUrl() {
    String part = "jdbc:mysql://";
    part = this.url.substring(part.length());
    String[] split = part.split(":");
    return split[0];
  }
  
  /**
   * get the DB Part from JDBC String
   * jdbc:mysql://10.0.10.4:3306/admintools?serverTimezone=Europe/Vienna
   * @return admintools
   */
  protected String getDatabasefromUrl(){
    String part = "jdbc:mysql://";
    part = this.url.substring(part.length());
    String[] split = part.split("/");
    // remove everything after ?
    part = split[1];
    String pattern = "?";
    
    int index = part.indexOf(pattern);
    if( index != -1){
      part = part.substring(0, part.indexOf(pattern));
    }
    return part;
  }
  
  /**
   * Handle your Resultset
   * Dont forget to close stmt an con after handeling the Resultset
   * @param rs a Resultset
   */
  protected abstract void handleResult(ResultSet rs);
  
  /**
   * Table to use in all SQL Statements per default
   * @param table 
   */
  public void setDefaultTable(String table) {
    this.default_table = table;
  }
  
  

}
