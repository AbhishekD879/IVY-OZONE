package com.coral.oxygen.middleware.ms.quickbet.connector.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;
import lombok.NonNull;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class LuckyDipBetPlacementRequest {

  @NonNull private String token;
  private String clientUserAgent;
  private String currency;
  private String ip;
  private String channel;
  @NonNull private String stake;
  @NonNull private String marketId;
  @NonNull private String winType;
}
