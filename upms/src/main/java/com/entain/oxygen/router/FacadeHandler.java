package com.entain.oxygen.router;

import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

public interface FacadeHandler {
  Mono<ServerResponse> saveOperation(ServerRequest request);

  Mono<ServerResponse> getOperation(ServerRequest request);

  Mono<ServerResponse> updateOperation(ServerRequest request);

  Mono<ServerResponse> deleteOperation(ServerRequest request);
}
