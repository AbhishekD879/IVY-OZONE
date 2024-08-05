package com.ladbrokescoral.aggregation.exception;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@Slf4j
@ControllerAdvice
public class ErrorHandler {

  @ExceptionHandler(BadRequestException.class)
  public ResponseEntity<String> handleNotFoundException(BadRequestException badRequestException) {
    String ouputErrorMessage = "Error occurred while fetching silks";
    log.error("BadRequestException: ", badRequestException.getMessage());
    return ResponseEntity.badRequest().body(ouputErrorMessage);
  }
}
