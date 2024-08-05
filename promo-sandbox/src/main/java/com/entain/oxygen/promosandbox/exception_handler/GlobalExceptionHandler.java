package com.entain.oxygen.promosandbox.exception_handler;

import com.entain.oxygen.promosandbox.dto.ErrorMessagedDto;
import com.entain.oxygen.promosandbox.exception.BppTokenRequiredException;
import com.entain.oxygen.promosandbox.exception.InvalidBppTokenException;
import com.entain.oxygen.promosandbox.exception.PromoSandboxException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import javax.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingRequestHeaderException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice(basePackages = "com.entain.oxygen.promosandbox.controller")
@Slf4j
public class GlobalExceptionHandler {

  @ExceptionHandler({MethodArgumentNotValidException.class, MissingRequestHeaderException.class})
  public ResponseEntity<String> handleMethodArgumentNotValidException(
      MethodArgumentNotValidException ex, HttpServletRequest request) {
    List<String> errors = new ArrayList<>();
    ex.getBindingResult()
        .getFieldErrors()
        .iterator()
        .forEachRemaining(
            error ->
                errors.add(String.format("%s %s", (error.getField()), error.getDefaultMessage())));

    return new ResponseEntity<>(
        errors.stream().collect(Collectors.joining(System.lineSeparator())),
        HttpStatus.BAD_REQUEST);
  }

  @ExceptionHandler(value = {BppTokenRequiredException.class})
  public ResponseEntity<ErrorMessagedDto> handleBppTokenRequiredException(
      BppTokenRequiredException ex) {
    log.error("Error in handleBppTokenRequiredException: {} ", ex.getMessage());
    return new ResponseEntity<>(
        new ErrorMessagedDto(ex.getLocalizedMessage()), HttpStatus.BAD_REQUEST);
  }

  @ExceptionHandler(value = {InvalidBppTokenException.class})
  public ResponseEntity<ErrorMessagedDto> handleInvalidBppTokenException(
      InvalidBppTokenException ex) {
    log.error("Error in handleInvalidBppTokenException: {} ", ex.getMessage());
    return new ResponseEntity<>(
        new ErrorMessagedDto(ex.getLocalizedMessage()), HttpStatus.UNAUTHORIZED);
  }

  @ExceptionHandler(value = {PromoSandboxException.class})
  public ResponseEntity<ErrorMessagedDto> handlePromoCmsException(PromoSandboxException ex) {
    log.error("Error in handlePromoCmsException: {} ", ex.getMessage());
    return new ResponseEntity<>(
        new ErrorMessagedDto(ex.getLocalizedMessage()), HttpStatus.INTERNAL_SERVER_ERROR);
  }

  @ExceptionHandler(value = {Exception.class})
  public ResponseEntity<Object> handleAllOtherException(Exception ex) {
    log.error("Error in handleAllOtherException: {} ", ex.getMessage());
    return new ResponseEntity<>(
        new ErrorMessagedDto(ex.getLocalizedMessage()), HttpStatus.INTERNAL_SERVER_ERROR);
  }
}
