package com.ladbrokescoral.cashout.config;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@ConfigurationProperties("cashout-offer.buffering")
@Component
public class CashoutOfferBufferingProperties {
  private Duration maxTime;
  private Duration windowTime;
  private int maxSize;
  private int allowedMaxSize;
  private Map<String, Integer> groups = new HashMap<>();

  public int maxSizeForGroup(String groupName) {
    if (groupName == null) {
      return maxSize;
    }
    // return groups.getOrDefault(groupName.toUpperCase(), maxSize) > allowedMaxSize ?
    // allowedMaxSize : groups.getOrDefault(groupName.toUpperCase(), maxSize) ;
    return groups.getOrDefault(groupName.toUpperCase(), maxSize);
  }
}
