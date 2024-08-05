package com.egalacoral.spark.liveserver.service;

import com.egalacoral.spark.liveserver.Subscriber;
import java.util.Set;
import lombok.Builder;
import lombok.Data;
import lombok.Singular;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
@Slf4j
public class LiveServerSubscriber {
  private final Subscriber liveServerClient;

  @Autowired
  public LiveServerSubscriber(final Subscriber liveServerClient) {
    this.liveServerClient = liveServerClient;
  }

  public void subscribe(EventSubscribeInfo eventSubscribeInfo) {
    if (eventSubscribeInfo == null || StringUtils.isBlank(eventSubscribeInfo.getId())) {
      log.warn("Invalid subscribe info: {}", eventSubscribeInfo);
      return;
    }

    String eventId = eventSubscribeInfo.getId();
    liveServerClient.subscribeOnEvent(eventId, eventSubscribeInfo.getCategoryId());
    liveServerClient.subscribeOnScore(eventId);
    liveServerClient.subscribeOnClock(eventId);

    Set<String> marketsToSubscribe = eventSubscribeInfo.getMarkets();
    if (!CollectionUtils.isEmpty(marketsToSubscribe)) {
      marketsToSubscribe.forEach(market -> liveServerClient.subscribeOnMarket(market, eventId));
    }

    Set<String> outcomesToSubscribe = eventSubscribeInfo.getOutcomes();
    if (!CollectionUtils.isEmpty(outcomesToSubscribe)) {
      outcomesToSubscribe.forEach(
          selection -> liveServerClient.subscribeOnSelection(selection, eventId));
    }
  }

  @Data
  @Builder
  public static class EventSubscribeInfo {
    private final int categoryId;
    private final String id;
    @Singular private Set<String> markets;
    @Singular private Set<String> outcomes;
  }
}
