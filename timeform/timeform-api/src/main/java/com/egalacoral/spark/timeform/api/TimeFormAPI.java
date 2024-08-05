package com.egalacoral.spark.timeform.api;

/**
 * This class allows you to login into TimeForm API
 *
 * <p>Instance of this class can be created through TimeFormAPIBuilder class
 */
@FunctionalInterface
public interface TimeFormAPI {

  /**
   * Login into timeform system
   *
   * @return instance of TimeFormService class which should be used for data retrivement
   */
  TimeFormService login(String userName, String password);
}
