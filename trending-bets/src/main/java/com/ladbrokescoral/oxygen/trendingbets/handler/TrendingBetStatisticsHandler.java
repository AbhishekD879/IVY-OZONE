package com.ladbrokescoral.oxygen.trendingbets.handler;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.impl.LiveServServiceImpl;
import com.ladbrokescoral.oxygen.trendingbets.context.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.trendingbets.context.PopularAccaContext;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingEventMap;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.messaging.Message;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Sinks;

@Component
@Qualifier("trendingStats")
@RequiredArgsConstructor
public class TrendingBetStatisticsHandler implements ApiHandler {

  private final LiveServService liveServService;

  @Override
  public Mono<ServerResponse> handle(ServerRequest request) {
    String stats = request.pathVariables().get("stats");

    if ("popularAccaStats".equals(stats)) {
      return ServerResponse.ok().bodyValue(getPopularStats());
    } else {
      return ServerResponse.ok().bodyValue(getTrendingStats());
    }
  }

  private Map<String, Object> getPopularStats() {

    Map<String, Object> stats = new HashMap<>();
    stats.put("PopularAccaEvents", PopularAccaContext.getEventAccas().keySet());
    stats.put("PopularAccaSelections", PopularAccaContext.getSelectionAccas().keySet());
    stats.put("popularTypesId", getAccaLeague());
    return stats;
  }

  private Map<String, Object> getTrendingStats() {
    AtomicInteger totalSubscriptions = new AtomicInteger();
    Map<String, Integer> subscriptions =
        ChannelHandlersContext.getChannels().entrySet().stream()
            .collect(
                Collectors.toMap(
                    Map.Entry::getKey,
                    (Map.Entry<String, Sinks.Many<Message<String>>> entry) -> {
                      totalSubscriptions.addAndGet(entry.getValue().currentSubscriberCount());
                      return entry.getValue().currentSubscriberCount();
                    }));
    Map<String, Object> stats = new HashMap<>();
    stats.put("TotalConnections", ChannelHandlersContext.getWsHandlers().size());
    stats.put("TotalSubscriptions", totalSubscriptions.get());
    stats.put("Subscriptions", subscriptions);
    stats.put("Channels", TrendingBetsContext.getTrendingBets());
    stats.put(
        "SelectionCountByEvent",
        getSelectionCountByEvent(TrendingBetsContext.getPopularSelections()));
    stats.put(
        "personalizedSelectionsCount", TrendingBetsContext.getPersonalizedSelections().size());
    stats.put("LocalSubscriptionsKey", TrendingBetsContext.getSubscribedChannels().keySet());
    stats.put(
        "LiveserveService", ((LiveServServiceImpl) liveServService).getSubscriptions().keySet());

    return stats;
  }

  public Map<String, Set<String>> getAccaLeague() {

    return PopularAccaContext.getLeagueAccas().entrySet().stream()
        .collect(
            Collectors.toMap(
                Map.Entry::getKey,
                map ->
                    map.getValue().stream()
                        .map(event -> event.getEvent().getSelectionId())
                        .collect(Collectors.toUnmodifiableSet())));
  }

  private Map<String, Integer> getSelectionCountByEvent(
      TrendingEventMap<String, List<TrendingEvent>> trendingSelections) {

    return trendingSelections.entrySet().stream()
        .filter(
            (Map.Entry<String, List<TrendingEvent>> channel) ->
                channel.getKey().startsWith("sEVENT"))
        .collect(
            Collectors.toMap(
                Map.Entry::getKey,
                (Map.Entry<String, List<TrendingEvent>> channel) -> channel.getValue().size()));
  }
}
