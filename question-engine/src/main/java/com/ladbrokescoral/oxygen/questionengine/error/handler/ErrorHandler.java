package com.ladbrokescoral.oxygen.questionengine.error.handler;

import com.ladbrokescoral.oxygen.questionengine.error.ApiError;
import com.ladbrokescoral.oxygen.questionengine.exception.InvalidBppTokenException;
import com.ladbrokescoral.oxygen.questionengine.exception.NotFoundException;
import com.ladbrokescoral.oxygen.questionengine.exception.QuizRewardNotAssignedException;
import com.ladbrokescoral.oxygen.questionengine.exception.QuizSubmissionException;
import com.ladbrokescoral.oxygen.questionengine.exception.UnauthorizedException;
import com.newrelic.api.agent.NewRelic;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import javax.inject.Provider;
import javax.validation.ConstraintViolation;
import javax.validation.ConstraintViolationException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.ArrayUtils;
import org.apache.commons.lang3.StringUtils;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;
import org.springframework.web.util.ContentCachingRequestWrapper;


@Slf4j
@RestControllerAdvice
@RequiredArgsConstructor
public class ErrorHandler extends ResponseEntityExceptionHandler {
  private static final String ERROR_DELIMITER = "; ";

  private final Provider<ContentCachingRequestWrapper> requestProvider;

  @ExceptionHandler(NotFoundException.class)
  @ResponseStatus(HttpStatus.NOT_FOUND)
  public ResponseEntity<ApiError> handleNotFoundException(NotFoundException ex) {
    log.warn("Not found. Request content: " + getRequestContent(), ex);
    return new ApiError()
        .setHttpStatus(HttpStatus.NOT_FOUND)
        .setReason(ex.getMessage())
        .asResponseEntity();
  }

  @ExceptionHandler(UnauthorizedException.class)
  @ResponseStatus(HttpStatus.UNAUTHORIZED)
  public ResponseEntity<ApiError> handleUnauthorizedException(UnauthorizedException ex) {
    log.warn("{}. Request content: {}", ex.getMessage(), getRequestContent());
    NewRelic.noticeError(ex);
    return new ApiError()
        .setHttpStatus(HttpStatus.UNAUTHORIZED)
        .setReason("Unauthorized")
        .asResponseEntity();
  }

  @ExceptionHandler(InvalidBppTokenException.class)
  @ResponseStatus(HttpStatus.UNAUTHORIZED)
  public ResponseEntity<ApiError> handleInvalidBppTokenException(InvalidBppTokenException ex) {
    log.warn("{}. Request content: {}", ex.getMessage(), getRequestContent());
    NewRelic.noticeError(ex);

    return new ApiError()
        .setHttpStatus(HttpStatus.UNAUTHORIZED)
        .setReason("Unauthorized")
        .asResponseEntity();
  }

  @ExceptionHandler(Exception.class)
  @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
  public ResponseEntity<ApiError> handleUnknownException(Exception ex) {
    log.error("Unexpected exception occurred. Request content: " + getRequestContent(), ex);
    NewRelic.noticeError(ex);

    return new ApiError()
        .setHttpStatus(HttpStatus.INTERNAL_SERVER_ERROR)
        .setReason("Oops... Something went wrong. Please ensure you're referring to the existing resource or contact our support team")
        .asResponseEntity();
  }

