package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.TestUtil;
import com.coral.oxygen.edp.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import java.io.IOException;
import org.junit.Assert;
import org.junit.Test;
import org.mockito.Mockito;

public class SimpleMarketMapperTest {

  @Test
  public void shouldMapMarketCorrectly() throws IOException {
    Event event = TestUtil.deserializeFromFile("SimpleEventMapperTest/event.json", Event.class);

    OutcomeMapper outcomeMapper = Mockito.mock(OutcomeMapper.class);

    SimpleMarketMapper mapper = new SimpleMarketMapper(outcomeMapper);

    OutputMarket outputMarket = mapper.map(event, event.getMarkets().get(0));

    Assert.assertEquals("215504430", outputMarket.getId());
    Assert.assertEquals("Total Goals Over/Under 3.5", outputMarket.getName());
    Assert.assertTrue(outputMarket.getIsMarketBetInRun());
    Assert.assertTrue(outputMarket.getIsLpAvailable());
    Assert.assertFalse(outputMarket.getIsSpAvailable());
    Assert.assertFalse(outputMarket.getIsGpAvailable());
    Assert.assertNull(outputMarket.getEachWayFactorNum());
    Assert.assertNull(outputMarket.getEachWayFactorDen());
    Assert.assertNull(outputMarket.getEachWayPlaces());
    Assert.assertNull(outputMarket.getNcastTypeCodes());
    Assert.assertNull(outputMarket.getDrilldownTagNames());
    Assert.assertEquals("sEVMKT0215504430,", outputMarket.getLiveServChannels());
    Assert.assertEquals("LP", outputMarket.getPriceTypeCodes());
    Assert.assertEquals("Y", outputMarket.getCashoutAvail());
    Assert.assertEquals("L", outputMarket.getMarketMeaningMajorCode());
    Assert.assertEquals("HL", outputMarket.getMarketMeaningMinorCode());
    Assert.assertEquals(Double.valueOf(3.5), outputMarket.getRawHandicapValue());
    Assert.assertEquals("HL", outputMarket.getDispSortName());
    Assert.assertEquals("A", outputMarket.getMarketStatusCode());
    Assert.assertEquals(Long.valueOf(1935498), outputMarket.getTemplateMarketId());
    Assert.assertEquals("Total Goals Over/Under", outputMarket.getTemplateMarketName());
  }
}
