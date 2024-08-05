package com.coral.oxygen.middleware.common.mappers;

import static org.junit.Assert.assertEquals;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Event;
import org.junit.Assert;
import org.junit.Test;

public class SimpleEventMapperTest {

  @Test
  public void map() {
    SimpleMarketMapper mapper1 = new SimpleMarketMapper(new SimpleOutcomeMapper());
    SimpleEventMapper mapper = new SimpleEventMapper(mapper1);
    EventsModuleData e = new EventsModuleData();
    Event d = new Event();
    d.setId("1");
    mapper.map(e, d);
    Assert.assertNull(d.getAwayTeamExtIds());
  }

  @Test
  public void testDisplayOrderInMapper() {
    SimpleMarketMapper simpleMarketMapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
    SimpleEventMapper simpleEventMapper = new SimpleEventMapper(simpleMarketMapper);

    EventsModuleData eventsModuleData = new EventsModuleData();
    eventsModuleData.setType("SurfaceBetModuleData");
    eventsModuleData.setDisplayOrder(2);
    Event event = new Event();
    event.setId("1");
    EventsModuleData resultMap = simpleEventMapper.map(eventsModuleData, event);

    assertEquals(
        "DisplayOrder should be same",
        eventsModuleData.getDisplayOrder(),
        resultMap.getDisplayOrder());
  }

  @Test
  public void testDisplayOrderInMapperForBybWidget() {
    SimpleMarketMapper simpleMarketMapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
    SimpleEventMapper simpleEventMapper = new SimpleEventMapper(simpleMarketMapper);

    EventsModuleData eventsModuleData = new EventsModuleData();
    eventsModuleData.setType("BybWidgetData");
    eventsModuleData.setDisplayOrder(2);
    Event event = new Event();
    event.setId("1");
    event.setDisplayOrder(1);
    EventsModuleData resultMap = simpleEventMapper.map(eventsModuleData, event);

    assertEquals(
        "DisplayOrder should be same",
        eventsModuleData.getDisplayOrder(),
        resultMap.getDisplayOrder());
  }

  @Test
  public void testDisplayOrderInMapperWithEventsModuleDataEmpty() {

    SimpleMarketMapper simpleMarketMapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
    SimpleEventMapper simpleEventMapper = new SimpleEventMapper(simpleMarketMapper);

    EventsModuleData eventsModuleData = new EventsModuleData();
    eventsModuleData.setType("SurfaceBetModuleData");
    eventsModuleData.setDisplayOrder(null);
    Event event = new Event();
    event.setId("1");
    EventsModuleData resultMap = simpleEventMapper.map(eventsModuleData, event);

    assertEquals(
        "DisplayOrder should be same",
        eventsModuleData.getDisplayOrder(),
        resultMap.getDisplayOrder());
  }

  @Test
  public void testWithEventDisplayOrderInMapper() {
    SimpleMarketMapper simpleMarketMapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
    SimpleEventMapper simpleEventMapper = new SimpleEventMapper(simpleMarketMapper);

    EventsModuleData eventsModuleData = new EventsModuleData();
    Event event = new Event();
    event.setId("1");
    event.setDisplayOrder(22);
    EventsModuleData resultMap = simpleEventMapper.map(eventsModuleData, event);

    assertEquals(
        "DisplayOrder should be same", event.getDisplayOrder(), resultMap.getDisplayOrder());
  }

  @Test
  public void testEventMapperForBYB() {
    SimpleMarketMapper simpleMarketMapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
    SimpleEventMapper simpleEventMapper = new SimpleEventMapper(simpleMarketMapper);

    EventsModuleData eventsModuleData = new EventsModuleData();
    Event event = new Event();
    event.setId("1");
    event.setDrilldownTagNames("EVFLAG_BB");
    event.setExtIds("BWIN_PG,2095477391,");
    simpleEventMapper.map(eventsModuleData, event);

    Assert.assertNotNull(event.getDrilldownTagNames());
  }

  @Test
  public void testEventMapperForBYBNullExtIds() {
    SimpleMarketMapper simpleMarketMapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
    SimpleEventMapper simpleEventMapper = new SimpleEventMapper(simpleMarketMapper);

    EventsModuleData eventsModuleData = new EventsModuleData();
    Event event = new Event();
    event.setId("1");
    event.setDrilldownTagNames("EVFLAG_BL");
    event.setExtIds("BWIN_PG,2095477391,");
    simpleEventMapper.map(eventsModuleData, event);

    Assert.assertNotNull(event.getDrilldownTagNames());
  }

  @Test
  public void testEventMapperForBYBNullDrillDown() {
    SimpleMarketMapper simpleMarketMapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
    SimpleEventMapper simpleEventMapper = new SimpleEventMapper(simpleMarketMapper);

    EventsModuleData eventsModuleData = new EventsModuleData();
    Event event = new Event();
    event.setId("1");
    event.setExtIds("BWIN_PG,2095477391,");
    simpleEventMapper.map(eventsModuleData, event);

    Assert.assertNotNull(event.getExtIds());
  }
}
