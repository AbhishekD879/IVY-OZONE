package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlayerBanachStatsDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PlayerBanachStatsResponse;
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
@Qualifier("player-stats-by-opta-id")
public class PlayerStatsByOptaIdHandler extends BanachApiProxyHandler<PlayerBanachStatsResponse> {

  public PlayerStatsByOptaIdHandler(BanachClient<Mono<PlayerBanachStatsResponse>> banachClient) {
    super(banachClient);
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    Optional<Long> obEventId = request.queryParam("obEventId").map(Long::parseLong);
    Optional<String> optaPlayerId = request.queryParam("optaPlayerId");
    return getClient()
        .execute(
            getCorrelationId(request),
            priceStatsQueryMap(obEventId.orElse(0L), optaPlayerId.orElse(null)))
        .onErrorReturn(
            WebClientResponseException.class,
            new PlayerBanachStatsResponse(new PlayerBanachStatsDto()))
        .map(BodyInserters::fromValue)
        .flatMap(ServerResponse.ok()::body);
  }

  private static Map<String, String> priceStatsQueryMap(Long obEventId, String playerId) {
    Map<String, String> source = new HashMap<>();
    source.put("obEventId", obEventId.toString());
    source.put("optaPlayerId", playerId);
    return source;
  }
}
