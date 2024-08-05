package com.entain.oxygen.router;

import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

public interface PreferenceFacadeHandler extends FacadeHandler {

  Mono<ServerResponse> getAllOddsPreferencesByBrand(ServerRequest request);

  Mono<ServerResponse> getAllOddsPreference(ServerRequest request);
}
