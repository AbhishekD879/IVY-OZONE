package com.egalacoral.spark.timeform.service;

import com.egalacoral.spark.timeform.service.greyhound.MeetingAbbreviationService;
import org.junit.Assert;
import org.junit.Test;

public class MeetingNameAbbreviationServiceTest {

  @Test
  public void testGetAbbreviationsEmpty() {
    MeetingAbbreviationService service = new MeetingAbbreviationService();
    service.init();
    Assert.assertTrue(service.getAbbreviations("test").isEmpty());
  }

  @Test
  public void testGetAbbreviations() {
    MeetingAbbreviationService service = new MeetingAbbreviationService();
    service.init();
    Assert.assertTrue(service.getAbbreviations("Yarmouth").size() == 2);
  }
}
