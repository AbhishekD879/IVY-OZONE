package com.coral.oxygen.middleware.ms.quickbet.connector.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

/** Created by azayats on 31.10.17. */
@Data
@NoArgsConstructor
public class RegularPlaceBetRequest {
  private String token;
  private String winType;
  private String stake;
  private String price;
  private String handicap;
  private String channel;
  private String ip;
  private String clientUserAgent;
  private FreeBetRequest freebet;
}
