package com.coral.oxygen.middleware.pojos.model.output;

import org.junit.Assert;
import org.junit.Test;

public class PrimaryMarketsTest {

  @Test
  public void getOrderIndex() {
    Assert.assertEquals(Integer.MAX_VALUE, PrimaryMarkets.FOOTBALL.getOrderIndex(null));
    Assert.assertEquals(0, PrimaryMarkets.FOOTBALL.getOrderIndex(MarketTemplateType.MATCH_BETTING));
    Assert.assertEquals(4, PrimaryMarkets.FOOTBALL.getOrderIndex(MarketTemplateType.TO_QUALIFY));
  }
}
