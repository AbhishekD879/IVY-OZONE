package com.ladbrokescoral.oxygen.buildyourbetms.handler;

import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

public interface FacadeHandler {
  Mono<ServerResponse> handle(ServerRequest request);
}
