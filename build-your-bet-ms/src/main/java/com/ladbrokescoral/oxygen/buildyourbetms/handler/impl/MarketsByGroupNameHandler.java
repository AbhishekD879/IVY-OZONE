package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.dto.MarketGroup;
import com.ladbrokescoral.oxygen.buildyourbetms.dto.MarketsGroupedDto;
import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.buildyourbetms.util.Util;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetMarketResponseDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.MarketsResponse;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import org.springframework.util.ObjectUtils;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("markets-by-group-name")
public class MarketsByGroupNameHandler extends BanachApiProxyHandler<MarketsResponse> {
  private static final String NO_GROUP_NAME = "NO_GROUP";

  public MarketsByGroupNameHandler(BanachClient<Mono<MarketsResponse>> banachClient) {
    super(banachClient);
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    return request
        .queryParam("obEventId")
        .map(Long::valueOf)
        .map(Util::eventIdToQueryMap)
        .map(queryMap -> getClient().execute(getCorrelationId(request), queryMap))
        .map(MarketsByGroupNameHandler::processResponse)
        .orElseGet(() -> ServerResponse.badRequest().build());
  }

  private static Mono<ServerResponse> processResponse(Mono<MarketsResponse> marketsResponse) {
    return marketsResponse
        .map(MarketsResponse::getData)
        .map(MarketsByGroupNameHandler::groupByGroupName)
        .map(BodyInserters::fromValue)
        .flatMap(ServerResponse.ok()::body);
  }

  private static MarketsGroupedDto groupByGroupName(List<GetMarketResponseDto> marketsResponse) {
    processUngroupedItem(marketsResponse);

    MarketsGroupedDto.MarketsGroupedDtoBuilder marketsGroupedBuilder = MarketsGroupedDto.builder();

    Map<String, List<GetMarketResponseDto>> groupedByName =
        marketsResponse.stream().collect(Collectors.groupingBy(GetMarketResponseDto::getGroupName));

    groupedByName.entrySet().stream()
        .map(
            entry ->
                MarketGroup.builder()
                    .marketGroupName(entry.getKey())
                    .markets(entry.getValue())
                    .build())
        .forEach(marketsGroupedBuilder::groupedMarket);

    return marketsGroupedBuilder.build();
  }

  private static void processUngroupedItem(List<GetMarketResponseDto> marketsResponse) {
    marketsResponse.forEach(
        market -> {
          if (ObjectUtils.isEmpty(market.getGroupName())) {
            market.setGroupName(NO_GROUP_NAME);
          }
        });
  }
}
