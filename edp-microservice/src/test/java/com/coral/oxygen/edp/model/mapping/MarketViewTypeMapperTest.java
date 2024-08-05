package com.coral.oxygen.edp.model.mapping;

import static org.mockito.ArgumentMatchers.any;

import com.coral.oxygen.edp.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class MarketViewTypeMapperTest {

  private MarketViewTypeMapper mapper;

  @Mock private MarketMapper chain;

  @Before
  public void setUp() {
    Mockito.when(chain.map(any(), any())).thenReturn(new OutputMarket());
    mapper = new MarketViewTypeMapper(chain);
  }

  private Event footballEvent() {
    Event event = new Event();
    event.setCategoryCode("FOOTBALL");
    return event;
  }

  @Test
  public void testHandicapsViewType() {
    // preparation
    Market market = new Market();
    market.setMarketMeaningMinorCode("MH");

    // action
    OutputMarket result = mapper.map(footballEvent(), market);

    // verification
    Assert.assertEquals("handicaps", result.getViewType());
  }

  @Test
  public void testCorrectScoreViewType() {
    // preparation
    Market market = new Market();
    market.setMarketMeaningMinorCode("CS");

    // action
    OutputMarket result = mapper.map(footballEvent(), market);

    // verification
    Assert.assertEquals("correctScore", result.getViewType());
  }

  @Test
  public void testCSAndNonFootballEvent() {
    // preparation
    Market market = new Market();
    market.setMarketMeaningMinorCode("CS");
    market.setDispSortName("");

    Event event = new Event();

    // action
    OutputMarket result = mapper.map(event, market);

    // verification
    Assert.assertEquals("columns-1", result.getViewType());
  }

  @Test
  public void testNoMarketDispSortName() {
    // preparation
    Market market = new Market();
    market.setMarketMeaningMinorCode("MH");

    Event event = new Event();
    event.setCategoryCode("TENNIS");

    // action
    OutputMarket result = mapper.map(event, market);

    // verification
    Assert.assertEquals("columns-1", result.getViewType());
  }

  @Test
  public void testLCMarketDispSortName() {
    Market market = new Market();
    market.setDispSortName("LC");

    // action
    OutputMarket result = mapper.map(footballEvent(), market);

    // verification
    Assert.assertEquals("columns-3", result.getViewType());
  }
}
