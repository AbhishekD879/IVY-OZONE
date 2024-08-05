package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.FreeBetRequest;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BanachPlaceBetRequestData {
  private String stake;
  private String token;
  private String currency;
  private String price;
  private String channel;
  private FreeBetRequest freebet;

  @JsonIgnore
  public boolean isFreeBetIncluded() {
    return freebet != null && freebet.getId() != null && !freebet.getId().equals(0L);
  }
}
