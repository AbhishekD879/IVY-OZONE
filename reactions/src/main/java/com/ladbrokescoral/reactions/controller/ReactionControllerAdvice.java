package com.ladbrokescoral.reactions.controller;

import com.ladbrokescoral.reactions.dto.ErrorDTO;
import com.ladbrokescoral.reactions.exception.*;
import java.time.OffsetDateTime;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.server.ServerWebInputException;

/**
 * @author PBalarangakumar 26-06-2023
 */
@Slf4j
@RestControllerAdvice
public class ReactionControllerAdvice {

  @ExceptionHandler({BadRequestException.class, ServerWebInputException.class})
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  public ErrorDTO handleBadRequest(final GenericException exception) {
    log.error("Bad request error occurred. ", exception);
    return buildErrorDTO(exception.getErrorCode(), exception.getMessage());
  }

  @ExceptionHandler({ServiceExecutionException.class, ServiceUnavailableException.class})
  @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
  public ErrorDTO handleServerError(final GenericException exception) {
    log.error("Server error occurred. ", exception);
    return buildErrorDTO(ErrorCode.SERVER_ERROR, exception.getMessage());
  }

  @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
  @ExceptionHandler({RuntimeException.class})
  public ErrorDTO handleUnexpected(final RuntimeException exception) {
    log.error("An unexpected internal error has occurred. ", exception);
    return buildErrorDTO(ErrorCode.SERVER_ERROR, "An unexpected error has occurred.");
  }

  @ExceptionHandler({UserNotFoundException.class})
  @ResponseStatus(HttpStatus.NOT_FOUND)
  public ErrorDTO handleNotFound(final GenericException exception) {
    log.error("Not found error occurred. ", exception);
    return buildErrorDTO(ErrorCode.NOT_FOUND, exception.getMessage());
  }

  private ErrorDTO buildErrorDTO(final ErrorCode errorCode, final String errorMessage) {

    return new ErrorDTO(errorCode, errorMessage, OffsetDateTime.now());
  }
}
