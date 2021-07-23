package main;

/**
 * @author Mag. Stefan Hagmann
 */
public class SetHostname {

  private static Controller controller;

  /**
   * @param args the command line arguments
   */
  public static void main(String[] args) {
    controller = new Controller();
    controller.StartWorking();
  }
}
