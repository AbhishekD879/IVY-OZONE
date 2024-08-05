package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.TestUtil;
import com.coral.oxygen.edp.model.output.OutputOutcome;
import com.coral.oxygen.edp.model.output.OutputPrice;
import com.egalacoral.spark.siteserver.model.Event;
import java.io.IOException;
import org.junit.Assert;
import org.junit.Test;

public class SimpleOutcomeMapperTest {

  @Test
  public void shouldMapOutcomeCorrectly() throws IOException {
    Event event = TestUtil.deserializeFromFile("SimpleEventMapperTest/event.json", Event.class);

    SimpleOutcomeMapper mapper = new SimpleOutcomeMapper();

    OutputOutcome outputOutcome =
        mapper.map(
            event, event.getMarkets().get(0), event.getMarkets().get(0).getOutcomes().get(0));

    Assert.assertEquals("688495346", outputOutcome.getId());
    Assert.assertEquals("HL", outputOutcome.getOutcomeMeaningMajorCode());
    Assert.assertEquals("H", outputOutcome.getOutcomeMeaningMinorCode());
    Assert.assertNull(outputOutcome.getOutcomeMeaningScores());
    Assert.assertNull(outputOutcome.getRunnerNumber());
    Assert.assertNull(outputOutcome.getIsResulted());
    Assert.assertEquals("A", outputOutcome.getOutcomeStatusCode());
    Assert.assertEquals("sSELCN0688495346,", outputOutcome.getLiveServChannels());
    Assert.assertEquals(Integer.valueOf(10), outputOutcome.getDisplayOrder());
    Assert.assertEquals("Over (+3.5)", outputOutcome.getName());

    Assert.assertEquals(1, outputOutcome.getPrices().size());
    OutputPrice outputPrice = outputOutcome.getPrices().get(0);

    Assert.assertEquals("1", outputPrice.getId());
    Assert.assertEquals("LP", outputPrice.getPriceType());
    Assert.assertEquals(Integer.valueOf(2), outputPrice.getPriceNum());
    Assert.assertEquals(Integer.valueOf(5), outputPrice.getPriceDen());
    Assert.assertEquals(Double.valueOf(1.40), outputPrice.getPriceDec());
    Assert.assertEquals(Double.valueOf(3.5), outputPrice.getRawHandicapValue());
    Assert.assertEquals("3.5", outputPrice.getHandicapValueDec());
  }
}
