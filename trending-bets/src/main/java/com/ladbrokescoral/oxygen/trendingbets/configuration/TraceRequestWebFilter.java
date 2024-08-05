package com.ladbrokescoral.oxygen.trendingbets.configuration;

import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Mono;

@Configuration
public class TraceRequestWebFilter implements WebFilter {

  @Override
  public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
    return checkTrace(exchange.getRequest()) ? handleTrace(exchange) : chain.filter(exchange);
  }

  private Mono<Void> handleTrace(ServerWebExchange exchange) {
    return Mono.fromRunnable(
            () -> exchange.getResponse().setStatusCode(HttpStatus.METHOD_NOT_ALLOWED))
        .then();
  }

  private boolean checkTrace(ServerHttpRequest request) {
    return request.getMethod() == HttpMethod.TRACE;
  }
}
