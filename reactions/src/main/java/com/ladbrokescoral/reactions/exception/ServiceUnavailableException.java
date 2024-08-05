package com.ladbrokescoral.reactions.exception;

/**
 * @author PBalarangakumar 22-06-2023
 */
public class ServiceUnavailableException extends GenericException {

  public ServiceUnavailableException(final String errorMessage) {
    super(errorMessage);
  }

  public ServiceUnavailableException(final String errorMessage, final Throwable cause) {
    super(errorMessage, cause);
  }

  @Override
  public ErrorCode getErrorCode() {
    return ErrorCode.SERVICE_UNAVAILABLE;
  }
}
