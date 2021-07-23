package crypt;

import org.jasypt.util.text.BasicTextEncryptor;

/**
 * Not really Save!!
 *
 * @author kustos
 */
public class CryptClass {
  private final String key="kjshgdhj3gk4hg324hgbkbhjblkfkw";

  /**
   * Encrpt a String
   * @param msg
   * @return 
   */
  public String encrypt(String msg) {
    BasicTextEncryptor textEncryptor = new BasicTextEncryptor();
    textEncryptor.setPassword(key);
    return "ENC(" + textEncryptor.encrypt(msg) + ")";
  }
  
  /**
   * Decrypt
   * @param hash ENC(.....)
   * @return 
   */
  public String decrypt(String hash) {
    BasicTextEncryptor textEncryptor = new BasicTextEncryptor();
    textEncryptor.setPassword(key);
    
    //remove ENC( )
    String newhash = hash.substring(4, hash.length()-1);
    
    return textEncryptor.decrypt(newhash);
  }
}
