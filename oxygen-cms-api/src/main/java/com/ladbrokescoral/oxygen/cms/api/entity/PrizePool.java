package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;
import lombok.NoArgsConstructor;

/*
 * Part of prize manager
 */
@Data
@NoArgsConstructor
public class PrizePool {

  private String cash;
  private String firstPlace;
  private String tickets;
  private String freeBets;
  private String vouchers;
  private String totalPrizes;
  private String summary;
}
