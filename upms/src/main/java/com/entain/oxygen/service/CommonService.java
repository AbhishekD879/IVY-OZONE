package com.entain.oxygen.service;

import com.entain.oxygen.dto.ErrorDto;
import com.entain.oxygen.entity.projection.view.Views;
import com.entain.oxygen.exceptions.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.codec.json.Jackson2CodecSupport;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Slf4j
public class CommonService {

  private static final String ERROR_LOG = "error response :: {}";
  private static final String COMMON_ERROR_LOG = "error response :: {}";

  protected Mono<ServerResponse> success(
      final Object responseEntity, boolean viewEnabled, HttpStatus status) {
    final ServerResponse.BodyBuilder responseBuilder = ServerResponse.status(status);

    addXSSHeaders(responseBuilder);
    if (viewEnabled) {
      responseBuilder.hint(Jackson2CodecSupport.JSON_VIEW_HINT, Views.Public.class);
    }

    return responseBuilder.bodyValue(responseEntity);
  }

  protected static ServerResponse.BodyBuilder addXSSHeaders(
      ServerResponse.BodyBuilder responseBuilder) {

    responseBuilder.header("Strict-Transport-Security", "max-age=63072000; includeSubDomains");
    responseBuilder.header("X-XSS-Protection", "1; mode=block");
    responseBuilder.header("X-Frame-Options", "SAMEORIGIN");
    responseBuilder.header("X-Content-Type-Options", "nosniff");
    return responseBuilder;
  }

  protected Mono<ServerResponse> error(final Throwable exception) {
    final ServerResponse.BodyBuilder responseBuilder;

    if (exception instanceof PreferenceDtoException) {
      log.error("preference error:: {}", exception.getMessage());
      responseBuilder = ServerResponse.status(HttpStatus.BAD_REQUEST);
    } else if (exception instanceof EntityNotFoundException
        || exception instanceof OddPreferenceDuplicateException) {
      log.error(ERROR_LOG, exception.getMessage());
      responseBuilder = ServerResponse.status(HttpStatus.OK);

    } else {
      log.error(COMMON_ERROR_LOG, exception.getMessage());
      responseBuilder = ServerResponse.status(HttpStatus.INTERNAL_SERVER_ERROR);
    }
    addXSSHeaders(responseBuilder);

    return responseBuilder.bodyValue(exception.getMessage());
  }

  protected Mono<ServerResponse> errorWithSpecificHttpStatus(final Throwable exception) {
    final ServerResponse.BodyBuilder responseBuilder;
    HttpStatus httpStatus = HttpStatus.INTERNAL_SERVER_ERROR;
    int errorCode = HttpStatus.INTERNAL_SERVER_ERROR.value();

    if (exception instanceof EntityNotFoundException) {
      log.error(ERROR_LOG, exception.getMessage());
      errorCode = HttpStatus.NOT_FOUND.value();
      httpStatus = HttpStatus.NOT_FOUND;

    } else if (exception instanceof ValidationsException vx) {
      log.error(ERROR_LOG, exception.getMessage());
      errorCode = vx.getErrorCode();
      httpStatus = HttpStatus.valueOf(errorCode);
    } else if (exception instanceof UserStableException userStableException) {
      log.error(ERROR_LOG, exception.getMessage());
      errorCode = userStableException.getErrorCode();
      httpStatus = HttpStatus.valueOf(errorCode);
    } else {
      log.error(COMMON_ERROR_LOG, exception.getMessage());
    }
    responseBuilder = ServerResponse.status(httpStatus);

    ErrorDto errorResponse = new ErrorDto(exception.getMessage(), errorCode);
    addXSSHeaders(responseBuilder);
    responseBuilder.contentType(MediaType.APPLICATION_JSON);

    return responseBuilder.bodyValue(errorResponse);
  }
  /** This is a fallback overloaded method for backward compatibility. */
  protected Mono<ServerResponse> success(final Object responseEntity, boolean viewEnabled) {
    return success(responseEntity, viewEnabled, HttpStatus.OK);
  }
}
