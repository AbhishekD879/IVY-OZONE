package com.coral.oxygen.middleware.pojos.model.output;

import org.junit.Assert;
import org.junit.Test;

public class RacingFormEventTest {

  RacingFormEvent formEvent = new RacingFormEvent();

  @Test
  public void testRaceClass() {
    formEvent.setRaceClass("7");
    Assert.assertEquals("7", formEvent.getRaceClass());
  }

  @Test
  public void testDistance() {
    formEvent.setDistance("7m");
    Assert.assertEquals("7m", formEvent.getDistance());
  }

  @Test
  public void testGoing() {
    formEvent.setGoing("Good");
    Assert.assertEquals("Good", formEvent.getGoing());
  }
}