  @ExceptionHandler(ConstraintViolationException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  public ResponseEntity<ApiError> handleValidationException(ConstraintViolationException ex) {
    log.warn("Constraint Violation Exception. Request content: " + getRequestContent(), ex);
    NewRelic.noticeError(ex);

    return new ApiError().setHttpStatus(HttpStatus.BAD_REQUEST)
        .setReason(CollectionUtils.isNotEmpty(ex.getConstraintViolations())
            ? buildValidationErrorMessage(ex.getConstraintViolations())
            : ex.getMessage())
        .asResponseEntity();
  }

  @Override
  protected ResponseEntity<Object> handleMethodArgumentNotValid(MethodArgumentNotValidException ex,
                                                                HttpHeaders headers,
                                                                HttpStatus status,
                                                                WebRequest request) {
    log.warn("Validation of argument is failed. Request content: " + getRequestContent(), ex);
    NewRelic.noticeError(ex);

    BindingResult bindingResult = ex.getBindingResult();
    Stream<String> fieldErrors = bindingResult.getFieldErrors()
        .stream()
        .map(error -> error.getField() + ": " + error.getDefaultMessage());
    Stream<String> objectErrors = bindingResult.getGlobalErrors()
        .stream()
        .map(error -> error.getObjectName() + ": " + error.getDefaultMessage());

    String reason = Stream.of(fieldErrors, objectErrors)
        .flatMap(Function.identity())
        .reduce((prev, next) -> prev + ERROR_DELIMITER + next)
        .orElse("Reason unknown");

    return new ResponseEntity<>(
        new ApiError()
            .setHttpStatus(HttpStatus.BAD_REQUEST)
            .setReason(reason),
        HttpStatus.BAD_REQUEST
    );
  }

  @ExceptionHandler(QuizSubmissionException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  public ResponseEntity<ApiError> handleQuizSubmissionError(QuizSubmissionException ex) {
    log.warn("User failed to submit quiz answers. Reason:  {}. Request content: {}", ex.getMessage(), getRequestContent());
    NewRelic.noticeError(ex);

    ApiError apiError = new ApiError()
        .setHttpStatus(HttpStatus.BAD_REQUEST)
        .setReason(ex.getMessage());
    if (ArrayUtils.isNotEmpty(ex.getErrorBody())) {
      apiError.setContext(ex.getErrorBody());
    }
    return apiError.asResponseEntity();
  }
  

  @ExceptionHandler(QuizRewardNotAssignedException.class)
  @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
  public ResponseEntity<ApiError> handleQuizRewardNotAssignedException(QuizRewardNotAssignedException ex) {
    log.error("Quiz reward wasn't assigned. Reason:  {}. Request content: {}", ex.getMessage(), getRequestContent());
    NewRelic.noticeError(ex);

    return new ApiError()
        .setHttpStatus(HttpStatus.INTERNAL_SERVER_ERROR)
        .setReason(ex.getMessage())
        .setErrorCode("REWARD_NOT_ASSIGNED_ERROR")
        .asResponseEntity();
  }
  
  @Override
  protected ResponseEntity<Object> handleExceptionInternal(Exception ex,
                                                           Object body,
                                                           HttpHeaders headers,
                                                           HttpStatus status,
                                                           WebRequest request) {
    log.warn("Unexpected error occurred. Request content: " + getRequestContent(), ex);
    NewRelic.noticeError(ex);
    return new ApiError()
        .setHttpStatus(status)
        .setReason("Reason unavailable. See Status Code or contact our support team for more details")
        .asRawResponseEntity();
  }

  @Override
  protected ResponseEntity<Object> handleMissingServletRequestParameter(MissingServletRequestParameterException ex,
                                                                        HttpHeaders headers,
                                                                        HttpStatus status,
                                                                        WebRequest request) {
    log.warn("Missing request parameter. Request content: " + getRequestContent(), ex);
    NewRelic.noticeError(ex);
    return new ApiError()
        .setHttpStatus(HttpStatus.BAD_REQUEST)
        .setReason(ex.getMessage())
        .asRawResponseEntity();
  }

  private String buildValidationErrorMessage(Set<ConstraintViolation<?>> constraintViolations) {
    return constraintViolations.stream().map(ConstraintViolation::getMessage).collect(Collectors.joining("; "));
  }

  private String getRequestContent() {
    ContentCachingRequestWrapper request = requestProvider.get();
    String body = new String(request.getContentAsByteArray()).replaceAll("[\r\n]+", " ");

    return String.format("%s %s%s %s",
        request.getMethod(),
        request.getRequestURI(),
        StringUtils.isNotEmpty(request.getQueryString()) ? "?=" + request.getQueryString() : "",
        body
    );
  }
}
