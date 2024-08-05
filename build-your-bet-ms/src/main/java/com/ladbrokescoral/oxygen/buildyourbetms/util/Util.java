package com.ladbrokescoral.oxygen.buildyourbetms.util;

import com.ladbrokescoral.oxygen.buildyourbetms.dto.LeaguesUpcomingDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetLeaguesResponseDto;
import com.newrelic.api.agent.HttpParameters;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Segment;
import java.net.URI;
import java.util.*;
import org.springframework.web.reactive.function.server.ServerRequest;

public class Util {
  private Util() {}

  public static Map<String, String> eventIdToQueryMap(Long eventId) {
    Map<String, String> eventIdToQueryMap = new HashMap<>();
    eventIdToQueryMap.put("obEventId", String.valueOf(eventId));
    return eventIdToQueryMap;
  }

  public static Map<String, String> toAndFromEpochMillisMap(Long fromMillis, Long toMillis) {
    Map<String, String> toAndFromEpochMillisMap = new HashMap<>();
    if (fromMillis != null) {
      toAndFromEpochMillisMap.put("fromEpochMillis", String.valueOf(fromMillis));
    }
    if (toMillis != null) {
      toAndFromEpochMillisMap.put("toEpochMillis", String.valueOf(toMillis));
    }
    return toAndFromEpochMillisMap;
  }

  public static Map<String, String> extractEpochMillisRangeFromRequest(ServerRequest request) {
    Optional<Long> fromEpochMillis = request.queryParam("fromEpochMillis").map(Long::parseLong);
    Optional<Long> toEpochMillis = request.queryParam("toEpochMillis").map(Long::parseLong);
    return toAndFromEpochMillisMap(fromEpochMillis.orElse(null), toEpochMillis.orElse(null));
  }

  public static Segment initTrackingSegment(String segmentName, URI uri) {
    Segment segment = NewRelic.getAgent().getTransaction().startSegment(segmentName);
    segment.reportAsExternal(
        HttpParameters.library("spring-webClient")
            .uri(uri)
            .procedure(segmentName)
            .noInboundHeaders()
            .build());
    return segment;
  }

  public static LeaguesUpcomingDto aggregate(LeaguesUpcomingDto l1, LeaguesUpcomingDto l2) {

    Optional<LeaguesUpcomingDto> optL2 = Optional.ofNullable(l2);

    Set<GetLeaguesResponseDto> upcoming =
        new HashSet<>(
            Optional.ofNullable(l1).map(LeaguesUpcomingDto::getUpcoming).orElseGet(ArrayList::new));
    upcoming.addAll(optL2.map(LeaguesUpcomingDto::getUpcoming).orElseGet(ArrayList::new));

    Set<GetLeaguesResponseDto> today =
        new HashSet<>(
            Optional.ofNullable(l1).map(LeaguesUpcomingDto::getToday).orElseGet(ArrayList::new));
    today.addAll(optL2.map(LeaguesUpcomingDto::getToday).orElseGet(ArrayList::new));

    return LeaguesUpcomingDto.builder()
        .today(new ArrayList<>(today))
        .upcoming(new ArrayList<>(upcoming))
        .build();
  }
}
