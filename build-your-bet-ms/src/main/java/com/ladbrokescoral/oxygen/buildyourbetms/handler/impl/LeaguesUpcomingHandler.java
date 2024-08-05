package com.ladbrokescoral.oxygen.buildyourbetms.handler.impl;

import com.ladbrokescoral.oxygen.buildyourbetms.dto.DataResponseWrapper;
import com.ladbrokescoral.oxygen.buildyourbetms.dto.LeaguesUpcomingDto;
import com.ladbrokescoral.oxygen.buildyourbetms.dto.TimeZone;
import com.ladbrokescoral.oxygen.buildyourbetms.handler.BanachApiProxyHandler;
import com.ladbrokescoral.oxygen.buildyourbetms.util.LogExecutionTime;
import com.ladbrokescoral.oxygen.buildyourbetms.util.Util;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetLeaguesResponseDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.LeaguesResponse;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.logging.Level;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.publisher.SignalType;

@Component
@Qualifier("leagues-upcoming")
public class LeaguesUpcomingHandler extends BanachApiProxyHandler<LeaguesResponse> {
  private final Clock clock;

  public LeaguesUpcomingHandler(BanachClient<Mono<LeaguesResponse>> banachClient, Clock clock) {
    super(banachClient);
    this.clock = clock;
  }

  @Override
  @LogExecutionTime
  public Mono<ServerResponse> handle(ServerRequest request) {
    long days =
        request
            .queryParam("days")
            .map(Long::parseLong)
            .filter(d -> d >= 1L)
            .orElseThrow(IllegalArgumentException::new);
    TimeZone zone =
        request.queryParam("tz").map(TimeZone::from).orElseThrow(IllegalArgumentException::new);

    Instant nowInstant = getNow();
    long now = nowInstant.toEpochMilli();

    LocalDateTime clientNextMignight = clientNextMidnightConvertedToUTC(nowInstant, zone);
    LocalDateTime upcomingLimit = clientNextMignight.plusDays(days - 1);

    long upcomingLimitTimeStamp =
        upcomingLimit.minusSeconds(1).toInstant(ZoneOffset.UTC).toEpochMilli();
    long nextMidnightTimeStamp = clientNextMignight.toInstant(ZoneOffset.UTC).toEpochMilli();
    long secondBeforeNextMidnight =
        clientNextMignight.minusSeconds(1).toInstant(ZoneOffset.UTC).toEpochMilli();
    Mono<List<GetLeaguesResponseDto>> todayLeagues =
        getClient()
            .execute(
                getCorrelationId(request),
                Util.toAndFromEpochMillisMap(now, secondBeforeNextMidnight))
            .map(LeaguesResponse::getData);

    Mono<List<GetLeaguesResponseDto>> upcomingLeagues =
        days > 1
            ? getClient()
                .execute(
                    getCorrelationId(request),
                    Util.toAndFromEpochMillisMap(nextMidnightTimeStamp, upcomingLimitTimeStamp))
                .map(LeaguesResponse::getData)
            : Mono.empty();

    return combineTodayAndUpcoming(todayLeagues, upcomingLeagues)
        .map(DataResponseWrapper::new)
        .log(getCorrelationId(request), Level.INFO, SignalType.ON_ERROR, SignalType.ON_NEXT)
        .map(BodyInserters::fromValue)
        .flatMap(ServerResponse.ok()::body);
  }

  private Instant getNow() {
    return Instant.now(clock);
  }

  private static LocalDateTime clientNextMidnightConvertedToUTC(Instant now, TimeZone zone) {
    ZoneId zoneId = ZoneId.ofOffset("UTC", ZoneOffset.ofTotalSeconds(zone.toSeconds()));
    Instant instant =
        ZonedDateTime.of(now.atZone(zoneId).toLocalDate(), LocalTime.MIDNIGHT, zoneId)
            .plusDays(1)
            .toInstant();

    return LocalDateTime.ofInstant(instant, ZoneId.of("UTC"));
  }

  public static Mono<LeaguesUpcomingDto> combineTodayAndUpcoming(
      Mono<List<GetLeaguesResponseDto>> todayLeagues,
      Mono<List<GetLeaguesResponseDto>> upcomingLeagues) {
    Mono<LeaguesUpcomingDto> empty = Mono.just(LeaguesUpcomingDto.builder().build());

    Mono<LeaguesUpcomingDto> todayMono =
        todayLeagues
            .map(leagues -> LeaguesUpcomingDto.builder().today(leagues).build())
            .switchIfEmpty(empty);

    Mono<LeaguesUpcomingDto> upcomingMono =
        upcomingLeagues
            .map(leagues -> LeaguesUpcomingDto.builder().upcoming(leagues).build())
            .switchIfEmpty(empty);

    Flux<LeaguesUpcomingDto> leaguesUpcomingDtoFlux = todayMono.mergeWith(upcomingMono);

    return leaguesUpcomingDtoFlux.reduce(Util::aggregate);
  }
}
