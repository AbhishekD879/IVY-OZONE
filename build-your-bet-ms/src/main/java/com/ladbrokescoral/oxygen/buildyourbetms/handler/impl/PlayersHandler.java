package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.buildyourbetms.util.Util;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PlayersResponse;
import java.util.Collections;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("players")
public class PlayersHandler extends BanachApiProxyHandler<PlayersResponse> {
  private static final ParameterizedTypeReference<PlayersResponse> TYPE_REFERENCE =
      new ParameterizedTypeReference<PlayersResponse>() {};

  public PlayersHandler(BanachClient<Mono<PlayersResponse>> banachClient) {
    super(banachClient);
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    return Mono.justOrEmpty(request.queryParam("obEventId"))
        .map(Long::valueOf)
        .map(Util::eventIdToQueryMap)
        .map(
            queryMap ->
                getClient()
                    .execute(getCorrelationId(request), queryMap)
                    .onErrorReturn(
                        WebClientResponseException.class,
                        new PlayersResponse(Collections.emptyList())))
        .flatMap(resp -> ServerResponse.ok().body(resp, TYPE_REFERENCE))
        .switchIfEmpty(ServerResponse.badRequest().build());
  }
}
