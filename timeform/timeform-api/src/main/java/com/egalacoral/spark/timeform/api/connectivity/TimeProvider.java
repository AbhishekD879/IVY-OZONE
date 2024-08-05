package com.egalacoral.spark.timeform.api.connectivity;

/**
 * Interface for providing current time.
 *
 * <p>Generally is used for testing purposes.
 */
@FunctionalInterface
public interface TimeProvider {

  /** @return current time in milliseconds */
  long currentTime();
}
