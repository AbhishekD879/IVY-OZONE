package com.ladbrokescoral.cashout.model.safbaf;

import com.ladbrokescoral.cashout.service.SelectionData;
import java.math.BigInteger;
import java.util.Objects;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class Market extends Entity implements HasStatus {
  private BigInteger marketKey;
  private String marketStatus;
  private Double handicapMakeup;
  private Double handicapValue;
  private String flags;

  @Override
  public boolean changeStatus(SelectionData data, boolean newStatus) {
    return data.changeMarketStatus(newStatus);
  }

  @Override
  public String getStatus() {
    return getMarketStatus();
  }

  @Override
  public String reasonForUpdate() {
    if (Objects.nonNull(getMarketStatus())) {
      return "StatusChanged/Market/" + getMarketStatus();
    } else if (Objects.nonNull(getHandicapValue()) || Objects.nonNull(getHandicapMakeup())) {
      return "HandicapChanged/Market";
    } else {
      return "Unknown/Market";
    }
  }
}
