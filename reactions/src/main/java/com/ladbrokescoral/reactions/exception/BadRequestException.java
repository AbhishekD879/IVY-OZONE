package com.ladbrokescoral.reactions.exception;

import java.io.Serial;

/**
 * @author PBalarangakumar 22-06-2023
 */
public class BadRequestException extends GenericException {

  @Serial private static final long serialVersionUID = 2582424685146051042L;

  private final ErrorCode errorCode;

  public BadRequestException(final String errorMessage) {
    super(errorMessage);
    this.errorCode = ErrorCode.BAD_REQUEST;
  }

  public BadRequestException(final String errorMessage, final ErrorCode errorCode) {
    super(errorMessage);
    this.errorCode = errorCode;
  }

  public BadRequestException(
      final String errorMessage, final ErrorCode errorCode, final Throwable cause) {
    super(errorMessage, cause);
    this.errorCode = errorCode;
  }

  @Override
  public ErrorCode getErrorCode() {
    return this.errorCode;
  }
}
