package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.dto.PriceRequestDto;
import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceRequestDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PriceResponse;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("price")
public class PriceHandler extends BanachApiProxyHandler<PriceResponse> {
  private static final ParameterizedTypeReference<PriceResponse> TYPE_REFERENCE =
      new ParameterizedTypeReference<PriceResponse>() {};

  public PriceHandler(BanachClient<Mono<PriceResponse>> banachClient) {
    super(banachClient);
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    return request
        .bodyToMono(PriceRequestDto.class)
        .map(requestDto -> toBanachModel(requestDto, getCorrelationId(request)))
        .map(BodyInserters::fromValue)
        .map(bodyInserter -> getClient().execute(getCorrelationId(request), bodyInserter))
        .flatMap(resp -> ServerResponse.ok().body(resp, TYPE_REFERENCE));
  }

  private static GetPriceRequestDto toBanachModel(
      PriceRequestDto requestDto, String correlationId) {
    GetPriceRequestDto.GetPriceRequestDtoBuilder builder = GetPriceRequestDto.builder();
    builder.obEventId(requestDto.getObEventId());
    requestDto.getSelectionIds().forEach(builder::selectionId);
    requestDto.getPlayerSelections().forEach(builder::virtualSelectionDetail);
    builder.correlationId(correlationId);
    return builder.build();
  }
}
