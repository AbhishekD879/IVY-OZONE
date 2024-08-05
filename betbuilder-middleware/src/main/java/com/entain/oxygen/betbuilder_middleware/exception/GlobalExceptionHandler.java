package com.entain.oxygen.betbuilder_middleware.exception;

import java.util.Map;
import org.redisson.client.RedisException;
import org.springframework.boot.autoconfigure.web.WebProperties;
import org.springframework.boot.autoconfigure.web.reactive.error.AbstractErrorWebExceptionHandler;
import org.springframework.boot.web.error.ErrorAttributeOptions;
import org.springframework.boot.web.reactive.error.ErrorAttributes;
import org.springframework.context.ApplicationContext;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerCodecConfigurer;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.server.RequestPredicates;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.RouterFunctions;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
public class GlobalExceptionHandler extends AbstractErrorWebExceptionHandler {

  public GlobalExceptionHandler(
      GlobalErrorAttributes errorAttributes,
      ApplicationContext applicationContext,
      ServerCodecConfigurer serverCodecConfigurer) {
    super(errorAttributes, new WebProperties.Resources(), applicationContext);
    super.setMessageWriters(serverCodecConfigurer.getWriters());
    super.setMessageReaders(serverCodecConfigurer.getReaders());
  }

  @Override
  protected RouterFunction<ServerResponse> getRoutingFunction(ErrorAttributes errorAttributes) {
    return RouterFunctions.route(RequestPredicates.all(), this::renderError);
  }

  private Mono<ServerResponse> renderError(final ServerRequest request) {

    final Map<String, Object> errorPropertiesMap =
        getErrorAttributes(request, ErrorAttributeOptions.defaults());

    return ServerResponse.status(getStatus(request))
        .contentType(MediaType.APPLICATION_JSON)
        .body(BodyInserters.fromValue(errorPropertiesMap));
  }

  private HttpStatus getStatus(ServerRequest request) {

    if (getError(request) instanceof PricingGatewayException) {
      return HttpStatus.INTERNAL_SERVER_ERROR;
    } else if (getError(request) instanceof PGConnectivityException) {
      return HttpStatus.SERVICE_UNAVAILABLE;
    } else if (getError(request) instanceof IllegalArgumentException) {
      return HttpStatus.BAD_REQUEST;
    } else if (getError(request) instanceof RedisException) {
      return HttpStatus.INTERNAL_SERVER_ERROR;
    } else {
      return HttpStatus.BAD_GATEWAY;
    }
  }
}
