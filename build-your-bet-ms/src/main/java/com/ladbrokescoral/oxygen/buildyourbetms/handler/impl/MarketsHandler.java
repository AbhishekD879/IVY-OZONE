package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.buildyourbetms.util.Util;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.MarketsResponse;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("markets")
public class MarketsHandler extends BanachApiProxyHandler<MarketsResponse> {
  private static final ParameterizedTypeReference<MarketsResponse> TYPE_REFERENCE =
      new ParameterizedTypeReference<MarketsResponse>() {};

  public MarketsHandler(BanachClient<Mono<MarketsResponse>> banachClient) {
    super(banachClient);
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    return Mono.justOrEmpty(request.queryParam("obEventId"))
        .map(Long::valueOf)
        .map(Util::eventIdToQueryMap)
        .map(queryMap -> getClient().execute(getCorrelationId(request), queryMap))
        .flatMap(resp -> ServerResponse.ok().body(resp, TYPE_REFERENCE))
        .switchIfEmpty(ServerResponse.badRequest().build());
  }
}
