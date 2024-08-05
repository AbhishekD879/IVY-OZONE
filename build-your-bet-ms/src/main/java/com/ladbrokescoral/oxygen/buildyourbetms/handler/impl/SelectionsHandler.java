package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetSelectionRequestDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.SelectionsResponse;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.MediaType;
import org.springframework.http.ReactiveHttpOutputMessage;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.BodyInserter;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

@Component
@Qualifier("selections")
public class SelectionsHandler extends BanachApiProxyHandler<SelectionsResponse> {
  private static final ParameterizedTypeReference<SelectionsResponse> TYPE_REFERENCE =
      new ParameterizedTypeReference<SelectionsResponse>() {};
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public SelectionsHandler(BanachClient<Mono<SelectionsResponse>> banachClient) {
    super(banachClient);
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    GetSelectionRequestDto requestBody = toBanachModel(request, getCorrelationId(request));
    ASYNC_LOGGER.error("/selections body: {}", requestBody);
    BodyInserter<GetSelectionRequestDto, ReactiveHttpOutputMessage> bodyInserter =
        BodyInserters.fromValue(requestBody);
    return ServerResponse.ok()
        .contentType(MediaType.APPLICATION_JSON)
        .body(getClient().execute(getCorrelationId(request), bodyInserter), TYPE_REFERENCE);
  }

  private static GetSelectionRequestDto toBanachModel(ServerRequest request, String correlationId) {
    Long obEventId =
        request
            .queryParam("obEventId")
            .map(Long::parseLong)
            .orElseThrow(IllegalStateException::new);

    List<Long> marketIds =
        request
            .queryParam("marketIds")
            .map(input -> input.replace(" ", "").split(","))
            .map(Arrays::asList)
            .map(list -> list.stream().map(Long::parseLong).collect(Collectors.toList()))
            .orElseThrow(IllegalStateException::new);

    return GetSelectionRequestDto.builder()
        .obEventId(obEventId)
        .marketIds(marketIds)
        .correlationId(correlationId)
        .build();
  }
}
