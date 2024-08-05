package com.ladbrokescoral.oxygen.model;

import java.io.Serializable;
import java.util.List;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class FreebetOffer implements Serializable {
  private String freebetOfferId;
  private String freebetOfferName;
  private String startTime;
  private String endTime;
  private String description;
  private String freebetOfferCcyCodes;
  private String status;
  private List<FreebetTrigger> freebetTrigger;
  private List<FreebetToken> freebetToken;
  private FreebetOfferLimits freebetOfferLimits;

  private OfferGroup offerGroup;
}
