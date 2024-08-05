package com.coral.oxygen.middleware.common.service;

import com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType;
import java.lang.reflect.Field;
import org.junit.Assert;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.springframework.test.util.ReflectionTestUtils;

public class MarketTemplateNameServiceTest {

  @Test
  public void getType() {
    MarketTemplateNameService service = new MarketTemplateNameService();
    Field[] fields = service.getClass().getDeclaredFields();
    for (Field field : fields) {
      if (field.getType().equals(String[].class)) {
        ReflectionTestUtils.setField(service, field.getName(), new String[] {"Default"});
      }
    }
    ReflectionTestUtils.setField(service, "matchBettingName", new String[] {"Match Betting"});
    ReflectionTestUtils.setField(service, "toQualifyName", new String[] {"To Qualify"});
    service.init();
    Assert.assertEquals(MarketTemplateType.MATCH_BETTING, service.getType("Match Betting"));
    Assert.assertEquals(MarketTemplateType.MATCH_BETTING, service.getType("match betting"));
    Assert.assertEquals(MarketTemplateType.MATCH_BETTING, service.getType("MATCH BETTING"));
    Assert.assertEquals(MarketTemplateType.TO_QUALIFY, service.getType("To Qualify"));
    Assert.assertEquals(MarketTemplateType.TO_QUALIFY, service.getType("To qualify"));
    Assert.assertNull(service.getType(null));
  }

  @Test
  public void asQueryFromMarketStringsTest() {
    MarketTemplateNameService service = new MarketTemplateNameService();
    String result =
        service.asQueryFromMarketStrings(new String[] {"win or each way", "Win or Each Way"});
    Assertions.assertEquals(
        "|win or each way|,win or each way,|Win or Each Way|,Win or Each Way", result);
  }
}
