package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import com.coral.oxygen.middleware.ms.liveserv.impl.ManagedLiveServeService;
import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import com.coral.oxygen.middleware.ms.liveserv.utils.StringUtils;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.ladbrokescoral.oxygen.timeline.api.service.SubscriptionService;
import io.vavr.collection.Stream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Map;
import java.util.Optional;
import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Data
@Component
public class SubscriptionServiceImpl implements SubscriptionService {

  private static final int CHANNEL_FINAL_LENGTH = 10;

  @Value("${siteServer.priceboost.enabled}")
  private boolean isPriceBoostEnabled;

  @Value("${siteServer.priceboost.simplefilter.key}")
  private String priceBoostSimpleFilterKey;

  @Value("${siteServer.priceboost.simplefilter.value}")
  private String priceBoostSimpleFilterValue;

  private final SiteServerApi siteServerApi;
  private final ManagedLiveServeService liveServService;

  @Override
  public Optional<Event> subscribe(String selectionId) {
    Optional<Event> optionalEvent = queryEventFromSiteserve(selectionId);
    optionalEvent
        .filter(this::isSubscriptionParametersValid)
        .ifPresent(
            event ->
                subscribeOnUpdates(
                    event,
                    event.getMarkets().get(0),
                    event.getMarkets().get(0).getOutcomes().get(0))); // todo demetra law

    return optionalEvent;
  }

  private boolean isSubscriptionParametersValid(Event event) {
    return !event.getMarkets().isEmpty() && !event.getMarkets().get(0).getOutcomes().isEmpty();
  }

  private void subscribeOnUpdates(Event event, Market market, Outcome outcome) {
    java.util.List<String> channels = new ArrayList<>();
    channels.add(
        ChannelType.sEVENT.getName()
            + StringUtils.addLeadingZeros(event.getId(), CHANNEL_FINAL_LENGTH));
    channels.add(
        ChannelType.sEVMKT.getName()
            + StringUtils.addLeadingZeros(market.getId(), CHANNEL_FINAL_LENGTH));
    channels.add(
        ChannelType.sSELCN.getName()
            + StringUtils.addLeadingZeros(outcome.getId(), CHANNEL_FINAL_LENGTH));
    channels.forEach(liveServService::subscribe);
  }

  private Optional<Event> queryEventFromSiteserve(String selectionId) {
    return siteServerApi
        .getEventToOutcomeForOutcome(
            Collections.singletonList(selectionId),
            (SimpleFilter)
                new SimpleFilter.SimpleFilterBuilder()
                    .addPriceStream(
                        priceBoostSimpleFilterKey, priceBoostSimpleFilterValue, isPriceBoostEnabled)
                    .build(),
            null,
            false)
        .filter(listOfEvents -> !listOfEvents.isEmpty())
        .map(listOfEvents -> listOfEvents.get(0));
  }

  @Scheduled(fixedDelay = 2 * 60 * 60 * 1000)
  private void unsubscribeFromFinishedEvents() {
    Map<String, SubscriptionStats> subscriptions = liveServService.getSubscriptions();
    Map<String, String> eventIdToChannel =
        Stream.ofAll(subscriptions.entrySet())
            .toMap(entry -> Long.toString(entry.getValue().getEventId()), Map.Entry::getKey)
            .toJavaMap();

    if (!eventIdToChannel.isEmpty())
      siteServerApi
          .getEvent(new ArrayList<>(eventIdToChannel.keySet()), Optional.empty(), Optional.empty())
          .map(Stream::ofAll)
          .orElse(Stream.empty())
          .filter(event -> Boolean.TRUE.equals(event.getIsFinished()))
          .map(Event::getId)
          .map(eventIdToChannel::get)
          .forEach(liveServService::unsubscribe);
  }
}
