package com.coral.oxygen.middleware.common.mappers;

import static org.junit.Assert.*;

import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import org.junit.Assert;
import org.junit.Test;

public class DFRacingEventDataMapperTest {

  @Test
  public void mapEmpty() {
    DFRacingEventDataMapper mapper = new DFRacingEventDataMapper();
    EventsModuleData d = new EventsModuleData();
    mapper.map(d, new RaceEvent());
    Assert.assertNull(d.getRacingFormEvent());
  }

  @Test
  public void mapEmptyGoing() {
    DFRacingEventDataMapper mapper = new DFRacingEventDataMapper();
    EventsModuleData d = new EventsModuleData();
    RaceEvent raceEvent = new RaceEvent();
    raceEvent.setDistance("1y");
    raceEvent.setYards(1);
    mapper.map(d, raceEvent);
    Assert.assertNotNull(d.getRacingFormEvent());
    Assert.assertNotNull(d.getRacingFormEvent().getDistance());
    Assert.assertNotNull(d.getRacingFormEvent().getGoing());
  }

  @Test
  public void mapEmptyDistance() {
    DFRacingEventDataMapper mapper = new DFRacingEventDataMapper();
    EventsModuleData d = new EventsModuleData();
    RaceEvent raceEvent = new RaceEvent();
    raceEvent.setGoingCode("1");
    mapper.map(d, raceEvent);
    Assert.assertNotNull(d.getRacingFormEvent());
    Assert.assertNotNull(d.getRacingFormEvent().getDistance());
    Assert.assertEquals("", d.getRacingFormEvent().getDistance());
    Assert.assertNotNull(d.getRacingFormEvent().getGoing());
  }

  @Test
  public void map() {
    DFRacingEventDataMapper mapper = new DFRacingEventDataMapper();
    EventsModuleData d = new EventsModuleData();
    RaceEvent raceEvent = new RaceEvent();
    raceEvent.setGoingCode("1");
    raceEvent.setDistance("1y");
    raceEvent.setYards(1);
    mapper.map(d, raceEvent);
    Assert.assertNotNull(d.getRacingFormEvent());
    Assert.assertNotNull(d.getRacingFormEvent().getDistance());
    Assert.assertNotNull(d.getRacingFormEvent().getGoing());
  }
}
