package com.coral.oxygen.middleware.ms.liveserv.utils;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LiveServeUtil {
  private static final Pattern subscriptionInRequest = Pattern.compile("S([0-9]){4}");

  private LiveServeUtil() {}

  public static int calculateSubscriptionCount(String requestBody) {
    if (requestBody == null) {
      return 0;
    }
    int subsCount = 0;
    Matcher matcher = subscriptionInRequest.matcher(requestBody);
    while (matcher.find()) subsCount++;
    return subsCount;
  }
}
