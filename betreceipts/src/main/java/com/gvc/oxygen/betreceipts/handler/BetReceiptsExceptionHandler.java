package com.gvc.oxygen.betreceipts.handler;

import com.gvc.oxygen.betreceipts.exceptions.JsonSerializeDeserializeException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@Slf4j
@RestControllerAdvice
public class BetReceiptsExceptionHandler extends ResponseEntityExceptionHandler {

  @ExceptionHandler(JsonSerializeDeserializeException.class)
  @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
  public ResponseEntity<String> handleJsonProcessingException(
      JsonSerializeDeserializeException ex) {
    log.warn("Error in json serialization/deserialization", ex.getCause());
    return new ResponseEntity<>(
        "Json Processing Error: " + ex.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
  }
}
