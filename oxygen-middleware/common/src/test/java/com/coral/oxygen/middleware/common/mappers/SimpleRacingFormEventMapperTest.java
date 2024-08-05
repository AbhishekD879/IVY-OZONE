package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.RacingFormEvent;
import org.junit.Assert;
import org.junit.Test;

public class SimpleRacingFormEventMapperTest {

  @Test
  public void mapEmpty() {
    SimpleRacingFormEventMapper mapper = new SimpleRacingFormEventMapper();
    EventsModuleData d = new EventsModuleData();
    mapper.map(d, new RacingFormEvent());
    Assert.assertNull(d.getRacingFormEvent());
  }

  @Test
  public void mapEmptyGoing() {
    SimpleRacingFormEventMapper mapper = new SimpleRacingFormEventMapper();
    EventsModuleData d = new EventsModuleData();
    RacingFormEvent RacingFormEvent = new RacingFormEvent();
    RacingFormEvent.setDistance("1");
    mapper.map(d, RacingFormEvent);
    Assert.assertNotNull(d.getRacingFormEvent());
    Assert.assertNotNull(d.getRacingFormEvent().getDistance());
    Assert.assertNotNull(d.getRacingFormEvent().getGoing());
  }

  @Test
  public void mapEmptyDistance() {
    SimpleRacingFormEventMapper mapper = new SimpleRacingFormEventMapper();
    EventsModuleData d = new EventsModuleData();
    RacingFormEvent RacingFormEvent = new RacingFormEvent();
    RacingFormEvent.setGoing("1");
    mapper.map(d, RacingFormEvent);
    Assert.assertNotNull(d.getRacingFormEvent());
    Assert.assertNotNull(d.getRacingFormEvent().getDistance());
    Assert.assertEquals("", d.getRacingFormEvent().getDistance());
    Assert.assertNotNull(d.getRacingFormEvent().getGoing());
  }

  @Test
  public void map() {
    SimpleRacingFormEventMapper mapper = new SimpleRacingFormEventMapper();
    EventsModuleData d = new EventsModuleData();
    RacingFormEvent RacingFormEvent = new RacingFormEvent();
    RacingFormEvent.setGoing("1");
    RacingFormEvent.setDistance("1");
    mapper.map(d, RacingFormEvent);
    Assert.assertNotNull(d.getRacingFormEvent());
    Assert.assertNotNull(d.getRacingFormEvent().getDistance());
    Assert.assertNotNull(d.getRacingFormEvent().getGoing());
  }
}
