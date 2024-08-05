package com.entain.oxygen.router;

import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

public interface StableFacadeHandler extends FacadeHandler {

  Mono<ServerResponse> getHorseNotesById(ServerRequest request);

  Mono<ServerResponse> getCachedHorseInfo(ServerRequest request);
}
