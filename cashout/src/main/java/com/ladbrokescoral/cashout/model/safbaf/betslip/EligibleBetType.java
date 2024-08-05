package com.ladbrokescoral.cashout.model.safbaf.betslip;

import com.ladbrokescoral.cashout.model.safbaf.Price;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class EligibleBetType {
  private Integer noOfLines;
  private String betType;
  private String betTypeName;
  private Double betMinStake;
  private Double betMaxStake;
  private Price betPrice;
  private Boolean betSyncAvailable;
  private Boolean eachWayAvailable;
  private String betMaxStakeEachWay;
  private List<EnhancedPrice> enhancedPrice = new ArrayList<>();
}
