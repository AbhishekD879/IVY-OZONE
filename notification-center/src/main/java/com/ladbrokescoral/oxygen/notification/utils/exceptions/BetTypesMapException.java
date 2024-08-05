package com.ladbrokescoral.oxygen.notification.utils.exceptions;

/**
 * Class that wraps the runtime exception for managing bet types uninitialized bet type map
 * exception.
 */
public class BetTypesMapException extends RuntimeException {

  public BetTypesMapException(String message) {
    super(message);
  }

  public BetTypesMapException(String message, Throwable cause) {
    super(message, cause);
  }
}
