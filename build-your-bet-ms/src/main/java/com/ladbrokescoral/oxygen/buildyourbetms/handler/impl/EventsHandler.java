package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.buildyourbetms.util.Message;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetEventsRequestDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.EventsResponse;
import java.time.Instant;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
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
@Qualifier("events")
// @Slf4j
public class EventsHandler extends BanachApiProxyHandler<EventsResponse> {

  public static final ParameterizedTypeReference<EventsResponse> TYPE_REFERENCE =
      new ParameterizedTypeReference<EventsResponse>() {};
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private Message message;

  public EventsHandler(BanachClient<Mono<EventsResponse>> banachClient) {
    super(banachClient);
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    Optional<Long> fromEpochMillis =
        request.queryParam("dateFrom").map(EventsHandler::fromIsoDateToTimeStamp);
    Optional<Long> toEpochMillis =
        request.queryParam("dateTo").map(EventsHandler::fromIsoDateToTimeStamp);

    Optional<List<Long>> leagueIds =
        request
            .queryParam("leagueIds")
            .map(
                p ->
                    Arrays.stream(p.split("[\\s,]+"))
                        .map(Long::parseLong)
                        .collect(Collectors.toList()));
    GetEventsRequestDto body =
        GetEventsRequestDto.builder()
            .obTypeIds(leagueIds.orElseGet(Collections::emptyList))
            .fromEpochMillis(fromEpochMillis.orElse(null))
            .toEpochMillis(toEpochMillis.orElse(null))
            .correlationId(getCorrelationId(request))
            .build();
    String correlationID = getCorrelationId(request);
    message = new Message();
    message.setMessage(correlationID.toString());
    ASYNC_LOGGER.info("/events body [{}]: {}", message, body);
    BodyInserter<Mono<GetEventsRequestDto>, ReactiveHttpOutputMessage> bodyInserter =
        BodyInserters.fromPublisher(Mono.just(body), GetEventsRequestDto.class);
    return ServerResponse.ok()
        .contentType(MediaType.APPLICATION_JSON)
        .body(getClient().execute(getCorrelationId(request), bodyInserter), TYPE_REFERENCE);
  }

  public static long fromIsoDateToTimeStamp(String iso8601DateInUtc) {
    return Instant.from(DateTimeFormatter.ISO_DATE_TIME.parse(iso8601DateInUtc)).toEpochMilli();
  }
}
