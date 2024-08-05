package com.ladbrokescoral.cashout.api.client.entity.request;

import java.util.List;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class CashoutPart {
  private String partNo;
  private String type;
  private String ladder;
  private String result;
  private String resultPlaces;
  private String eachWayDen;
  private String eachWayPlaces;
  private String previousOfferedPlaces;
  private String priceType;
  private String categoryId;
  private String isOff;
  private CashoutPrice returnedSP;
  private CashoutPrice strikePrice;
  private CashoutPrice spotPrice;
  private List<Deduction> deductions;
}
