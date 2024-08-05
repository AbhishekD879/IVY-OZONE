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
public class MarketHandicapTypeMapperTest {
  private static final String HANDICAP_SECOND_HALF = "Handicap Second Half";

  private MarketHandicapTypeMapper mapper;

  @Mock private MarketMapper chain;

  @Before
  public void setUp() {
    Mockito.when(chain.map(any(), any())).thenReturn(new OutputMarket());
    mapper = new MarketHandicapTypeMapper(chain);
  }

  private Event footballEvent() {
    Event event = new Event();
    event.setCategoryCode("FOOTBALL");
    return event;
  }

  @Test
  public void testMatchResult() {
    // preparation
    Event event = footballEvent();

    Market market = new Market();
    market.setMarketMeaningMinorCode("MH");
    market.setCollectionNames("Handicap Match Result");

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertEquals("matchResult", outputMarket.getHandicapType());
  }

  @Test
  public void testFirstHalf() {
    // preparation
    Event event = footballEvent();

    Market market = new Market();
    market.setMarketMeaningMinorCode("MH");
    market.setCollectionNames("Handicap First Half");

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertEquals("firstHalf", outputMarket.getHandicapType());
  }

  @Test
  public void testSecondHalf() {
    // preparation
    Event event = footballEvent();

    Market market = new Market();
    market.setMarketMeaningMinorCode("MH");
    market.setCollectionNames(HANDICAP_SECOND_HALF);

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertEquals("secondHalf", outputMarket.getHandicapType());
  }

  @Test
  public void testNotFootball() {
    // preparation
    Event event = new Event();
    event.setCategoryCode("SOMESPORT");

    Market market = new Market();
    market.setMarketMeaningMinorCode("MH");
    market.setCollectionNames(HANDICAP_SECOND_HALF);

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertNull(outputMarket.getHandicapType());
  }

  @Test
  public void testNullCategoryCode() {
    // preparation
    Event event = new Event();
    event.setCategoryCode(null);

    Market market = new Market();
    market.setMarketMeaningMinorCode("MH");
    market.setCollectionNames(HANDICAP_SECOND_HALF);

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertNull(outputMarket.getHandicapType());
  }

  @Test
  public void testNotMH() {
    // preparation
    Event event = footballEvent();

    Market market = new Market();
    market.setMarketMeaningMinorCode("AA");
    market.setCollectionNames(HANDICAP_SECOND_HALF);

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertNull(outputMarket.getHandicapType());
  }

  @Test
  public void testOtherCollectionNames() {
    // preparation
    Event event = footballEvent();

    Market market = new Market();
    market.setMarketMeaningMinorCode("MH");
    market.setCollectionNames("SomeSome");

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertNull(outputMarket.getHandicapType());
  }
}
