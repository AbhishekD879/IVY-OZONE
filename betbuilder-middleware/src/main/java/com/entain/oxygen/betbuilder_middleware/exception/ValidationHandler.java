package com.entain.oxygen.betbuilder_middleware.exception;

import java.text.SimpleDateFormat;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.context.support.DefaultMessageSourceResolvable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.support.WebExchangeBindException;

@ControllerAdvice
public class ValidationHandler {

  @ExceptionHandler(WebExchangeBindException.class)
  public ResponseEntity<Map<String, Object>> handleException(WebExchangeBindException e) {
    List<String> errors =
        e.getBindingResult().getAllErrors().stream()
            .map(DefaultMessageSourceResolvable::getDefaultMessage)
            .toList();
    Map<String, Object> errorMap = new HashMap<>();

    errorMap.put("path", "/checkPrice");
    errorMap.put("errorMessage", errors);
    errorMap.put(
        "timestamp",
        new SimpleDateFormat("yyyy-MM-dd'T'hh:mm:ss.SSS").format(System.currentTimeMillis()));

    return ResponseEntity.badRequest().body(errorMap);
  }
}
