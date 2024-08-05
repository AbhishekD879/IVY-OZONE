package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.StatisticValueRangeResponse;
import java.util.HashMap;
import java.util.Map;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("statistic-value-range")
public class StatisticValueRangeHandler extends BanachApiProxyHandler<StatisticValueRangeResponse> {
  public StatisticValueRangeHandler(BanachClient<Mono<StatisticValueRangeResponse>> banachClient) {
    super(banachClient);
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    Long obEventId = request.queryParam("obEventId").map(Long::parseLong).orElse(0L);
    Long playerId = request.queryParam("playerId").map(Long::parseLong).orElse(0L);
    Long statId = request.queryParam("statId").map(Long::parseLong).orElse(0L);
    return getClient()
        .execute(getCorrelationId(request), toStatValueRangeQueryMap(obEventId, playerId, statId))
        .onErrorReturn(WebClientResponseException.class, new StatisticValueRangeResponse(null))
        .map(BodyInserters::fromValue)
        .flatMap(ServerResponse.ok()::body);
  }

  private static Map<String, String> toStatValueRangeQueryMap(
      Long obEventId, Long playerId, Long statId) {
    Map<String, String> statValueRangeQueryMap = new HashMap<>();
    statValueRangeQueryMap.put("obEventId", obEventId.toString());
    statValueRangeQueryMap.put("playerId", playerId.toString());
    statValueRangeQueryMap.put("statId", statId.toString());
    return statValueRangeQueryMap;
  }
}
