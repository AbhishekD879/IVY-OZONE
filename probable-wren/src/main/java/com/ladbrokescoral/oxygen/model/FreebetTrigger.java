package com.ladbrokescoral.oxygen.model;

import java.io.Serializable;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class FreebetTrigger implements Serializable {
  private String freebetTriggerId;

  private String freebetTriggerType;
  private String freebetTriggerRank;
  private String freebetTriggerQualification;
  private FreebetTriggerAmount freebetTriggerAmount;
  private String freebetTriggerBetType;
  private String freebetTriggerMinPriceNum;
  private String freebetTriggerMinPriceDen;
  private String freebetTriggerMinLegPriceNum;
  private String freebetTriggerMinLegPriceDen;
  private String freebetTriggerMinLoseLegs;
  private String freebetTriggerMaxLoseLegs;
  private String freebetTriggerPrecentageBonus;
  private String freebetTriggerBonus;
  private String freebetTriggerMaxBonus;
  private String freebetTriggerCalcMethod;
}
