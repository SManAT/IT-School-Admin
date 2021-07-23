package main;

import java.util.ArrayList;
import java.util.Iterator;

public class HostObject {

  private int id;
  private ArrayList<String> macs;
  private String name = "NotSet";
  private String domainname = "NotSet";

  public HostObject() {
    macs = new ArrayList<>();
    // default
    this.id = -1; 
  }

  public int getId() {
    return id;
  }

  public void setId(int id) {
    this.id = id;
  }

  public ArrayList<String> getMacs() {
    return macs;
  }

  public void setMacs(ArrayList<String> macs) {
    this.macs = macs;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getDomainname() {
    return domainname;
  }

  public void setDomainname(String domainname) {
    this.domainname = domainname;
  }

  public String getFQDN() {
    return name + "." + domainname;
  }

  /**
   * Erste Mac aus Liste
   * @return
   */
  public String getFirstMac() {
    try {
      return this.macs.get(0);
    } catch (IndexOutOfBoundsException e) {
      return "";
    }
  }

  /**
   * liefert für den SQL String die OR für Macs
   * @return 
   */
  public String getSQL() {
    String sql = "";
    Iterator<String> iterator = macs.iterator();
    while (iterator.hasNext()) {
      String mac = iterator.next();
      sql += "mac='" + mac + "' OR ";
    }
    return sql.substring(0, sql.length() - 4);
  }

  /**
   * String Liste der MAC Adressen
   * @return
   */
  public String getMacListasString() {
    try {
      String erg = "";
      Iterator<String> iterator = macs.iterator();
      while (iterator.hasNext()) {
        String mac = iterator.next();
        erg += mac + ";  ";
      }
      return erg.substring(0, erg.length() - 3);
    } catch (Exception ex) {
      return "Error";
    }
  }
}
