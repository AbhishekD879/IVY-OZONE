package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import java.util.List;
import java.util.stream.Collectors;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
public class ValidImageErrorHandler {

  @ExceptionHandler(BindException.class)
  public ResponseEntity<String> processException(final BindException ex) {

    List<FieldError> errorList = ex.getBindingResult().getFieldErrors();

    String errorMessage =
        errorList.stream()
            .map(fieldError -> fieldError.getField() + " - " + fieldError.getDefaultMessage())
            .sorted()
            .collect(Collectors.joining(",\n"));

    return new ResponseEntity<>(errorMessage, HttpStatus.INTERNAL_SERVER_ERROR);
  }
}
