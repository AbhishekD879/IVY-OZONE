package com.ladbrokescoral.reactions.exception;

/**
 * @author PBalarangakumar 22-06-2023
 */
public abstract class GenericException extends RuntimeException {
  protected GenericException(final String errorMessage) {
    super(errorMessage);
  }

  protected GenericException(final String errorMessage, final Throwable cause) {
    super(errorMessage, cause);
  }

  public abstract ErrorCode getErrorCode();
}
