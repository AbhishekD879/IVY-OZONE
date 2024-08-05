package com.ladbrokescoral.oxygen.trendingbets.handler;

import java.util.Optional;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

public interface ApiHandler {

  String TOKEN_HEADER = "token";

  Mono<ServerResponse> handle(ServerRequest request);

  default Optional<String> getToken(ServerRequest request) {
    return Optional.ofNullable(request.headers()).map(headers -> headers.firstHeader(TOKEN_HEADER));
  }
}
