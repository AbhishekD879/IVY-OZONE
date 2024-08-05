package com.ladbrokescoral.cashout.model.context;

import com.ladbrokescoral.cashout.repository.HasRedisKey;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class SelectionPrice implements HasRedisKey {
  private static final String SELECTION_PRICE = "SelectionPrice_";

  private String outcomeId;
  private String priceNum;
  private String priceDen;

  @Override
  public String redisKey() {
    return SELECTION_PRICE + outcomeId;
  }
}
