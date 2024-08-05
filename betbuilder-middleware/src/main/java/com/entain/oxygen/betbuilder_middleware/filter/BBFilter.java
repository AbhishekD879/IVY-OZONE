package com.entain.oxygen.betbuilder_middleware.filter;

import com.entain.oxygen.betbuilder_middleware.service.BBUtil;
import org.jetbrains.annotations.NotNull;
import org.slf4j.MDC;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.ServerWebExchangeDecorator;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Mono;
import reactor.util.context.Context;

@Component
public class BBFilter implements WebFilter {

  @NotNull
  @Override
  public Mono<Void> filter(ServerWebExchange exchange, @NotNull WebFilterChain webFilterChain) {
    final long startTime = System.currentTimeMillis();
    String transactionPath = exchange.getRequest().getPath().value();
    String correlationId = BBUtil.X_CORRELATION_ID;
    if (exchange.getRequest().getHeaders().toSingleValueMap().get(BBUtil.X_CORRELATION_ID)
        != null) {
      correlationId =
          exchange.getRequest().getHeaders().toSingleValueMap().get(BBUtil.X_CORRELATION_ID);
      exchange.getResponse().getHeaders().set(BBUtil.X_CORRELATION_ID, correlationId);
    }
    String finalCorrelationId = correlationId;
    ServerWebExchangeDecorator decorator =
        new ServerWebExchangeDecorator(exchange) {
          @NotNull
          @Override
          public ServerHttpResponse getResponse() {
            return new ResponseLoggingInterceptor(
                super.getResponse(), startTime, transactionPath, finalCorrelationId);
          }
        };

    return webFilterChain
        .filter(decorator)
        .contextWrite(
            Context.of(
                BBUtil.CORRELATION_ID, correlationId,
                BBUtil.TRANSACTION_PATH, transactionPath))
        .doFinally(signal -> MDC.clear());
  }
}
