package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PlayerStatisticsResponse;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("player-statistics")
public class PlayerStatisticsHandler extends BanachApiProxyHandler<PlayerStatisticsResponse> {

  public PlayerStatisticsHandler(BanachClient<Mono<PlayerStatisticsResponse>> banachClient) {
    super(banachClient);
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    Optional<Long> obEventId = request.queryParam("obEventId").map(Long::parseLong);
    Optional<Long> playerId = request.queryParam("playerId").map(Long::parseLong);
    return getClient()
        .execute(
            getCorrelationId(request),
            priceStatsQueryMap(obEventId.orElse(0L), playerId.orElse(0L)))
        .onErrorReturn(
            WebClientResponseException.class, new PlayerStatisticsResponse(Collections.emptyList()))
        .map(BodyInserters::fromValue)
        .flatMap(ServerResponse.ok()::body);
  }

  private static Map<String, String> priceStatsQueryMap(Long obEventId, Long playerId) {
    Map<String, String> priceStatsQueryMap = new HashMap<>();
    priceStatsQueryMap.put("obEventId", obEventId.toString());
    priceStatsQueryMap.put("id", playerId.toString());
    return priceStatsQueryMap;
  }
}
