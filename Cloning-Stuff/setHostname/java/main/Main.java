package main;

/**
 * Starter Class otherwise we are getting errors when we start from Console
 * or with double click (missing JavaFX Components)
 * 
 * If the JavaFX library is on the class-path then your main class cannot be an instance of Application. 
 * You'll have to create a separate launcher class an invoke Application.launch(YourApp.class, args) from the main method
 * @author Mag. Stefan Hagmann
 */
public class Main{
  /**
   * @param args the command line arguments
   */
  public static void main(String[] args) {
    SetHostname.main(args);
  }
}
