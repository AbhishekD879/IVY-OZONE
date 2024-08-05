package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.google.common.collect.Iterables;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.controller.public_api.Public;
import com.ladbrokescoral.oxygen.cms.api.exception.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import javax.servlet.http.HttpServletRequest;
import javax.validation.ConstraintViolationException;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.boot.web.servlet.error.ErrorAttributes;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.multipart.MultipartException;

@ControllerAdvice(basePackageClasses = {AbstractCrudController.class, Public.class})
@Slf4j
public class ApiErrorHandler extends AbstractErrorHandler {

  private static final String VALIDATION_ERROR_MESSAGE = "Validation error : ";

  public ApiErrorHandler(ErrorAttributes errorAttributes) {
    super(errorAttributes);
  }

  @ExceptionHandler(ValidationException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  @ResponseBody
  public String validationError(ValidationException e) {
    log.error(VALIDATION_ERROR_MESSAGE, e);
    return e.getMessage();
  }

  @ExceptionHandler(SiteServeMarketValidationException.class)
  @ResponseStatus(HttpStatus.OK)
  @ResponseBody
  public Map<String, Object> siteserveMarketValidationError(
      SiteServeMarketValidationException e, HttpServletRequest request) {
    log.error(VALIDATION_ERROR_MESSAGE, e);
    return buildResponseEntity(
        request, HttpStatus.OK.value(), "SiteServeMarketValidation", "Market", e.getMessage());
  }

  @ExceptionHandler(ConstraintViolationException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  @ResponseBody
  public String constraintViolationError(ConstraintViolationException e) {
    List<String> violationsList = new ArrayList<>();
    e.getConstraintViolations()
        .iterator()
        .forEachRemaining(
            violation ->
                violationsList.add(
                    String.format(
                        "%s %s",
                        Iterables.getLast(violation.getPropertyPath()), violation.getMessage())));

    return violationsList.stream().collect(Collectors.joining(System.lineSeparator()));
  }

  @ExceptionHandler(MultipartException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  @ResponseBody
  public String multipartError(MultipartException e) {
    log.error("Multipart request exception : ", e);
    return e.getMessage();
  }

  @ExceptionHandler(HttpMessageNotReadableException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  @ResponseBody
  public Map<String, Object> notReadableRequest(
      HttpMessageNotReadableException e, HttpServletRequest request) {
    String fieldName = "";
    if (e.getCause() instanceof JsonMappingException) {
      fieldName = ((JsonMappingException) e.getCause()).getPath().get(0).getFieldName();
    } else if (e.getCause() instanceof JsonParseException) {
      fieldName =
          ((JsonParseException) e.getCause()).getProcessor().getParsingContext().getCurrentName();
    }
    return buildResponseEntity(
        request,
        HttpStatus.BAD_REQUEST.value(),
        "InvalidRequestedData",
        fieldName,
        String.format("Wrong requested data of field: %s ", fieldName));
  }

  @ExceptionHandler(IllegalArgumentException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  @ResponseBody
  public Map<String, Object> illegalArgumentError(
      IllegalArgumentException exception, HttpServletRequest request) {
    log.error(VALIDATION_ERROR_MESSAGE, exception);

    return buildResponseEntity(
        request,
        HttpStatus.BAD_REQUEST.value(),
        "InvalidRequestedData",
        HttpStatus.BAD_REQUEST.name(),
        exception.getMessage());
  }

  @ExceptionHandler(MethodArgumentTypeMismatchException.class)
  @ResponseBody
  public ResponseEntity<Object> handleMethodArgumentTypeMismatchException(
      MethodArgumentTypeMismatchException e, HttpServletRequest request) {
    Class<?> type = e.getRequiredType();
    String message;
    if (type.isEnum()) {
      message =
          "The parameter "
              + e.getName()
              + " must have a value from list : "
              + StringUtils.join(type.getEnumConstants(), ", ");
    } else {
      message = "The parameter " + e.getName() + " must be of type " + type.getTypeName();
    }
    return new ResponseEntity<>(message, HttpStatus.BAD_REQUEST);
  }

  @ExceptionHandler(BadRequestException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  @ResponseBody
  public String badRequestException(BadRequestException e) {
    return e.getMessage();
  }

  @ExceptionHandler(InternalServerException.class)
  @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
  @ResponseBody
  public String internalServerError(InternalServerException e) {
    log.error("Internal Server Error", e);
    return e.getMessage();
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  @ResponseBody
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  public String handleMethodArgumentNotValidException(
      MethodArgumentNotValidException ex, HttpServletRequest request) {

    List<String> errors = new ArrayList<>();

    ex.getBindingResult()
        .getFieldErrors()
        .iterator()
        .forEachRemaining(
            error ->
                errors.add(
                    String.format(
                        "%s %s %s",
                        (error.getField()),
                        (error.getRejectedValue()),
                        error.getDefaultMessage())));

    ex.getBindingResult()
        .getGlobalErrors()
        .iterator()
        .forEachRemaining(
            error ->
                errors.add(
                    String.format("%s %s", (error.getObjectName()), error.getDefaultMessage())));

    return errors.stream().collect(Collectors.joining(System.lineSeparator()));
  }

  @ExceptionHandler({LuckyDipConfigNotFoundException.class, LuckyDipMappingNotFoundException.class})
  @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
  @ResponseBody
  public ResponseDto handleInternalServerException(Exception e) {
    log.error("Internal Server Error", e);
    return new ResponseDto(e.getMessage());
  }

  @Data
  @AllArgsConstructor
  public static class ResponseDto {
    private String message;
  }
}
