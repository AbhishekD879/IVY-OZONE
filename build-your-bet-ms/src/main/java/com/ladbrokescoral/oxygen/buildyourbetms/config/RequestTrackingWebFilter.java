package com.ladbrokescoral.oxygen.buildyourbetms.config;

import com.newrelic.api.agent.NewRelic;
import java.net.URI;
import java.util.Optional;
import java.util.UUID;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Mono;

@Component
// @Slf4j
public class RequestTrackingWebFilter implements WebFilter {
  public static final String CORRELATION_ID_HEADER_KEY = "X-Correlation-Id";
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Override
  public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
    String path = exchange.getRequest().getPath().pathWithinApplication().value();
    if (path.contains("api")) {
      long start = System.currentTimeMillis();
      exchange = maybeMutateExchange(exchange);
      String correlationId = getCorrelationId(exchange).orElse("unknown");

      String metric = "Custom/" + path;
      URI uri = exchange.getRequest().getURI();
      String logPrefix = exchange.getLogPrefix();
      ASYNC_LOGGER.info("[{}] {} Incoming {}", correlationId, logPrefix, uri);
      exchange
          .getResponse()
          .beforeCommit(
              () -> {
                Runnable runnable =
                    () -> {
                      long timeSpent = System.currentTimeMillis() - start;
                      ASYNC_LOGGER.info(
                          "[{}] {} Handled {} in {} ms", correlationId, logPrefix, uri, timeSpent);
                      NewRelic.recordResponseTimeMetric(metric, timeSpent);
                    };

                return Mono.fromRunnable(runnable);
              });
      NewRelic.incrementCounter(metric);
    }
    return chain.filter(exchange);
  }

  // if "X-Correlation-Id" is present in request, it simply returns unchanged exchange.
  // if it's not present, correlationId is generate with "ms-" prefix and mutate exchange is
  // returned with header set.
  private ServerWebExchange maybeMutateExchange(ServerWebExchange exchange) {
    if (!getCorrelationId(exchange).isPresent()) {
      String generatedCorrelationId = UUID.randomUUID().toString();
      return exchange
          .mutate()
          .request(builder -> builder.header(CORRELATION_ID_HEADER_KEY, generatedCorrelationId))
          .build();
    }

    return exchange;
  }

  private Optional<String> getCorrelationId(ServerWebExchange exchange) {
    return extractCorrelationIdFromRequest(exchange);
  }

  public static Optional<String> extractCorrelationIdFromRequest(ServerWebExchange exchange) {
    Optional<String> correlationId =
        Optional.ofNullable(exchange.getRequest().getHeaders().get(CORRELATION_ID_HEADER_KEY))
            .map(l -> l.get(l.size() - 1))
            .filter(RequestTrackingWebFilter::isValidUuid);
    return correlationId;
  }

  private static boolean isValidUuid(String uuidString) {
    try {
      UUID.fromString(uuidString);
      return true;
    } catch (IllegalArgumentException e) {
      return false;
    }
  }
}
