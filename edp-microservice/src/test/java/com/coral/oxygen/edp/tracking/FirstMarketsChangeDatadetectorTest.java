package com.coral.oxygen.edp.tracking;

import com.coral.oxygen.edp.TestUtil;
import com.coral.oxygen.edp.tracking.firstmarkets.FirstMarketsChangeDetector;
import com.coral.oxygen.edp.tracking.model.FirstMarketsData;
import java.io.IOException;
import org.junit.Assert;
import org.junit.Test;

public class FirstMarketsChangeDatadetectorTest {

  public static final String FIRST_MARKET_JSON = "marketsChangeDetector/firstMarket.json";
  private FirstMarketsChangeDetector marketsChangeDetector = new FirstMarketsChangeDetector();

  @Test
  public void testIsDataChanged() {

    FirstMarketsData newData = getFirstMarketData();

    boolean dataChanged = marketsChangeDetector.dataIsChanged(newData, null);

    Assert.assertTrue(dataChanged);
  }

  @Test
  public void testIsDataChangedByMarketsCount() {

    FirstMarketsData newData = getFirstMarketData();
    newData.getEvent().setMarketsCount(38);

    FirstMarketsData oldData = getFirstMarketData();
    boolean dataChanged = marketsChangeDetector.dataIsChanged(newData, oldData);

    Assert.assertTrue(dataChanged);
  }

  @Test
  public void testIsDataChangedByMarketsId() {

    FirstMarketsData newData = getFirstMarketData();
    newData.getEvent().getMarkets().remove(0);

    FirstMarketsData oldData = getFirstMarketData();
    boolean dataChanged = marketsChangeDetector.dataIsChanged(newData, oldData);

    Assert.assertTrue(dataChanged);
  }

  @Test
  public void testIsDataChangedByDispOrder() {

    FirstMarketsData newData = getFirstMarketData();
    newData.getEvent().getMarkets().get(0).setDisplayOrder(800);

    FirstMarketsData oldData = getFirstMarketData();
    boolean dataChanged = marketsChangeDetector.dataIsChanged(newData, oldData);

    Assert.assertTrue(dataChanged);
  }

  @Test
  public void testIsDataChangedByOutcomeId() {

    FirstMarketsData newData = getFirstMarketData();
    newData.getEvent().getMarkets().get(0).getOutcomes().remove(0);

    FirstMarketsData oldData = getFirstMarketData();
    boolean dataChanged = marketsChangeDetector.dataIsChanged(newData, oldData);

    Assert.assertTrue(dataChanged);
  }

  @Test
  public void testIsDataNotChanged() {

    FirstMarketsData newData = getFirstMarketData();
    FirstMarketsData oldData = getFirstMarketData();

    boolean dataChanged = marketsChangeDetector.dataIsChanged(newData, oldData);

    Assert.assertFalse(dataChanged);
  }

  private FirstMarketsData getFirstMarketData() {
    try {
      return TestUtil.deserializeFromFile(FIRST_MARKET_JSON, FirstMarketsData.class);
    } catch (IOException e) {
      throw new IllegalArgumentException("Cannot deserialize: " + FIRST_MARKET_JSON);
    }
  }
}
