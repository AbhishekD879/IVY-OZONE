package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import com.egalacoral.spark.liveserver.Subscriber;
import com.egalacoral.spark.liveserver.service.LiveServerSubscriber;
import com.egalacoral.spark.liveserver.service.LiveServerSubscriptionsQAStorage;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/** Created by llegkyy on 06.04.17. */
@Service
public class FeaturedLiveServerSubscriber {
  private final Subscriber liveServerClient;
  private final LiveServerSubscriptionsQAStorage lsQAStorage;
  private final LiveServerSubscriber liveServerSubscriber;

  @Autowired
  public FeaturedLiveServerSubscriber(
      Subscriber liveServerClient,
      LiveServerSubscriptionsQAStorage lsQAStorage,
      LiveServerSubscriber liveServerSubscriber) {
    this.liveServerClient = liveServerClient;
    this.lsQAStorage = lsQAStorage;
    this.liveServerSubscriber = liveServerSubscriber;
  }

  public void subscribe(List<EventsModuleData> events) {
    events.stream().map(this::toSubscribeInfo).forEachOrdered(liveServerSubscriber::subscribe);

    lsQAStorage.storeActiveLiveServePayload(liveServerClient.getPayloadItems());
  }

  private LiveServerSubscriber.EventSubscribeInfo toSubscribeInfo(EventsModuleData module) {
    List<OutputMarket> marketsToSubscribe = filterMarkets(module);

    return LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(Integer.parseInt(module.getCategoryId()))
        .id(module.getId().toString())
        .markets(extractMarkets(marketsToSubscribe))
        .outcomes(extractOutcomes(marketsToSubscribe))
        .build();
  }

  private List<OutputMarket> filterMarkets(EventsModuleData module) {
    List<OutputMarket> marketsToSubscribe = new ArrayList<>(module.getPrimaryMarkets());
    marketsToSubscribe.addAll(module.getMarkets());
    return marketsToSubscribe;
  }

  private Set<String> extractOutcomes(List<OutputMarket> markets) {
    return markets.stream()
        .flatMap(m -> m.getOutcomes().stream())
        .map(OutputOutcome::getId)
        .collect(Collectors.toSet());
  }

  private Set<String> extractMarkets(List<OutputMarket> markets) {
    return markets.stream().map(OutputMarket::getId).collect(Collectors.toSet());
  }
}
