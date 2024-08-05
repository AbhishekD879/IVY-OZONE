package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import com.coral.oxygen.middleware.ms.liveserv.utils.StringUtils;
import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class RequestBuilder {

  private static final transient Logger LOGGER = LoggerFactory.getLogger(RequestBuilder.class);

  private static final String UNCHANGED_SIZE_PREFIX = "S";
  private static final String PAYLOAD_COMMON_UPDATED_PREFIX = "CL0000";
  private static final String UNCHANGED_LAST_MESSAGE_ID = "!!!!!!!!!0";
  private static final int EVENT_ID_LENGTH = 10;

  public String build(Collection<SubscriptionStats> subscriptionStats) {
    StringBuilder payloadBuilder = new StringBuilder();
    payloadBuilder.append(PAYLOAD_COMMON_UPDATED_PREFIX);
    List<SubscriptionStats> unchanged =
        subscriptionStats.stream()
            .filter(item -> Objects.isNull(item.getWaterMark()))
            .collect(Collectors.toList());
    buildUnchangedItems(payloadBuilder, unchanged);
    List<SubscriptionStats> changed =
        subscriptionStats.stream()
            .filter(item -> Objects.nonNull(item.getWaterMark()))
            .collect(Collectors.toList());
    buildChangedItems(payloadBuilder, changed);
    return payloadBuilder.toString();
  }

  private void buildChangedItems(
      StringBuilder payloadBuilder, List<SubscriptionStats> subscriptions) {
    subscriptions.forEach(
        subscription -> {
          payloadBuilder.append("S0001");
          payloadBuilder.append(subscription.getChannel());
          payloadBuilder.append(subscription.getWaterMark());
        });
  }

  private void buildUnchangedItems(
      StringBuilder payloadBuilder, List<SubscriptionStats> unchanged) {
    int chunkStart = 0;
    while (chunkStart < unchanged.size()) {
      int chunkEnd = Math.min(chunkStart + 9999, unchanged.size());
      buildUnchangedItemsChunk(payloadBuilder, unchanged.subList(chunkStart, chunkEnd));
      chunkStart = chunkEnd;
    }
  }

  private void buildUnchangedItemsChunk(
      StringBuilder payloadBuilder, List<SubscriptionStats> unchanged) {
    payloadBuilder.append(UNCHANGED_SIZE_PREFIX);
    String count = StringUtils.addLeadingZeros(String.valueOf(unchanged.size()), 4);
    payloadBuilder.append(count);
    for (SubscriptionStats subscriptionStats : unchanged) {
      payloadBuilder.append(subscriptionStats.getChannel());
    }
    payloadBuilder.append(UNCHANGED_LAST_MESSAGE_ID);
  }
}
