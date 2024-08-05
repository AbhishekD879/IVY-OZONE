package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;

@Data
public class BetPack {
  private Boolean isBetPack;
  private String bodyText;
  private String congratsMsg;
  private String offerId;
  private String triggerIds;
  private String betValue;
  private String lowFundMessage;
  private String notLoggedinMessage;
  private String errorMessage;
}
