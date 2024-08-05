package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.buildyourbetms.util.Util;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.EventResponse;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClientResponseException.NotFound;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("event")
public class EventHandler extends BanachApiProxyHandler<EventResponse> {

  private static final ParameterizedTypeReference<EventResponse> TYPE_REFERENCE =
      new ParameterizedTypeReference<EventResponse>() {};
  private static final EventResponse EMPTY_EVENT = new EventResponse(null);

  public EventHandler(BanachClient<Mono<EventResponse>> banachClient) {
    super(banachClient);
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    return Mono.just(request.pathVariable("id"))
        .map(Long::valueOf)
        .map(Util::eventIdToQueryMap)
        .map(
            queryMap ->
                getClient()
                    .execute(getCorrelationId(request), queryMap)
                    .onErrorReturn(NotFound.class, EMPTY_EVENT))
        .flatMap(resp -> ServerResponse.ok().body(resp, TYPE_REFERENCE))
        .switchIfEmpty(ServerResponse.badRequest().build());
  }
}
