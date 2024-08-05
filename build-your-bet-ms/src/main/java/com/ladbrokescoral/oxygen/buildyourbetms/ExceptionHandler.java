package com.ladbrokescoral.oxygen.buildyourbetms;

import com.newrelic.api.agent.NewRelic;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpStatus;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebExceptionHandler;
import reactor.core.publisher.Mono;

@Component
@Order(-2) // to get called before default handlers (which have -1 and 0 order assigned)
// @Slf4j
public class ExceptionHandler implements WebExceptionHandler {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Override
  public Mono<Void> handle(ServerWebExchange exchange, Throwable ex) {
    ASYNC_LOGGER.error("Error occured", ex);
    NewRelic.noticeError(ex);
    if (ex instanceof NumberFormatException || ex instanceof IllegalStateException) {
      ServerHttpResponse response = exchange.getResponse();
      response.setStatusCode(HttpStatus.BAD_REQUEST);
      return response.setComplete();
    }
    return Mono.error(ex);
  }
}
