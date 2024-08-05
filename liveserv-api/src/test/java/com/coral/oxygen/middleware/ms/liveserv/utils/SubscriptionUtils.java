package com.coral.oxygen.middleware.ms.liveserv.utils;

import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import org.junit.Assert;

public class SubscriptionUtils {

  public static SubscriptionStats newSubscription(String channel) {
    return new SubscriptionStats(channel, 1L);
  }

  public static SubscriptionStats updatedSubscription(String channel, String watermark) {
    SubscriptionStats stats = new SubscriptionStats(channel, 1L);
    if (watermark.length() > 10) {
      Assert.fail("Too long watermark. Incorrect test configuration");
    }
    StringBuilder watermarkBuilder = new StringBuilder(watermark);
    while (watermarkBuilder.length() < 10) {
      watermarkBuilder.insert(0, "!");
    }
    watermark = watermarkBuilder.toString();
    stats.setWaterMark(watermark);
    return stats;
  }
}
