package com.coral.oxygen.middleware.ms.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import com.coral.siteserver.api.SiteServerService;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

/** Created by ogavur on 5/15/17. */
@Service
@Slf4j
public class UnsubscribeService {

  private final LiveServService liveServService;
  private final SiteServerService siteServerService;
  private final ApplicationEventPublisher applicationEventPublisher;

  @Autowired
  public UnsubscribeService(
      LiveServService liveServService,
      SiteServerService siteServerService,
      ApplicationEventPublisher applicationEventPublisher) {
    this.liveServService = liveServService;
    this.siteServerService = siteServerService;
    this.applicationEventPublisher = applicationEventPublisher;
  }

  private void unsubscribeChannel(String channel) {
    applicationEventPublisher.publishEvent(new ChannelUnsubcribeEvent(this, channel));
  }

  private Map<Long, List<String>> getEventSubscriptions() {
    Map<Long, List<String>> result = new HashMap<>();
    Collection<SubscriptionStats> stats = liveServService.getSubscriptions().values();
    for (SubscriptionStats stat : stats) {
      long eventId = stat.getEventId();
      List<String> list = result.computeIfAbsent(eventId, absent -> new ArrayList<>());
      list.add(stat.getChannel());
    }
    return result;
  }

  @ConditionalOnProperty("${enable.unsubscribe.scheduler}")
  @Scheduled(
      initialDelayString = "${unsubscribe.initialDelay.millis}",
      fixedDelayString = "${unsubscribe.fixedDelay.millis}")
  private void run() {
    try {
      unSubscribe();
    } catch (Exception e) {
      log.error("Unsubscribe error - ", e);
      NewRelic.noticeError(e);
    }
  }

  /**
   * Publishes channel unsubscribe event {@link ChannelUnsubcribeEvent} for each of OpenBet Event
   * channels if it's undisplayed in SiteServer
   */
  @Trace(metricName = "UnSubscribeRequest")
  public void unSubscribe() {
    // get current subscriptions
    Map<Long, List<String>> items = getEventSubscriptions();
    final int channelsSize = items.values().stream().map(List::size).reduce(0, (a, b) -> a + b);
    final int numOfEventsSubscribed = items.size();

    log.debug("Subscribed to {} events and {} channels", numOfEventsSubscribed, channelsSize);
    if (numOfEventsSubscribed > 0) {
      // get all available events from siteserv
      List<Long> activeEvents = siteServerService.getEventIdS(new ArrayList<>(items.keySet()));
      // un subscribe all not active events
      List<String> inactiveEvents =
          items.entrySet().stream()
              .filter(e -> !activeEvents.contains(e.getKey()))
              .flatMap(e -> e.getValue().stream())
              .collect(Collectors.toList());

      log.debug("inactive items {}", inactiveEvents);
      if (!inactiveEvents.isEmpty()) {
        log.info("Unsubscribing from {} channels: {}", inactiveEvents.size(), inactiveEvents);
        inactiveEvents.forEach(this::unsubscribeChannel);
      }
    }
  }
}
