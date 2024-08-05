package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.buildyourbetms.util.Util;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.LeaguesResponse;
import java.util.Map;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("leagues")
public class LeaguesHandler extends BanachApiProxyHandler<LeaguesResponse> {
  private static final ParameterizedTypeReference<LeaguesResponse> TYPE_REFERENCE =
      new ParameterizedTypeReference<LeaguesResponse>() {};

  public LeaguesHandler(BanachClient<Mono<LeaguesResponse>> banachClients) {
    super(banachClients);
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    Map<String, String> leaguesQueryParam = Util.extractEpochMillisRangeFromRequest(request);
    return ServerResponse.ok()
        .body(getClient().execute(getCorrelationId(request), leaguesQueryParam), TYPE_REFERENCE);
  }
}
