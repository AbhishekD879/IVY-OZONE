package com.ladbrokescoral.reactions.exception;

import java.io.Serial;

/**
 * @author PBalarangakumar 22-06-2023
 */
public class ServiceExecutionException extends GenericException {

  @Serial private static final long serialVersionUID = -4869190787933894304L;

  public ServiceExecutionException(final String errorMessage) {
    super(errorMessage);
  }

  public ServiceExecutionException(final String errorMessage, final Throwable cause) {
    super(errorMessage, cause);
  }

  @Override
  public ErrorCode getErrorCode() {
    return ErrorCode.SERVER_ERROR;
  }
}
