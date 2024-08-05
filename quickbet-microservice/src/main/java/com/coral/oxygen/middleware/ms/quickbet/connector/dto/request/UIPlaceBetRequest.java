package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.UIBet;
import io.vavr.collection.List;
import lombok.Value;

@Value
public class UIPlaceBetRequest {
  private String channel;
  private String clientUserAgent;
  private String currency;
  private List<UIBet> uiBets;
}
