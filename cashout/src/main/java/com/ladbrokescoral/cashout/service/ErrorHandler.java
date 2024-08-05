package com.ladbrokescoral.cashout.service;

import com.ladbrokescoral.cashout.model.SSEType;
import com.ladbrokescoral.cashout.model.response.BetResponse;
import org.springframework.http.codec.ServerSentEvent;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface ErrorHandler {
  Mono<ServerSentEvent<BetResponse>> handleMono(Throwable throwable, SSEType sseType);

  Flux<ServerSentEvent<BetResponse>> handleFlux(Throwable throwable, SSEType sseType);
}
