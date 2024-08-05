package com.egalacoral.spark.timeform.api.connectivity;

/**
 * Interface for providing current time.
 *
 * Generally is used for testing purposes.
 * */
public interface TimeProvider {

  /**
   * @return current time in milliseconds
   * */
  long currentTime();

}
