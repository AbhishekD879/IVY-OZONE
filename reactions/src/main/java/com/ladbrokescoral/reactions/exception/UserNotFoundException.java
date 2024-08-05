package com.ladbrokescoral.reactions.exception;

import java.io.Serial;

/**
 * @author PBalarangakumar 11-09-2023
 */
public class UserNotFoundException extends GenericException {

  @Serial private static final long serialVersionUID = 2582999685146051049L;

  private final ErrorCode errorCode;

  public UserNotFoundException(final String errorMessage) {
    super(errorMessage);
    this.errorCode = ErrorCode.NOT_FOUND;
  }

  @Override
  public ErrorCode getErrorCode() {
    return this.errorCode;
  }
}
